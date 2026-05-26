from flask import Flask, render_template, make_response
from routes.tools import tools_bp
from routes.blog import blog_bp
from routes.legal import legal_bp 
app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(tools_bp, url_prefix='/tools')

app.register_blueprint(blog_bp, url_prefix='/blog')
app.register_blueprint(legal_bp)

@app.route('/')
def home():
    tools = [
        {"title": "Calculadora de Sueldo Neto", "desc": "Calcula cuánto vas a cobrar limpio tras los descuentos de TSS e ISR en RD.", "url": "/tools/sueldo-neto", "icon": "bi-briefcase"},
        {"title": "Prestaciones Laborales", "desc": "Estima tu liquidación, cesantía y derechos adquiridos según el Código de Trabajo de RD.", "url": "/tools/prestaciones-laborales", "icon": "bi-cash-coin"},
        {"title": "Calculadora ITBIS", "desc": "Calcula el ITBIS incluido o aparte en RD (18% y 16%).", "url": "/tools/calculadora-itbis", "icon": "bi-calculator"},
        {"title": "Conversor USD ↔ DOP", "desc": "Tasa de cambio actualizada de Dólar a Peso Dominicano.", "url": "/tools/usd-dop", "icon": "bi-currency-exchange"},
        {"title": "Generador QR", "desc": "Crea códigos QR descargables gratis para tus enlaces o redes.", "url": "/tools/generador-qr", "icon": "bi-qr-code"},
        {"title": "JPG a PDF", "desc": "Convierte tus imágenes a documento PDF en segundos.", "url": "/tools/jpg-a-pdf", "icon": "bi-file-earmark-pdf"}
    ]
    return render_template('index.html', tools=tools)

@app.route('/robots.txt')
def robots():
    response = make_response(app.send_static_file('robots.txt'))
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml'), 200, {'Content-Type': 'application/xml'}



if __name__ == '__main__':
    app.run(debug=True)