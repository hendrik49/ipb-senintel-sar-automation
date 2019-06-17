from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import config

api = SentinelAPI(config.username, config.password)
footprint = geojson_to_wkt(read_geojson(config.geojson))
products = api.query(
                     date=('20180101', '20180102'),
                     platformname='Sentinel-2',
                     producttype='S2MSI1C',
                     orbitdirection=config.orbitdirection)
api.download_all(products)

