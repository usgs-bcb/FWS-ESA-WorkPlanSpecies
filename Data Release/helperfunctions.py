import json

def workplan_species():
    # Open up the cached workplan species
    with open("cache/workplan_species.json", "r") as f:
        workplan_species = json.loads(f.read())

    lookup_name_list = name_list(workplan_species)

    return lookup_name_list


def name_list(workplan_list):
    # Prepare a list of names to use for lookup that includes the name and its source in the prepared workplan species data
    lookup_name_list = [(r["Lookup Name"], "Lookup Name") for r in workplan_list]
    lookup_name_list.extend([(r["Valid ITIS Scientific Name"], "Valid ITIS Scientific Name") for r in workplan_list if "Valid ITIS Scientific Name" in r.keys()])
    
    return lookup_name_list

    