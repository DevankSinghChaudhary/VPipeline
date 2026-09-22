import json
from pathlib import Path

from mutagen import File

from vcp.state import global_state
from vcp.utils import root

MANIFEST_PATH = root.find() / "renderer/data"
MANIFEST_FILE = MANIFEST_PATH / "RendererManifest.json"
PUBLIC_PATH = root.find() / "renderer/public"


def get_audio_duration(audio_path: str) -> float:
    audio = File(audio_path)

    if audio is None or audio.info is None:
        raise ValueError(f"Could not read audio metadata: {audio_path}")

    return float(audio.info.length)


def get_public_audio_path(audio_path: str) -> str:
    path = Path(audio_path)

    try:
        relative_path = path.relative_to(PUBLIC_PATH)
    except ValueError as exc:
        raise ValueError(
            f"Audio file is outside Remotion public directory:\n"
            f"  Audio:  {path}\n"
            f"  Public: {PUBLIC_PATH}"
        ) from exc

    return f"/{relative_path.as_posix()}"


def get_audio_words(audio: dict) -> list[dict]:
    return audio["result"]["word_segments"]


def build_audio(audio: dict) -> dict:
    audio_path = audio["path"]

    return {
        "path": get_public_audio_path(audio_path),
        "words": get_audio_words(audio),
    }


def build_visual(scene) -> dict:
    if scene.visual_modalities == ["IMAGE"]:
        return {
            "template": "default",
            "image": scene.image.asset,
        }

    if scene.visual_modalities == ["IMAGE_WITH_TEXT"]:
        return {
            "template": "key_line",
            "text": scene.image.text,
            "image": scene.image.asset,
        }

    if scene.visual_modalities == ["TYPOGRAPHY"]:
        return {
            "template": scene.typography.type_typography,
            "text": scene.typography.text,
        }

    if scene.visual_modalities == ["NONE"]:
        return {
            "template": "word_by_word",
        }

    raise ValueError(
        f"Unsupported visual modality for scene "
        f"{scene.scene_id}: {scene.visual_modalities}"
    )


def manifest(state: global_state):
    scenes = state["decomposition"].scene
    audio_data = state["stt"]

    audio_by_id = {int(audio["audio_id"]): audio for audio in audio_data}

    MANIFEST_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_scenes = []
    seen_scene_ids = set()

    for source_scene in scenes:
        scene_id = int(source_scene.scene_id)

        if scene_id in seen_scene_ids:
            print(f"Warning: duplicate scene {scene_id} skipped.")
            continue

        seen_scene_ids.add(scene_id)

        audio = audio_by_id.get(scene_id)

        if audio is None:
            print(f"Warning: no audio found for scene {scene_id}. Scene skipped.")
            continue

        audio_path = audio["path"]
        duration = get_audio_duration(audio_path)

        modalities = source_scene.visual_modalities

        if modalities == ["IMAGE"]:
            scene_type = "IMAGE"

        elif modalities == ["IMAGE_WITH_TEXT"]:
            scene_type = "IMAGE_WITH_TEXT"

        elif modalities == ["TYPOGRAPHY"]:
            scene_type = "TYPOGRAPHY"

        elif modalities == ["NONE"]:
            scene_type = "NONE"

        else:
            raise ValueError(
                f"Unsupported visual modality for scene {scene_id}: {modalities}"
            )

        scene = {
            "scene_id": scene_id,
            "type": scene_type,
            "duration": duration,
            "audio": build_audio(audio),
            "visual": build_visual(source_scene),
        }

        all_scenes.append(scene)

        print()
        print(f"Scene {scene_id}: {scene_type}")
        print(f"Duration: {duration:.3f}s")
        print(f"Template: {scene['visual']['template']}")

    with open(
        MANIFEST_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            all_scenes,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print()
    print(f"Manifest written to {MANIFEST_FILE}")
    print(f"Total scenes: {len(all_scenes)}")
