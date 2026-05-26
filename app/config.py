class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/srv_monitor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False