from flask import Blueprint, render_template

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    return render_template('blog/blog.html')

@blog_bp.route('/como-calcular-itbis-republica-dominicana-dgii')
def post_itbis():
    # Artículo 1: ITBIS
    return render_template('blog/post_itbis.html')

@blog_bp.route('/introduccion-desarrollo-web-flask-python')
def post_flask():
    # Artículo 2: Flask
    return render_template('blog/post_flask.html')