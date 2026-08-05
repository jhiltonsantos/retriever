import http from 'node:http';
import path from 'node:path';
import { spawn, type ChildProcess } from 'node:child_process';
import fs from 'node:fs';
import {
	DESKTOP_API_PORT,
	getApiUrl,
	getChromaDir,
	getTmpUploadDir,
	resolveApiExecutable,
	resolveApiRoot,
	resolvePythonExecutable
} from './paths.js';

function ensureDir(dir: string): void {
	fs.mkdirSync(dir, { recursive: true });
}

export function waitForHealth(maxAttempts = 60, intervalMs = 500): Promise<void> {
	return new Promise((resolve, reject) => {
		let attempts = 0;

		const check = () => {
			const req = http.get(`${getApiUrl()}/health`, (res) => {
				res.resume();
				if (res.statusCode === 200) {
					resolve();
				} else {
					retry();
				}
			});
			req.on('error', retry);
			req.setTimeout(2000, () => {
				req.destroy();
				retry();
			});
		};

		const retry = () => {
			attempts += 1;
			if (attempts >= maxAttempts) {
				reject(new Error('FastAPI não respondeu a tempo.'));
				return;
			}
			setTimeout(check, intervalMs);
		};

		check();
	});
}

export async function startApiProcess(): Promise<ChildProcess> {
	const apiRoot = resolveApiRoot();
	const chromaDir = getChromaDir();
	const tmpDir = getTmpUploadDir();

	ensureDir(chromaDir);
	ensureDir(tmpDir);

	const env = {
		...process.env,
		API_PORT: DESKTOP_API_PORT,
		DESKTOP_MODE: '1',
		CHROMA_DIR: chromaDir,
		TMP_UPLOAD_DIR: tmpDir
	};

	const packagedExe = resolveApiExecutable();
	let child: ChildProcess;

	if (packagedExe) {
		child = spawn(packagedExe, [], {
			cwd: path.dirname(packagedExe),
			env,
			stdio: 'pipe'
		});
	} else {
		const python = resolvePythonExecutable(apiRoot);
		child = spawn(
			python,
			['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', DESKTOP_API_PORT],
			{ cwd: apiRoot, env, stdio: 'pipe' }
		);
	}

	child.stdout?.on('data', (chunk) => console.log('[api]', chunk.toString()));
	child.stderr?.on('data', (chunk) => console.error('[api]', chunk.toString()));

	await waitForHealth();
	return child;
}

export function stopApiProcess(child: ChildProcess | null): void {
	if (!child || child.killed) return;
	child.kill();
}

export async function checkOllama(baseUrl = 'http://localhost:11434'): Promise<boolean> {
	return new Promise((resolve) => {
		const req = http.get(`${baseUrl}/api/tags`, (res) => {
			res.resume();
			resolve(res.statusCode === 200);
		});
		req.on('error', () => resolve(false));
		req.setTimeout(3000, () => {
			req.destroy();
			resolve(false);
		});
	});
}
