"""
File processing utilities for various document formats
"""
import os
from typing import Tuple
import PyPDF2
from docx import Document
import logging

logger = logging.getLogger(__name__)


class FileProcessor:
    """Process different file formats to extract text"""
    
    SUPPORTED_FORMATS = {'.pdf', '.docx', '.doc', '.txt'}
    
    @staticmethod
    def extract_text(file_path: str) -> Tuple[str, str]:
        """
        Extract text from various file formats
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (text, file_type)
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext not in FileProcessor.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {ext}")
        
        if ext == '.pdf':
            return FileProcessor._extract_from_pdf(file_path), 'pdf'
        elif ext in ['.docx', '.doc']:
            return FileProcessor._extract_from_docx(file_path), 'docx'
        elif ext == '.txt':
            return FileProcessor._extract_from_txt(file_path), 'txt'
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = []
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    try:
                        text.append(page.extract_text())
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num}: {e}")
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Error reading PDF file: {e}")
            raise
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Error reading DOCX file: {e}")
            raise
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading TXT file: {e}")
            raise
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """Get metadata about the file"""
        stat_info = os.stat(file_path)
        _, ext = os.path.splitext(file_path)
        
        return {
            'file_name': os.path.basename(file_path),
            'file_path': file_path,
            'file_size': stat_info.st_size,
            'file_type': ext.lower(),
            'created_at': stat_info.st_ctime,
            'modified_at': stat_info.st_mtime
        }
