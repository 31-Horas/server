from flask import Flask
import psycopg2

app = Flask(__name__)

# Conectar a la base de datos de PostgreSQL
conn = psycopg2.connect(
    host="ibmdb.cxc7zm15y7c9.us-east-2.rds.amazonaws.com",
    database="ibmdb",
    user="postgres",
    password="rodo1997",
    sslmode="require"
)

# Crear un objeto cursor para ejecutar comandos SQL
cur = conn.cursor()

#TODO= Aqui se incluira las diferentes vistas de la aplicacion
# Definir una ruta para mostrar las tablas de la base de datos
@app.route("/tables")
def tables():
    # Ejecutar una consulta para obtener la lista de tablas
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    rows = cur.fetchall()

    # Crear una tabla HTML para mostrar los resultados
    table_html = "<table>"
    table_html += "<tr><th>Nombre de la tabla</th></tr>"
    for row in rows:
        table_html += "<tr><td>{}</td></tr>".format(row[0])
    table_html += "</table>"
    
    # Cerrar el cursor y devolver la tabla HTML
    cur.close()
    return table_html

# Definir una ruta para la página principal
@app.route("/")
def home():
    return "Hola, mundo!"

if __name__ == "__main__":
    app.run()