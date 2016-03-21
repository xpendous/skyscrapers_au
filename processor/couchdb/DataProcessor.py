__author__ = 'viva'

from shapely.geometry import Polygon, Point
import couchdb


# extract cbd coordinates
perth_cbd = [[115.85, -31.959], [115.855, -31.957], [115.859, -31.959], [115.867, -31.961], [115.868, -31.957],
             [115.87, -31.953], [115.858, -31.95], [115.85, -31.947], [115.848, -31.952], [115.849, -31.956]]

bris_cbd = [[153.015, -27.465], [153.026, -27.475], [153.031, -27.471], [153.032, -27.466], [153.035, -27.46],
            [153.034, -27.459], [153.033, -27.459], [153.032, -27.46], [153.028, -27.462], [153.022, -27.465],
            [153.018, -27.464]]

sydn_cbd = [[151.207, -33.882], [151.212, -33.876], [151.213, -33.869], [151.213, -33.863], [151.214, -33.86],
            [151.206, -33.859], [151.205, -33.862], [151.203, -33.866], [151.202, -33.873]]

melb_cbd = [[144.958, -37.828], [144.971, -37.824], [144.975, -37.814], [144.974, -37.811], [144.972, -37.806],
            [144.963, -37.805], [144.947, -37.809]]


poly = Polygon(perth_cbd)

server = couchdb.Server('http://127.0.0.1:5984')
db = server['melbourne_coordinates']
try:
    db_new = server['melbourne_coordinates_cbd']
except:
    db_new = server.create('melbourne_coordinates_cbd')

i = 0
for dbid in db:
    i += 1
    print i
    coords = db[dbid]['value']['geo']['coordinates']

    if poly.contains(Point(coords[1], coords[0])):
        db_new.save(db[dbid])
    else:
        pass
