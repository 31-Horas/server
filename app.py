from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from csv_to_json import make_json
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Data(Resource):
    def get(self):
        data = {'message': 'Hola desde Flask!'}
        return jsonify(data)

class Index(Resource):
    def get(self):
        return jsonify({'message': 'Hola, este es un punto final de prueba!'})

class Welcome(Resource):
    def get(self):
        return jsonify({'message': 'Hola, desde welcome!'})

class ProcesarCSV(Resource):
    def post(self):
        archivo_csv = request.files['archivo_csv']
        # Llamar al script que procesa el archivo CSV y devuelve los datos en formato JSON
        datos_json = make_json(archivo_csv)
        print(datos_json)
        return jsonify(datos_json)

api.add_resource(HelloWorld, '/api/helloworld')
api.add_resource(Data, '/api/data')
api.add_resource(Index, '/api/')
api.add_resource(Welcome, '/api/welcome')
api.add_resource(ProcesarCSV, '/api/procesar-csv')

if __name__ == '__main__':
    app.run(debug=True)