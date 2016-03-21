__author__ = 'viva'

import shapefile

import utm

import re

import couchdb

import json

from shapely.geometry import Polygon, Point


'''
# shapefile test

# shp = shapefile.Reader("building_foot_prints/melbourne/BuildingFootPrints.shp")
shp = shapefile.Reader("test/extract/buildings.shp")

shapes = shp.shapes()
records = shp.records()
fields = shp.fields


# print shapes[1808].points


for point in shapes[18908].points:
    print utm.to_latlon(point[0], point[1], 55, northern=False)


for record in records:
    print record
'''


#

server = couchdb.Server('http://127.0.0.1:5984/')
# db = server['original_melbourne']

try:
    db_new = server['coords_bris']
except:
    db_new = server.create('coords_bris')



'''
i = 0
for dbid in db:
    i += 1
    print i
    if db[dbid]["user"]["id_str"] == '317680173':
        pass
    else:
        db_new.save(db[dbid])
'''

myjson = open('/Users/viva/Downloads/bris_coords.txt', mode='r')

i = 0
for line in myjson:
    i += 1
    data = json.loads(line[:-3])
    db_new.save(data)
    print i



'''
# all tweets with coordinates, and filter municipal ones
# db: melbourne, db_new: melbourne_municipal_coordinates

mmb_shp = shapefile.Reader("municipal_boundary/melbourne/Melbourne Municipal Boundary.shp")
mmb_shapes = mmb_shp.shapes()
poly = Polygon(mmb_shapes[0].points)

j = 0

for dbid in db:
    j += 1
    print j
    point = Point(utm.from_latlon(db[dbid]["value"]["geo"]["coordinates"][0], db[dbid]["value"]["geo"]["coordinates"][1])[0:2])
    if poly.contains(point):
        db_new.save(db[dbid])

'''

'''
# db: original_melbourne_database (harvester's database)
# calculate the number of tweets with coordinates
i = 0
for dbid in db:

    try:
        if db[dbid]["coordinates"]:
            i += 1
            print i
    except:
        pass
'''