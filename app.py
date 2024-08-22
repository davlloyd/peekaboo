import os
import sys
from dotenv import load_dotenv
from main import create_app

# Load environment variables
load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
	app.run(debug=app.config['DEBUG'],host='0.0.0.0', port=int(os.getenv('PORT', '8080')))

