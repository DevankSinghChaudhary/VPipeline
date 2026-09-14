import json
import shutil

from vcp.state import global_state
from vcp.utils import root

MANIFEST_PATH = root.find() / "renderer/data"
AUDIO_PATH = root.find() / "renderer/public/audio"


def manifest(state: global_state):
    scenes = state["decomposition"].scene
    _audio = state["stt"]

    image_scene = {}
    image_audio = {}

    image_with_text = {}
    image_with_text_audio = {}
    image_typography = {}
    image = {}

    text_scene = {}
    typography = {}
    typography_audio = {}

    none = {}
    none_audio = {}

    all_scenes = []

    if MANIFEST_PATH.exists():
        shutil.rmtree(MANIFEST_PATH)
        MANIFEST_PATH.mkdir(parents=True, exist_ok=True)

    for s in scenes:
        for audio in _audio:
            if s.visual_modalities == ["IMAGE"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Image scene.")
                    image_scene["scene_id"] = s.scene_id

                    image_audio["path"] = audio["path"]
                    image_audio["result"] = audio["result"]["word_segments"]

                    image_scene["audio"] = image_audio
                    image_scene["type"] = "IMAGE"
                    image_scene["Image"] = s.image.asset
                    all_scenes.append(image_scene)
                    print(f"Sent {s.scene_id} as Image Scene for rendering.")

            elif s.visual_modalities == ["IMAGE_WITH_TEXT"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Image with Text scene.")
                    image_with_text["scene_id"] = s.scene_id
                    image_with_text["type"] = "IMAGE_WITH_TEXT"

                    image_with_text_audio["path"] = audio["path"]
                    image_with_text_audio["result"] = audio["result"]["word_segments"]

                    image["image"] = s.image.asset

                    image_with_text["audio"] = image_with_text_audio
                    image_typography["type_text"] = s.image.type_text
                    image_typography["text"] = s.image.text
                    image_typography["image"] = image
                    image_with_text["typography"] = image_typography
                    all_scenes.append(image_with_text)
                    print(f"Sent {s.scene_id} as Image with Text scene for rendering.")

            elif s.visual_modalities == ["TYPOGRAPHY"]:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as Typography scene.")
                    text_scene["scene_id"] = s.scene_id
                    text_scene["type"] = "TYPOGRAPHY"

                    typography_audio["path"] = audio["path"]
                    typography_audio["result"] = audio["result"]["word_segments"]

                    text_scene["audio"] = typography_audio
                    typography["type"] = s.typography.type_typography
                    typography["text"] = s.typography.text
                    text_scene["typography"] = typography
                    all_scenes.append(text_scene)
                    print(f"Sent {s.scene_id} as Typography scene for rendering.")

            else:
                if int(audio["audio_id"]) == int(s.scene_id):
                    print()
                    print(f"Identified {s.scene_id} as None.")
                    none["id"] = s.scene_id
                    none_audio["path"] = audio["path"]
                    none_audio["result"] = audio["result"]["word_segments"]

                    none["audio"] = none_audio
                    all_scenes.append(none)
                    print(
                        f"Sent {s.scene_id} as Normal Word-to-Word Typography for rendering."
                    )
    with open(f"{MANIFEST_PATH}/RendererManifest.json", "w", encoding="utf-8") as file:
        json.dump(all_scenes, file, indent=4, ensure_ascii=False)
