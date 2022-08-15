import os
import sys
from flask import current_app
from peekaboo import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
print('DB URI: {0}'.format(app.config["SQLALCHEMY_DATABASE_URI"]), file=sys.stdout)

if __name__ == "__main__":
	app.run(debug=app.config['DEBUG'],host='0.0.0.0', port=int(os.getenv('PORT', '80')))

