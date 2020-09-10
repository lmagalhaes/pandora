import os


DEBUG = bool(os.getenv('DEBUG', False))

DB_CONFIG = dict(
    db_host=os.getenv('DB_HOST'),
    db_port=int(os.getenv('DB_PORT')),
    db_name=os.getenv('DB_NAME'),
    db_username=os.getenv('DB_USERNAME'),
    db_password=os.getenv('DB_PASSWORD'),
)

SQLALCHEMY_URI = 'mysql+mysqldb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'.format(**DB_CONFIG)
