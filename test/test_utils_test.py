import unittest
from .script.utils_test import compare_text_to_pdf

class TestUtilsTest(unittest.TestCase):

    
    def test_compare_text_to_pdf(self):
        input_text = "Instead of requiring humans to manually derive rules and build models from analyzing large amounts"
        pdf_path = "test/dummy_pdf/dummy1.pdf"
        expected_result = True

        result = compare_text_to_pdf(input_text, pdf_path)

        self.assertEqual(result, expected_result)

    def test_compare_text_to_pdf(self):
        input_text = "Instead of requiring humans to manually derive rules and build models from analyzing large amounts"
        pdf_path = "test/dummy_pdf/dummy2.pdf"
        expected_result = False

        result = compare_text_to_pdf(input_text, pdf_path)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()