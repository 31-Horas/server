import pandas
import json


def get_statistic_data(filename, sheet_name):
    statistic_data = pandas.read_excel(
        "./statistic-data/" + filename,
        sheet_name=sheet_name,
    )
    json_str = statistic_data.to_json(orient="records")
    return json_str


print(
    get_statistic_data(
        "statistic_id1358087_ownership-of-cybersecurity-certifications-worldwide-2022.xlsx",
        "Data",
    )
)
