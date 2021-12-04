from flask import Flask, Blueprint, render_template

#http status
bp = Blueprint('error_handler', __name__)

@bp.app_errorhandler(403)
#Forbidden
def forbidden(e):
    return render_template('error.html', error_msg = e), 403

@bp.app_errorhandler(404)
#Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again..
def page_not_found(e):
    return render_template('error.html', error_msg = e,status=404), 404

@bp.app_errorhandler(405)
#Method Not Allowed
def method_not_allowed(e):
    return render_template('error.html', error_msg = e, status=405), 405

@bp.app_errorhandler(408)
#request timeout
def request_timeout(e):
    return render_template('error.html', error_msg = e,status=408), 408

@bp.app_errorhandler(500)
#Internal Server Error
def internal_server(e):
    return render_template('error.html', error_msg = e, status=500), 500

@bp.app_errorhandler(ValueError)
def value_error(e):
    return render_template('error.html', error_msg = e,status=500), 500
