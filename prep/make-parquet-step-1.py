import json
import glob
import datetime

taxi_companies = [
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
]
payment_types = [
    "Unknown",
    "Mobile",
    "Prepaid",
    "No Charge",
    "Cash",
    "Credit Card",
    "Pcard",
    "Dispute",
    "Prcard",
]

DIRECTORY = "/mnt/storage/data/taxi-trips/"


def order(x):
    return int(x.replace(DIRECTORY + "taxi-data/taxis-2019-offset-", "").replace(".jsons", ""))


taxis = {}

for filename in sorted(glob.glob(DIRECTORY + "taxi-data/*.jsons"), key=order):
    with open(filename, "r") as file:
        data = json.load(file)
        if len(data) > 0:
            print(filename)

        for item in data:
            taxi_id = item["taxi_id"]
            taxi_company = taxi_companies.index(item["company"])
            taxi_key = (taxi_id, taxi_company)

            if taxi_key not in taxis:
                taxis[taxi_key] = open(f"{DIRECTORY}/by-taxi/{taxi_company}_{taxi_id}.csv", "w")

            trip_seconds = item.get("trip_seconds", None)
            if trip_seconds is not None:
                trip_seconds = float(trip_seconds)

            trip_miles = item.get("trip_miles", None)
            if trip_miles is not None:
                trip_miles = float(trip_miles)

            trip_begin_time = item.get("trip_start_timestamp", None)
            if trip_begin_time is not None:
                datetime.datetime.fromisoformat(trip_begin_time)

            trip_end_time = item.get("trip_end_timestamp", None)
            if trip_end_time is not None:
                datetime.datetime.fromisoformat(trip_end_time)

            trip_begin_lon = item.get("pickup_centroid_longitude", None)
            if trip_begin_lon is not None:
                trip_begin_lon = float(trip_begin_lon)

            trip_begin_lat = item.get("pickup_centroid_latitude", None)
            if trip_begin_lat is not None:
                trip_begin_lat = float(trip_begin_lat)

            trip_end_lon = item.get("dropoff_centroid_longitude", None)
            if trip_end_lon is not None:
                trip_end_lon = float(trip_end_lon)

            trip_end_lat = item.get("dropoff_centroid_latitude", None)
            if trip_end_lat is not None:
                trip_end_lat = float(trip_end_lat)

            payment_fare = item.get("fare", None)
            if payment_fare is not None:
                payment_fare = float(payment_fare)

            payment_tips = item.get("tips", None)
            if payment_tips is not None:
                payment_tips = float(payment_tips)

            payment_total = item.get("trip_total", None)
            if payment_total is not None:
                payment_total = float(payment_total)

            payment_type = payment_types.index(item["payment_type"])

            taxis[taxi_key].write(
                ",".join(
                    [
                        "None" if trip_seconds is None else str(trip_seconds),
                        "None" if trip_miles is None else str(trip_miles),
                        "None" if trip_begin_lon is None else str(trip_begin_lon),
                        "None" if trip_begin_lat is None else str(trip_begin_lat),
                        "None" if trip_begin_time is None else trip_begin_time,
                        "None" if trip_end_lon is None else str(trip_end_lon),
                        "None" if trip_end_lat is None else str(trip_end_lat),
                        "None" if trip_end_time is None else trip_end_time,
                        "None" if payment_fare is None else str(payment_fare),
                        "None" if payment_tips is None else str(payment_tips),
                        "None" if payment_total is None else str(payment_total),
                        str(payment_type),
                    ]
                ) + "\n"
            )


for file in taxis.values():
    file.close()

print("DONE!")
