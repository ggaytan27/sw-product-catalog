SQLITE = "sqlite:///project.db"
POSTGRESQL = ""


class Config:
    DEBUG = False
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = SQLITE

    CKEDITOR_PGK_TYPE = 'basic'