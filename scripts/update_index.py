from pathlib import Path

new_flags = [
    "barbados",
    "brazil",
    "brunei",
    "burundi",
    "central-african-republic",
    "dominican-republic",
    "ecuador",
    "eritrea",
    "haiti",
    "kazakhstan",
    "kyrgyzstan",
    "liechtenstein",
    "mongolia",
    "montenegro",
    "namibia",
    "nepal",
    "new-zealand",
    "palestine",
    "micronesia",
    "marshall-islands",
    "san-marino",
    "serbia",
    "slovakia",
    "uruguay",
    "venezuela",
]

index_path = Path("index.html")
content = index_path.read_text().splitlines()

# Insert link tags before </head>
head_idx = next(i for i, line in enumerate(content) if "</head>" in line)
link_lines = [f'  <link rel="stylesheet" href="{flag}.css">' for flag in new_flags]
content[head_idx:head_idx] = link_lines

# Insert figures before </section>
section_idx = next(i for i, line in enumerate(content) if "</section>" in line)

def format_caption(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))

figure_lines = []
for flag in new_flags:
    caption = format_caption(flag)
    figure_lines.extend([
        "  <figure class=\"flag-card\">",
        f"    <div id=\"{flag}\"></div>",
        f"    <figcaption>{caption}</figcaption>",
        "  </figure>",
        "",
    ])
content[section_idx:section_idx] = figure_lines

index_path.write_text("\n".join(content) + "\n")
