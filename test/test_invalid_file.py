import os
import pytest
from pypdf import PdfReader
from script.cropPage import scaleCropPDFMargins

@pytest.fixture
def real_pdf_environment(tmp_path):
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    invalid_pdf_path = "/Users/stephaniekhuu/Documents/curaitor/test/PDFFiles/invalid_file.pdf"
    valid_pdf_path = "/Users/stephaniekhuu/Documents/curaitor/test/PDFFiles/valid_file.pdf"

    # Provide paths to the test functions
    return {
        'invalid_pdf': str(invalid_pdf_path),
        'valid_pdf': str(valid_pdf_path),
        'output_dir': str(output_dir)
    }


def test_valid_pdf_handling(real_pdf_environment):

    # Using real environment setup to get the paths
    valid_pdf = real_pdf_environment['valid_pdf']
    output_directory = real_pdf_environment['output_dir']
    
    # Test should not raise an exception for a valid PDF
    try:
        scaleCropPDFMargins(valid_pdf, output_directory)
    except Exception as e:
        pytest.fail(f"Function should not have raised an exception for a valid PDF: {str(e)}")

def test_real_invalid_pdf_handling(real_pdf_environment):
    # Using real environment setup to get the paths
    invalid_pdf = real_pdf_environment['invalid_pdf']
    output_directory = real_pdf_environment['output_dir']

    # Expecting an exception due to invalid PDF
    with pytest.raises(Exception) as excinfo:
        scaleCropPDFMargins(invalid_pdf, output_directory)
    
    # # Assert to check specific error message
    # assert "expected error message" in str(excinfo.value)

