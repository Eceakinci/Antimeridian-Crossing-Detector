# Antimeridian Crossing Detector

A REST API that determines whether a satellite pass between two geographic points crosses the antimeridian (International Date Line at ±180° longitude).

## Requirements

- Python 3.10+

## Setup

```bash
git clone https://github.com/Eceakinci/Antimeridian-Crossing-Detector.git
cd Antimeridian-Crossing-Detector
python -m pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://localhost:8000/docs`.

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

**Example (Linux/macOS)**
```bash
curl -X POST http://localhost:8000/api/check-antimeridian \
  -H "Content-Type: application/json" \
  -d '{"point1": {"type": "Point", "coordinates": [170.5, 45.0]}, "point2": {"type": "Point", "coordinates": [-175.3, 50.2]}}'
```

**Example (Windows Command Prompt)**
```cmd
curl -X POST http://localhost:8000/api/check-antimeridian -H "Content-Type: application/json" -d "{\"point1\": {\"type\": \"Point\", \"coordinates\": [170.5, 45.0]}, \"point2\": {\"type\": \"Point\", \"coordinates\": [-175.3, 50.2]}}"
```

**Validation rules**
- `type` must be `"Point"`
- `coordinates` must be `[longitude, latitude]`
- Longitude: `-180` to `180`
- Latitude: `-90` to `90`

Invalid input returns `422` with an `error` field describing the problem.

## Tests

```bash
python -m pytest
```