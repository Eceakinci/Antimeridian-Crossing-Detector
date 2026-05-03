class GeoPoint:
    """
    Represents a GeoJSON point with longitude and latutdie.

    Validates:
        - coordinates must be numbers
        - type must be string
        - type must be Point, e.g. LineString
        - longitude must be between -180 and 180
        - latitude must be between -90 and 90
    """
    def __init__(self, geo_type: str, coordinates: list[float]):
        """
        Args:
            geo_type: GeoJSON type, must be "Point"
            coordinates: [longitude, latitude]

        Raises:
            TypeError: if coordinates are not numbers
            ValueError: if coordinates are out of valid range or type is not "Point"
        """

        if len(coordinates) != 2:
            raise ValueError(f"Coordinates must have exactly 2 values, got: {len(coordinates)}")

        longitude, latitude = coordinates

        if not all(isinstance(c, (int, float)) for c in coordinates):
            raise TypeError(f"Coordinates must be numbers, got: {coordinates}")
        if not isinstance(geo_type, str) or geo_type != "Point":
            raise ValueError(f"Type must be 'Point', got: {geo_type}")
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Longitude must be between -180 and 180, got {longitude}")
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Latitude must be between -90 and 90, got {latitude}")

        self.geo_type = geo_type
        self.longitude = longitude
        self.latitude = latitude
