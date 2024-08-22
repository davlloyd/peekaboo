from flask import current_app, render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html', error_description=e.description)
    