from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


class RdwClient:
    client = ApiClient(RDW_URL, RDW_KEY)

    def fetch_by_plate(self, plate) -> dict:
        data = None
        try:
            data = self.client.get('/voertuiggegevens/' + plate)
        except Exception as err:
            print('API error: ', err)

        return data

    def validate_plate(self, carData) -> bool:
        valid = True
        date = carData['datumeersteafgiftenederland']
        year = date.split("-")
        fuel_type = carData['hoofdbrandstof']

        if fuel_type.lower() == 'diesel' and int(year[0]) >= int('2001'):
            valid = False

        return valid
