import json
import os
import traceback

PATH_TO_PLATINUM = os.environ.get("PATH_TO_PLATINUM", "../pokemonplatinum") 

events_list = os.listdir(PATH_TO_PLATINUM + "/res/field/events")
items = []
hidden_items = []
regions = []
item_map = []
hidden_item_map = []
item_map = [None] * 327  # Assuming there are at most 1000 items
hidden_item_map = [None] * 500  # Assuming there are at most 1000 hidden items
trainers = []
trainer_name_to_id = {}

valid_trainer_types = ["TRAINER_TYPE_NORMAL", "TRAINER_TYPE_VIEW_ALL_DIRECTIONS", "TRAINER_TYPE_FACE_SIDES", "TRAINER_TYPE_FACE_COUNTERCLOCKWISE", "TRAINER_TYPE_FACE_CLOCKWISE", "TRAINER_TYPE_SPIN_COUNTERCLOCKWISE", "TRAINER_TYPE_SPIN_CLOCKWISE"]

i = 0
# if the previous files exist, delete them
if os.path.exists("./items.json"):
    os.remove("./items.json")
if os.path.exists("./hidden_items.json"):
    os.remove("./hidden_items.json")
if os.path.exists("./items.csv"):
    os.remove("./items.csv")
if os.path.exists("./trainers.json"):
    os.remove("./trainers.json")
if os.path.exists("./regions.json"):
    os.remove("./regions.json")

# Load the script file that defines what item is being given
with open(PATH_TO_PLATINUM + "/res/field/scripts/scripts_unk_0404.s", "r") as f:
    script_data = f.readlines()
    for line in script_data:
        if i > 326:  # We only have 327 items, so we stop at 326
            break
        if line.__contains__("SetVar VAR_0x8008"):
            item_map[i] = {"item": line.replace("SetVar VAR_0x8008,", "").strip(), "item_count": 1}
        elif line.__contains__("SetVar VAR_0x8009"):
            item_map[i]["item_count"] = int(line.replace("SetVar VAR_0x8009,", "").strip())
            i += 1

# For some reason, hiddens are handled much differently.... Sad. We have to parse the header file instead.
with open(PATH_TO_PLATINUM + "/include/data/field/hidden_items.h", "r") as f:
    # find the const HiddenItem gHiddenItems[]
    start_reading = False
    hidden_item_data = f.readlines()
    for line in hidden_item_data:
        if line.__contains__("const HiddenItem gHiddenItems[] ="):
            start_reading = True
            print("Found start of hidden items")
        if start_reading and line.__contains__("HIDDEN_ITEM_ENTRY"):
            entry = line.replace("HIDDEN_ITEM_ENTRY(", "").replace("),", "").strip()
            parts = [p.strip() for p in entry.split(",")]
            # parts[0] = ItemId, parts[1] = Quantity, parts[2] = Range?, parts[3] = Script ID (also item/flag id)
            hidden_item_map[int(parts[3])] = {
                "item": parts[0],
                "item_count": int(parts[1])
            }
            print(f"Found hidden item {parts[0]} with count {parts[1]} at script id {parts[3]}")

# Trainers are defined as a list of enums and name based off the ID. Parties are found as a json related to the Name.
with open(PATH_TO_PLATINUM + "/generated/trainers.txt", "r") as f:
    for i, line in enumerate(f):
        trainer_name = line.strip()
        if trainer_name:
            trainer_name_to_id[trainer_name] = i

for file in events_list:
    with open(PATH_TO_PLATINUM + "/res/field/events/" + file, "r") as f:
        try:
            data = json.load(f)
            object_events = data["object_events"]
            for event in object_events:
                if event["graphics_id"] == "OBJ_EVENT_GFX_POKEBALL":
                    items.append({
                        "region": f"REGION_{file.replace(".json", "").replace("events_", "").upper()}/MAIN",
                        "flag": int(event["script"]) - 7000 + 0x3F6,
                        "id": item_map[int(event["script"]) - 7000]["item"],
                        "item_count": item_map[int(event["script"]) - 7000]["item_count"]
                    })
                if valid_trainer_types.__contains__(event["trainer_type"]):
                    # There is 2 types of trainer battles. Single/Double. Script IDs differ but the flag offset is the same. Strange.
                    script_offset = 0
                    if int(event["script"]) >= 5000 and int(event["script"]) < 7000:
                        script_offset = 5000
                    elif int(event["script"]) >= 3000 and int(event["script"]) < 5000:
                        script_offset = 3000
                    else:
                        continue
                    trainer_id = int(event["script"]) - script_offset
                    trainer_name = None
                    # Find the trainer name by id
                    for name, idx in trainer_name_to_id.items():
                        if idx == trainer_id:
                            trainer_name = name
                            break
                    trainers.append({
                        "name": trainer_name,
                        "region": f"REGION_{file.replace('.json', '').replace('events_', '').upper()}/MAIN",
                        "flag": trainer_id + 0x551,
                        "trainer_id": trainer_id,
                    })

            bg_events = data["bg_events"]
            for event in bg_events:
                # Refer to script_manager.c for where the hidden items are defined in the script flags
                if int(event["script"]) > 8000 and int(event["script"]) < 8800:
                    hidden_items.append({
                        "region": f"REGION_{file.replace('.json', '').replace('events_', '').upper()}/MAIN",
                        "flag": int(event["script"]) - 8000 + 0x2DA,
                        "item": hidden_item_map[int(event["script"]) - 8000]["item"],
                        "item_count": hidden_item_map[int(event["script"]) - 8000]["item_count"]
                    })
        
            warp_events = data["warp_events"]
            region_exits = list(set(
                f"REGION_{str(event['dest_header_id']).replace('MAP_HEADER_', '').upper()}/MAIN"
                for event in warp_events
            ))
            regions.append({
                "name": f"REGION_{file.replace('.json', '').replace('events_', '').upper()}/MAIN",
                "exits": region_exits
            })

        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file}")
        except TypeError as e:
            print(f"Type error, please check the output: {e}")
            traceback.print_exc()
        except IndexError as e:
            print(f"Index error, please check the output: {e}")
            traceback.print_exc()

# ItemName to ItemId mapping generation
with open(PATH_TO_PLATINUM + "/generated/items.txt", "r") as f:
    with open("./items.csv", "w") as f_out:
        f_out.write("ItemName,ItemId\n")
        i = 0
        for line in f.readlines():
            f_out.write(f"{line.strip()},{i}\n")
            i += 1

with open("./items.json", "w") as f:
    json.dump(sorted(items, key=lambda x: x["flag"]), f, indent=4)
with open("./hidden_items.json", "w") as f:
    json.dump(sorted(hidden_items, key=lambda x: x["flag"]), f, indent=4)
with open("./trainers.json", "w") as f:
    json.dump(sorted([t for t in trainers if t is not None], key=lambda x: x["flag"]), f, indent=4)
with open("./regions.json", "w") as f:
    json.dump(sorted(regions, key=lambda x: x["name"]), f, indent=4)