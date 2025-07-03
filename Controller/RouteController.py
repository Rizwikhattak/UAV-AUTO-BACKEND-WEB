from Model import Route,LocationPins
from config import db
from Controller import LocationPinsController,StationController


class RouteController():
    @staticmethod
    def insert_route(data):
        try:

            station = StationController.insert_station(data)
            route = Route(name=data['name'], station_id=station.get('id'), rows=data['rows'], columns=data['columns'])
            db.session.add(route)
            db.session.commit()

            location_pins = LocationPinsController.insert_location_pins_list(route.id, data['locations'])
            return {'id': route.id, 'name': route.name}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_routes_without_location_pins():
        try:
            routes = Route.query.filter_by(validity=1).all()
            if routes:
                for r in routes:
                    station = StationController.get_station_by_id(r.station_id)
                    return {'id': r.id, 'name': r.name,
                            'station_latitude': station['latitude'],
                            'station_longitude': station['longitude'],
                            'rows': r.rows,
                            'columns': r.columns
                            }
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_all_routes_with_location_pins():
        try:
            routes = (db.session.query(Route, LocationPins)
                      .join(LocationPins, Route.id == LocationPins.route_id)
                      .filter(Route.validity == 1)
                      .all())

            if routes:

                # Create a dictionary to group location pins by route
                route_dict = {}
                for route, location in routes:
                    station = StationController.get_station_by_id(route.station_id)
                    if route.id not in route_dict:
                        route_dict[route.id] = {
                            'id': route.id,
                            'name': route.name,
                            'station_latitude': station['latitude'],
                            'station_longitude': station['longitude'],
                            'number_of_drones':station['number_of_drones'],
                            'station_name':station['name'],
                            'station_id':station['id'],
                            'rows': route.rows,
                            'columns': route.columns,
                            'locations': []  # Initialize the list of locations
                        }
                    # Append location data to the corresponding route
                    route_dict[route.id]['locations'].append({
                        'location_pin_id': location.id,
                        'latitude': location.latitude,
                        'longitude': location.longitude
                    })
                # Convert the dictionary to a list of routes
                return list(route_dict.values())
            else:
                return []
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_route_by_id(id):
        try:
            # Query for a single route and its pins
            result = (
                db.session.query(Route, LocationPins)
                .join(LocationPins, Route.id == LocationPins.route_id)
                .filter(Route.validity == 1, Route.id == id)
                .all()  # Fetch all LocationPins for this single route
            )

            if not result:
                return None  # No route found

            # Build the route dictionary
            route_obj, _ = result[0]
            station = StationController.get_station_by_id(route_obj.station_id)
            route_dict = {
                "id": route_obj.id,
                "name": route_obj.name,
                "station_latitude": station["latitude"],
                "station_longitude": station["longitude"],
                "number_of_drones": station["number_of_drones"],
                "station_name": station["name"],
                "station_id": station["id"],
                "rows": route_obj.rows,
                "columns": route_obj.columns,
                "locations": [],
            }

            for _, location in result:
                if location.validity:
                    route_dict["locations"].append({
                        "location_pin_id": location.id,
                        "latitude": location.latitude,
                        "longitude": location.longitude
                    })

            return route_dict

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def delete_route_by_id(route_id):
        try:
            route = Route.query.filter_by(id=route_id, validity=1).first()
            location_pins = LocationPins.query.filter_by(route_id=route_id,validity=1).all()
            StationController.delete_station_by_id(route.station_id)
            if route:
                route.validity = 0
                db.session.commit()
                if location_pins:
                    for location_pin in location_pins:
                        location_pin.validity = 0
                        db.session.commit()
                return {'id':route.id,'name':route.name}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def update_route_by_id(data):
        try:
            route = Route.query.filter_by(id=data['id'], validity=1).first()
            if route:
                route.name = data['name']
                route.rows = data.get('rows')
                route.columns = data.get('columns')
                db.session.commit()
                stationPayload = {'id':route.station_id,'name':route.name,'latitude':data['station_latitude'],'longitude':data['station_longitude']}
                StationController.update_station_by_id(stationPayload)
                for location in data.get('locations'):
                    if(location.get('location_pin_id')):
                        location['id'] = location.get('location_pin_id')
                        LocationPinsController.update_location_pin_by_id(location)
                    else:
                        location['route_id'] = route.id
                        LocationPinsController.insert_location_pins(location)
                for pin_id in data.get("deleted_pins"):
                    if pin_id:
                        LocationPinsController.delete_location_pin_by_id(pin_id)

                return {'id':route.id,'name':route.name}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}