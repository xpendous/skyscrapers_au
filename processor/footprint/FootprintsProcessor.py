__author__ = 'viva'

import shapefile
import utm


# calculate the simple polygon area
def simple_polygon_area(coordinates):
    n = len(coordinates)
    simple_area = 0.0
    for x in range(n):
        y = (x + 1) % n
        simple_area += coordinates[x][0] * coordinates[y][1]
        simple_area -= coordinates[y][0] * coordinates[x][1]
    simple_area = abs(simple_area) / 2.0
    return simple_area


class FootprintsProcessor:
    def __init__(self, footprints):
        self.footprints = footprints

    @property
    def to_polygons(self):

        shapes = self.footprints.shapes()
        records = self.footprints.records()

        fields = self.footprints.fields
        # print fields

        write = shapefile.Writer(shapefile.POLYGON)
        write.fields = fields

        # store polygons of different buildings
        list_of_polygons = []

        for index_of_record, record in enumerate(records):

            # store polygons for parts of one building which is above 200 meters high
            if record[5] > 200 and record[2] != 'NA':

                # write.record = record
                write.records.append(record)

                parts = shapes[index_of_record].parts
                utm_points = shapes[index_of_record].points

                points =[]

                for point in utm_points:
                    latlon_point = utm.to_latlon(point[0], point[1], 55, 'H')
                    points.append([latlon_point[1], latlon_point[0]])


                num_points = len(points)
                parts.append(num_points)
                num_part = len(parts)

                # print "parts: " + str(num_part-1)

                list_of_points = []
                polygons = []

                if num_part > 2:

                    for i in range(num_part):
                        if i < num_part - 1:
                            list_of_points.append(points[parts[i]:(parts[i + 1])])
                    # print list_of_points

                    areas = []

                    # calculate area of every part of one building
                    for points in list_of_points:
                        areas.append(simple_polygon_area(points))

                    # print "areas are:" + str(areas)
                    large_areas = [areas[0]]
                    polygons.append(list_of_points[0])

                    # filter polygons by areas
                    for index, area in enumerate(areas):
                        if large_areas[0] / area < 100 and large_areas[0] != area:
                            large_areas.append(area)
                            polygons.append(list_of_points[index])

                    write.poly(parts=polygons)
                else:
                    # only one part
                    polygons = [points]
                    write.poly(parts=polygons)

                write.save("../../atlas/skyscraper_foot_prints/melbourne/SkyscraperFootprints")

                list_of_polygons.append(polygons)

        return list_of_polygons
