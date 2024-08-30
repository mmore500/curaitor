from .textMining import clean_pdf_text, read_pdf

def compare_text_to_pdf(input_text: str, pdf_path: str) -> bool:
   """
   Compare input text to content of a PDF file.

   Args:
       input_text: Text to search for in PDF
       pdf_path: Path to PDF file

   Returns:
       bool: True if input_text found in PDF, False otherwise
   """
   pdf_text = read_pdf(pdf_path)
   pdf_text = clean_pdf_text(pdf_text)
   
   return input_text in pdf_text

# Test function
input_text = "Instead of requiring humans to manually derive rules and build models from analyzing large amounts"
pdf_path = "test/dummy_pdf/dummy1.pdf"
result = compare_text_to_pdf(input_text, pdf_path)
print(result)