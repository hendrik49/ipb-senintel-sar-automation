from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

api = SentinelAPI('didok49', 'sentinel49')
footprint = geojson_to_wkt(read_geojson('Lampung_extent_1.geojson'))
products = api.query(footprint,
                     date=('20180401', '20181230'),
                     platformname = 'Sentinel-1',
                     producttype='GRD',
                     orbitdirection='Descending')
api.download_all(products)

