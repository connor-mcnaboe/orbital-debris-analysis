import os

HOST: str = os.environ.get("DEBRIS_HOST", "localhost")
PORT: int = int(os.environ.get("DEBRIS_PORT", 8000))
DEBUG: bool = os.environ.get("DEBRIS_DEBUG", False)