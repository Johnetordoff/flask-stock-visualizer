import csv
import sys
import json
from operator import itemgetter

def get_data():
    fieldnames =[]
    with open('ShortTicketSales .csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for value, key in row.iteritems():
                fieldnames.append(key)
            break

    csv_filename = 'TicketSales.csv'
    print "Opening CSV file: ",csv_filename
    f=open(csv_filename, 'r')
    csv_reader = csv.DictReader(f,fieldnames)
    json_filename = csv_filename.split(".")[0]+".json"
    print "Saving JSON to file: ",json_filename
    jsonf = open(json_filename,'w')
    data = json.dumps([r for r in csv_reader])
    jsonf.write(data)
    f.close()
    jsonf.close()

def splitjson():
    with open('ShortTicketSales.json') as data_file:
        data = json.load(data_file)

    Allcities = []
    for row in data:
        print(row['city'])
        try:
            Allcities.append(str(row['city']).lower().capitalize())
        except:
            pass
    cities = set(Allcities)

    proNames = [
        'Swan Lake',
        'The Nutcracker',
        'Strength and Longing',
        'Speed and Precision',
        'Serenade & Other Dances',
        'Prodigal Son',
        'Press Play',
        'Nutcracker Tea',
        'Keigwin, Fonte & Forsythe',
        'Jewels',
        'Gift to the City',
        'Fonte & Forsythe',
        'Doubletree Nutcracker Tea',
        'Don Quixote',
        "Director's Choice",
        'Curtain Pass Members',
#        'Copp\xc3lia',
 #       "Copp\xc3lia Children's Party",
        'Carmina Burana w Stravinsky',
        'A Tribute to Jerome Robbins',
        'A Program of "Firsts"',
        'A 50th Finale',
        '1314 Ruth Chris Dinner',
        'Gift to the City(Reserve)'
    ]
    for y in proNames:
        rows = []
        for x in data:
            if x['perf_desc'] == y:
                rows.append(x)

        with open( y+'.json', 'w') as f:
            json.dump(rows, f)

        cities = set(Allcities)
        cityGraphData = []

        for city in cities:
            dictCity = {}
            dictCity['city'] = city
            dictCity['pur'] = 0
            for row in rows:
                if row['city'] == city:
                    dictCity['pur'] += 1
            cityGraphData.append(dictCity)

        cityGraphData = sorted(cityGraphData, key=itemgetter('pur'))
        cityGraphData.reverse()
        print(cityGraphData)
        with open( y+'cityGraph.json', 'w') as f:
            json.dump(cityGraphData, f)


splitjson()