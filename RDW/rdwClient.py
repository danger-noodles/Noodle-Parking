from Utils.config import RDW_KEY, RDW_URL
from RDW.apiClient import ApiClient


class RdwClient:
    """
        Author: Nick Bout
        Class: RdwClient
        This class uses the API client to fetch the car data from the RDW api based on licence plate
    """
    client = ApiClient(RDW_URL, RDW_KEY)
    data = None

    def get_plate_data(self) -> dict:
        """
            Function to get the data returned by the RDW API

            ARGS:
                --
            Returns:
                DICT: Dictionary with all returned data
        """
        return self.data

    def fetch_by_plate(self, plate) -> bool:
        """
            Function to fetch car data by licence plate from the RDW API

            ARGS:
                plate STRING: the licence plate in string format. E.G: xx-99-xx
            Returns:
                BOOL: Returns if API call was a success
        """
        try:
            # API call to get plate data
            data = self.client.get('/voertuiggegevens/' + plate)
        except Exception as err:
            print('API error:', err)
            return False

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

            return True
        else:
            return False
