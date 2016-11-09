def validate_plate(data) -> bool:
    if not data:
        return False

    date = data['datumeersteafgiftenederland']
    year = date.split("-")
    fuel_type = data['hoofdbrandstof']

    if fuel_type.lower() == 'diesel' and int(year[0]) < int('2001'):
        return False
    return True
