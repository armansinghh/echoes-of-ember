import json
import pygame

def load_level(name):
    with open(f"levels/{name}.json") as f:
        data = json.load(f)

    data["start_pos"] = tuple(data["start_pos"])
    data["lantern"] = tuple(data["lantern"])
    data["platforms"] = [pygame.Rect(*r) for r in data["platforms"]]
    data["voids"] = [(pygame.Rect(*v["rect"]), tuple(v["color"])) for v in data.get("voids", [])]
    data["hazards"] = [pygame.Rect(*r) for r in data.get("hazards",[])]
    return data