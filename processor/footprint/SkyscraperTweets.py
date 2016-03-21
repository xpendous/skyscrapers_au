from SkyscraperFootprints import SkyscraperFootprint
from shapely.geometry import Polygon, Point
import couchdb

server = couchdb.Server('http://127.0.0.1:5984')

'''
db = server['coords_bris_cbd']
try:
    db_new = server['sky_bris']
except:
    db_new = server.create('sky_bris')

skyscraper_footprints = SkyscraperFootprint('brisbane').get_skyscraper_by_city()

print skyscraper_footprints

i = 0
for dbid in db:
    i += 1
    print i
    coords = db[dbid]['value']['coordinates']['coordinates']

    for skyscraper in skyscraper_footprints:
        polygon = skyscraper_footprints[skyscraper]
        poly = Polygon(polygon)

        if poly.contains(Point(coords[0], coords[1])):
            print 'yes'
            db_new.save(db[dbid])
            doc = db_new[dbid]
            doc['sky'] = skyscraper
            db_new.save(doc)
            break
        else:
            pass

'''


db = server['sky_perth']
for dbid in db:
    print db[dbid]['sky'], db[dbid]['value']['created_at']
