from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


class RdwClient:
    client = ApiClient(RDW_URL, RDW_KEY)
    data = None

    def get_plate_date(self) -> dict:
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
            self.data = data
            return True
        else:
            return False

    def validate_plate(self) -> bool:
        if not self.data:
            return False

        date = self.data['datumeersteafgiftenederland']
        year = date.split("-")
        fuel_type = self.data['hoofdbrandstof']

        if fuel_type.lower() == 'diesel' and int(year[0]) >= int('2001'):
            return False
        return True
