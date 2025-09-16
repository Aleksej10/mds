from flask import Flask
from routes import blueprints

app = Flask(__name__)

for bp in blueprints:
  app.register_blueprint(bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3193)
