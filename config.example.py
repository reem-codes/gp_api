class Config:
    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = "postgres://username:password@localhost/dbname"
    SQLALCHEMY_NATIVE_UNICODE = "utf-8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FLASK
    SECRET_KEY = "I am a secret <3"

    # OURS
    ERROR_MESSAGE = "errrrroororrrr"
    DELETE_MESSAGE = "resource deleted successfully"
    PUT_MESSAGE = "resource updated successfully"
    POST_MESSAGE = "resource added successfully"

    # JWT
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
