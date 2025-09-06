from pathlib import Path
import sys

# Mapping for filenames that don't convert cleanly to country names
SPECIAL_NAMES = {
    "usa": "United States",
    "czech-republic": "Czech Republic",
    "congo-drc": "Democratic Republic of the Congo",
    "congo-republic": "Republic of the Congo",
    "ivory-coast": "Ivory Coast",
    "trinidad-and-tobago": "Trinidad and Tobago",
    "united-arab-emirates": "United Arab Emirates",
}


def format_name(file_stem: str) -> str:
    """Convert a CSS filename stem into a human-friendly country name."""
    if file_stem in SPECIAL_NAMES:
        return SPECIAL_NAMES[file_stem]
    words = file_stem.replace('_', '-').split('-')
    return " ".join(word.capitalize() for word in words)


def main(output_path: str = "README.md") -> None:
    css_files = sorted(Path(".").glob("**/*.css"), key=lambda p: p.stem)
    countries = [format_name(f.stem) for f in css_files]

    lines = [
        "# Flags of the World",
        "",
        "A showcase of national flags rendered with pure CSS.",
        "",
        f"Currently, **{len(countries)}** flags are included.",
        "",
        "## Completed",
        "",
    ]
    for name in countries:
        wiki_name = name.replace(" ", "_")
        lines.append(f"* [{name}](https://en.wikipedia.org/wiki/Flag_of_{wiki_name})")
    lines.append("")
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    main(out)
