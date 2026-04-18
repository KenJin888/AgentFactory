from __future__ import annotations

from pathlib import Path

import uvicorn

from app.plugin.module_oh.oh_http import create_http_app


def main() -> None:
    app = create_http_app(cwd=Path.cwd())
    uvicorn.run(app, host="127.0.0.1", port=8787)


if __name__ == "__main__":
    main()
