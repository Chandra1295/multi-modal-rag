


import os
import logging
from typing import Union
from io import BytesIO
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.utils.constants import PartitionStrategy
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def validate_pdf(file: Union[str, BytesIO]) -> None:
    """Validate PDF file before processing
    
    Args:
        file: Either file path (str) or file-like object (BytesIO)
    
    Raises:
        ValueError: If file is invalid
    """
    # Check file type
    if isinstance(file, str):
        if not file.lower().endswith('.pdf'):
            raise ValueError("Invalid file extension. Only PDFs are supported")
    else:  # Streamlit UploadedFile/BytesIO
        if not getattr(file, 'name', '').lower().endswith('.pdf'):
            raise ValueError("Invalid file type. Please upload a PDF")

    # Check file size
    max_size = 50 * 1024 * 1024  # 50MB
    if isinstance(file, str):
        file_size = os.path.getsize(file)
    else:
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset pointer
    
    if file_size > max_size:
        raise ValueError(f"File too large. Max size: {max_size/1024/1024}MB")

def extract_content_from_pdf(file_path: str, figures_dir: str = "temp/figures") -> str:
    """Extract and structure PDF content"""
    os.makedirs(figures_dir, exist_ok=True)
    
    elements = partition_pdf(
        file_path,
        strategy=PartitionStrategy.FAST,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_output_dir=figures_dir,
        max_image_size=400
    )
    
    text_content = []
    for element in elements:
        if hasattr(element, 'text') and element.text.strip():
            text_content.append(element.text.strip())
    
    return "\n\n".join(text_content)

def process_pdf(file_path: str):
    """Orchestrate PDF processing pipeline"""
    try:
        validate_pdf(file_path)  # Add validation
        content = extract_content_from_pdf(file_path)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len
        )
        return splitter.split_text(content)
    
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}")
        raise