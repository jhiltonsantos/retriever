import os

import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("main:app", host="127.0.0.1", port=port, log_level="info")
