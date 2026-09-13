script = "In nineteen fifty, physicist Enrico Fermi posed a question that would challenge humanity’s place in the cosmos."
whisper = [
    {"word": "In", "start": 0.252, "end": 0.333, "score": 0.907},
    {"word": "1950,", "start": 0.454, "end": 1.178, "score": 0.636},
    {"word": "physicist", "start": 1.239, "end": 1.722, "score": 0.911},
    {"word": "Enrico", "start": 1.762, "end": 2.164, "score": 0.638},
    {"word": "Fermi", "start": 2.205, "end": 2.547, "score": 0.841},
    {"word": "posed", "start": 2.607, "end": 2.869, "score": 0.804},
    {"word": "a", "start": 2.909, "end": 2.929, "score": 0.999},
    {"word": "question", "start": 2.969, "end": 3.352, "score": 0.814},
    {"word": "that", "start": 3.392, "end": 3.493, "score": 1.0},
    {"word": "would", "start": 3.513, "end": 3.654, "score": 0.898},
    {"word": "challenge", "start": 3.714, "end": 4.157, "score": 0.837},
    {"word": "humanity's", "start": 4.197, "end": 4.741, "score": 0.873},
    {"word": "place", "start": 4.801, "end": 5.063, "score": 0.795},
    {"word": "in", "start": 5.103, "end": 5.163, "score": 0.781},
    {"word": "the", "start": 5.203, "end": 5.264, "score": 0.998},
    {"word": "cosmos.", "start": 5.284, "end": 5.807, "score": 0.938},
]
matched = {}

range_ = 0
for word in script.split():
    for data in whisper:
        if word == data["word"]:
            range_ = range_ + 1
            matched[f"{word}_script"] = data["word"]

print(matched)
print(f"Ran for: {range_} times")
