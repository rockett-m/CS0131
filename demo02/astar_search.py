import sys
import re

def parse_city_data_file(data_file):
    city_data_regex = re.compile(r"(?P<city>^.+) "
                                 r"(?P<lat>-*\d+\.\d+) "
                                 r"(?P<lon>-*\d+\.\d+)"
                                 )

    city_distance_regex = re.compile(r"(?P<city1>^.+), "
                                     r"(?P<city2>.+): "
                                     r"(?P<dist>-?\d+.\d+)"
                                    )

    city_count = 0
    city_file = open(data_file)
    for line in city_file.readlines():
        city_result = city_data_regex.search(line)
        city_distance_result = city_distance_regex.search(line)
        if city_result != None:
            city_name = city_result.group('city')
            latitude = float(city_result.group('lat'))
            longitude = float(city_result.group('lon'))
    
            city_count = city_count + 1
            print("%3d. %s is located at (latitude, longitude) = (%.2f, %.2f)" % 
                    (city_count, city_name, latitude, longitude))
        elif city_distance_result != None:
            city1_name = city_distance_result.group('city1')
            city2_name = city_distance_result.group('city2')
            distance = float(city_distance_result.group('dist'))

            print("%s is %.2f miles from %s" % (city1_name, distance, city2_name))

# Run as: python astar_search.py FILENAME
def main():
    filename = sys.argv[1]
    parse_city_data_file(filename)

main()
