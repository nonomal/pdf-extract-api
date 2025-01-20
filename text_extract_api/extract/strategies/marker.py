import os
import tempfile
import time

from text_extract_api.extract.strategies.strategy import Strategy
from text_extract_api.files.file_formats.file_format import FileFormat
from text_extract_api.files.file_formats.image import ImageFileFormat
from text_extract_api.files.file_formats.pdf import PdfFileFormat
import requests


class MarkerStrategy(Strategy):
    """Marker PDF via API - strategy"""

    @classmethod
    def name(cls) -> str:
        return "marker"

    def extract_text(self, file_format: FileFormat, language: str = 'en') -> str:

        if (
                not isinstance(file_format, PdfFileFormat)
                and not file_format.can_convert_to(PdfFileFormat)
        ):
            raise TypeError(
                f"Marker PDF - format {file_format.mime_type} is not supported (yet?)"
            )

        pdf_files = FileFormat.convert_to(file_format, PdfFileFormat)
        extracted_text = ""
        start_time = time.time()
        ocr_percent_done = 0
        
        if len(pdf_files) > 1:
            raise ValueError("Only one PDF file is supported.")
        
        if len(pdf_files) == 0:
            raise ValueError("No PDF file found - conversion error.")

        try: 
            url = os.getenv("MARKER_API_URL", "http://localhost:8002/marker/upload")
            files = {'file': ('document.pdf', pdf_files[0].binary, 'application/pdf')}
            data = {
                'page_range': None,
                'languages': language,
                'force_ocr': False,
                'paginate_output': False,
                'output_format': 'markdown' # TODO: support JSON output format
            }

            meta = {
                'progress': str(30 + ocr_percent_done),
                'status': 'OCR Processing',
                'start_time': start_time,
                'elapsed_time': time.time() - start_time}
            self.update_state_callback(state='PROGRESS', meta=meta)

            response = requests.post(url, files=files, data=data)
            if response.status_code != 200:
                raise Exception(f"Failed to upload PDF file: {response.content}")

            extracted_text = response.json().get('output', '')
        except Exception as e:
            print('Error:', e)
            raise Exception("Failed to generate text with Marker PDF API. Make sure marker-pdf server is up and running: marker_server --port 8002. Details: https://github.com/VikParuchuri/marker")
            
        return extracted_text
