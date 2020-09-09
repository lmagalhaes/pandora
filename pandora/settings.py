import os


root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

settings = {
    'debug': bool(os.getenv('DEBUG', False)),
    'database': dict(
        db_host=os.getenv('EXT_DB_HOST'),
        db_port=os.getenv('EXT_DB_PORT'),
        db_name=os.getenv('DB_NAME'),
        db_username=os.getenv('EXT_DB_USERNAME'),
        db_password=os.getenv('EXT_DB_PASSWORD'),
    )
}