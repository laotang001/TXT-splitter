# AI Book Processing Tool - TXT Document Splitter

[中文版本](README_CN.md)

A professional TXT document splitting software designed for AI book processing and local knowledge base creation. Supports intelligent chapter recognition, multi-encoding compatibility, and batch processing capabilities.

## Key Features

1. **Intelligent Chapter Recognition**
   - **Enhanced: Automatically identifies common chapter markers in both Chinese and English books**
   - **Chinese**: Chapter X (第X章), Part X (第X回), Section X (第X节), etc.
   - **English**: Chapter X, Part X, Section X, Book X, Volume X, etc.
   - Supports custom regular expressions for chapter identification

2. **Flexible Splitting Logic**
   - Prioritizes chapter-based splitting when chapters are detected
   - Automatically splits by 8000 characters when chapters cannot be identified
   - **New: When chapter content exceeds 10,000 characters (including Chinese characters and punctuation), the chapter is automatically split into multiple sub-files named "ChapterName_Number"**
   - Preserves complete document content without losing any text

3. **Multi-Encoding Support**
   - Automatically detects and supports multiple Chinese encodings (GBK, UTF-8, etc.)
   - Ensures split documents maintain original encoding format

4. **Standardized Output**
   - Each split document saved as "OriginalFileName_Number.txt" format
   - Preserves original chapter titles at the beginning of files (when split by chapters)
   - **New: Supports custom output directory selection - split files are saved to the specified directory**
   - **New: After large chapter splitting, files are named in "ChapterName_Number.txt" format**

5. **User-Friendly Interface**
   - Clean and intuitive graphical user interface
   - Progress bar display when processing large files
   - Supports batch processing of multiple TXT documents

## Installation Requirements

Install the Python libraries listed in `requirements.txt` before use:

```bash
pip install -r requirements.txt
```

## Usage Instructions

1. Run the program:
   ```bash
   python txt_splitter.py
   ```

2. Click the "Select Files" button in the interface to choose TXT files for splitting (multiple selection supported)

3. **New: Click the "Select Directory" button to choose the output directory for split files. If not selected, files are saved to the source file directory by default.**

## Ideal for AI Applications

This tool is specifically designed for:
- **AI Book Processing**: Prepare entire books for AI model training and analysis
- **Local Knowledge Base Creation**: Split large documents into manageable chunks for local AI systems
- **Document Preprocessing**: Optimize text files for various AI and machine learning applications
- **Research and Analysis**: Process large text corpora for academic and research purposes

## Language Support

The application supports both English and Chinese interfaces. The default language is English, but you can switch to Chinese through the language selection feature.

## Technical Specifications

- **Supported Formats**: Plain text files (.txt)
- **Encoding Support**: UTF-8, GBK, GB2312, GB18030, Big5
- **Chapter Recognition**: Customizable regular expressions
- **Split Size**: Configurable character count (default: 8000)
- **Large Chapter Handling**: Automatic splitting for chapters exceeding 10,000 characters

## Perfect for AI Knowledge Base Development

This tool enables efficient processing of entire books and large documents, making it ideal for creating comprehensive local knowledge bases that AI systems can effectively utilize. The intelligent splitting mechanism ensures that content remains contextually coherent while being optimized for AI processing limitations.