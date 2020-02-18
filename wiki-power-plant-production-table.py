#!/opt/local/bin/python3

"""
    wiki-power-plant-production-table.py

    Generate a Wikipedia table of electrical production data for a power plant.
"""

import datetime
import requests
from io import StringIO

S = requests.Session()
URL = "http://api.eia.gov/series/"


'''
    Return the Electrical Information Administration data as a wiki table

    series_is is a string like
    "ELEC.PLANT.CONS_TOT_BTU.57074-NG-ALL.M"
    
    totals is a YYYYMM indexed dictionary of the total values.

    start_min is the earliest start date seen thus far.

    end_max is the latest end date seen thus far.
''' 
def get_series(series_id, totals, start_min, end_max):

    # Get the eai-key. See https://www.eia.gov/opendata/register.php
    f = open("eai-key.txt", "r")
    api_key = f.readlines()[0].rstrip()
    # print(api_key)
    f.close()

    headers = { 
        'User-Agent': 'WikiPowerPlantProductionTable/0.1 (User:Cxbrx)',
        'From': 'cxbrooks@gmail.com'
    }

    PARAMS = {
        "api_key": api_key,
        #"series_id": "ELEC.PLANT.CONS_TOT_BTU.%s-NG-ALL.M" %(plant_id)
        "series_id": series_id
    }

    results = S.get(url=URL, params=PARAMS, headers=headers)
    #print(results)
    #print(results.json())
    series= results.json()['series']

    # The data that we get from the eia has a start field and an end
    # field.  The dates are in YYYYMM format, so we need to be able to
    # iterate through them.

    start = series[0]['start']
    end = series[0]['end']
    data = series[0]['data']

    # Update start_min and start_max for later use.
    if int(start) < start_min:
        start_min = start
    if int(end) > end_max:
        end_max = end

    return _generate_wiki_table(start, end, data, totals)

def _generate_wiki_table(start, end, data, totals):        
    start_year = int(start[0:4])
    start_month = int(start[4:])
    end_year = int(end[0:4])
    end_month = int(end[4:])
    # print(start, start_year, start_month, end, end_year, end_month)

    # The month with leading 0s.
    months = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    overall_total = 0
    key_index = len(data) - 1
    buffer = StringIO()
    for year in range(start_year, end_year + 1):
        buffer.write("|-\n! " + str(year) + "\n|")
        year_total = 0
        for month in range(1,13):
            if (month > 1):
                buffer.write("|| ")
            if (year == start_year and month < start_month):
                buffer.write("NR ")
                continue
            if (year >= end_year and month > end_month):
                buffer.write("n/a ")
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
                # Search the array for the YYYYMM starting at key_index
                for index in range(key_index, 0, -1):
                    pair = data[index]
                    if pair[0] == key:
                        value = pair[1]
                        key_index = index
            totals[key] = value
            buffer.write(str(f"{value:,d}") + " ")
            if value != "NR":
                year_total += int(value)
        overall_total += int(year_total)             
        buffer.write("! " + str(f"{year_total:,d}") + "\n")
    buffer.write("""|-
! colspan="13" |Total!!   %s
|}""" %(f"{overall_total:,d}"))
    return buffer.getvalue()

def get_ref(ref_name, plant_id, plant_name):
    # For electrical production define the reference with a name.
    # FIXME: get the name from the page
    # For gas consumption, use the reference

    now = datetime.datetime.now()
    today = now.strftime("%B %d, %Y")
    ref="""<ref name=%s>{{cite web
 |url= http://www.eia.gov/electricity/data/browser/#/plant/%s
 |title=Electricity data browser - %s
 |work=Electricity Data Browser
 |publisher=[[Energy Information Administration]]
 |accessdate=%s}}</ref>""" %(ref_name, plant_id, plant_name, today)

    columns = _wiki_table_columns()
    return("""{| class=wikitable
|+Net electricity production (All) [MWh]%s
%s
|-""" %(ref, columns))

def _wiki_table_columns():
    return("""|-
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
""")

if __name__ == '__main__':
    totals = {}
    start_min = 999999
    end_max = 0

    
    plant_id = 56405
    print(get_ref('eia-solar', plant_id, "Nevada Solar 1"))
    print(get_series("ELEC.PLANT.GEN.%s-SUN-ALL.M" %(plant_id), totals, start_min, end_max))

    # plant_id = 60885
    # print(get_ref('isegs1', plant_id, "Boulder Solar 2"))
    # print(get_series("ELEC.PLANT.GEN.%s-ALL-ALL.M" %(plant_id), totals, start_min, end_max))

    # plant_id = 60352
    # print(get_ref('isegs1', plant_id, "Boulder Solar 1"))
    # print(get_series("ELEC.PLANT.GEN.%s-ALL-ALL.M" %(plant_id), totals, start_min, end_max))

    # plant_id = 59472
    # print(get_ref('isegs1', plant_id, "Ft. Churchill PV"))
    # print(get_series("ELEC.PLANT.GEN.%s-ALL-ALL.M" %(plant_id), totals, start_min, end_max))

    #plant_id = 57275
    #print(get_ref('isegs1', plant_id, "Crescent Dunes Solar Energy"))
    #print(get_series("ELEC.PLANT.GEN.%s-ALL-ALL.M" %(plant_id), totals, start_min, end_max))

    # plant_id = 57074
    # print(get_ref('isegs1', plant_id, "Ivanpah 1"))
    # print(get_series("ELEC.PLANT.CONS_TOT_BTU.%s-NG-ALL.M" %(plant_id), totals, start_min, end_max))

    # plant_id = 57073
    # print(get_ref('isegs2', plant_id, "Ivanpah 2"))
    # print(get_series("ELEC.PLANT.CONS_TOT_BTU.%s-NG-ALL.M" %(plant_id), totals, start_min, end_max))                  

    # plant_id = 57075
    # print(get_ref('isegs3', plant_id, "Ivanpah 3"))
    # print(get_series("ELEC.PLANT.CONS_TOT_BTU.%s-NG-ALL.M" %(plant_id), totals, start_min, end_max))
                  
    # print(_wiki_table_columns())
    # # Because we are calling _generate_wiki_table, which operates on totals, we need a second dummy dictionary.
    # totals_placeholder = {}
    # print(start_min, end_max)
    # print(_generate_wiki_table(str(start_min), str(end_max), totals, totals_placeholder))
