from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

api = SentinelAPI('didok49', 'sentinel49')
footprint = geojson_to_wkt(read_geojson('search_polygon.geojson'))
products = api.query(footprint,
                     producttype='SLC',
                     orbitdirection='ASCENDING')
api.download_all(products)