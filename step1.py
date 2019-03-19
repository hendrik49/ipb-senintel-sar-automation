from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import config

api = SentinelAPI(config.username, config.password)
footprint = geojson_to_wkt(read_geojson(config.geojson))
products = api.query(footprint,
                     date=(config.start_date, config.end_date),
                     platformname = config.platformname,
                     producttype=config.producttype,
                     orbitdirection=config.orbitdirection)
api.download_all(products)

