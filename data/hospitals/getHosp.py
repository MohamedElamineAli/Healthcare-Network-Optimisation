import json

def getHospitalsfromSpecialities(hospitals, specialities, general=false):
    results = []
    if general:
        specialities.append("General Emergency")
    if specialities == "all":
        for hospital in hospitals:
            results.append({"name": hospital["name"], "id": hospital["id"], "x": hospital["x"], "y": hospital["y"]})
        return results

    for hospital in hospitals:
        for spc in specialities:
            if spc in hospital["services"]:
                results.append({"name": hospital["name"], "id": hospital["id"], "x": hospital["x"], "y": hospital["y"]})
                break

    return results

with open('hospitalWithID.json') as f:
    data = json.load(f)

hospitals = data["hospitals"]
specialities = ["Anatomical Pathology"]
general = false

hosps = getHospitalsfromSpecialities(hospitals, specialities, general)
i = 0
for  hosp in hosps:
    i = i +1
    print(i, end="/   ")
    print(hosp)
