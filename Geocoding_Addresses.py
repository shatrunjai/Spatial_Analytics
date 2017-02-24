
# coding: utf-8

# In[ ]:

########################################################################################################################################################################
###    Author: Shatrunjai Singh
###
###    Title: Analyzing hospitals for LTC welness
###
###    Date: 02/22/2017
###
###    Dataset: Hospital data obtained from:
###             https://data.medicare.gov/Hospital-Compare/Hospital-General-Information/xubh-q36u
###
###    Purpose: To get geocode hopital lattitude, longitude from address
###
###    Description: Geocoding was performed using a the google geocoder 
###                 The original dataset was imported into pandas and the final results were saved in a new csv file "zipcodes" 
########################################################################################################################################################################



# In[26]:

import geocoder
import csv
import pandas as pd
import time
import json
import urllib2


# In[ ]:

#Read the hospital address as a file
hosp = pd.read_csv('C:\TEST\geocoding\Hospital_General_Information.csv')
hosp.head(5)


# In[24]:

#Use provider id and hospital address for geocoding
address=[]
provider_id=[]
latlong=[]
address=hosp['Complete_Add'].values.tolist()
provider_id=hosp['Provider ID'].values.tolist()
latlong=zip(provider_id,address)


# In[27]:

#Using the google geocoder to geocode for postcodes of the given hospital addresses
#The website limited reverse geocoding to less than 120 hits/minute but does not impose a daily limit :)
with open('C:\TEST\geocoding\hospital_latlong.csv', 'wb') as fp: #writing the zipcodes to a new file called zipcodes_for_challenge.csv
    a=csv.writer(fp, delimiter=',')
    zipplace=[] #a list to store ListID, Lattitude, Longitude and the Zipcode
    for item in latlong:       
            
            try:

                            time.sleep(0.32) #restricts the hits to website to less than 120/minute 
                            result = geocoder.google(item[1])                            
                            zipplace=[item[0],item[1],result.x,result.y] #zipping the different fields together
                            print zipplace
                            a.writerow(zipplace) #writing these fields into a new csv file
            except:
                            a.writerow("NA") #To make sure an error does not halt the entire process and I this will help figure out which postcodes are mising
                            print "Not working here-->wait 10 sec at item number: ",item[0]
                            time.sleep(10)
                            pass


    a.close()

