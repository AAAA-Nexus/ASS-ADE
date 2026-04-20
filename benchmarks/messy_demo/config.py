from utils import get_value

DB_HOST = "localhost"
DB_PORT = 5432
SECRET = "hardcoded-secret-123"
MAX_RETRIES = 3
MAX_RETRIES_DUPLICATE = 3

def load_config():
    val = get_value("config")
    return {"host": DB_HOST, "port": DB_PORT, "secret": SECRET}

def load_config_again():
    val = get_value("config")
    return {"host": DB_HOST, "port": DB_PORT, "secret": SECRET}
