import yaml
import glob
import os

catalog_root = os.path.dirname(__file__)
catalog_root = os.path.join(catalog_root, "catalog")
pattern = os.path.join(catalog_root, "*.yml")
entries = [os.path.relpath(x) for x in glob.glob(pattern)]
datasets = {}


def read_entry(entry):
    with open(entry) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


remotes = {}
for entry in entries:
    data = read_entry(entry)
    remotes[data["name"]] = data


def write_yml(entry):
    file_name = entry["name"].lower()
    file_name = file_name.replace(" ", "_")
    file_name += ".yml"
    file_name = "catalog/" + file_name
    with open(file_name, "w") as out_file:
        _ = yaml.dump(entry, out_file)


# This was used to migrate old remotes.py examples

# from libpysal.examples.remotes import datasets as remotes
# for remote in remotes:
#    remote_dict = remotes[remote].json_dict()
#    remode_dict['k'] = remotes[remote].k
#    remode_dict['k'] = remotes[remote].n
#    print(remotes[remote].k)
#    write_yml(remote_dict)
