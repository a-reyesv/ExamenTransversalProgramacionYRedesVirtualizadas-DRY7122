#Geolocalización con GraphHopper

import requests
import urllib.parse

# API Key de GraphHopper
graphhopper_key = "7800e48b-b354-4f22-be76-4b1e930f0cd8"

# URLs de GraphHopper
graphhopper_geocode_url = "https://graphhopper.com/api/1/geocode?"
graphhopper_route_url = "https://graphhopper.com/api/1/route?"

def geocode(location, key):
    url = graphhopper_geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    status = replydata.status_code

    if status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        return status, lat, lng
    else:
        return status, None, None

def route_distance_duration(origin, destination, key, vehicle="car"):
    params = {
        "point": [f"{origin[1]},{origin[2]}", f"{destination[1]},{destination[2]}"],
        "vehicle": vehicle,
        "locale": "es",  # Establecer el idioma de la narrativa en español
        "key": key
    }
    url = graphhopper_route_url + urllib.parse.urlencode(params, doseq=True)  # Utilizar doseq=True para manejar múltiples valores para la misma clave
    replydata = requests.get(url)
    json_data = replydata.json()
    status = replydata.status_code

    if status == 200 and json_data.get("paths"):
        distance_km = json_data["paths"][0]["distance"] / 1000  # en kilómetros
        distance_miles = distance_km * 0.621371  # convertir a millas

        time_seconds = json_data["paths"][0]["time"] / 1000  # en segundos
        time_minutes = time_seconds / 60  # en minutos

        # Convertir segundos a horas y minutos
        hours = int(time_minutes // 60)
        minutes = int(time_minutes % 60)

        narrative = json_data["paths"][0]["instructions"]

        return distance_km, distance_miles, hours, minutes, narrative
    else:
        return None, None, None, None, None

def main():
    print("Bienvenido al calculador de viajes con GraphHopper")
    print("Ingrese 's' para salir.")

    while True:
        ciudad_origen = input("Ciudad de Origen (ej. Santiago, Chile): ").strip()
        if ciudad_origen.lower() == 's':
            print("¡Hasta luego!")
            break
        
        ciudad_destino = input("Ciudad de Destino (ej. Buenos Aires, Argentina): ").strip()
        if ciudad_destino.lower() == 's':
            print("¡Hasta luego!")
            break
        
        # Geocodificación usando GraphHopper (ciudad_origen y ciudad_destino son en formato "Ciudad, País")
        origen = geocode(ciudad_origen, graphhopper_key)
        destino = geocode(ciudad_destino, graphhopper_key)

        if origen[0] == 200 and destino[0] == 200:
            # Permitir al usuario seleccionar el tipo de vehículo
            print("\nSeleccione el medio de transporte:")
            print("1. Automóvil")
            print("2. Bicicleta")
            print("3. Caminar")
            option = input("Elija una opción (por defecto, Automóvil): ").strip()

            if option == '2':
                vehicle = "bike"
            elif option == '3':
                vehicle = "foot"
            else:
                vehicle = "car"

            # Calcular distancia y duración usando GraphHopper
            distancia_km, distancia_millas, duracion_horas, duracion_minutos, narrativa = route_distance_duration(origen, destino, graphhopper_key, vehicle)
            
            if distancia_km is not None and duracion_horas is not None and duracion_minutos is not None and narrativa:
                print("\nInformación de la Ruta (GraphHopper):")
                print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
                print(f"Duración del viaje: {duracion_horas} horas {duracion_minutos} minutos")
                print("\nNarrativa del viaje:")
                print(narrativa)
            else:
                print("No se pudo obtener la información de la ruta desde GraphHopper.")
        
        else:
            print(f"No se pudo encontrar una o ambas ciudades en la geocodificación con GraphHopper: Origen {ciudad_origen}, Destino {ciudad_destino}")
        
        print("-----------------------------------------------------------------------")

if __name__ == "__main__":
    main()