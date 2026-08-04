"""Generates the Clay Terminal file/folder icon set (PNGs) and the icon theme JSON.

Real brand logos (GitHub, VS Code, npm, Docker, JS/TS/Python/etc.) are pulled
from simple-icons (CC0-licensed SVGs, https://simpleicons.org) and composited
white-on-color onto our badge shapes, the same approach material-icon-theme
uses. Kinds with no real logo (json/yaml/txt/config/test/...) fall back to a
short text label — material-icon-theme does the same for those.

ponytail: no SVG rendering library dependency — shells out to the system
`rsvg-convert` (already installed) to rasterize, then PIL tints/composites.
Downloaded SVGs are cached in icons/.cache/ (gitignored); only final PNGs are
committed. Re-run this after editing ICONS/FOLDERS/LOGO maps below.
"""
from PIL import Image, ImageDraw, ImageFont
import json
import os
import subprocess
import urllib.request

SIZE = 128
ROOT = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(ROOT, "..", "themes", "clay-icon-theme.json")
CACHE_DIR = os.path.join(ROOT, ".cache")

CLAY = (217, 119, 87)
CLAY_LIGHT = (240, 180, 140)
WHITE = (255, 255, 255)

SIMPLE_ICONS_CDN = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg"


def font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def fetch_glyph(slug, tint=WHITE, px=256):
    """Downloads+rasterizes a simple-icons brand mark, tinted solid `tint`.
    Returns None on any failure so callers can fall back to a text label."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    svg_path = os.path.join(CACHE_DIR, f"{slug}.svg")
    png_path = os.path.join(CACHE_DIR, f"{slug}.png")
    try:
        if not os.path.isfile(svg_path):
            urllib.request.urlretrieve(SIMPLE_ICONS_CDN.format(slug=slug), svg_path)
        if not os.path.isfile(png_path):
            subprocess.run(
                ["rsvg-convert", "-w", str(px), "-h", str(px), svg_path, "-o", png_path],
                check=True, capture_output=True,
            )
        glyph = Image.open(png_path).convert("RGBA")
        solid = Image.new("RGBA", glyph.size, tint + (255,))
        solid.putalpha(glyph.getchannel("A"))
        return solid
    except Exception:
        return None


def paste_centered(base, glyph, cx, cy, target_size):
    g = glyph.copy()
    g.thumbnail((target_size, target_size), Image.LANCZOS)
    x = int(cx - g.width / 2)
    y = int(cy - g.height / 2)
    base.paste(g, (x, y), g)


def document(fill, label=None, logo=None, label_color=WHITE):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = 14
    fold_size = 20
    d.rounded_rectangle([m, m, SIZE - m, SIZE - m], radius=10, fill=fill)
    fold_color = tuple(max(0, c - 35) for c in fill)
    d.polygon(
        [(SIZE - m - fold_size, m), (SIZE - m, m + fold_size), (SIZE - m - fold_size, m + fold_size)],
        fill=fold_color,
    )
    if logo is not None:
        paste_centered(img, logo, SIZE / 2, SIZE / 2 + 8, 74)
    elif label:
        f = font(36 if len(label) <= 2 else 28)
        bbox = d.textbbox((0, 0), label, font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((SIZE - w) / 2 - bbox[0], (SIZE - h) / 2 - bbox[1] + 10), label, font=f, fill=label_color)
    return img


def folder(color, open_=False, label=None, logo=None, label_color=WHITE):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fill = tuple(min(255, c + 25) for c in color) if open_ else color
    tab_h = 16
    body_top = 40
    d.rounded_rectangle([14, body_top - tab_h, 54, body_top + 4], radius=6, fill=fill)
    if open_:
        d.polygon([(10, body_top), (118, body_top), (108, SIZE - 20), (20, SIZE - 20)], fill=fill)
    else:
        d.rounded_rectangle([10, body_top, 118, SIZE - 20], radius=10, fill=fill)

    cx, cy = SIZE / 2, body_top + (SIZE - 20 - body_top) / 2 + 6
    if logo is not None:
        paste_centered(img, logo, cx, cy, 64)
    elif label:
        f = font(32 if len(label) <= 2 else 24)
        bbox = d.textbbox((0, 0), label, font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text((cx - w / 2 - bbox[0], cy - h / 2 - bbox[1]), label, font=f, fill=label_color)
    return img


# file "kind" -> (color, text fallback label)
ICONS = {
    "js": ((219, 147, 0), "JS"),
    "jsx": ((219, 147, 0), "JSX"),
    "ts": ((109, 167, 236), "TS"),
    "tsx": ((109, 167, 236), "TSX"),
    "json": ((235, 201, 183), "{ }"),
    "md": ((196, 195, 183), "MD"),
    "py": ((12, 163, 12), "PY"),
    "go": ((98, 153, 135), "GO"),
    "rs": ((217, 119, 87), "RS"),
    "java": ((236, 126, 126), "JV"),
    "html": ((217, 119, 87), "<>"),
    "css": ((130, 125, 189), "CSS"),
    "scss": ((130, 125, 189), "SC"),
    "yaml": ((98, 153, 135), "YML"),
    "toml": ((98, 153, 135), "TML"),
    "txt": ((92, 90, 82), "TXT"),
    "image": ((160, 150, 235), "IMG"),
    "pdf": ((208, 59, 59), "PDF"),
    "lock": ((92, 90, 82), "LK"),
    "env": ((217, 119, 87), "ENV"),
    "docker": ((109, 167, 236), "DKR"),
    "license": ((235, 201, 183), "LIC"),
    "readme": ((217, 119, 87), "RM"),
    "git": ((92, 90, 82), "GIT"),
    "shell": ((26, 26, 25), "SH"),
    "xml": ((235, 201, 183), "XML"),
    "sql": ((98, 153, 135), "SQL"),
    "vue": ((12, 163, 12), "VUE"),
    "eslint": ((130, 125, 189), "ES"),
    "prettier": ((98, 153, 135), "PR"),
    "webpack": ((109, 167, 236), "WP"),
    "vite": ((219, 147, 0), "VT"),
    "jest": ((208, 59, 59), "JST"),
    "babel": ((235, 201, 183), "BBL"),
    "c": ((109, 167, 236), "C"),
    "cpp": ((109, 167, 236), "C++"),
    "csharp": ((130, 125, 189), "C#"),
    "php": ((130, 125, 189), "PHP"),
    "ruby": ((208, 59, 59), "RB"),
    "swift": ((219, 147, 0), "SW"),
    "kotlin": ((160, 150, 235), "KT"),
    "graphql": ((236, 126, 126), "GQL"),
    "terraform": ((130, 125, 189), "TF"),
    "svelte": ((219, 147, 0), "SV"),
    "dart": ((12, 163, 12), "DART"),
    "lua": ((109, 167, 236), "LUA"),
}

# file "kind" -> simple-icons slug, only where a real brand mark exists
FILE_LOGO_SLUGS = {
    "js": "javascript",
    "jsx": "react",
    "ts": "typescript",
    "tsx": "react",
    "md": "markdown",
    "readme": "markdown",
    "py": "python",
    "go": "go",
    "rs": "rust",
    "java": "java",
    "html": "html5",
    "css": "css3",
    "scss": "sass",
    "env": "dotenv",
    "docker": "docker",
    "git": "git",
    "shell": "gnubash",
    "vue": "vuedotjs",
    "eslint": "eslint",
    "prettier": "prettier",
    "webpack": "webpack",
    "vite": "vite",
    "jest": "jest",
    "babel": "babel",
    "c": "c",
    "cpp": "cplusplus",
    "csharp": "csharp",
    "php": "php",
    "ruby": "ruby",
    "swift": "swift",
    "kotlin": "kotlin",
    "graphql": "graphql",
    "terraform": "terraform",
    "svelte": "svelte",
    "dart": "dart",
    "lua": "lua",
}

FILE_EXTENSIONS = {
    "js": "js", "mjs": "js", "cjs": "js",
    "jsx": "jsx",
    "ts": "ts", "mts": "ts",
    "tsx": "tsx",
    "json": "json", "jsonc": "json",
    "md": "md", "markdown": "md", "mdx": "md",
    "py": "py", "pyw": "py",
    "go": "go",
    "rs": "rs",
    "java": "java",
    "html": "html", "htm": "html",
    "css": "css", "less": "css",
    "scss": "scss", "sass": "scss",
    "yaml": "yaml", "yml": "yaml",
    "toml": "toml",
    "txt": "txt",
    "png": "image", "jpg": "image", "jpeg": "image", "gif": "image",
    "svg": "image", "webp": "image", "ico": "image",
    "pdf": "pdf",
    "lock": "lock",
    "env": "env",
    "xml": "xml",
    "sql": "sql",
    "vue": "vue",
    "sh": "shell", "bash": "shell", "zsh": "shell",
    "c": "c", "h": "c",
    "cpp": "cpp", "cc": "cpp", "hpp": "cpp",
    "cs": "csharp",
    "php": "php",
    "rb": "ruby",
    "swift": "swift",
    "kt": "kotlin", "kts": "kotlin",
    "graphql": "graphql", "gql": "graphql",
    "tf": "terraform", "tfvars": "terraform",
    "svelte": "svelte",
    "dart": "dart",
    "lua": "lua",
}

FILE_NAMES = {
    "dockerfile": "docker",
    "docker-compose.yml": "docker",
    "docker-compose.yaml": "docker",
    "license": "license",
    "license.md": "license",
    "license.txt": "license",
    "readme.md": "readme",
    "readme": "readme",
    "readme.txt": "readme",
    "package-lock.json": "lock",
    "yarn.lock": "lock",
    "pnpm-lock.yaml": "lock",
    ".gitignore": "git",
    ".gitattributes": "git",
    ".gitmodules": "git",
    ".env": "env",
    ".env.local": "env",
    ".env.example": "env",
    ".eslintrc": "eslint",
    ".eslintrc.json": "eslint",
    ".eslintrc.js": "eslint",
    ".eslintrc.cjs": "eslint",
    ".eslintrc.yml": "eslint",
    ".prettierrc": "prettier",
    ".prettierrc.json": "prettier",
    ".prettierrc.js": "prettier",
    ".prettierrc.yml": "prettier",
    "webpack.config.js": "webpack",
    "webpack.config.ts": "webpack",
    "vite.config.js": "vite",
    "vite.config.ts": "vite",
    "jest.config.js": "jest",
    "jest.config.ts": "jest",
    "babel.config.js": "babel",
    ".babelrc": "babel",
}

# folder "kind" -> (color, text fallback label, [name aliases])
# Mirrors material-icon-theme's approach: match on bare folder name; dot-prefixed
# duplicates (e.g. ".github") are generated automatically below.
FOLDERS = {
    "git": ((92, 90, 82), "GIT", ["git", "github", "gitlab", "gitea", "forgejo", "githooks"]),
    "vscode": ((109, 167, 236), "VSC", ["vscode", "vscode-test"]),
    "node": ((12, 163, 12), "NPM", ["node_modules", "node"]),
    "src": (CLAY_LIGHT, "SRC", ["src", "source", "sources", "app"]),
    "dist": ((92, 90, 82), "DIST", ["dist", "build", "out", "output", "release", "bin"]),
    "test": ((219, 147, 0), "TEST", ["test", "tests", "spec", "specs", "__tests__"]),
    "docs": ((235, 201, 183), "DOC", ["docs", "doc", "documentation"]),
    "config": ((130, 130, 122), "CFG", ["config", "configs", "settings", "cfg"]),
    "assets": ((160, 150, 235), "IMG", ["images", "img", "imgs", "assets", "static", "public"]),
    "scripts": ((219, 147, 0), "SH", ["scripts", "script"]),
    "components": ((109, 167, 236), "CMP", ["components", "widgets"]),
    "styles": ((130, 125, 189), "CSS", ["styles", "stylesheets"]),
    "i18n": ((98, 153, 135), "i18n", ["i18n", "locales", "lang", "languages"]),
    "api": ((109, 167, 236), "API", ["api", "apis"]),
    "database": ((12, 163, 12), "DB", ["database", "db", "models"]),
    "docker": ((109, 167, 236), "DKR", ["docker"]),
    "kubernetes": ((98, 153, 135), "K8S", ["k8s", "kubernetes"]),
    "ci": ((219, 147, 0), "CI", ["ci", "workflows"]),
    "coverage": ((208, 59, 59), "COV", ["coverage"]),
    "temp": ((92, 90, 82), "TMP", ["tmp", "temp", "cache"]),
    "vendor": ((92, 90, 82), "VND", ["vendor", "third_party", "third-party"]),
}

# folder "kind" -> simple-icons slug, only where a real brand mark exists
FOLDER_LOGO_SLUGS = {
    "git": "git",
    "vscode": "visualstudiocode",
    "node": "npm",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "test": "jest",
    "ci": "githubactions",
    "styles": "css3",
    "scripts": "gnubash",
}

os.makedirs(ROOT, exist_ok=True)

icon_definitions = {}

document((60, 59, 55)).save(f"{ROOT}/file-default.png")
icon_definitions["_file"] = {"iconPath": "../icons/file-default.png"}

for key, (color, label) in ICONS.items():
    logo = fetch_glyph(FILE_LOGO_SLUGS[key]) if key in FILE_LOGO_SLUGS else None
    document(color, label=label, logo=logo).save(f"{ROOT}/file-{key}.png")
    icon_definitions[f"_{key}"] = {"iconPath": f"../icons/file-{key}.png"}

folder(CLAY).save(f"{ROOT}/folder.png")
folder(CLAY, open_=True).save(f"{ROOT}/folder-open.png")
icon_definitions["_folder"] = {"iconPath": "../icons/folder.png"}
icon_definitions["_folder_open"] = {"iconPath": "../icons/folder-open.png"}

folder_names = {}
for key, (color, label, aliases) in FOLDERS.items():
    logo = fetch_glyph(FOLDER_LOGO_SLUGS[key]) if key in FOLDER_LOGO_SLUGS else None
    folder(color, label=label, logo=logo).save(f"{ROOT}/folder-{key}.png")
    folder(color, open_=True, label=label, logo=logo).save(f"{ROOT}/folder-{key}-open.png")
    icon_definitions[f"_folder_{key}"] = {"iconPath": f"../icons/folder-{key}.png"}
    icon_definitions[f"_folder_{key}_open"] = {"iconPath": f"../icons/folder-{key}-open.png"}
    for alias in aliases:
        folder_names[alias] = f"_folder_{key}"
        folder_names[f".{alias}"] = f"_folder_{key}"

folder_names_expanded = {alias: f"{ref}_open" for alias, ref in folder_names.items()}

theme = {
    "iconDefinitions": icon_definitions,
    "folder": "_folder",
    "folderExpanded": "_folder_open",
    "rootFolder": "_folder",
    "rootFolderExpanded": "_folder_open",
    "file": "_file",
    "fileExtensions": {ext: f"_{kind}" for ext, kind in FILE_EXTENSIONS.items()},
    "fileNames": {name: f"_{kind}" for name, kind in FILE_NAMES.items()},
    "folderNames": folder_names,
    "folderNamesExpanded": folder_names_expanded,
}

with open(THEME_PATH, "w") as f:
    json.dump(theme, f, indent=2)
    f.write("\n")

total_icons = 3 + len(ICONS) + len(FOLDERS) * 2
print(f"generated {total_icons} icon files and {THEME_PATH}")
