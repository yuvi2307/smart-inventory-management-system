class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/smart_inventory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False