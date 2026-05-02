from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models import GeoPoint

app = FastAPI()


@app.post("/api/check-antimeridian")
def check_antimeridian(request: dict):
    """
    Determines if a satellite pass between two points crosses the antimeridian.
    A path crosses if the absolute longitude difference is greater than 180°.

    Returns:
        point1: longitude and latitude of the first point
        point2: longitude and latitude of the second point
        crosses_antimeridian: true if the path crosses the antimeridian
        longitude_difference: absolute difference between the two longitudes
    """
    try:
        p1 = GeoPoint(request["point1"]["type"], request["point1"]["coordinates"])
        p2 = GeoPoint(request["point2"]["type"], request["point2"]["coordinates"])
    except (KeyError, ValueError, TypeError) as e:
        return JSONResponse(status_code=422, content={"error": str(e)})

    diff = abs(p1.longitude - p2.longitude)
    diff = diff if diff != 360 else 0

    is_crosses = diff > 180

    return {
        "point1": {"longitude": p1.longitude, "latitude": p1.latitude},
        "point2": {"longitude": p2.longitude, "latitude": p2.latitude},
        "crosses_antimeridian": is_crosses,
        "longitude_difference": diff
    }
