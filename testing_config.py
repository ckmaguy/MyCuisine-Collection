class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_user:password@localhost/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False