from pathlib import Path
import configparser
from urllib.parse import quote
my_file_path = "D:/DOCUMENTS/PYTHON/config.ini"
# change the  location of your .ini file if none hard code
# your postgres credentials though it is not recommended 

config_path = Path(my_file_path)

config = configparser.ConfigParser()
config.read(config_path)
secret_password = config.get('database', 'password')
username = config.get('database', 'username')
password = quote(str(secret_password))
host = config.get('database', 'host')
database_name = config.get('database', 'database_name')
