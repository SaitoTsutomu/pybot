from os import getenv

HOST = getenv("SERVER_HOST", "0.0.0.0")
PORT = int(getenv("SERVER_PORT", "5000"))
SECRET_KEY = getenv("SECRET_KEY", "to-be-changed")
