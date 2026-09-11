SYSTEM_PROMPT = (
    "THIS IS NOTHING BUT A TESTING PURPOSE"
    + "\n\n"
    + "=" * 15
    + "\n\n"
    + "HUMAN SCOPE RULLES TO KEEP IN MIND"
)


from vcp.utils import root

BASE = root.find()
AUDIO = BASE / "renderer/public/audio"

print(AUDIO)
# print(SYSTEM_PROMPT)
