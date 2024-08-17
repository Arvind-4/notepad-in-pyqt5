import os
import uuid


def hexuuid() -> str:
    return str(uuid.uuid4().hex)


def splitText(p: str) -> str:
    return os.path.splitext(p)[1].lower()


def fontList() -> list[str]:
    return [str(i) for i in range(1, 289)]
