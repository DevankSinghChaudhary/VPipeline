import json

from vcp.state import global_state
from vcp.utils import timed

# for _script in script:
# print(_script.script)


@timed
def matcher(state: global_state):
    original_script = state["original_script"].script
    whisper_script = state["stt"]

    manifest = {}
    _words = {}

    try:
        for _script in original_script:
            for script in _script.script.split():
                for _word in whisper_script:
                    for word in _word["result"]["word_segments"]:
                        if word["word"] == script:
                            _words["word"] = script
                            _words["start"] = word["start"]
                            _words["end"] = word["end"]

                            manifest["id"] = _script.id
                            manifest["segment"] = _words
                            with open(f"{_script.id}.json", "w") as file:
                                json.dump(manifest, file, indent=4)
    except KeyError as e:
        raise ValueError(f"Key dosn't exist: {e}")
