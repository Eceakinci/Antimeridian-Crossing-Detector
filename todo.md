- [] Implement main function that gets request and returns response
- [] Implement a model, structure of response and request 
- [] FastAPI, Uvicorn
- [] Implement test

- [] Additional responses based on the request, if any, e.g. approximate name of the given long/lang

**Terminal:**
- uvicorn main:app --reload


**Sources:**
- https://blog.postman.com/how-to-build-an-api-in-python/
- GeoJSON as a standard
-------------------
**Endpoint:** `POST /api/check-antimeridian`
-------------------
**Input**
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
-------------------
**Output**
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