import requests
from haversine import haversine

from models.permit import Permit

FOOD_TRUCK_FIELDS=['objectId','applicant','address','status','latitude','longitude']
FOOD_TRUCK_URL = 'https://data.sfgov.org/resource/rqzj-sfat.json?$select='


def createPermits(data):
    permits = []
    for permit in data:
        permits.append(Permit(locationId=permit['objectId'],
            applicant=permit['applicant'],
            address=permit['address'],
            status=permit['status'],
            latitude=permit['latitude'],
            longitude=permit['longitude']))

    return permits


def get_permits():
    url = FOOD_TRUCK_URL + ','.join(FOOD_TRUCK_FIELDS)
    data = requests.get(url).json()

    return createPermits(data)


def valid_coordinates(lat, lon):
    return True if -90 < lat < 90 and -180 < lon < 180 else False


def get_five_closest(permits, lat, lon):
    permits = sorted(permits, key=lambda permit: haversine((lat, lon), (permit.latitude, permit.longitude)))
    return permits[:5]
