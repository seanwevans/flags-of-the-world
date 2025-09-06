from pathlib import Path

INDEX_PATH = Path('index.html')

STYLE_BLOCK = """  <style>
    body {
      font-family: sans-serif;
      margin: 2rem;
    }
    h1 {
      text-align: center;
    }
    #flags {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }
    div {
      border: 1px solid black;
    }
  </style>"""

def format_caption(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split('-'))


def main():
    flags = sorted(p.stem for p in Path('.').glob('*.css'))

    head_parts = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <title>Flags of the World</title>",
    ]
    head_parts.extend(f"  <link rel=\"stylesheet\" href=\"{flag}.css\">" for flag in flags)
    head_parts.append(STYLE_BLOCK)
    head_parts.append("</head>")

    body_parts = ["", "<body>", "", "<section id=\"flags\">", ""]
    for flag in flags:
        caption = format_caption(flag)
        body_parts.extend([
            "  <figure class=\"flag-card\">",
            f"    <div id=\"{flag}\"></div>",
            f"    <figcaption>{caption}</figcaption>",
            "  </figure>",
            "",
        ])
    body_parts.extend(["</section>", "</body>", "</html>", ""])

    content = "\n".join(head_parts + body_parts)
    INDEX_PATH.write_text(content)

if __name__ == "__main__":
    main()
