import app
import os

handler = app.create_app()

if __name__ == "__main__":
	app.create_app().run(debug=True,host='0.0.0.0', port=int(os.getenv('PORT', '80')))
