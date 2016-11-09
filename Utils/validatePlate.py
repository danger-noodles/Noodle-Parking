def validate_plate(fuel_type, year) -> bool:
    if fuel_type.lower() == 'diesel' and int(year[0]) < int('2001'):
        return False
    return True
