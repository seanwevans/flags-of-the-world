import textwrap
from pathlib import Path

flags = [
    {
        "name": "ecuador",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Ecuador",
        "height": 2,
        "width": 3,
        "orientation": "horizontal",
        "colors": [
            ("#ffdd00", 0.5),
            ("#003893", 0.25),
            ("#ce1126", 0.25),
        ],
    },
    {
        "name": "haiti",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Haiti",
        "height": 3,
        "width": 5,
        "orientation": "horizontal",
        "colors": [
            ("#00209f", 0.5),
            ("#d21034", 0.5),
        ],
    },
    {
        "name": "liechtenstein",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Liechtenstein",
        "height": 3,
        "width": 5,
        "orientation": "horizontal",
        "colors": [
            ("#002b7f", 0.5),
            ("#ce1126", 0.5),
        ],
    },
    {
        "name": "mongolia",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Mongolia",
        "height": 2,
        "width": 3,
        "orientation": "vertical",
        "colors": [
            ("#c4272f", 1/3),
            ("#005aa7", 1/3),
            ("#c4272f", 1/3),
        ],
    },
    {
        "name": "montenegro",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Montenegro",
        "height": 1,
        "width": 3/2,
        "orientation": "solid",
        "background": "#d81e05",
        "border": "#c6aa76",
    },
    {
        "name": "serbia",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Serbia",
        "height": 2,
        "width": 3,
        "orientation": "horizontal",
        "colors": [
            ("#ff0000", 1/3),
            ("#0c4076", 1/3),
            ("#ffffff", 1/3),
        ],
    },
    {
        "name": "slovakia",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Slovakia",
        "height": 2,
        "width": 3,
        "orientation": "horizontal",
        "colors": [
            ("#ffffff", 1/3),
            ("#0b4ea2", 1/3),
            ("#ef3340", 1/3),
        ],
    },
    {
        "name": "barbados",
        "ref": "https://en.wikipedia.org/wiki/Flag_of_Barbados",
        "height": 2,
        "width": 3,
        "orientation": "vertical",
        "colors": [
            ("#00267f", 1/3),
            ("#ffc726", 1/3),
            ("#00267f", 1/3),
        ],
    },
]

TEMPLATE = textwrap.dedent(
    """/* reference: {ref} */

:root {{
  --flag-height: {height};
  --flag-width: {width};
}}

#{name} {{
  position: relative;
  height: 180px;
  aspect-ratio: var(--flag-width) / var(--flag-height);
  background: {background};
  {extra}
}}
"""
)

for f in flags:
    if f["orientation"] == "solid":
        background = f['background']
        extra = f"border: 15px solid {f['border']};"
    else:
        direction = "90deg" if f["orientation"] == "vertical" else "180deg"
        stops = []
        pos = 0
        for color, ratio in f["colors"]:
            end = pos + ratio * 100
            stops.append(f"{color} {pos:.3f}% {end:.3f}%")
            pos = end
        background = f"linear-gradient({direction}, " + ", ".join(stops) + ")"
        extra = ""
    css = TEMPLATE.format(ref=f['ref'], height=f['height'], width=f['width'], name=f['name'], background=background, extra=extra)
    Path(f"{f['name']}.css").write_text(css)
