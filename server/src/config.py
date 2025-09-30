from decouple import config

class Config:
    UPLOAD_FOLDER= config("UPLOAD_FOLDER", default="files")
    ALLOWED_EXTENSIONS= set(config("ALLOWED_EXTENSIONS", default="txt,pdf").split(","))
    MAX_CONTENT_LENGTH= config("MAX_CONTENT_LENGTH", default=16000000, cast=int) # 16mb