from pathlib import Path


def parse_filename(name):
    if not name.endswith(".png"):
        return None
    parts = name.removesuffix(".png")
    stems = parts.rsplit("_",1)
    if stems[1] not in ("BaseColor", "Normal", "Metallic", "Roughness"):
        return None
    return stems

def list_files(folder_str):
    passed = []
    rejected = []
    folder = Path(folder_str)
    for item in folder.iterdir():
        result = parse_filename(item.name)
        if result is None:
            rejected.append(item.name)
        else:
            passed.append(result)
    return passed,rejected


def group_by_asset(passed):
    group = {}
    for passed_item in passed:
        if passed_item[0] not in group:
            group[passed_item[0]] = [passed_item[1]]
        else:
            group[passed_item[0]].append(passed_item[1])
    return group

def find_missing(types):
    missing = []
    for t in ("BaseColor", "Normal", "Metallic", "Roughness"):
        if t not in types:
            missing.append(t)
    return missing
print(find_missing(['BaseColor', 'Roughness']))
    

passed,rejected = list_files(r"C:\Users\johnnykong\Documents\Unreal Projects\Space_Colony\Python\Practice\Day1 Texture set completness check\Test data")
groups = group_by_asset(passed)


