"""Create manual screenshot drop folders for every visual in the original deck."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLIDES_ROOT = ROOT / "ignore" / "Deconstructed Original Slides"
WORKLIST = ROOT / "sources" / "extracted" / "slide-worklist.json"

# Slides whose native image objects are newspaper pieces or article compositions.
CLIPPING_SLIDES = {
    1,
    21, 22, 23,
    29, 30, 31,
    33, 34, 35, 36,
    *range(39, 49),
    50, 51, 52,
    *range(54, 62),
    67, 68, 69, 70,
    73,
}

# Mixed layouts need both kinds. Counts follow the meaningful native objects.
MIXED_SLIDES = {
    24: {"clippings": 1, "images": 3},
    32: {"clippings": 3, "images": 2},
    53: {"clippings": 5, "images": 2},
}


def numbered_folder(number: int, kind: str, index: int) -> str:
    return f"{index:03d} {kind} {index}"


def main() -> None:
    deck = json.loads(WORKLIST.read_text(encoding="utf-8"))
    inventory = []

    for slide in deck["slides"]:
        number = slide["slide"]
        slide_folder = SLIDES_ROOT / f"{number:03d} Slide {number}"
        slide_folder.mkdir(parents=True, exist_ok=True)

        image_count = sum("image" in element for element in slide["elements"])
        video_count = sum("video" in element for element in slide["elements"])

        if number in MIXED_SLIDES:
            counts = MIXED_SLIDES[number]
            clipping_count = counts["clippings"]
            image_folder_count = counts["images"]
        elif number in CLIPPING_SLIDES:
            clipping_count = image_count
            image_folder_count = video_count
        else:
            clipping_count = 0
            image_folder_count = image_count + video_count

        expected_names = []
        ordinal = 1
        for index in range(1, clipping_count + 1):
            name = numbered_folder(number, "Clipping", index)
            (slide_folder / name).mkdir(exist_ok=True)
            expected_names.append(name)
            ordinal += 1

        for index in range(1, image_folder_count + 1):
            name = f"{ordinal:03d} Image {index}"
            (slide_folder / name).mkdir(exist_ok=True)
            expected_names.append(name)
            ordinal += 1

        inventory.append(
            {
                "slide": number,
                "slide_id": slide["slide_id"],
                "clipping_folders": clipping_count,
                "image_folders": image_folder_count,
                "folders": expected_names,
            }
        )

    manifest = SLIDES_ROOT / "folder-inventory.json"
    manifest.write_text(
        json.dumps({"slides": inventory}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Created {sum(len(item['folders']) for item in inventory)} asset folders "
        f"across {len(inventory)} slide folders."
    )


if __name__ == "__main__":
    main()
