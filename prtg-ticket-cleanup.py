# /home/bocchrj/miniconda3/bin/python
# source activate dev01
# PRTG Ticket Cleanup
# Rich Bocchinfuso - 20191226
# prtg-ticket-cleanup.py

# importing required libraries
import os
import sys
import requests
import configparser
import pandas as pd

# read and parse config file
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# api credentials
username = config['creds']['username']
password = config['creds']['password']

# function to remove pesky ^m from eol
def cleanOutput():
    inputfile = '_prtg.out'
    tmpfile = open('_prtg.tmp', 'w')
    for line in open(inputfile):
        line = line.rstrip()
        # print (line)
        tmpfile.write(line + '\n')
    tmpfile.close()
    os.rename('_prtg.tmp', '_prtg.csv')
    os.remove('_prtg.out')


# api-endpoint
apiurl = config['api']['apiurl']
closeapiurl = config['api']['closeapiurl']

# defining a params dict for the parameters to be sent to the API
listParams = (('content', 'tickets'), ('columns', 'datetime,parentid,status'),
              ('filter_status', '1'), ('username', username), ('password', password))
# print (listParams)

# sending get request and saving the response as response object
r = requests.get(url=apiurl, params=listParams)

# output open tickets to CSV for import into pandas dataframe
d = (r.text.encode('utf8'))
# print (d.decode())
f = open('_prtg.out', 'w')
print(d.decode(), file=f)
f.close()
cleanOutput()

# import open tickets into pandas dataframe
df = pd.read_csv('_prtg.csv')
# print (df)

# crate list of values from ticket ID column
ticketList = df['Ticket ID'].values
# print (ticketList)

# loop through all open tickets and close them
len(ticketList)
if len(ticketList) > 0:
    for ID in ticketList:
        # defining a params dict for the parameters to be sent to the API
        closeParams = (('id', ID), ('content', 'close'),
                       ('username', username), ('password', password))
        # print (closeParams)
        print('Closing Ticket #' + str(ID))
        closeRequest = requests.get(url=closeapiurl, params=closeParams)
else:
    print('No tickets to be closed!')

# cleanup
os.remove('_prtg.csv')

