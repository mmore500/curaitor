import os
import pytest
from unittest.mock import patch, MagicMock
from pypdf import PdfReader
from curaitor import scaleCropPDFMargins  # Adjust the import according to your project structure

@pytest.fixture
def setup_invalid_pdf_environment(tmp_path):
    # Create a test input directory using pytest's tmp_path fixture
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    # Path for an invalid PDF file
    invalid_pdf_path = input_dir / "invalid_file.pdf"
    with open(invalid_pdf_path, 'wb') as f:
        f.write(b"Unable to read file")

    # Return paths for use in tests
    return str(invalid_pdf_path), str(output_dir)

def test_invalid_pdf_handling(setup_invalid_pdf_environment):
    invalid_pdf, output_directory = setup_invalid_pdf_environment

    # Patch the PdfReader to raise an IOError when trying to read an invalid PDF
    with patch('pypdf.PdfReader', side_effect=IOError("Invalid PDF file")):
        # Expecting an IOError to be raised due to invalid PDF
        with pytest.raises(IOError) as excinfo:
            scaleCropPDFMargins(invalid_pdf, output_directory)
        
        assert "Invalid PDF file" in str(excinfo.value)
