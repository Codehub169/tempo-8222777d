import os
import PyPDF2

def get_file_extension(filename):
    """Helper function to get the file extension from a filename."""
    return os.path.splitext(filename)[1].lower()

def process_uploaded_file(file_path):
    """
    Processes an uploaded file (.txt or .pdf) and extracts its text content.

    Args:
        file_path (str): The absolute path to the uploaded file.

    Returns:
        str: The extracted text content from the file.
        None: If the file type is unsupported or an error occurs during processing.
    """
    try:
        ext = get_file_extension(file_path)
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            text_content = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text_content += page.extract_text() or ""
            return text_content
        else:
            # Unsupported file type
            print(f"Unsupported file type: {ext}")
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF file {file_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")
        return None

if __name__ == '__main__':
    # Create dummy files for testing
    if not os.path.exists('test_uploads'):
        os.makedirs('test_uploads')

    with open('test_uploads/sample.txt', 'w') as f:
        f.write("This is a sample text file.\nIt has multiple lines.")

    # Note: Creating a valid PDF programmatically for testing is complex.
    # For PyPDF2 testing, manually place a sample.pdf in 'test_uploads'.
    # For now, we'll just test the .txt functionality and PDF error handling.
    
    print("Testing with sample.txt:")
    txt_content = process_uploaded_file('test_uploads/sample.txt')
    if txt_content:
        print(f"Extracted text:\n{txt_content}")
    else:
        print("Failed to process sample.txt")

    print("\nTesting with non_existent_file.pdf:")
    pdf_content_non_existent = process_uploaded_file('test_uploads/non_existent_file.pdf')
    if pdf_content_non_existent:
        print(f"Extracted text: {pdf_content_non_existent}") # Should not happen
    else:
        print("Correctly handled non-existent PDF file.")

    # To test PDF processing, create a 'sample.pdf' in 'test_uploads' directory
    # print("\nTesting with sample.pdf (ensure it exists in test_uploads):")
    # pdf_content = process_uploaded_file('test_uploads/sample.pdf')
    # if pdf_content:
    #     print(f"Extracted text from PDF (first 100 chars): {pdf_content[:100]}...")
    # else:
    #     print("Failed to process sample.pdf. Make sure it exists and is a valid PDF.")
