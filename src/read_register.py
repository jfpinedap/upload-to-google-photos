import json
import os

register_dict = {
    "uploaded": [],
    "error": [],
}

def create_uploaded_images_report():
    for filename in os.listdir("registers"):
        if filename.startswith("register") and filename.endswith(".json"):
            with open(f"registers/{filename}") as f:
                data = json.load(f)
                register_dict["uploaded"].extend(data.get("uploaded", []))
                register_dict["error"].extend(data.get("error", []))

    register_dict["uploaded"] = list(set(register_dict["uploaded"]))
    register_dict["total_uploaded"] = len(register_dict["uploaded"])
    register_dict["error"] = list(set(register_dict["error"]))
    register_dict["total_error"] = len(register_dict["error"])

    with open(f"total_register.json", "w") as f:
        # Use the json module to dump the list to the file
        json.dump(register_dict, f)


if __name__ == "__main__":
    create_uploaded_images_report()