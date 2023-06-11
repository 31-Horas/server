import pandas
import json

# import mysql.connector as mysqldb

# conn = mysqldb.connect(host="", user="", passwd="", db="")


def get_json_statistic_data(filename, sheet_name):
    statistic_data = pandas.read_excel(
        "./statistic-data/" + filename,
        sheet_name=sheet_name,
    )
    json_data = statistic_data.to_json(orient="records")
    return json.loads(json_data)


# def values_to_string(values):
#     values_str = ""
#     for i, record in enumerate(values):
#         val_list = []
#         for v, val in enumerate(record):
#             if type(val) == str:
#                 val = "'{}'".format(val.replace("'", "''"))
#             val_list += [str(val)]
#         values_str += "(" + ", ".join(val_list) + "),\n"
#     values_str = values_str[:-2] + ";"
#     return values_str


json_obj = get_json_statistic_data(
    "statistic_id1293871_salaries-in-the-it-industry-in-the-united-states-2021-by-type-of-job.xlsx",
    "Data",
)

print(json.dumps(json_obj))

# table_name = "Ownership_of_cybersecurity_certifications_worldwide_2022"
# columns = [list(x.keys()) for x in json_obj][0]
# values = [list(y.values()) for y in json_obj]

# conn.execute(
#     "INSERT INTO %s (%s)\nVALUES\n%s"
#     % (table_name, ", ".join(columns), values_to_string(values))
# )
