from app import app
from testing_config import TestingConfig

app.config.from_object(TestingConfig)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
