#!/usr/bin/env python3

## IMPORTS

from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


## CLASSES

class RdwClient:
    client = ApiClient(RDW_URL, RDW_KEY)
    data = None

    def get_plate_data(self) -> dict:
        return(self.data)

    def fetch_by_plate(self, plate) -> dict:
        try:
            # API call to get plate data
            data = self.client.get('/voertuiggegevens/' + plate)
        except Exception as err:
            print('API error:', err)

            return(False)

        # Return if necessary data is given
        if 'datumeersteafgiftenederland' in data or 'hoofdbrandstof' in data:
            # Replace these horrible dutch key names with the ones we use in the database
            try:
                data['parking_car_type'] = data.pop('voertuigsoort')
            except KeyError:
                data['parking_car_type'] = 'None'
            try:
                data['parking_car_body'] = data.pop('inrichting')
            except KeyError:
                data['parking_car_body'] = 'None'
            try:
                data['parking_car_name'] = data.pop('merk')
            except KeyError:
                data['parking_car_name'] = 'None'
            try:
                data['parking_car_fuel'] = data.pop('hoofdbrandstof')
            except KeyError:
                data['parking_car_fuel'] = 'None'
            try:
                data['parking_car_cylinder_capacity'] = data.pop('cilinderinhoud')
            except KeyError:
                data['parking_car_cylinder_capacity'] = 'None'
            try:
                data['parking_car_releasedate'] = data.pop('datumeersteafgiftenederland')
            except KeyError:
                data['parking_car_releasedate'] = 'None'

            self.data = data

            return(True)
        else:
            return(False)
