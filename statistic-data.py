import pandas
import json
import MySQLdb

conn = MySQLdb.connect(host = "",
                       user = "",
                       passwd = "",
                       db = "")

def get_json_statistic_data(filename, sheet_name):
    statistic_data = pandas.read_excel(
        "./statistic-data/" + filename,
        sheet_name=sheet_name,
    )
    json_data = statistic_data.to_json(orient="records")
    return json.loads(json_data)


json_obj = get_json_statistic_data(
    "statistic_id1358087_ownership-of-cybersecurity-certifications-worldwide-2022.xlsx",
    "Data",
)

print(json.dumps(json_obj))

table_name = "Ownership_of_cybersecurity_certifications_worldwide_2022"
columns = [list(x.keys()) for x in json_obj][0]
values = [list(x.values()) for x in json_obj]

values_str = ""
for i, record in enumerate(values):
    val_list = []
    for v, val in enumerate(record):
        if type(val) == str:
            val = "'{}'".format(val.replace("'", "''"))
        val_list += [ str(val) ]
    values_str += "(" + ', '.join( val_list ) + "),\n"
values_str = values_str[:-2] + ";"

conn.execute("INSERT INTO %s (%s)\nVALUES\n%s" % (
    table_name,
    ', '.join(columns),
    values_str
)