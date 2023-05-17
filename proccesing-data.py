# Pseudocodigo
# 1. Obtener mediante queries los datos de la base de datos
# 2. Procesar los datos para obtener los datos de interes
# 3. Guardar los datos en un archivo json
# 4. Leer el archivo json y convertirlo en un container de React
# 5. Mostrar los datos en la pagina web

# Importo las librerias necesarias
import pandas
import json
import mysql.connector as mysqldb

conn = mysqldb.connect(host="", user="", passwd="", db="")


# Funcion que convierte los datos de un archivo excel a un archivo json
def get_json_statistic_data(filepath, sheet_name):
    statistic_data = pandas.read_excel(
        "./statistic-data/" + filepath,
        sheet_name=sheet_name,
    )
    json_data = statistic_data.to_json(orient="records")
    return json.loads(json_data)


# Obtengo los Paths de cada archivo de la base de datos
industryFile_path = list()
industryFile_path = conn.execute("SELECT industryFile_path FROM industryFile")

# Por cada Path obtengo los datos de interes y los guardo en un archivo json
json_data = list()
for path in industryFile_path:
    print(path)
    json_data.append(get_json_statistic_data(path, "Data"))
print(json_data)

# Por cada json guardado en la lista json_data obtengo los nombres de las columnas y los valores
for data in json_data:
    columns = [list(x.keys()) for x in data][0]
    values = [list(y.values()) for y in data]
    print(columns)
    print(values)
    # Aqui tendria que obtener los excels de cada usuario y compararlas con las columnas y valores obtenidos
