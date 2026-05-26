from flask import Blueprint, render_template

legal_bp = Blueprint('legal', __name__)

@legal_bp.route('/politica-de-privacidad')
def privacidad():
    return render_template('footer/privacidad.html')

@legal_bp.route('/terminos-y-condiciones')
def terminos():
    return render_template('footer/terminos.html')

@legal_bp.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('footer/sobre_nosotros.html')

@legal_bp.route('/contacto')
def contacto():
    return render_template('footer/contacto.html')