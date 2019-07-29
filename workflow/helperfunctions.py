import json
import yaml
import bispy
import os

bis_utils = bispy.bis.Utils()

statename_to_abbr = {
    # Other
    'District of Columbia': 'DC',
    
    # States
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO',
    'Wyoming': 'WY',
}

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


def state_name(abbreviation):    
    return next((k for k, v in statename_to_abbr.items() if v == abbreviation), None)


def cache_schema(data_file):
    with open(f'cache/{data_file}.json', 'r') as f:
        data = json.loads(f.read())
        f.close()

    schema = bis_utils.generate_json_schema(data)
    d_schema = json.loads(schema)
    
    with open(f'documentation/{data_file}-schema.json', 'w') as f:
        f.write(schema)
    
    return d_schema


def load_schema(data_file, filetype='json', outputtype='dictionary'):
    if not os.path.exists(f'documentation/{data_file}-schema.json'):
        return None
    
    with open(f'documentation/{data_file}-schema.json', 'r') as f:
        if outputtype == 'json':
            return f.read()
        elif outputtype == 'dictionary':
            return json.loads(f.read())
        elif outputtype == 'yaml':
            return yaml.dump(json.loads(f.read()))
