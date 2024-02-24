import os

HOST: str = os.environ.get("DEBRIS_HOST", "localhost")
PORT: int = int(os.environ.get("DEBRIS_PORT", 8080))
DEBUG: bool = os.environ.get("DEBRIS_DEBUG", False)