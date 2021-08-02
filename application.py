"""
Main app script that calls everything
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, subprocess
import sys
import pandas as pd
import numpy as np

#files
trip_file = './data/trips.csv'
loc_file = './data/locations.csv'

#read in files as dataframes
df_trip = pd.read_csv(trip_file)
df_loc = pd.read_csv(loc_file)

application = Flask(__name__)


@application.route("/")
def welcome():
    return render_template("input.html")



@application.route("/receiver", methods=['POST', 'GET'])
def receiver():
    if request.method=='POST':
        default_name = '0'
        loc = str(request.form.get('loc', default_name))
        ott = get_lat_long_fac(loc)
        print('')
        print('--------------------------------------------------------')
        try:
            print(str(ott[0])+str(': ')+'Lat: '+str(ott[1])+' Long:'+str(ott[2])+', '+ott[3])
            print('')
            nn = find_number_of_trips(loc)
            print(nn[0])
            print('')
            print(nn[1])
            print('--------------------------------------------------------')
            print('')
            return ('{},{}'.format(str(ott[0])+str(': ')+'Lat: '+str(ott[1])+' Long:'+str(ott[2])+' '+ott[3],nn))
        except:
            print(ott[0])
            print('--------------------------------------------------------')
            print('')
            return ('{},{}'.format(loc,('Please Choose another Location','Please choose another location')))


def get_lat_long_fac(loc):
    '''
    function to get lat/long and if facility is owned by Carvana
    '''
    l1 = loc
    if l1 in np.array(df_loc['LocationCode']):
        target = df_loc[df_loc['LocationCode'] == l1]
        target = target.reset_index(drop=True)
        target_loc = target['LocationCode'][0]
        target_lat = target['Latitude'][0]
        target_lon = target['Longitude'][0]
        target_fac = int(target['FacilityOwnedByCarvana'][0])
        if target_fac == 1:
            owned = 'Owned by Carvana'
        else:
            owned = 'Not Owned by Carvana'
        return target_loc, target_lat, target_lon, owned
    else:
        msg = 'Location is not in the databasae...Try again'
    return [msg]

def find_number_of_trips(l2):
    #Origin
    do = df_trip[df_trip['Origin'] == l2]
    do = do.reset_index(drop=True)
    do.loc['Total'] = pd.Series(do['WeeklyCapacity'].sum(), index = ['WeeklyCapacity'])
    do.replace(float("NaN"), "", inplace=True)
    #Desitnation
    dd = df_trip[df_trip['Destination'] == l2]
    dd = dd.reset_index(drop=True)
    dd.loc['Total'] = pd.Series(dd['WeeklyCapacity'].sum(), index = ['WeeklyCapacity'])
    dd.replace(float("NaN"), "", inplace=True)
    return do, dd

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)
