from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


class RdwClient:
    client = ApiClient(RDW_URL, RDW_KEY)
    data = None

    def get_plate_data(self) -> dict:
        return self.data

    def fetch_by_plate(self, plate) -> dict:
        try:
            # API call to get plate data
            data = self.client.get('/voertuiggegevens/' + plate)
        except Exception as err:
            print('API error:', err)
            return False

        # Return if necessary data is given
        if 'datumeersteafgiftenederland' in data or 'hoofdbrandstof' in data:
            # Rename keys to match the database
            data['parking_car_type'] = data.pop('voertuigsoort')
            data['parking_car_body'] = data.pop('inrichting')
            data['parking_car_fuel'] = data.pop('merk')
            data['parking_car_fuel'] = data.pop('hoofdbrandstof')
            data['parking_car_cylinder_capacity'] = data.pop('cilinderinhoud')
            data['parking_car_releasedate'] = data.pop('datumeersteafgiftenederland')
            self.data = data
            return True
        else:
            return False
