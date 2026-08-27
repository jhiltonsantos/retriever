use std::sync::Mutex;

use tauri::Manager;
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

const DESKTOP_API_PORT: &str = "18765";

struct ApiProcess(Mutex<Option<CommandChild>>);

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .plugin(tauri_plugin_shell::init())
    .manage(ApiProcess(Mutex::new(None)))
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }

      // Failed to start api process, not stopping the app
      match start_api_process(app.handle()) {
        Ok(child) => {
          app.state::<ApiProcess>().0.lock().unwrap().replace(child);
        }
        Err(err) => {
          log::error!("Failed to start api process: {err}");
        }
      }

      Ok(())
    })
    .on_window_event(|window, event| {
      if let tauri::WindowEvent::CloseRequested { .. } = event {
        let state = window.state::<ApiProcess>();
        let child = state.0.lock().unwrap().take();
        if let Some(child) = child {
          let _ = child.kill();
        }
      }
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

fn start_api_process(
  app: &tauri::AppHandle,
) -> Result<CommandChild, Box<dyn std::error::Error>> {
  let app_data_dir = app.path().app_data_dir()?;
  let chroma_dir = app_data_dir.join("chroma_data");
  let tmp_upload_dir = app_data_dir.join("tmp_uploads");
  std::fs::create_dir_all(&chroma_dir)?;
  std::fs::create_dir_all(&tmp_upload_dir)?;

  let sidecar = app
    .shell()
    .sidecar("retriever-api")?
    .env("API_PORT", DESKTOP_API_PORT)
    .env("DESKTOP_MODE", "1")
    .env("CHROMA_DIR", chroma_dir.to_string_lossy().to_string())
    .env("TMP_UPLOAD_DIR", tmp_upload_dir.to_string_lossy().to_string());

  let (mut rx, child) = sidecar.spawn()?;

  tauri::async_runtime::spawn(async move {
    while let Some(event) = rx.recv().await {
      match event {
        CommandEvent::Stdout(line) => {
          log::info!("[api] {}", String::from_utf8_lossy(&line));
        }
        CommandEvent::Stderr(line) => {
          log::error!("[api] {}", String::from_utf8_lossy(&line));
        }
        CommandEvent::Error(err) => {
          log::error!("[api] error in the api process: {err}");
        }
        _ => {}
      }
    }
  });

  Ok(child)
}
