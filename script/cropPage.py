import os

from pypdf import PageObject, PaperSize, PdfReader, PdfWriter, Transformation
from tqdm import tqdm


def scaleCropPDFMargins(uploaded_file, outputDirectory):
    # Construct output path
    outputFilename = os.path.splitext(uploaded_file)[0] + "_cropped.pdf"
    # outputPath = os.path.join(outputDirectory, outputFilename)

    input1 = PdfReader(uploaded_file)
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

        # Use page height, width to calculate scale factor for A4
        scaleFactorWidth, scaleFactorHeight = (
            A4_w / pageWidth,
            A4_h / pageHeight,
        )

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
    with open(outputFilename, "wb") as pdfFileOut:
        output.write(pdfFileOut)


# Function to calculate center of a page
def calculate_center(page):
    width = page.mediabox.upper_right[0] - page.mediabox.lower_left[0]
    height = page.mediabox.upper_right[1] - page.mediabox.lower_left[1]
    center_x = page.mediabox.lower_left[0] + width / 2
    center_y = page.mediabox.lower_left[1] + height / 2
    return (center_x, center_y)


def cropAllPdfs(uploaded_files, outputDirectory, totalFiles):
    # Ensure the output directory exists, create it if not
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    with tqdm(total=totalFiles, desc="Processing files") as pbar:
        processed_count = 0
        # Iterate through uploaded PDF files
        for uploaded_file in uploaded_files:
            path_file = os.path.join(outputDirectory, uploaded_file)
            scaleCropPDFMargins(path_file, outputDirectory)
            processed_count += 1
            pbar.set_description(
                f"Processing files (Processed: {processed_count}/{totalFiles})"
            )
            pbar.update(1)
