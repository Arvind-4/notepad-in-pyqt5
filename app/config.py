import pathlib

_ROOT_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent

ICON_DIR = _ROOT_DIR / "icons"

MIN_HEIGHT = 1000
MIN_WIDTH = 2000

imageExtensions = [".jpg", ".png", ".bmp"]
htmlExtensions = [".htm", ".html"]
