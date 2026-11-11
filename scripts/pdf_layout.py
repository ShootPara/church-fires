"""Extract editable slide compositions from the PDF for the local build."""
import base64
import hashlib
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
HREF = "{http://www.w3.org/1999/xlink}href"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def export_layout(page, number, output):
    root = ET.fromstring(page.get_svg_image(text_as_path=False))
    namespace = {"svg": SVG}
    tabs = {"summary", "timeline", "deaths", "investigations", "rebuilding"}
    for group in root.iter():
        children = list(group)
        labels = [
            i for i, node in enumerate(children)
            if node.tag == f"{{{SVG}}}text"
            and "".join(node.itertext()).strip().lower() in tabs
        ]
        if len(labels) >= 4:
            # The deck paints the tab bar before the slide's foreground.
            for node in children[max(1, labels[0] - 3):labels[-1] + 1]:
                group.remove(node)
    if number == 62:
        for parent in root.iter():
            for node in list(parent):
                if node.tag == f"{{{SVG}}}text" and "rebuildin" in "".join(node.itertext()).lower():
                    parent.remove(node)
        ET.SubElement(root, f"{{{SVG}}}rect", x="72", y="131", width="576", height="144", fill="#f9f4e9")
        ET.SubElement(root, f"{{{SVG}}}text", x="360", y="228", fill="#241d19",
                      attrib={"text-anchor": "middle", "font-family": "Arial",
                              "font-weight": "bold", "font-size": "68"}).text = "rebuilding"
    for node in root.findall(".//svg:image", namespace):
        source = node.get(HREF, "")
        match = re.fullmatch(r"data:image/(png|jpeg);base64,(.*)", source, re.S)
        if match:
            content = base64.b64decode(match[2])
            name = f"pdf-{hashlib.sha256(content).hexdigest()[:24]}.{match[1]}"
            (output / name).write_bytes(content)
            node.set(HREF, f"assets/{name}")
    for node in root.iter():
        for attribute, value in list(node.attrib.items()):
            if attribute == "id":
                node.set(attribute, f"s{number}-{value}")
            elif attribute == HREF and value.startswith("#"):
                node.set(attribute, f"#s{number}-{value[1:]}")
            elif "url(#" in value:
                node.set(attribute, value.replace("url(#", f"url(#s{number}-"))
    root.set("aria-hidden", "true")
    return ET.tostring(root, encoding="unicode")
