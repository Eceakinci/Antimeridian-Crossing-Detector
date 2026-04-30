from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/api/check-antimeridian")
async def check(request: Request):
    data = await request.json()
    lon1 = data["point1"]["coordinates"][0]
    lon2 = data["point2"]["coordinates"][0]

    diff = abs(lon1 - lon2)

    return {
        "crosses_antimeridian": diff > 180,
        "longitude_difference": diff
    }

# def crosses_antimeridian(lon1, lon2):
#     diff = abs(lon1 - lon2)
#     return diff > 180
#
# print(crosses_antimeridian(170.5, -175.3))
# print(crosses_antimeridian(10, 50))