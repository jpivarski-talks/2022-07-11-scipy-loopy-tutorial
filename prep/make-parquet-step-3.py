import csv
import glob
import datetime
import ast

import numpy as np
import awkward._v2 as ak

DIRECTORY = "/mnt/storage/data/taxi-trips/"

def batches(num_trips):
    payment_types = ak.from_iter(
        [
            "Unknown",
            "Mobile",
            "Prepaid",
            "No Charge",
            "Cash",
            "Credit Card",
            "Pcard",
            "Dispute",
            "Prcard",
        ],
        highlevel=False,
    )

    taxi_companies = ak.from_iter(
        [
            "Patriot Taxi Dba Peace Taxi Associat",
            "Chicago Carriage Cab Corp",
            "Taxi Affiliation Services",
            "Checker Taxi",
            "Gold Coast Taxi",
            "3094 - 24059 G.L.B. Cab Co",
            "CMT-Sales",
            "4732 - Maude Lamy",
            "Globe Taxi",
            "Metro Jet Taxi A",
            "Setare Inc",
            "5874 - 73628 Sergey Cab Corp.",
            "3011 - 66308 JBL Cab Inc.",
            "5 Star Taxi",
            "U Taxicab",
            "6574 - Babylon Express Inc.",
            "Taxi Affiliation Service Yellow",
            "Metro Jet Cab Association Inc.",
            "6742 - 83735 Tasha ride inc",
            "American United Taxi Affiliation",
            "City Service",
            "3623 - 72222 Arrington Enterprises",
            "Leonard Cab Co",
            "5074 - 54002 Ahzmi Inc",
            "3556 - 36214 RC Andrews Cab",
            "4053 - 40193 Adwar H. Nikola",
            "312 Medallion Management Corp",
            "2733 - 74600 Benny Jona",
            "Yellow Cab",
            "5006 - 39261 Salifu Bawa",
            "Checker Taxi Affiliation",
            "3620 - 52292 David K. Cab Corp.",
            "Chicago Taxicab",
            "KOAM Taxi Association",
            "6743 - 78771 Luhak Corp",
            "Top Cab",
            "Metro Jet Taxi A.",
            "American United",
            "Suburban Dispatch LLC",
            "Chicago Medallion Management",
            "Flash Cab",
            "Blue Diamond",
            "Nova Taxi Affiliation Llc",
            "4623 - 27290 Jay Kim",
            "Chicago Star Taxicab",
            "Taxicab Insurance Agency Llc",
            "1469 - 64126 Omar Jada",
            "Metro Jet Taxi Ass",
            "Sun Taxi",
            "Medallion Leasin",
            "24 Seven Taxi",
            "3591 - 63480 Chuks Cab",
            "T.A.S. - Payment Only",
            "Petani Cab Corp",
            "Blue Ribbon Taxi Association Inc.",
            "Top Cab Affiliation",
            "4787 - 56058 Reny Cab Co",
            "Taxicab Insurance Agency, LLC",
            "4523 - 79481 Hazel Transit Inc",
            "5062 - 34841 Sam Mestas",
            "3721 - Santamaria Express, Alvaro Santamaria",
            "Star North Management LLC",
            "2092 - 61288 Sbeih company",
            "Choice Taxi Association",
            "Chicago Independents",
            "1085 - 72312 N and W Cab Co",
        ],
        highlevel=False,
    )

    taxi_offsets = [0]

    all_trip_seconds = []
    msk_trip_seconds = []
    all_trip_km = []
    msk_trip_km = []
    all_trip_begin_lon = []
    msk_trip_begin_lon = []
    all_trip_begin_lat = []
    msk_trip_begin_lat = []
    all_trip_begin_time = []
    msk_trip_begin_time = []
    all_trip_end_lon = []
    msk_trip_end_lon = []
    all_trip_end_lat = []
    msk_trip_end_lat = []
    all_trip_end_time = []
    msk_trip_end_time = []
    all_payment_fare = []
    msk_payment_fare = []
    all_payment_tips = []
    msk_payment_tips = []
    all_payment_total = []
    msk_payment_total = []

    all_payment_type = []
    all_path_lon = []
    all_path_lat = []
    all_path_offsets = [0]
    all_company = []

    def batch():
        layout = ak.contents.ListOffsetArray(
            ak.index.Index32(np.array(taxi_offsets, dtype=np.int32)),
            ak.contents.RecordArray(
                [
                    ak.contents.RecordArray(
                        [
                            ak.contents.ByteMaskedArray(
                                ak.index.Index8(
                                    np.array(msk_trip_seconds, dtype=np.int8)
                                ),
                                ak.contents.NumpyArray(
                                    np.array(all_trip_seconds, dtype=np.float32)
                                ),
                                valid_when=True,
                            ),
                            ak.contents.ByteMaskedArray(
                                ak.index.Index8(
                                    np.array(msk_trip_km, dtype=np.int8)
                                ),
                                ak.contents.NumpyArray(
                                    np.array(all_trip_km, dtype=np.float32)
                                ),
                                valid_when=True,
                            ),
                            ak.contents.RecordArray(
                                [
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_begin_lon, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_begin_lon, dtype=np.float64)
                                        ),
                                        valid_when=True,
                                    ),
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_begin_lat, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_begin_lat, dtype=np.float64)
                                        ),
                                        valid_when=True,
                                    ),
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_begin_time, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_begin_time, dtype="datetime64[s]")
                                        ),
                                        valid_when=True,
                                    ),
                                ],
                                ["lon", "lat", "time"],
                            ),
                            ak.contents.RecordArray(
                                [
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_end_lon, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_end_lon, dtype=np.float64)
                                        ),
                                        valid_when=True,
                                    ),
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_end_lat, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_end_lat, dtype=np.float64)
                                        ),
                                        valid_when=True,
                                    ),
                                    ak.contents.ByteMaskedArray(
                                        ak.index.Index8(
                                            np.array(msk_trip_end_time, dtype=np.int8)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_trip_end_time, dtype="datetime64[s]")
                                        ),
                                        valid_when=True,
                                    ),
                                ],
                                ["lon", "lat", "time"],
                            ),
                            ak.contents.ListOffsetArray(
                                ak.index.Index64(np.array(all_path_offsets, dtype=np.int64)),
                                ak.contents.RecordArray(
                                    [
                                        ak.contents.NumpyArray(
                                            np.array(all_path_lon, dtype=np.float32)
                                        ),
                                        ak.contents.NumpyArray(
                                            np.array(all_path_lat, dtype=np.float32)
                                        ),
                                    ],
                                    ["londiff", "latdiff"],
                                ),
                            ),
                        ],
                        ["sec", "km", "begin", "end", "path"],
                    ),
                    ak.contents.RecordArray(
                        [
                            ak.contents.ByteMaskedArray(
                                ak.index.Index8(np.array(msk_payment_fare, dtype=np.int8)),
                                ak.contents.NumpyArray(
                                    np.array(all_payment_fare, dtype=np.float32),
                                ),
                                valid_when=True,
                            ),
                            ak.contents.ByteMaskedArray(
                                ak.index.Index8(np.array(msk_payment_tips, dtype=np.int8)),
                                ak.contents.NumpyArray(
                                    np.array(all_payment_tips, dtype=np.float32),
                                ),
                                valid_when=True,
                            ),
                            ak.contents.ByteMaskedArray(
                                ak.index.Index8(np.array(msk_payment_total, dtype=np.int8)),
                                ak.contents.NumpyArray(
                                    np.array(all_payment_total, dtype=np.float32),
                                ),
                                valid_when=True,
                            ),
                            ak.contents.IndexedArray(
                                ak.index.Index32(np.array(all_payment_type, dtype=np.int32)),
                                payment_types,
                                parameters={"__array__": "categorical"},
                            )
                        ],
                        ["fare", "tips", "total", "type"],
                    ),
                    ak.contents.IndexedArray(
                        ak.index.Index32(np.array(all_company, dtype=np.int32)),
                        taxi_companies,
                        parameters={"__array__": "categorical"},
                    )
                ],
                ["trip", "payment", "company"],
            )
        )

        ak.validity_error(layout, exception=True)

        print("writing row-group")

        return ak.Array(layout)

    filenames = sorted(glob.glob(DIRECTORY + "by-taxi-paths/*.csv"), key=lambda x: x.split("_")[::-1])
    for index, filename in enumerate(filenames):
        print(index, len(filenames), filename)

        company = int(filename.split("_")[0].split("/")[-1])

        with open(filename, "r") as file:
            for trip in csv.reader(file):
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
                    path,
                ) = trip
                if trip_begin_time.startswith("2022-") or trip_end_time.startswith("2022-"):
                    continue

                if trip_seconds == "None":
                    all_trip_seconds.append(0.0)
                    msk_trip_seconds.append(False)
                else:
                    all_trip_seconds.append(float(trip_seconds))
                    msk_trip_seconds.append(True)
                if trip_miles == "None":
                    all_trip_km.append(0.0)
                    msk_trip_km.append(False)
                else:
                    all_trip_km.append(float(trip_miles) * 1.609344)
                    msk_trip_km.append(True)
                if trip_begin_lon == "None":
                    all_trip_begin_lon.append(0.0)
                    msk_trip_begin_lon.append(False)
                else:
                    all_trip_begin_lon.append(float(trip_begin_lon))
                    msk_trip_begin_lon.append(True)
                if trip_begin_lat == "None":
                    all_trip_begin_lat.append(0.0)
                    msk_trip_begin_lat.append(False)
                else:
                    all_trip_begin_lat.append(float(trip_begin_lat))
                    msk_trip_begin_lat.append(True)
                if trip_begin_time == "None":
                    all_trip_begin_time.append(datetime.datetime.fromtimestamp(0))
                    msk_trip_begin_time.append(False)
                else:
                    all_trip_begin_time.append(datetime.datetime.fromisoformat(trip_begin_time))
                    msk_trip_begin_time.append(True)
                if trip_end_lon == "None":
                    all_trip_end_lon.append(0.0)
                    msk_trip_end_lon.append(False)
                else:
                    all_trip_end_lon.append(float(trip_end_lon))
                    msk_trip_end_lon.append(True)
                if trip_end_lat == "None":
                    all_trip_end_lat.append(0.0)
                    msk_trip_end_lat.append(False)
                else:
                    all_trip_end_lat.append(float(trip_end_lat))
                    msk_trip_end_lat.append(True)
                if trip_end_time == "None":
                    all_trip_end_time.append(datetime.datetime.fromtimestamp(0))
                    msk_trip_end_time.append(False)
                else:
                    all_trip_end_time.append(datetime.datetime.fromisoformat(trip_end_time))
                    msk_trip_end_time.append(True)
                if payment_fare == "None":
                    all_payment_fare.append(0.0)
                    msk_payment_fare.append(False)
                else:
                    all_payment_fare.append(float(payment_fare))
                    msk_payment_fare.append(True)
                if payment_tips == "None":
                    all_payment_tips.append(0.0)
                    msk_payment_tips.append(False)
                else:
                    all_payment_tips.append(float(payment_tips))
                    msk_payment_tips.append(True)
                if payment_total == "None":
                    all_payment_total.append(0.0)
                    msk_payment_total.append(False)
                else:
                    all_payment_total.append(float(payment_total))
                    msk_payment_total.append(True)

                all_payment_type.append(int(payment_type))

                if path != "None":
                    for x, y in ast.literal_eval(path.replace(" ", ",")):
                        all_path_lon.append(x)
                        all_path_lat.append(y)
                all_path_offsets.append(len(all_path_lon))

                all_company.append(company)

        taxi_offsets.append(len(all_trip_seconds))

        if len(all_trip_seconds) >= num_trips:
            yield batch()

            taxi_offsets.clear()
            taxi_offsets.append(0)

            all_trip_seconds.clear()
            msk_trip_seconds.clear()
            all_trip_km.clear()
            msk_trip_km.clear()
            all_trip_begin_lon.clear()
            msk_trip_begin_lon.clear()
            all_trip_begin_lat.clear()
            msk_trip_begin_lat.clear()
            all_trip_begin_time.clear()
            msk_trip_begin_time.clear()
            all_trip_end_lon.clear()
            msk_trip_end_lon.clear()
            all_trip_end_lat.clear()
            msk_trip_end_lat.clear()
            all_trip_end_time.clear()
            msk_trip_end_time.clear()
            all_payment_fare.clear()
            msk_payment_fare.clear()
            all_payment_tips.clear()
            msk_payment_tips.clear()
            all_payment_total.clear()
            msk_payment_total.clear()

            all_payment_type.clear()
            all_path_lon.clear()
            all_path_lat.clear()
            all_path_offsets.clear()
            all_path_offsets.append(0)
            all_company.clear()

    if len(all_trip_seconds) != 0:
        yield batch()


ak.to_parquet(
    batches(1000000),
    DIRECTORY + "chicago-taxi.parquet",
    categorical_as_dictionary=True,
    extensionarray=False,
    compression="zstd",
    compression_level=22,
)

print("DONE")
