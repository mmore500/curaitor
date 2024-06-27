from .textMining import clean_pdf_text, read_pdf

# from textMining import *


def compare_text_to_pdf(input_text, pdf_path):
    # Read the text from the PDF
    pdf_text = read_pdf(pdf_path)
    pdf_text = clean_pdf_text(pdf_text)
    # pdf_text = clean_pdf_text2(pdf_text)
    # print(pdf_text)

    # Compare the input text to the PDF text
    if input_text in pdf_text:
        return True
    else:
        return False


# # funtion to clean nextline in text
# def clean_pdf_text2(text):

#     # Remove newline characters
#     cleaned_text = text.replace("\n", "")

#     # Remove extra whitespaces at the end
#     cleaned_text = cleaned_text.strip()

#     return cleaned_text


# run the function using dummy pdf
input_text = "Instead of requiring humans to manually derive rules and build models from analyzing large amounts"
pdf_path = "test/dummy_pdf/dummy1.pdf"
result = compare_text_to_pdf(input_text, pdf_path)
print(result)
