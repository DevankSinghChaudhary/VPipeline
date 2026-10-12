data = {
    "pipeline": [
        {
            "id": "Technical",
            "description": "Technical documentary profile",
            "standards": {
                "writer": ["asd-ste100"],
                "researcher": ["iso"],
                "formatter": ["iso"],
            },
            "system_prompts": {"writer": "You are the Writer node in VPipeline"},
        }
    ]
}


class RulesLoader:
    def load(self, data):
        rules = data["pipeline"]
        for node in rules[0]["standards"]:
            for standards in node:
                print(standards)


rules = RulesLoader()
rules.load(data)
