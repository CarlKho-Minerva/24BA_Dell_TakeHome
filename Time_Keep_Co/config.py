import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-please-change"
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"csv"}
