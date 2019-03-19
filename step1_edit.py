#1st Step: Automatic Download
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import urllib2, urllib, os 
import xml.etree.ElementTree as etree
import itertools, threading, time, sys
import config

# Here for convert date
def format_date(in_date):
    """Format date or datetime input or a YYYYMMDD string input to
    YYYY-MM-DDThh:mm:ssZ string format. In case you pass an
    """
    if type(in_date) == datetime or type(in_date) == date:
        return in_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        try:
            return datetime.strptime(in_date, '%Y%m%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            return in_date

# Start
# Define initial date, end date, and parameter for download SAR
cwd = os.getcwd()
footprint = geojson_to_wkt(read_geojson(config.geojson))
type_sar = config.producttype # can cange to SLC
orbit = config.orbitdirection
in_date = config.start_date
end_date = config.end_date
url =  config.url
username = config.username # ask ITC for the username and password
password = config.password 

#Get info product 
api = SentinelAPI(username, password) # fill with SMARTSeeds user and password
products = api.query(footprint,
                     producttype =type_sar,
                     orbitdirection =orbit,
                     date=(config.start_date, config.end_date))

# convert to Pandas DataFrame
df = api.to_dataframe(products)
#df = df.drop_duplicates(subset=['orbitnumber'], keep='first')
df = df.sort_values(['beginposition'], ascending=[False])
#df = df.head(2)
dirpath = cwd + config.sentineldirpath
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
# Start Download
for entry in range(0, len(df)):     
    #The uuid element allows to create the path to the file 
    uuid_element = df['uuid'][entry]
    id_sar = df['identifier'][entry]
    sentinel_link = df['link'][entry] 
    
    #Destinationpath with filename where download to be stored
    destinationpath = dirpath + id_sar + '.zip'
    
    if os.path.exists(destinationpath): 
        print id_sar +' already downloaded'
    else:
        #Download file and read
        try:
            api.download(df['uuid'][entry], directory_path=dirpath, checksum=True)
        except:
            print "error connection!.... Download Interrupted!"
            time.sleep(2)
            #sys.stdout.write('\rDownload Interrupted!     ')
            os.remove(destinationpath+'.incomplete')