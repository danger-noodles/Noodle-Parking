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
            self.data = data
            return True
        else:
            return False
