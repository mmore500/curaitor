import unittest
from unittest.mock import mock_open, patch
from script import clean_pdf_text, read_pdf

class TestPDFProcessing(unittest.TestCase):
    def test_clean_pdf_text_removes_references(self):
        # Sample text simulating PDF content
        text = """
        ABSTRACT: Example abstract. This should be removed.
        INTRODUCTION: This should stay.
        REFERENCES
        1. Doe, J. Example. 2020.
        """
        expected_text = """
        INTRODUCTION: This should stay.
        """
        # Cleaning text
        result = clean_pdf_text(text)
        self.assertIn("INTRODUCTION", result)
        self.assertNotIn("ABSTRACT", result)
        self.assertNotIn("REFERENCES", result)

    def test_read_pdf_reads_content(self):
        # Content that simulates the text extracted from a PDF
        fake_pdf_content = "Fake PDF Content"
        with patch("builtins.open", mock_open(read_data=fake_pdf_content)), \
             patch("pdfminer.pdfinterp.PDFResourceManager"), \
             patch("pdfminer.converter.TextConverter"), \
             patch("pdfminer.pdfpage.PDFPage"), \
             patch("pdfminer.pdfinterp.PDFPageInterpreter"), \
             patch("pdfminer.pdfdocument.PDFDocument"), \
             patch("pdfminer.pdfparser.PDFParser"), \
             patch("io.StringIO", return_value=StringIO(fake_pdf_content)) as mock_stringio:
            result = read_pdf("dummy_path.pdf")
            mock_stringio.assert_called_once()  # Ensure StringIO was used to capture PDF text
            self.assertEqual(result, fake_pdf_content)

if __name__ == '__main__':
    unittest.main()
