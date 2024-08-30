import os
from pypdf import PageObject, PaperSize, PdfReader, PdfWriter, Transformation
from tqdm import tqdm

def scaleCropPDFMargins(uploaded_file: str, outputDirectory: str) -> None:
    """
    Scale and crop PDF margins to fit A4 size.

    Args:
        uploaded_file (str): Path to the input PDF file.
        outputDirectory (str): Directory to save the output file.

    Returns:
        None
    """
    outputFilename = f"{os.path.splitext(uploaded_file)[0]}_cropped.pdf"
    input1 = PdfReader(uploaded_file)
    output = PdfWriter()
    A4_w, A4_h = float(PaperSize.A4.width), float(PaperSize.A4.height)
    
    print(f"Document has {len(input1.pages)} pages.")
    
    for page in input1.pages:
        pageWidth, pageHeight = float(page.mediabox[2]), float(page.mediabox[3])
        scaleFactorWidth, scaleFactorHeight = A4_w / pageWidth, A4_h / pageHeight
        
        # Scale page to fit A4
        transformScale = Transformation().scale(scaleFactorWidth, scaleFactorHeight)
        page.add_transformation(transformScale)
        
        # Create blank A4 page and center original content
        page_A4 = PageObject.create_blank_page(width=A4_w, height=A4_h)
        center_page = calculate_center(page)
        center_page_A4 = calculate_center(page_A4)
        translationX = -(center_page[0] - center_page_A4[0]) / 2
        translationY = -(center_page[1] - center_page_A4[1]) / 2
        transform = Transformation().translate(translationX, translationY)
        
        # Merge and transform pages
        page_A4.merge_page(page)
        page_A4.add_transformation(transform)
        
        # Apply cropping
        cropSides, cropBottom, cropTop = 35, 50, 30
        page_A4.mediabox.lower_left = (
            page_A4.mediabox.lower_left[0] + cropSides,
            page_A4.mediabox.lower_left[1] + cropBottom,
        )
        page_A4.cropbox.upper_right = (
            page_A4.mediabox.upper_right[0] - cropSides,
            page_A4.mediabox.upper_right[1] - cropTop,
        )
        output.add_page(page_A4)
    
    # Write output
    with open(outputFilename, "wb") as pdfFileOut:
        output.write(pdfFileOut)

def calculate_center(page: PageObject) -> tuple:
    """
    Calculate center coordinates of a page.

    Args:
        page (PageObject): The page object to calculate center for.

    Returns:
        tuple: A tuple containing the x and y coordinates of the page center.
    """
    width = page.mediabox.upper_right[0] - page.mediabox.lower_left[0]
    height = page.mediabox.upper_right[1] - page.mediabox.lower_left[1]
    center_x = page.mediabox.lower_left[0] + width / 2
    center_y = page.mediabox.lower_left[1] + height / 2
    return (center_x, center_y)

def cropAllPdfs(uploaded_files: list, outputDirectory: str, totalFiles: int) -> None:
    """
    Process all uploaded PDF files.

    Args:
        uploaded_files (list): List of uploaded PDF file paths.
        outputDirectory (str): Directory to save processed files.
        totalFiles (int): Total number of files to process.

    Returns:
        None
    """
    os.makedirs(outputDirectory, exist_ok=True)
    
    with tqdm(total=totalFiles, desc="Processing files") as pbar:
        for uploaded_file in uploaded_files:
            path_file = os.path.join(outputDirectory, uploaded_file)
            scaleCropPDFMargins(path_file, outputDirectory)
            pbar.set_description(f"Processing files (Processed: {pbar.n + 1}/{totalFiles})")
            pbar.update(1)