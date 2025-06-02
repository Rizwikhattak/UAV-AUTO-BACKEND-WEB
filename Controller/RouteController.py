from Model import Route,LocationPins
from config import db
from Controller import LocationPinsController,StationController


class RouteController():

    @staticmethod
    def insert_route(data):
        try:

            station = StationController.insert_station(data)
            route = Route(name=data['name'],station_id=station.get('id'),rows=data['rows'],columns=data['columns'])
            db.session.add(route)
            db.session.commit()

            location_pins = LocationPinsController.insert_location_pins_list(route.id, data['locations'])
            return {'id':route.id,'name':route.name}
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def get_all_routes_without_location_pins():
        try:
            routes = Route.query.filter_by(validity=1).all()
            if routes:
                return [{'id':r.id,'name':r.name} for r in routes]
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
                    if route.id not in route_dict:
                        route_dict[route.id] = {
                            'id': route.id,
                            'name': route.name,
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
            route = Route.query.filter_by(id=id,validity=1).first()
            if route:
                return {'id':route.id,'name':route.name}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}


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
            StationController.update_station_by_id(data)
            if route:
                route.name = data['name']
                db.session.commit()
                return {'id':route.id,'name':route.name}
            else:
                return {}
        except Exception as e:
            print(e)
            return {}

