import json
import csv
import pandas as pd

def make_json(csvFilePath, jsonFilePath):
    tablelabels = []                                                # stores certification names
    tabledata = []                                                  # stores number of times a certification appears
    df = pd.read_csv(csvFilePath)

    for certification in df['certification']:
        if certification in tablelabels:
            tabledata[tablelabels.index(certification)] += 1        # if a certification was already saved, add 1 to the counter
        else:
            tablelabels.append(certification)                       # else add the certification to the array
            tabledata.append(1)                                     # and initialize its counter at 1
    
    dataset = [{'label': 'Certifications in IBM',                   # stores data to be displayed in the graph
                'data': tabledata,
                'backgroundColor': 'rgba(75, 192, 192, 0.6)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1}]

    graphdata = {                                                   # stores dataset array and certification names as labels
        'labels': tablelabels,
        'datasets': dataset,
    }

    tableoptions = {                                                # stores scaling options of graph
        'scales': {
            'x': {'type': 'category'},
            'y': {'beginAtZero': True}
        }
    }

    datajson = {                                                    # stores previous dictionaries
        'type': 'bar',
        'data': graphdata,
        'options': tableoptions
    }

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(datajson, indent=4))                 # writes datajson in new .json file
    

csvFilePath = r'testcsv.csv'                                        # stores input .csv file
jsonFilePath = r'badges-report.json'                                # stores output .json file

make_json(csvFilePath, jsonFilePath)