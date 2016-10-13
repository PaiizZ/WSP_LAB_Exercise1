import  webbrowser
import  urllib.request
u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open('rt22.xml','wb')
f.write(data)
f.close()

office_lat = 41.980262
office_lon = -87.668452

from xml.etree.ElementTree import parse
from math import sin, cos, sqrt, atan2, radians

def findBus(doc):
    for bus in doc.findall('bus'):
        lat = float(bus.findtext('lat'))
        lon = float(bus.findtext('lon'))
        d = str(bus.findtext('d'))
        if lat == office_lat and lon == office_lon and d == 'North Bound':
            print(''+bus.findtext('id'))
        else:
            print('not found')

def calMile(lat,lon):
    R = 6373.0
    M = 0.621371

    lat1 = radians(office_lat)
    lon1 = radians(office_lon)
    lat2 = radians(lat)
    lon2 = radians(lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * M
    return  distance


def findCloser(doc):
    map = 'https://maps.googleapis.com/maps/api/staticmap?size=600x400&zoom=13&center=41.980262,-87.668452&markers=color:red%7Clabel:P%7C41.980262,-87.668452'
    for bus in doc.findall('bus'):
        lat = float(bus.findtext('lat'))
        lon = float(bus.findtext('lon'))
        d = str(bus.findtext('d'))
        distance = calMile(lat,lon)

        if distance <= 0.5 and d == 'North Bound':
            map+='&markers=color:blue%7Clabel:B%7C'+str(lat)+','+str(lon)
        else:
            print('distance :'+str(distance))
    webbrowser.open_new_tab(map)

doc = parse('rt22.xml')
findBus(doc)
findCloser(doc)





