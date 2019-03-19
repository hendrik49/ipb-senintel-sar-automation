#1st Step: Automatic Download
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import urllib2, urllib, os 
import xml.etree.ElementTree as etree
import itertools, threading, time, sys

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
footprint = geojson_to_wkt(read_geojson('Lampung_extent_1.geojson'))
type_sar = 'GRD' # can cange to SLC
orbit = 'DESCENDING'
in_date = datetime(2018,4,1,0,0,0,0)
end_date = datetime(2018,10,31,23,59,59,519)
url =  'https://scihub.copernicus.eu/apihub/' 
username = 'didok49' # ask ITC for the username and password
password = 'sentinel49' 

#Get info product 
api = SentinelAPI(username, password) # fill with SMARTSeeds user and password
products = api.query(footprint,
                     producttype =type_sar,
                     orbitdirection =orbit,
                     date='['+format_date(in_date)+' TO '+format_date(end_date)+']')

# convert to Pandas DataFrame
df = api.to_dataframe(products)
#df = df.drop_duplicates(subset=['orbitnumber'], keep='first')
df = df.sort_values(['beginposition'], ascending=[False])
#df = df.head(2)
dirpath = cwd+'//sentineldata//'
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