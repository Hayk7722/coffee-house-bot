import json

def load_menu(file_path="menu.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Menu load error:", e)
        return {}
