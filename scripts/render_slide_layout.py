"""Render native layout records with named local image assets."""
from html import escape


def render_layout(layout, urls, video):
    parts = []
    for element in layout["elements"]:
        x, y, w, h = element["box"]
        style = f"left:{x/7.2}%;top:{y/4.05}%;width:{w/7.2}%;height:{h/4.05}%"
        kind = element["kind"]
        tag = f'data-object="{escape(element["id"])}"'
        if element.get("border"):
            border = element["border"]
            style += f';border:{border["width"]/7.2}cqw solid {border["color"]}'
        if kind in {"image", "video"}:
            source = element.get("source")
            if source and not (kind == "video" and video):
                url = urls[source]
                alt = source.partition(" - ")[2].rsplit(" ", 3)[0]
                crop = element.get("crop", {})
                image_style = ""
                if crop:
                    left, right, top, bottom = (crop.get(key, 0) for key in ("leftOffset", "rightOffset", "topOffset", "bottomOffset"))
                    cw, ch = 1-left-right, 1-top-bottom
                    if cw > 0 and ch > 0:
                        image_style = f"position:absolute;width:{100/cw}%;height:{100/ch}%;left:{-100*left/cw}%;top:{-100*top/ch}%;object-fit:fill"
                rotation = element.get("rotation", 0)
                frame_style = "position:absolute;inset:0;overflow:hidden"
                if abs(rotation) == 90:
                    frame_style = f"position:absolute;left:50%;top:50%;width:{h/w*100}%;height:{w/h*100}%;transform:translate(-50%,-50%) rotate({rotation}deg);overflow:hidden"
                parts.append(f'<a class="placed" {tag} style="{style};overflow:hidden" href="{url}"><span style="{frame_style}"><img style="{image_style}" src="{url}" loading="lazy" alt="{escape(alt)}"></span></a>')
            if kind == "video" and video:
                parts.append(f'<div class="placed" {tag} style="{style}">{video}</div>')
        elif kind == "arrow":
            x1,y1,x2,y2 = element["points"]
            color = element["color"]
            parts.append(f'<svg class="slide-arrow" viewBox="0 0 720 405" aria-hidden="true"><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"/></svg>')
        else:
            fill = element["fill"]
            if kind == "text" and all(run["color"] == fill for run in element["runs"]):
                fill = "transparent"
            style += f';background:{fill}'
            if kind == "shape":
                corner = {"HALF_FRAME": " corner", "RIGHT_ARROW": " right-arrow"}.get(element["shape"], "")
                if element["flip"]:
                    style += ";transform:scaleX(-1)"
                parts.append(f'<div class="placed{corner}" {tag} style="{style}" aria-hidden="true"></div>')
                continue
            align = {"start":"left","end":"right","center":"center","justified":"justify"}.get(element["align"], "left")
            vertical = {"top":"start","middle":"center","bottom":"end"}.get(element["valign"],"start")
            if fill in {"#f9f4e9", "#ffffff"}:
                vertical = "center"
            style += f";text-align:{align};justify-content:{vertical}"
            runs = []
            for index, run in enumerate(element["runs"]):
                size = run["size"]
                if layout["slide"] == 62 and "rebuild" in run["text"].lower():
                    size = min(size, 68)
                weight = 700 if run["bold"] else 400
                text = run["text"].rstrip() if index == len(element["runs"]) - 1 else run["text"]
                runs.append(f'<span style="font-size:{size/7.2}cqw;font-weight:{weight};color:{run["color"]}">{escape(text)}</span>')
            parts.append(f'<div class="placed native-text" {tag} style="{style}"><div class="text-content">{"".join(runs)}</div></div>')
    return "".join(parts)
