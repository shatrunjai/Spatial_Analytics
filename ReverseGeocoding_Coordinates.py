
# coding: utf-8

# In[1]:

########################################################################################################################################################################
###    Author: Shatrunjai Singh
###
###    Title: Reverse Geocoding a set of lattitude and longitude coordinates
###
###    Date: 05/04/2015
###
###    Dataset: Open dataset
###
###    Purpose: To get reverse geocoded postal codes for the given longitudes/lattitude
###
###    Description: Reverse geocoding was performed using a free webservice which returns a JSON object when given long/lat coordinates. 
###                 The original dataset was imported into pandas and the final results were saved in a new csv file "zipcodes" 
########################################################################################################################################################################





# In[3]:

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pygeocoder import Geocoder
import time
import csv
import json
import urllib2


# In[ ]:


#Reading the original challenge csv file into a pandas dataframe called 'data'. 
#Saving the the ListingID,Latitude and Longitudes each into a separate list and then 'zipping' them together into a list called 'latlong' 
data=pd.read_csv('C:/data/opendoor/challenge.csv')
#data.head()
latitude=[]
longitude=[]
latlong=[]
latitude=data['GeoLat'].values.tolist()
longitude=data['GeoLon'].values.tolist()
Listid=data['ListingId'].values.tolist()
latlong=zip(Listid,latitude,longitude)


# In[ ]:

#Using the free open geocoder to reverse geocode for postcodes of the given lattitude/longitude coordinates
#Took around 9 hours to get all the codes 
#The website limited reverse geocoding to less than 120 hits/minute but does not impose a daily limit :)
with open('C:/data/opendoor/zipcodes.csv', 'wb') as fp: #writing the zipcodes to a new file called zipcodes_for_challenge.csv
    a=csv.writer(fp, delimiter=',')
    zipplace=[] #a list to store ListID, Lattitude, Longitude and the Zipcode
    for item in latlong:       
            
            try:

                            time.sleep(0.32) #restricts the hits to website to less than 120/minute 
                            url="http://www.geoplugin.net/extras/postalcode.gp?lat="+str(item[1])+"&long="+str(item[2])+"&format=json" #this url returns a JSON object with the postcode in it
                            postalcode=json.load(urllib2.urlopen(url))
                            zipcode=postalcode.get("geoplugin_postCode") #this extracts the postal code from the JSON object
                            zipplace=[item[0],item[1],item[2],zipcode] #zipping the different fields together
                            print zipplace
                            a.writerow(zipplace) #writing these fields into a new csv file
            except:
                            a.writerow("NA") #To make sure an error does not halt the entire process and I this will help figure out which postcodes are mising
                            print "Not working here-->wait 10 sec at item number: ",item[0]
                            time.sleep(10)
                            pass


    a.close()

