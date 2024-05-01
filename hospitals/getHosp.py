import json

def getHospitalsfromSpecialities(hospitals, specialities):
    results = []
    if specialities == "all":
        for hospital in hospitals:
            results.append({"name": hospital["name"], "id": hospital["id"], "c": hospital["x"], "y": hospital["y"]})
        return results

    for hospital in hospitals:
        for spc in specialities:
            if spc in hospital["services"]:
                results.append({"name": hospital["name"], "id": hospital["id"], "c": hospital["x"], "y": hospital["y"]})
                break

    return results

with open('hospitalWithID.json') as f:
    data = json.load(f)

hospitals = data["hospitals"]
specialities = ["Anatomical Pathology"]

hosps = getHospitalsfromSpecialities(hospitals, specialities)
i = 0
for  hosp in hosps:
    i = i +1
    print(i, end="/   ")
    print(hosp)
