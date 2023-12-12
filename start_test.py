from app import app,init_app
from testing_config import TestingConfig

init_app(TestingConfig)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
