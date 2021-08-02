import pandas as pd
import numpy as np
import argparse
import sys


#files
trip_file = './data/trips.csv'
loc_file = './data/locations.csv'

#read in files as dataframes
df_trip = pd.read_csv(trip_file)
df_loc = pd.read_csv(loc_file)

#parse the location from the command line
parser = argparse.ArgumentParser(description='Location Script')
parser.add_argument('--loc', type=str,
                    help='Thelocation code for input')
args = vars(parser.parse_args())
location = args['loc']

#functions for finding results of input
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

#get locatioin from command line input
ff = location

#print the results out to screen
print('')
print('--------------------------------------------------------')
mm = get_lat_long_fac(ff)
try:
    print(str(mm[0])+str(': ')+'Lat: '+str(mm[1])+' Long:'+str(mm[2])+', '+mm[3])
    print('')
    nn = find_number_of_trips(ff)
    print(nn[0])
    print('')
    print(nn[1])
    print('--------------------------------------------------------')
    print('')
except:
    print(mm[0])
    print('--------------------------------------------------------')
    print('')