import unittest
from unittest.mock import patch, mock_open, MagicMock
from script.textMining import clean_pdf_text, read_pdf, write_cleaned_text, process_pdf

class TestPDFTextMining(unittest.TestCase):
    def test_clean_pdf_text(self):
        # Sample text simulating extracted content from a PDF
        sample_text = """
        ABSTRACT: Example abstract. This should be removed.\nIntroduction: This should stay.\nREFERENCES: Reference content to remove.
        """
        expected_output = "Introduction: This should stay."
        cleaned_text = clean_pdf_text(sample_text)
        
        # Use strip to remove leading/trailing whitespace and compare
        self.assertEqual(cleaned_text.strip(), expected_output)

    @patch('textMining.StringIO')
    @patch('textMining.PDFResourceManager')
    @patch('textMining.TextConverter')
    @patch('textMining.PDFPageInterpreter')
    @patch('textMining.PDFDocument')
    @patch('textMining.PDFParser')
    def test_read_pdf(self, mock_parser, mock_document, mock_interpreter, mock_converter, mock_resourcemanager, mock_stringio):
        # Set up StringIO to return a specific string
        mock_stringio.return_value.getvalue.return_value = "Extracted text"
        with patch('builtins.open', mock_open(read_data="dummy data")) as mocked_file:
            result = read_pdf("dummy_path.pdf")
            self.assertEqual(result, "Extracted text")

    @patch('builtins.open', new_callable=mock_open, create=True)
    def test_write_cleaned_text(self, mock_open):
        write_cleaned_text("Some cleaned text", "output_path.txt")
        mock_open.assert_called_once_with("output_path.txt", "w")
        mock_open().write.assert_called_once_with("Some cleaned text")

    @patch('textMining.read_pdf', return_value="Raw text from PDF")
    @patch('textMining.clean_pdf_text', return_value="Cleaned text")
    @patch('textMining.write_cleaned_text')
    def test_process_pdf(self, mock_write, mock_clean, mock_read):
        with patch('builtins.open', new_callable=mock_open) as mocked_file:
            process_pdf("input.pdf", "output_directory")
            # Ensure no FileNotFoundError and correct function calls
            mock_read.assert_called_once_with("input.pdf")
            mock_clean.assert_called_once_with("Raw text from PDF")
            mock_write.assert_called_once_with("Cleaned text", "output_directory/input_output_text.txt")
            # Verify that file handling was invoked correctly
            mocked_file.assert_called_once_with("output_directory/input_output_text.txt", "w")

if __name__ == '__main__':
    unittest.main()
