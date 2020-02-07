#!/opt/local/bin/python3

"""
    wiki-power-plant-production-table.py

    Generate a Wikipedia table of electrical production data for a power plant.
"""

import datetime
import requests

S = requests.Session()
URL = "http://api.eia.gov/series/"

# Get the eai-key. See https://www.eia.gov/opendata/register.php
f = open("eai-key.txt", "r")
api_key = f.readlines()[0].rstrip()
print(api_key)
f.close()

plant_id = 57074
plant_name = "Ivanpah 1"
now = datetime.datetime.now()
today = now.strftime("%B %d, %Y")

headers = {
    'User-Agent': 'WikiPowerPlantProductionTable/0.1 (User:Cxbrx)',
    'From': 'cxbrooks@gmail.com'
}

PARAMS = {
    "api_key": api_key,
    "series_id": "ELEC.PLANT.CONS_TOT_BTU.%s-NG-ALL.M" %(plant_id)
}

results = S.get(url=URL, params=PARAMS, headers=headers)
series= results.json()['series']

# For electrical production define the reference with a name.
# FIXME: get the name from the page
# For gas consumption, use the reference

ref="""<ref name=isegs1>{{cite web
 |url= http://www.eia.gov/electricity/data/browser/#/plant/%s
 |title=Electricity data browser - %s
 |work=Electricity Data Browser
 |publisher=[[Energy Information Administration]]
 |accessdate=%s}}</ref>""" %(plant_id, plant_name, today)

print("""{| class=wikitable
|+Net electricity production (All) [MWh]%s
|-
!Year
! style="width:75px;"| Jan
! style="width:75px;"| Feb
! style="width:75px;"| Mar
! style="width:75px;"| Apr
! style="width:75px;"| May
! style="width:75px;"| Jun
! style="width:75px;"| Jul
! style="width:75px;"| Aug
! style="width:75px;"| Sept
! style="width:75px;"| Oct
! style="width:75px;"| Nov
! style="width:75px;"| Dec
! style="width:75px;"| Total
|-""" %(ref))

# The data that we get from the eia has a start field and an end
# field.  The dates are in YYYYMM format, so we need to be able to
# iterate through them.

start = series[0]['start']
end = series[0]['end']
data = series[0]['data']

start_year = int(start[0:4])
start_month = int(start[4:])
end_year = int(end[0:4])
end_month = int(end[4:])
# print(start, start_year, start_month, end, end_year, end_month)

# The month with leading 0s
months = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

overall_total = 0
key_index = len(data) - 1
for year in range(start_year, end_year + 1):
    print("|" + str(year), end= " ")
    year_total = 0
    for month in range(1,13):
        if (year == start_year and month < start_month):
            print("|| NR", end=" ")
            continue
        if (year >= end_year and month > end_month):
            print("|| n/a", end=" ")
            continue
        key = str(year) + months[month]
        #print(key)

        pair = data[key_index]
        # Search the array for our month.  In theory, the data array
        # has no holes in it, but we should check.
        value = "NR"
        if pair[0] == key:
            key_index -= 1
            value = pair[1]
        else:
            for index in range(key_index, 0, -1):
                pair = data[index]
                if pair[0] == key:
                    value = pair[1]
                    key_index = index
        print("||", value, end=" ")
        if value != "NR":
            year_total += int(value)
    overall_total += int(year_total)             
    print("! ", year_total)

print("""|-
! colspan="13" |Total!!   %d
|}""" %(overall_total))
