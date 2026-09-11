import json
import shutil

from vcp.state import global_state
from vcp.utils import root

SCENE_DATA = root.find() / "renderer/data"
AUDIO_PATH = root.find() / "renderer/public/audio"


def manifest(state: global_state):
    scenes = state["decomposition"].scene
    _audio = state["stt"]

    image_scene = {}
    image_audio = {}

    image_with_text = {}
    image_with_text_audio = {}
    image_typography = {}

    text_scene = {}
    typography = {}
    typography_audio = {}

    none = {}
    none_audio = {}

    if SCENE_DATA.exists():
        shutil.rmtree(SCENE_DATA)
        SCENE_DATA.mkdir(parents=True, exist_ok=True)

    for s in scenes:
        for audio in _audio:
            if s.visual_modalities == ["IMAGE"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Image scene.")
                    image_scene["scene_id"] = s.scene_id

                    image_audio["path"] = audio["path"]
                    image_audio["result"] = audio["result"]

                    image_scene["audio"] = image_audio
                    image_scene["type"] = "IMAGE"
                    image_scene["Image"] = s.image.asset
                    with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                        json.dump(image_scene, file, indent=4)
                    print(f"Sent {s.scene_id} as Image Scene for rendering.")

            elif s.visual_modalities == ["IMAGE_WITH_TEXT"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Image with Text scene.")
                    image_with_text["scene_id"] = s.scene_id
                    image_with_text["type"] = "IMAGE_WITH_TEXT"

                    image_with_text_audio["path"] = audio["path"]
                    image_with_text_audio["result"] = audio["result"]

                    image_with_text["audio"] = image_with_text_audio
                    image_typography["type_text"] = s.image.type
                    image_typography["text"] = s.image.text
                    image_with_text["typography"] = image_typography
                    with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                        json.dump(image_with_text, file, indent=4)
                    print(f"Sent {s.scene_id} as Image with Text scene for rendering.")

            elif s.visual_modalities == ["TYPOGRAPHY"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Typography scene.")
                    text_scene["scene_id"] = s.scene_id
                    text_scene["type"] = "TYPOGRAPHY"

                    typography_audio["path"] = audio["path"]
                    typography_audio["result"] = audio["result"]

                    text_scene["audio"] = typography_audio
                    typography["type"] = s.typography.type_typography
                    typography["text"] = s.typography.text
                    text_scene["typography"] = typography
                    with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                        json.dump(text_scene, file, indent=4)
                    print(f"Sent {s.scene_id} as Typography scene for rendering.")

            else:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as None.")
                    none["id"] = s.scene_id
                    none_audio["path"] = audio["path"]
                    none_audio["result"] = audio["result"]

                    none["audio"] = none_audio
                    with open(f"{SCENE_DATA}/{s.scene_id}_data.json", "w") as file:
                        json.dump(none, file, indent=4)
                    print(
                        f"Sent {s.scene_id} as Normal Word-to-Word Typography for rendering."
                    )
