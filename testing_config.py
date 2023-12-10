class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://efrei:mlinprod@localhost/test_mycuisine_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
