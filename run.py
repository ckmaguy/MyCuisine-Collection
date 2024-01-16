#run app

from app import app, init_app
from config import Config

init_app(Config)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
