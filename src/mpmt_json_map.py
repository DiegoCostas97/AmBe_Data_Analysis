#%%
import json
import numpy as np
#%%
# Read .json
def extract_pmt_locations(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    mpmt_data = data.get("mpmts", {})
    result = []

    # Iterar sobre los MPMTs ordenados por índice
    for mpmt_idx in sorted(mpmt_data.keys(), key=int):
        mpmt = mpmt_data[mpmt_idx]
        pmt_dict = {}

        pmts = mpmt.get("pmts", {})
        for pmt_idx in sorted(pmts.keys(), key=int):
            pmt = pmts[pmt_idx]
            location = pmt["placement"]["location"]
            pmt_dict[int(pmt_idx)] = location

        result.append(pmt_dict)

    return result
#%%
# Compute distances from AmBe position 1 to every pmt
pmt_positions = extract_pmt_locations("/Users/diiego/Downloads/wcte_v11_20250513.json")
source_position = np.array([0, 1159, 0])
pmt_to_source = []

for mpmt in pmt_positions:
    for coordinates in mpmt.values():
        coord = np.array(coordinates)
        dist = np.linalg.norm(coord - source_position)
        pmt_to_source.append(dist)

pmt_to_source = np.array(pmt_to_source)*1e-3
# %%
# Compute time takes light travel that distance
rindex = 1.33
c = 3e8/1.33
water_light_time = (pmt_to_source/c)

d = {}
counter = 0
for i in range(106):  # mpmt
    for j in range(19):  # pmt
        key = i * 100 + j  # p.ej. 7402
        d[key] = water_light_time[counter]*1e9
        counter += 1

#%%
with open('../data/mpmt_tof_pos1.json', 'w') as fp:
    json.dump(d, fp, indent=4)
