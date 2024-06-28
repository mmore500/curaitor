from io import StringIO
import unittest
from unittest.mock import MagicMock, mock_open, patch

from script.textMining import (
    clean_pdf_text,
    process_pdf,
    read_pdf,
    write_cleaned_text,
)


class TestPDFTextMining(unittest.TestCase):
    def test_clean_pdf_text(self):
        sample_text = """ABSTRACT:Example abstract. This should be removed.
        Introduction: This should stay.
        """
        expected_output = "Introduction: This should stay."
        cleaned_text = clean_pdf_text(sample_text)
        self.assertEqual(cleaned_text.strip(), expected_output)

    @patch(
        "script.textMining.StringIO",
        create=True,
        return_value=StringIO("Extracted text"),
    )
    @patch("script.textMining.PDFResourceManager")
    @patch(
        "script.textMining.TextConverter",
        return_value=MagicMock(auto_spec=True),
    )
    @patch("script.textMining.PDFPageInterpreter")
    @patch(
        "script.textMining.PDFDocument", return_value=MagicMock(auto_spec=True)
    )
    @patch(
        "script.textMining.PDFParser", return_value=MagicMock(auto_spec=True)
    )
    def test_read_pdf(
        self,
        mock_parser,
        mock_document,
        mock_interpreter,
        mock_converter,
        mock_resourcemanager,
        mock_stringio,
    ):
        with patch("builtins.open", mock_open(read_data="dummy data")):
            result = read_pdf("dummy_path.pdf")
            self.assertEqual(result, "Extracted text")

    @patch("builtins.open", new_callable=mock_open, create=True)
    def test_write_cleaned_text(self, mock_open):
        write_cleaned_text("Some cleaned text", "output_path.txt")
        mock_open.assert_called_once_with(
            "output_path.txt", "w", encoding="utf-8"
        )
        mock_open().write.assert_called_once_with("Some cleaned text")

    @patch("script.textMining.read_pdf", return_value="Raw text from PDF")
    @patch("script.textMining.clean_pdf_text", return_value="Cleaned text")
    @patch("script.textMining.write_cleaned_text")
    def test_process_pdf(self, mock_write, mock_clean, mock_read):
        with patch("builtins.open", new_callable=mock_open):
            process_pdf("input.pdf", "output_directory")
            mock_read.assert_called_once_with("input.pdf")
            mock_clean.assert_called_once_with("Raw text from PDF")
            mock_write.assert_called_once_with(
                "Cleaned text", "output_directory/input_output_text.txt"
            )


if __name__ == "__main__":
    unittest.main()
