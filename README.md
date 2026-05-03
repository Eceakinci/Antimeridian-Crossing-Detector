# Antimeridian Crossing Detector

A REST API that determines whether a satellite pass between two geographic points crosses the antimeridian (International Date Line at ±180° longitude).

## Requirements

- Python 3.10+

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.
Interactive docs (Swagger UI) at http://localhost:8000/docs.

## Endpoint

### `POST /api/check-antimeridian`

**Request**
```json
{
  "point1": {
    "type": "Point",
    "coordinates": [170.5, 45.0]
  },
  "point2": {
    "type": "Point",
    "coordinates": [-175.3, 50.2]
  }
}
```

**Response**
```json
{
  "point1": {
    "longitude": 170.5,
    "latitude": 45.0
  },
  "point2": {
    "longitude": -175.3,
    "latitude": 50.2
  },
  "crosses_antimeridian": true,
  "longitude_difference": 345.8
}
```

**Validation rules**
- `type` must be `"Point"`
- `coordinates` must be `[longitude, latitude]`
- Longitude: `-180` to `180`
- Latitude: `-90` to `90`

Invalid input returns `422` with an `error` field describing the problem.

## Tests

```bash
pytest
```