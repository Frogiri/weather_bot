def is_valid_city_name(city_name: str) -> bool:
    """Проверяет, что название города корректное"""
    if not city_name or len(city_name) <2:
        return False
    return city_name.isalpha() or " " in city_name
def is_valid_units(units: str) -> bool:
    """Проверяет, что единица измерения корректные"""
    return units in ["metric", "imperial", "standard"]