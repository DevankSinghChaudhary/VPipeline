import json
import shutil

from vcp.state import global_state
from vcp.utils import root

SCENE_DATA = root.find() / "renderer/data"
AUDIO_PATH = root.find() / "renderer/public/audio"


def link(state: global_state):
    scenes = state["decomposition"].scene
    image_scene = {}

    image_with_text = {}
    image_typography = {}

    text_scene = {}
    typography = {}

    none = {}

    if SCENE_DATA.exists():
        shutil.rmtree(SCENE_DATA)
        SCENE_DATA.mkdir(parents=True, exist_ok=True)

    for s in scenes:
        if s.visual_modalities == ["IMAGE"]:
            print()
            print(f"Identified {s.scene_id} as Image scene.")
            image_scene["scene_id"] = s.scene_id
            image_scene["type"] = "IMAGE"
            image_scene["Image"] = s.image.asset
            with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                json.dump(image_scene, file, indent=4)
            print(f"Sent {s.scene_id} as Image Scene for rendering.")

        elif s.visual_modalities == ["IMAGE_WITH_TEXT"]:
            print()
            print(f"Identified {s.scene_id} as Image with Text scene.")
            image_with_text["scene_id"] = s.scene_id
            image_with_text["type"] = "IMAGE_WITH_TEXT"
            image_typography["type_text"] = s.image.type
            image_typography["text"] = s.image.text
            image_with_text["typography"] = image_typography
            with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                json.dump(image_with_text, file, indent=4)
            print(f"Sent {s.scene_id} as Image with Text scene for rendering.")

        elif s.visual_modalities == ["TYPOGRAPHY"]:
            print()
            print(f"Identified {s.scene_id} as Typography scene.")
            text_scene["scene_id"] = s.scene_id
            text_scene["type"] = "TYPOGRAPHY"
            typography["type"] = s.typography.type_typography
            typography["text"] = s.typography.text
            text_scene["typography"] = typography
            with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                json.dump(text_scene, file, indent=4)
            print(f"Sent {s.scene_id} as Typography scene for rendering.")

        elif s.visual_modalities == [None]:
            print()
            print(f"Identified {s.scene_id} as None.")
            none["id"] = s.scene_id
            with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                json.dump(none, file, indent=4)
            print(f"Sent {s.scene_id} as Normal Word-to-Word Typography for rendering.")
