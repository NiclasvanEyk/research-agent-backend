import os
from dataclasses import dataclass
from mimetypes import guess_file_type
from os.path import getsize
from pathlib import Path

import anyio
from fastapi import UploadFile


class MissingFilenameError(RuntimeError): ...


class MissingFileExtensionError(RuntimeError): ...


class CouldNotGuessMimeTypeError(RuntimeError): ...


class FileNotFoundError(RuntimeError): ...


@dataclass
class SuccessfullyStoredFile:
    location: Path
    size: int
    mime_type: str


@dataclass
class SourceContent:
    content: bytes
    mime_type: str


class ResearchSources:
    def __init__(self, base: Path) -> None:
        self._base = base

    async def store(self, file: UploadFile) -> SuccessfullyStoredFile:
        self._base.mkdir(parents=True, exist_ok=True)

        if not file.filename:
            raise MissingFilenameError()

        target = self._base / file.filename
        if not target.suffix:
            raise MissingFileExtensionError()

        mime_type, _ = guess_file_type(target)
        if mime_type is None:
            raise CouldNotGuessMimeTypeError

        try:
            async with await anyio.open_file(target, "wb") as buffer:
                while chunk := await file.read(65536):  # 64KB
                    await buffer.write(chunk)
        finally:
            await file.close()

        return SuccessfullyStoredFile(
            location=target,
            size=getsize(target),
            mime_type=mime_type,
        )

    async def list_sources(self) -> list[str]:
        """
        Lists the base names of all files that we stored.
        """
        source_names = []
        for name in os.listdir(self._base):
            if not (self._base / name).is_file():
                continue
            if name == ".gitignore":
                continue
            source_names.append(name)
        return source_names

    async def read_source_content(self, name: str) -> SourceContent:
        path = self._base / name
        if not path.exists():
            raise FileNotFoundError(path)

        mime_type, _ = guess_file_type(path)
        if mime_type is None:
            raise CouldNotGuessMimeTypeError

        async with await anyio.open_file(path, "rb") as buffer:
            return SourceContent(content=await buffer.read(), mime_type=mime_type)
