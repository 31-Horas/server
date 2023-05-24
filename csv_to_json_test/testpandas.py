# import csv
import mysql.connector as mysqldb
import json
import pandas as pd

conn = mysqldb.connect (
    host = "localhost",
    user = "kreiji",
    password = "Marca17*",
    db= "thirtyone_otters"
)

def insert_into_mysql(jsonFilePath):
    # Load JSON data into a pandas DataFrame
   # Load JSON data into a dictionary
    with open(jsonFilePath) as file:
        data = json.load(file)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data.items(), columns=['certification', 'count'])

    # Prepare the INSERT query
    table_name = "badges_report"
    columns = ['certification', 'count']
    placeholders = ', '.join(['%s'] * len(columns))
    query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ', '.join(columns), placeholders)

    # Iterate over the DataFrame and insert each row into the MySQL database
    cursor = conn.cursor()

    # cursor.execute("CREATE TABLE badges_report (certification LONGTEXT, count INT)")

    for _, row in df.iterrows():
        values = tuple(row)
        cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

def make_json(csvFilePath, jsonFilePath):

    df = pd.read_csv(csvFilePath)
    column = 'certification'

    data = {}

    for certification in df[column]:
        if certification in data:
            data[certification] += 1
        else:
            data[certification] = 1
    
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


csvFilePath = r'badges-report-2023-01-25-1404_IBMTEC.xlsx - Sheet1.csv'
jsonFilePath = r'badges-report.json'

# make_json(csvFilePath, jsonFilePath)
insert_into_mysql(jsonFilePath)