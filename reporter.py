import os
from flask import current_app
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
	app.run(debug=app.config['DEBUG'],host='0.0.0.0', port=int(os.getenv('PORT', '80')))

