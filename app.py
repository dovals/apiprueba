from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from alembic.ddl import mysql
from flask_mysqldb import MySQL

app = Flask(__name__)
# BasicAuth
api = Api(app, prefix="/api/sepomex")
auth = HTTPBasicAuth()
USER_DATA = {
    "admin": "sepomex"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class PrivateResource(Resource):
    @auth.login_required
    def get(self):
        inicio
        return {"ingreso exitoso":42}


# conexion a BD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sepomex'
mysql = MySQL(app)


@app.route('/')
def inicio():
    return render_template("busqueda.html")


@app.route('/busqueda_cp', methods=['POST', 'GET'])
def busqueda_cp():
    if request.method == 'POST':
        dato = request.form['dato']
        print(dato)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT asentamiento FROM sepomex WHERE d_codigo = %s", (dato,))
        resultado = cursor.fetchall()
        return jsonify(resultado)


@app.route('/busqueda_nombre', methods=['POST', 'GET'])
def busqueda_nombre():
    if request.method == 'POST':
        dato = request.form['nombre']
        print(dato)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM sepomex WHERE municipio = %s OR d_estado = %s OR ciudad = %s ",
                       (dato, dato, dato))
        result = cursor.fetchall()
        if cursor is None:
            return
        else:
            return jsonify(result)


@app.route('/registro')
def registro():
    return render_template('registros.html')


@app.route('/action_registro', methods=['POST', 'GET'])
def action_registro():
    if request.method == 'POST':
        idEstado = request.form['idEstado']
        d_estado = request.form['d_estado']
        municipio = request.form['municipio']
        ciudad = request.form['ciudad']
        cp = request.form['cp']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sepomex (idEstado,d_estado,municipio,ciudad,d_codigo) VALUES (%s,%s,%s,%s,%s)",
                    (idEstado, d_estado, municipio, ciudad, cp))
        mysql.connection.commit()
        registro_correcto = cur.fetchone()
        if cur is None:
            return render_template("registros.html")
        else:
            return render_template('busqueda.html')

api.add_resource(PrivateResource,'/admin')

if __name__ == '__main__':
    app.run(debug=True)
