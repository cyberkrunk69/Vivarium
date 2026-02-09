import json
import re

def auto_tag_lessons(lessons):
    knowledge_packs = {
        "categories": [
            "claude",
            "groq",
            "api:spotify",
            "api:github",
            "safety",
            "ui"
        ],
        "lessons": {
            "claude": [],
            "groq": [],
            "api:spotify": [],
            "api:github": [],
            "safety": [],
            "ui": []
        }
    }

    for lesson in lessons:
        content = lesson["content"]
        if re.search(r"claude|optimal|techniques", content, re.IGNORECASE):
            knowledge_packs["lessons"]["claude"].append(lesson)
        elif re.search(r"groq|optimizations|efficient", content, re.IGNORECASE):
            knowledge_packs["lessons"]["groq"].append(lesson)
        elif re.search(r"spotify|music|streaming", content, re.IGNORECASE):
            knowledge_packs["lessons"]["api:spotify"].append(lesson)
        elif re.search(r"github|api|patterns", content, re.IGNORECASE):
            knowledge_packs["lessons"]["api:github"].append(lesson)
        elif re.search(r"safety|security|lessons", content, re.IGNORECASE):
            knowledge_packs["lessons"]["safety"].append(lesson)
        elif re.search(r"ui|frontend|dashboard", content, re.IGNORECASE):
            knowledge_packs["lessons"]["ui"].append(lesson)

    return knowledge_packs

with open('learned_lessons.json') as f:
    lessons = json.load(f)

knowledge_packs = auto_tag_lessons(lessons)

with open('knowledge_packs.json', 'w') as f:
    json.dump(knowledge_packs, f, indent=4)