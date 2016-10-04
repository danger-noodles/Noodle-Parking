from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


class RdwClient:
    client = ApiClient(RDW_URL, RDW_KEY)
    data = None

    def fetch_by_plate(self, plate) -> dict:
        data = None
        try:
            data = self.client.get('/voertuiggegevens/' + plate)
        except Exception as err:
            print('API error: ', err)

        self.data = data

    def validate_plate(self) -> bool:
        if not self.data:
            return False

        date = self.data['datumeersteafgiftenederland']
        year = date.split("-")
        fuel_type = self.data['hoofdbrandstof']

        if fuel_type.lower() == 'diesel' and int(year[0]) >= int('2001'):
            return False
        return True
