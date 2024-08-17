import os

from PyQt5 import QtWidgets

from app.main import main

os.environ["XDG_SESSION_TYPE"] = "xcb"


if __name__ == "__main__":
    main()
