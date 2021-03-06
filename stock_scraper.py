import csv
import sys
import json
from operator import itemgetter

def countUniValues():

    with open('csvtojson.json') as data_file:
        data = json.load(data_file)

    rows = []
    ticketTypes = []
    for row in data:
        if row['mos_desc'] == "TP Web":
            ticketTypes.append(row['price_type_desc'])

    ticketTypes = list(set(ticketTypes))

    tickets = 0
    for row in data:
        if row['mos_desc'] == "TP Call Center" and float(row['tot_due_amt'])  > 200:
            tickets += 1
    print(tickets)
    tickets = 0
    for row in data:
        if row['mos_desc'] == "TP Web" and float(row['tot_due_amt'])  > 200:
            tickets += 1
    print(tickets)
    tickets = 0
    for row in data:
        if row['mos_desc'] == "TP Box Office" and float(row['tot_due_amt']) < 200 and float(row['tot_due_amt']) > 100:
            tickets += 1
    print(tickets)


    #10.19 tickets per repeat
    #2408 non-repeat box office
    #1470 repeat box office customers

    #4.225 repeat
    #2.789 non-repeat
    #2519 repeat call customers
    #3462 non-repeat call customers

    #4682 repeat web customers
    #16825 non-repeat web

    #7830 repeat customers
    #3878 box office customers
    #5981 call customers
    #21507 web customers
    #30773 total customers
    #63688 total purchases
    #166434 ticket

def calc():

    print 4682*6.053 - 4682*2.658
calc()

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

    for row in data:
        del row['perf_no']


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

        with open( y+'cityGraph.json', 'w') as f:
            json.dump(cityGraphData[:10], f)

        for row in rows:
            del row['city']

        with open( y+'.json', 'w') as f:
            json.dump(rows, f)



