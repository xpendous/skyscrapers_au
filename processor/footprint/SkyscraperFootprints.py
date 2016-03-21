import shapefile
import FootprintsProcessor


# bfp_shp = shapefile.Reader("../../atlas/skyscraper_foot_prints/melbourne/SkyscraperFootPrints.shp")

bris = ['Infinity Tower', 'Soleil', 'Aurora', 'Riparian Plaza', 'ONE ONE ONE Eagle Street']
melb = ['Eureka Tower', '120 Collins Street', '101 Collins Street', 'Prima Pearl', 'Rialto Towers',
        '568 Collins Street', 'Bourke Place', 'Telstra Corporate Centre', 'Melbourne Central Tower',
        'Freshwater Place']
perth = ['Central Park', 'Brookfield Place', '108 St Georges Terrace', 'QV1', 'Exchange Plaza']
sydn = ['Chifley Tower', 'Citigroup Centre', 'Deutsche Bank Place', 'Meriton World Tower', 'MLC Centre',
        'Governor Phillip Tower', 'Ernst & Young Tower', 'RBS Tower', 'ANZ Tower', 'Suncrop Place']

skyscraper = {'brisbane': bris, 'melbourne': melb, 'perth': perth, 'sydney': sydn}


class SkyscraperFootprint:
    def __init__(self, city):
        self.city = city
        print self.city

    def get_skyscraper_by_city(self):
        bfp_shp = shapefile.Reader("../../atlas/cbd_building_foot_prints/" + self.city + "/buildings.shp")
        records = bfp_shp.records()
        shapes = bfp_shp.shapes()

        print 'hahha'

        list_of_polygons = {}

        for i in range(0, len(records) - 1):
            name = records[i][0]
            if name in skyscraper[self.city]:

                list_of_polygons[name] = shapes[i].points
        return list_of_polygons


'''
list_of_polygons = FootprintsProcessor(bfp_shp).to_polygons

for polygons in list_of_polygons:
        print len(polygons)
        print polygons
'''

'''
sky = shapefile.Reader("atlas/skyscraper_foot_prints/melbourne/SkyscraperFootprints.shp")

sky_shapes = sky.shapes()
records = sky.records()
fields = sky.fields
# print len(bfp_shp.shapes())

print sky_shapes[0].points
print len(sky_shapes)
print records[55]
'''
