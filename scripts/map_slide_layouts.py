"""Generate editable layout records. PDF renders are used only to match named files."""
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "ignore/Deconstructed Original Slides/media"
deck = json.loads((ROOT / "ignore/drive-review/raw-template.json").read_text(encoding="utf8"))["structuredContent"]
files = sorted(MEDIA.iterdir())


def number(value):
    return value.get("magnitude", 0) / (12700 if value.get("unit") == "EMU" else 1)


def rgb(fill, default):
    color = fill.get("color", fill)
    if "rgbColor" in color:
        return "#" + "".join(f"{round(color['rgbColor'].get(key, 0)*255):02x}" for key in ("red", "green", "blue"))
    return {"LIGHT1": "#f9f4e9", "LIGHT2": "#eeeeee", "DARK1": "#241d19", "DARK2": "#241d19"}.get(color.get("themeColor"), default)


def thumbnail(image):
    return image.convert("RGB").resize((32, 32), Image.Resampling.LANCZOS)


layouts = []
for slide_number, slide in enumerate(deck["slides"], 1):
    elements = []
    slots = []
    candidates = [
        path for path in files
        if re.match(rf"SLIDE 0*{slide_number} |.*also SLIDE 0*{slide_number}(?!\d)", path.name)
        and " Audio icon " not in path.name
        and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    ]
    for element in slide.get("pageElements", []):
        transform = element.get("transform", {})
        size = element.get("size", {})
        if not size:
            continue
        x, y = (number({"magnitude": transform.get(key, 0), "unit": transform.get("unit")})
                for key in ("translateX", "translateY"))
        w, h = (number(size[key]) for key in ("width", "height"))
        a, b, c, d = (transform.get(key, default) for key, default in
                      (("scaleX", 1), ("shearY", 0), ("shearX", 0), ("scaleY", 1)))
        corners = [(x+a*u+c*v, y+b*u+d*v) for u, v in ((0, 0), (w, 0), (0, h), (w, h))]
        left, top = (min(p[i] for p in corners) for i in (0, 1))
        width, height = (max(p[i] for p in corners)-min(p[i] for p in corners) for i in (0, 1))
        if min(width, height) <= 0:
            continue
        record = {"id": element["objectId"], "box": [round(v, 3) for v in (left, top, width, height)]}
        if "image" in element or "video" in element:
            if re.search(r"\.mp3|speaker|audio", element.get("title", ""), re.I):
                continue
            record["kind"] = "video" if "video" in element else "image"
            record["crop"] = element.get("image", {}).get("imageProperties", {}).get("cropProperties", {})
            record["rotation"] = round(math.degrees(math.atan2(b, a))) if b else 0
            slots.append(record)
        elif "line" in element:
            record.update(kind="arrow", points=[x, y, x+a*w+c*h, y+b*w+d*h],
                          color=rgb(element["line"].get("lineProperties", {}).get("lineFill", {}).get("solidFill", {}), "#80a943"))
        elif "shape" in element:
            shape = element["shape"]
            props = shape.get("shapeProperties", {})
            runs = [run["textRun"] for run in shape.get("text", {}).get("textElements", []) if "textRun" in run]
            label = "".join(run["content"] for run in runs).strip()
            if label.casefold() == "brian ream":
                continue
            if slide_number >= 3 and top > 350 and (not label or label.lower() in {
                "summary", "timeline", "deaths", "investigations", "rebuilding", "fcc", "mec", "pres"
            }):
                continue
            fill = rgb(props.get("shapeBackgroundFill", {}).get("solidFill", {}), "transparent")
            if props.get("shapeBackgroundFill", {}).get("propertyState") == "NOT_RENDERED":
                fill = "transparent"
            outline = props.get("outline", {})
            if outline and outline.get("propertyState") != "NOT_RENDERED":
                record["border"] = {"color": rgb(outline.get("outlineFill", {}).get("solidFill", {}), "#241d19"), "width": number(outline.get("weight", {}))}
            if not label and fill == "transparent" and "border" not in record:
                continue
            record.update(kind="text" if label else "shape", fill=fill, shape=shape["shapeType"], flip=a<0)
            if label:
                markers = [r["paragraphMarker"] for r in shape["text"]["textElements"] if "paragraphMarker" in r]
                record.update(align=markers[0].get("style", {}).get("alignment", "START").lower() if markers else "start",
                              valign=props.get("contentAlignment", "TOP").lower(),
                              runs=[{"text": run["content"], "size": run["style"].get("fontSize", {}).get("magnitude", 14),
                                     "bold": run["style"].get("bold", False),
                                     "color": rgb(run["style"].get("foregroundColor", {}).get("opaqueColor", {}), "#241d19")}
                                    for run in runs])
        else:
            continue
        elements.append(record)
    reference_path = ROOT / f"ignore/extraction/presentation/page-{slide_number:03}.png"
    if slide_number == 73 and len(candidates) == 1:
        for slot in slots:
            slot["source"] = candidates[0].name
    elif slots and candidates and reference_path.exists():
        with Image.open(reference_path) as reference:
            references = []
            for slot in slots:
                x, y, w, h = slot["box"]
                references.append(thumbnail(reference.crop((x*reference.width/720, y*reference.height/405,
                                                           (x+w)*reference.width/720, (y+h)*reference.height/405))))
        pairs = []
        for path in candidates:
            with Image.open(path) as image:
                sample = thumbnail(image)
            for i, reference in enumerate(references):
                score = sum(ImageStat.Stat(ImageChops.difference(sample, reference)).mean)
                pairs.append((score, path.name, i))
        used = set()
        for score, filename, i in sorted(pairs):
            if filename in used or "source" in slots[i]:
                continue
            slots[i].update(source=filename, matchScore=round(score, 1))
            used.add(filename)
    if slide_number == 53:
        base = next(slot for slot in slots if slot["id"] == "g2f9d3c916e9_0_276")
        inset = next(slot for slot in slots if slot["id"] == "g2fc9d28a78a_0_61")
        base["source"], inset["source"] = inset["source"], base["source"]
    if slide_number == 58:
        elements = [element for element in elements if element["kind"] != "arrow"]
    layouts.append({"slide": slide_number, "elements": elements,
                    "unresolved": [slot["id"] for slot in slots if "source" not in slot],
                    "unassigned": [path.name for path in candidates if all(element.get("source") != path.name for element in elements)]})
(ROOT / "sources/slide-layouts.json").write_text(json.dumps(layouts, indent=2, ensure_ascii=False), encoding="utf8")
for layout in layouts:
    if layout["unresolved"] or layout["unassigned"]:
        print(layout["slide"], layout["unresolved"], layout["unassigned"])
