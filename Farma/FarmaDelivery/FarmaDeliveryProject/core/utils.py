import requests

PAIS = 'Argentina'
USER_AGENT = 'FarmaDelivery/1.0 '


def obtener_coordenadas(calle, numero, ciudad, provincia, timeout=10):
    """Consulta el servicio de geocodificación de Nominatim.

    Devuelve un dict con 'latitud', 'longitud' y 'direccion_encontrada',
    o None si no encuentra la dirección.
    """
    direccion = f'{calle} {numero}, {ciudad}, {provincia}, {PAIS}'
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': direccion, 'format': 'json', 'limit': 1, 'countrycodes': 'ar'}
    headers = {'User-Agent': USER_AGENT}
    r = requests.get(url, params=params, headers=headers, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if data:
        return {
            'latitud': float(data[0]['lat']),
            'longitud': float(data[0]['lon']),
            'direccion_encontrada': data[0]['display_name'],
        }
    return None