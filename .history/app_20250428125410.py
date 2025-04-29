import pickle
from flask import Flask
from model import predict_blueprint

# Initialize the Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(predict_blueprint, url_prefix='/predict')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
