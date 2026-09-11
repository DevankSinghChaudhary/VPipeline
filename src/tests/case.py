import json

from vcp.utils import root

PATH = root.find() / "src/vcp/nodes"

image = {}

mock = [
    {"id": 1, "type": "IMAGE", "image": "Fermi_potrait.png"},
    {"id": 2, "type": "QUESTION", "text": "Where is everybody?"},
    {
        "id": 3,
        "type": "IMAGE_WITH_TEXT",
        "image": "equation.jpg",
        "text": "Missing Piece",
    },
    {"id": 4, "type": "IMAGE", "image": "equation.png"},
]


def link():
    for s in mock:
        if s["type"] == "IMAGE":
            image["id"] = s["id"]
            image["image"] = s["image"]
            with open(f"{s['id']}_data.json", "w") as file:
                json.dump(image, file, indent=4)
        print(f"Saved to {PATH}/{s['id']}_data.json")


link()
print(image)
