import os

from pypdf import PageObject, PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
from tqdm import tqdm


def scaleCropPDFMargins(inputPDFPath, outputDirectory):
    # Construct output path
    outputFilename = (
        os.path.splitext(os.path.basename(inputPDFPath))[0] + "_cropped.pdf"
    )
    outputPath = os.path.join(outputDirectory, outputFilename)
    print(inputPDFPath)

    with open(inputPDFPath, "rb") as pdfFile:
        input1 = PdfReader(pdfFile)
        output = PdfWriter()
        A4_w = float(PaperSize.A4.width)
        A4_h = float(PaperSize.A4.height)

        numPages = len(input1.pages)
        print("document has %s pages." % numPages)

        for page in input1.pages:
            # Retrieve page height, width
            pageWidth, pageHeight = float(page.mediabox[2]), float(
                page.mediabox[3]
            )
            # print(pageWidth, pageHeight)

            # Use page height, width to calculate scale factor for A4
            scaleFactorWidth, scaleFactorHeight = (
                A4_w / pageWidth,
                A4_h / pageHeight,
            )
            # print(scaleFactorWidth, scaleFactorHeight)

            # Apply scale factor
            transformScale = Transformation().scale(
                scaleFactorWidth, scaleFactorHeight
            )
            page.add_transformation(transformScale)

            # prepare A4 blank page
            page_A4 = PageObject.create_blank_page(width=A4_w, height=A4_h)

            # Calculate translation between centers
            center_page = calculate_center(page)
            center_page_A4 = calculate_center(page_A4)

            # Calculate translation
            translationX = -(center_page[0] - center_page_A4[0]) / 2
            translationY = -(center_page[1] - center_page_A4[1]) / 2
            # print(center_page)
            # print("center of A4 page: ", center_page_A4)
            # print(translationX)
            # print(translationY)

            transform = Transformation().translate(translationX, translationY)

            # merge the pages to fit inside A4
            page_A4.merge_page(page)
            page_A4.add_transformation(transform)

            cropSides = 35
            cropBottom = 50
            cropTop = 30

            page_A4.mediabox.lower_left = (
                page_A4.mediabox.lower_left[0] + cropSides,
                page_A4.mediabox.lower_left[1] + cropBottom,
            )
            page_A4.cropbox.upper_right = (
                page_A4.mediabox.upper_right[0] - cropSides,
                page_A4.mediabox.upper_right[1] - cropTop,
            )

            output.add_page(page_A4)

        # Write output to specified path
        with open(outputPath, "wb") as pdfFileOut:
            output.write(pdfFileOut)


# Function to calculate center of a page
def calculate_center(page):
    width = page.mediabox.upper_right[0] - page.mediabox.lower_left[0]
    height = page.mediabox.upper_right[1] - page.mediabox.lower_left[1]
    center_x = page.mediabox.lower_left[0] + width / 2
    center_y = page.mediabox.lower_left[1] + height / 2
    return (center_x, center_y)


def cropAllPdfs(pdfsDirectory, outputDirectory, totalFiles):
    # Ensure the output directory exists, create it if not
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    with tqdm(total=totalFiles, desc="Processing files") as pbar:
        processed_count = 0
        # Iterate through PDF files in the directory
        for filename in os.listdir(pdfsDirectory):
            if filename.endswith(".pdf"):
                input_pdf_path = os.path.join(pdfsDirectory, filename)
                scaleCropPDFMargins(input_pdf_path, outputDirectory)
            processed_count += 1
            pbar.set_description(
                f"Processing files (Processed: {processed_count}/{totalFiles})"
            )
            pbar.update(1)


# # Directory containing PDFs to process
# pdfsDirectory = 'articles'
# totalFiles = len(os.listdir(pdfsDirectory))

# # Output directory for cleaned text files
# outputDirectory = os.path.join(pdfsDirectory, 'output')

# # Crop all PDFs in the directory
# cropAllPdfs(pdfsDirectory, outputDirectory, totalFiles)

# # Test single PDF
# # pdfPath= "review/1-s2.0-S0143416016300094-main.pdf"
# # cropPDFMargins(pdfPath, outputDirectory)
