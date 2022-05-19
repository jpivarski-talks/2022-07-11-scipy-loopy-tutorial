import glob
import json
import math
import subprocess
import sys

import awkward._v2 as ak
import numpy as np

PART, TOTAL = int(sys.argv[1]), int(sys.argv[2])

DIRECTORY = "/mnt/storage/data/taxi-trips/"

# longitude min: -87.913624596 max: -87.530712484 mean: -87.66178320769112 std: 0.07611011163806429
# latitude  min:  41.650221676 max:  42.021223593 mean: 41.896777262111726 std: 0.047619558496878614
LONGITUDE, LATITUDE = -87.66178320769112, 41.896777262111726
LON_TO_KM, LAT_TO_KM = 82.98452409203695, 111.07127961503745

filenames = sorted(glob.glob(DIRECTORY + "by-taxi/*.csv"))

FRAC = int(math.ceil(len(filenames) / TOTAL))
PORT = 5001 + PART

for filename in filenames[FRAC * PART : FRAC * (PART + 1)]:
    print(filename)
    with open(filename, "r") as file:
        with open(filename.replace("by-taxi/", "by-taxi-paths/"), "w") as output:
            for line in file:
                (
                    trip_seconds,
                    trip_miles,
                    trip_begin_lon,
                    trip_begin_lat,
                    trip_begin_time,
                    trip_end_lon,
                    trip_end_lat,
                    trip_end_time,
                    payment_fare,
                    payment_tips,
                    payment_total,
                    payment_type,
                ) = line.split(",")

                result = subprocess.run(
                    [
                        "curl",
                        f"http://127.0.0.1:{PORT}/route/v1/driving/{trip_begin_lon},{trip_begin_lat};{trip_end_lon},{trip_end_lat}?steps=true",
                    ],
                    capture_output=True,
                )

                result_json = json.loads(result.stdout)
                if "routes" in result_json:
                    assert len(result_json["routes"]) == 1, len(result_json["routes"])
                    assert len(result_json["routes"][0]["legs"]) == 1, len(result_json["routes"][0]["legs"])

                    last_x_km, last_y_km, fill = None, None, True
                    path = []
                    x0, y0 = float(trip_begin_lon), float(trip_begin_lat)
                    for step in result_json["routes"][0]["legs"][0]["steps"]:
                        for index, intersection in enumerate(step["intersections"]):
                            x, y = intersection["location"]

                            x_km, y_km = (x - LONGITUDE) * LON_TO_KM, (x - LATITUDE) * LAT_TO_KM
                            fill = (
                                index == 0
                                or last_x_km is None
                                or math.sqrt(
                                    (x_km - last_x_km)**2 + (y_km - last_y_km)**2
                                ) > 1.0
                            )

                            if fill:
                                last_x_km, last_y_km = x_km, y_km
                                path.append([x - x0, y - y0])

                    if not fill:
                        path.append([x - x0, y - y0])

                    strpath = str(path).replace(", ", " ")
                    assert "," not in strpath

                else:
                    strpath = "None"

                output.write(
                    ",".join(
                        [
                            trip_seconds,
                            trip_miles,
                            trip_begin_lon,
                            trip_begin_lat,
                            trip_begin_time,
                            trip_end_lon,
                            trip_end_lat,
                            trip_end_time,
                            payment_fare,
                            payment_tips,
                            payment_total,
                            payment_type.rstrip("\n"),
                            strpath,
                        ]
                    ) + "\n"
                )
