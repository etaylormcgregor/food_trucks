import requests

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
