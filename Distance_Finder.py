from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic

# API LIMITATION IS 2500 REQUESTS PER DAY

def find_distance(A, B):
    key = 'YOUR-API-KEY'  # get api key from:  https://opencagedata.com
    geocoder = OpenCageGeocode(key)

    result_A = geocoder.geocode(A)
    lat_A = result_A[0]['geometry']['lat']
    lng_A = result_A[0]['geometry']['lng']

    result_B = geocoder.geocode(B)
    lat_B = result_B[0]['geometry']['lat']
    lng_B = result_B[0]['geometry']['lng']


    return (geodesic((lat_A, lng_A), (lat_B, lng_B)).miles)