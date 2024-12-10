import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-please-change"
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"csv"}
    DEV_MODE = os.environ.get("DEV_MODE", "True") == "True"
    DEFAULT_TAR_FILE = os.environ.get("DEFAULT_TAR_FILE", "/Users/cvk/Downloads/[CODE] Local Projects/Dell_TakeHome/ServiceCodes_TAR.csv")
    DEFAULT_ECB_FILE = os.environ.get("DEFAULT_ECB_FILE", "/Users/cvk/Downloads/[CODE] Local Projects/Dell_TakeHome/ServiceCodes_ECB.csv")
