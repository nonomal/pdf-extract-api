from typing import Type, Callable, Dict, Iterator

from text_extract_api.files.converters.pdf_to_jpeg import PdfToJpeg
from text_extract_api.files.file_formats.file_format import FileFormat
from text_extract_api.files.file_formats.image_file_format import ImageFileFormat


class PdfFileFormat(FileFormat):
    @staticmethod
    def accepted_mime_types() -> list[str]:
        return ["application/pdf"]

    @staticmethod
    def is_pageable() -> bool:
        return True

    @classmethod
    def default_iterator_file_format(cls) -> Type[ImageFileFormat]:
        return ImageFileFormat

    @staticmethod
    def convertible_to() -> Dict[Type["FileFormat"], Callable[[], Iterator["FileFormat"]]]:
        return {
            ImageFileFormat: PdfToJpeg.convert
        }
