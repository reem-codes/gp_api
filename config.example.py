class Config:
    SQLALCHEMY_DATABASE_URI = "postgres://username:password@localhost/dbname"
    SQLALCHEMY_NATIVE_UNICODE = "utf-8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret key"
