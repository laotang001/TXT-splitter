import os
import re
import chardet
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import threading
import json

# Language configuration and translation system
class LanguageManager:
    def __init__(self):
        self.current_language = "english"
        self.translations = {
            "english": {
                "app_title": "AI Book Processing Tool - TXT Document Splitter",
                "file_selection": "File Selection",
                "select_file": "Select File",
                "select_folder": "Select Folder",
                "output_folder": "Output Folder",
                "select_output": "Select Output",
                "split_settings": "Split Settings",
                "chapter_pattern": "Chapter Pattern",
                "split_by_chapter": "Split by Chapter",
                "split_by_size": "Split by Size",
                "split_size_mb": "Split Size (MB)",
                "split_options": "Split Options",
                "remove_blank_lines": "Remove Blank Lines",
                "remove_extra_spaces": "Remove Extra Spaces",
                "encoding": "Encoding",
                "auto_detect": "Auto Detect",
                "start_split": "Start Split",
                "stop_split": "Stop Split",
                "progress": "Progress",
                "status": "Status",
                "files_processed": "Files Processed: {}/{}",
                "total_files": "Total Files",
                "estimated_time": "Estimated Time",
                "elapsed_time": "Elapsed Time",
                "remaining_time": "Remaining Time",
                "processing": "Processing...",
                "completed": "Completed",
                "paused": "Paused",
                "error": "Error",
                "warning": "Warning",
                "success": "Complete",
                "select_files": "Select Files",
                "clear_list": "Clear List",
                "output_directory": "Output Directory",
                "default_output": "Default: Use source file directory",
                "select_directory": "Select Directory",
                "reset_to_default": "Reset to Default",
                "files_to_process": "Files to Process",
                "custom_chapter_regex": "Custom Chapter Regular Expression:",
                "default_split_size": "Default Split Size (characters):",
                "enable_text_cleaning": "Enable text cleaning (remove extra blank lines, standardize punctuation, etc.)",
                "start_processing": "Start Processing",
                "ready": "Ready",
                "processing_file": "Processing: {}",
                "complete": "Complete! Processed {} files, generated {} split files, saved to: {}",
                "warning_no_files": "Please select files to process first!",
                "warning_processing": "Files are currently being processed, please wait!",
                "warning_invalid_size": "Default split size must be a positive integer!",
                "error_create_dir": "Failed to create output directory: {}",
                "error_read_file": "Failed to read file: {}",
                "error_split_file": "Failed to split file: {}",
                "success_complete": "Complete!\n\nProcessed {} files\nGenerated {} split files\nSaved to: {}",
                "select_txt_files": "Select TXT Files",
                "text_files": "Text Files",
                "select_output_dir": "Select Output Directory",
                "language_selection": "Language Selection"
            },
            "chinese": {
                "app_title": "AI书籍处理工具 - TXT文档拆分器",
                "file_selection": "文件选择",
                "select_file": "选择文件",
                "select_folder": "选择文件夹",
                "output_folder": "输出文件夹",
                "select_output": "选择输出",
                "split_settings": "拆分设置",
                "chapter_pattern": "章节模式",
                "split_by_chapter": "按章节拆分",
                "split_by_size": "按大小拆分",
                "split_size_mb": "拆分大小 (MB)",
                "split_options": "拆分选项",
                "remove_blank_lines": "移除空行",
                "remove_extra_spaces": "移除多余空格",
                "encoding": "编码",
                "auto_detect": "自动检测",
                "start_split": "开始拆分",
                "stop_split": "停止拆分",
                "progress": "进度",
                "status": "状态",
                "files_processed": "已处理文件: {}/{}",
                "total_files": "总文件数",
                "estimated_time": "预计时间",
                "elapsed_time": "已用时间",
                "remaining_time": "剩余时间",
                "processing": "处理中...",
                "completed": "已完成",
                "paused": "已暂停",
                "error": "错误",
                "warning": "警告",
                "success": "完成",
                "select_files": "选择文件",
                "clear_list": "清除列表",
                "output_directory": "输出目录",
                "default_output": "默认使用源文件目录",
                "select_directory": "选择目录",
                "reset_to_default": "重置为默认",
                "files_to_process": "待处理文件",
                "custom_chapter_regex": "自定义章节正则表达式:",
                "default_split_size": "默认拆分字数:",
                "enable_text_cleaning": "启用文本整理（去除多余空行、统一标点符号等）",
                "start_processing": "开始拆分",
                "ready": "就绪",
                "processing_file": "正在处理: {}",
                "complete": "处理完成！共处理 {} 个文件，生成 {} 个拆分文件，保存在: {}",
                "warning_no_files": "请先选择要处理的文件！",
                "warning_processing": "正在处理文件，请稍候！",
                "warning_invalid_size": "默认拆分字数必须是正整数！",
                "error_create_dir": "创建输出目录失败: {}",
                "error_read_file": "读取文件失败: {}",
                "error_split_file": "拆分文件失败: {}",
                "success_complete": "完成！\n\n共处理 {} 个文件\n生成 {} 个拆分文件\n保存在: {}",
                "select_txt_files": "选择TXT文件",
                "text_files": "文本文件",
                "select_output_dir": "选择输出目录",
                "language_selection": "语言选择"
            }
        }
        self.load_preferences()
    
    def load_preferences(self):
        """Load language preferences from file"""
        try:
            if os.path.exists("preferences.json"):
                with open("preferences.json", "r", encoding="utf-8") as f:
                    prefs = json.load(f)
                    self.current_language = prefs.get("language", "english")
        except:
            self.current_language = "english"  # Default to English
    
    def save_preferences(self):
        """Save language preferences to file"""
        try:
            prefs = {"language": self.current_language}
            with open("preferences.json", "w", encoding="utf-8") as f:
                json.dump(prefs, f, ensure_ascii=False, indent=2)
        except:
            pass  # Silently fail if preferences can't be saved
    
    def set_language(self, language):
        """Set current language"""
        if language in self.translations:
            self.current_language = language
            self.save_preferences()
    
    def get_text(self, key, *args):
        """Get translated text with optional formatting"""
        text = self.translations[self.current_language].get(key, key)
        if args:
            return text.format(*args)
        return text


class TxtSplitter:
    def __init__(self):
        # Default chapter recognition patterns - supports bilingual Chinese/English recognition
        self.chapter_patterns = [
            # Chinese chapter patterns
            r'^第[0-9一二三四五六七八九十百千]+[章回节]',  # Chapter X, Part X, Section X
            r'^第[0-9一二三四五六七八九十百千]+[卷]',      # Volume X
            r'^[0-9一二三四五六七八九十百千]+[、.]',       # X、or X.
            r'^[第]?[0-9]+[章节回]',                     # Chapter 1, 1章
            r'^[第]?[0-9]+',                           # Chapter 1, 1
            r'.*（[一二三四五六七八九十]+）',              # XXX（一）
            r'.*\([一二三四五六七八九十]+\)',              # XXX(一)
            
            # English chapter patterns
            r'^\s*Chapter\s+[0-9IVXLCDM]+',           # Chapter 1, Chapter I, Chapter IV
            r'^\s*CHAPTER\s+[0-9IVXLCDM]+',          # CHAPTER 1, CHAPTER I
            r'^\s*Part\s+[0-9IVXLCDM]+',             # Part 1, Part I
            r'^\s*PART\s+[0-9IVXLCDM]+',             # PART 1, PART I
            r'^\s*Section\s+[0-9IVXLCDM]+',          # Section 1, Section I
            r'^\s*SECTION\s+[0-9IVXLCDM]+',          # SECTION 1, SECTION I
            r'^\s*Book\s+[0-9IVXLCDM]+',             # Book 1, Book I
            r'^\s*BOOK\s+[0-9IVXLCDM]+',             # BOOK 1, BOOK I
            r'^\s*Volume\s+[0-9IVXLCDM]+',           # Volume 1, Volume I
            r'^\s*VOLUME\s+[0-9IVXLCDM]+',           # VOLUME 1, VOLUME I
            r'^\s*[0-9IVXLCDM]+\.',                  # 1., I., IV.
            r'^\s*[0-9IVXLCDM]+\s+',                 # 1 , I , IV (空格分隔)
            r'^\s*[0-9IVXLCDM]+\s*$',                # 1, I, IV (单独一行)
            r'^\s*[A-Z]\s*\.',                     # A., B., C.
            r'^\s*[A-Z]\s+',                        # A , B , C (空格分隔)
            r'^\s*[A-Z]\s*$',                       # A, B, C (单独一行)
            r'^\*\*\*\s*Chapter\s+[0-9IVXLCDM]+\s*\*\*\*',  # *** Chapter 1 ***
            r'^\*\*\*\s*CHAPTER\s+[0-9IVXLCDM]+\s*\*\*\*',  # *** CHAPTER 1 ***
            r'^\*\*\*\s*Part\s+[0-9IVXLCDM]+\s*\*\*\*',     # *** Part 1 ***
            r'^\*\*\*\s*PART\s+[0-9IVXLCDM]+\s*\*\*\*',     # *** PART 1 ***
            r'^\*\*\*\s*Section\s+[0-9IVXLCDM]+\s*\*\*\*',  # *** Section 1 ***
            r'^\*\*\*\s*SECTION\s+[0-9IVXLCDM]+\s*\*\*\*',  # *** SECTION 1 ***
            r'^\*\*\*\s*Book\s+[0-9IVXLCDM]+\s*\*\*\*',     # *** Book 1 ***
            r'^\*\*\*\s*BOOK\s+[0-9IVXLCDM]+\s*\*\*\*',     # *** BOOK 1 ***
            r'^\*\*\*\s*Volume\s+[0-9IVXLCDM]+\s*\*\*\*',   # *** Volume 1 ***
            r'^\*\*\*\s*VOLUME\s+[0-9IVXLCDM]+\s*\*\*\*',   # *** VOLUME 1 ***
            r'^\*\*\*\s*[0-9IVXLCDM]+\s*\*\*\*',              # *** 1 ***, *** I ***
            r'^\*\*\*\s*[A-Z]\s*\*\*\*',                     # *** A ***, *** B ***
            r'^#\s+Chapter\s+[0-9IVXLCDM]+',      # # Chapter 1, # Chapter I
            r'^#\s+CHAPTER\s+[0-9IVXLCDM]+',      # # CHAPTER 1, # CHAPTER I
            r'^#\s+[0-9IVXLCDM]+',                   # # 1, # I, # IV
            r'^#\s+[A-Z]',                           # # A, # B, # C
            r'^##\s+[0-9IVXLCDM]+\.\s+',          # ## 1. , ## I. 
            r'^##\s+[A-Z]\.\s+',                  # ## A. , ## B.
            r'^\\d+\\.\\s+\\w+',                   # 1. Title, 2. Title
            r'^[IVXLCDM]+\\.\\s+\\w+',               # I. Title, II. Title
            r'^[A-Z]\\.\\s+\\w+',                    # A. Title, B. Title
            r'^\\d+\\s+-\\s+\\w+',                   # 1 - Title, 2 - Title
            r'^[IVXLCDM]+\\s+-\\s+\\w+',               # I - Title, II - Title
            r'^[A-Z]\\s+-\\s+\\w+',                    # A - Title, B. Title
            r'^\\d+\\.\\s*$',                       # 1., 2. (单独一行)
            r'^[IVXLCDM]+\\.\\s*$',                   # I., II. (单独一行)
            r'^[A-Z]\\.\\s*$',                        # A., B. (单独一行)
        ]
        self.custom_pattern = None
        self.default_split_size = 8000  # Default split by 8000 characters
        self.encoding = None
        self.output_dir = None  # Output directory, None means use source file directory
        self.enable_clean_text = True  # Whether to enable text cleaning
        
    def detect_encoding(self, file_path):
        """Detect file encoding"""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']
    
    def read_file(self, file_path):
        """Read file content"""
        try:
            # Detect encoding
            self.encoding = self.detect_encoding(file_path)
            if not self.encoding:
                self.encoding = 'utf-8'  # Default to UTF-8
            
            # Read in binary mode to avoid encoding issues
            with open(file_path, 'rb') as f:
                content_bytes = f.read()
                
            # Attempt to decode
            try:
                content = content_bytes.decode(self.encoding, errors='replace')
            except UnicodeDecodeError:
                # If decoding fails, try other common encodings
                for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']:
                    try:
                        content = content_bytes.decode(enc, errors='replace')
                        self.encoding = enc
                        break
                    except UnicodeDecodeError:
                        continue
                        
            return content
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
    
    def clean_text(self, content):
        """Clean text content"""
        if not content:
            return content
            
        # Split by lines
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove leading/trailing spaces
            line = line.strip()
            
            # Skip empty lines (optionally keep some for paragraph separation)
            if not line:
                # If previous line is not empty, keep this empty line for paragraph separation
                if cleaned_lines and cleaned_lines[-1]:
                    cleaned_lines.append('')
                continue
            
            # Merge multiple consecutive spaces into one space
            line = re.sub(r'\s+', ' ', line)
            
            # Standardize punctuation (half-width to full-width)
            punctuation_map = {
                ',': '，',
                '.': '。',
                '?': '？',
                '!': '！',
                ':': '：',
                ';': '；',
                '(': '（',
                ')': '）',
                '"': '"',
                "'": "'",
                '[': '【',
                ']': '】'
            }
            
            for half, full in punctuation_map.items():
                line = line.replace(half, full)
            
            # Handle quote pairing
            line = re.sub(r'"([^"]*)"', r'"\1"', line)
            line = re.sub(r"'([^']*)'", r"'\1'", line)
            
            cleaned_lines.append(line)
        
        # Remove extra empty lines at beginning and end of document
        while cleaned_lines and not cleaned_lines[0]:
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()
        
        # Merge consecutive empty lines into single empty line
        final_lines = []
        prev_empty = False
        for line in cleaned_lines:
            if not line:
                if not prev_empty:
                    final_lines.append(line)
                prev_empty = True
            else:
                final_lines.append(line)
                prev_empty = False
        
        return '\n'.join(final_lines)
    
    def find_chapters(self, content):
        """Identify chapters"""
        lines = content.split('\n')
        chapters = []
        
        # Combine all patterns
        patterns = self.chapter_patterns.copy()
        if self.custom_pattern:
            patterns.append(self.custom_pattern)
        
        # Find all chapters
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            for pattern in patterns:
                if re.match(pattern, line):
                    chapters.append((i, line))
                    break
        
        return chapters, lines
    
    def split_by_chapters(self, content, file_path):
        """Split by chapters"""
        chapters, lines = self.find_chapters(content)
        
        # If no chapters found, split by size
        if not chapters:
            return self.split_by_size(content, file_path)
        
        # Split by chapters
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # Use specified output directory or source file directory
        output_dir = self.output_dir if self.output_dir else os.path.dirname(file_path)
        
        result_files = []
        for i in range(len(chapters)):
            start_idx = chapters[i][0]
            # If it's the last chapter, end index is end of file
            if i == len(chapters) - 1:
                end_idx = len(lines)
            else:
                end_idx = chapters[i+1][0]
            
            # Extract chapter content
            chapter_content = '\n'.join(lines[start_idx:end_idx])
            chapter_title = lines[start_idx].strip()
            
            # Check if chapter content exceeds 10,000 characters
            if len(chapter_content) > 10000:
                # Calculate number of parts needed
                parts_count = (len(chapter_content) + 9999) // 10000  # Round up
                
                # Split chapter into approximately equal parts
                part_size = len(chapter_content) // parts_count
                
                for part_idx in range(parts_count):
                    start_pos = part_idx * part_size
                    end_pos = min((part_idx + 1) * part_size, len(chapter_content))
                    part_content = chapter_content[start_pos:end_pos]
                    
                    # Use chapter name + number as filename
                    safe_title = re.sub(r'[\\/*?:"<>|]', '_', chapter_title)  # Remove invalid filename characters
                    output_file = os.path.join(output_dir, f"{safe_title}_{part_idx+1}.txt")
                    
                    with open(output_file, 'wb') as f:
                        f.write(part_content.encode(self.encoding, errors='replace'))
                    
                    result_files.append(output_file)
            else:
                # Chapter content does not exceed 10,000 characters, save directly
                # Use chapter name as filename
                safe_title = re.sub(r'[\\/*?:"<>|]', '_', chapter_title)  # Remove invalid filename characters
                output_file = os.path.join(output_dir, f"{safe_title}.txt")
                
                with open(output_file, 'wb') as f:
                    f.write(chapter_content.encode(self.encoding, errors='replace'))
                
                result_files.append(output_file)
        
        return result_files
    
    def split_by_size(self, content, file_path):
        """Split by character count"""
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # Use specified output directory or source file directory
        output_dir = self.output_dir if self.output_dir else os.path.dirname(file_path)
        
        # Calculate number of files to split into
        total_chars = len(content)
        num_files = max(1, (total_chars + self.default_split_size - 1) // self.default_split_size)
        
        result_files = []
        for i in range(num_files):
            start_idx = i * self.default_split_size
            end_idx = min((i + 1) * self.default_split_size, total_chars)
            
            # Extract content
            part_content = content[start_idx:end_idx]
            
            # Save file
            output_file = os.path.join(output_dir, f"{base_name}_{i+1}.txt")
            with open(output_file, 'wb') as f:
                f.write(part_content.encode(self.encoding, errors='replace'))
            
            result_files.append(output_file)
        
        return result_files
    
    def split_file(self, file_path, progress_callback=None, enable_clean=True):
        """Split file"""
        try:
            # Read file
            content = self.read_file(file_path)
            
            # If text cleaning is enabled, clean the text
            if enable_clean:
                content = self.clean_text(content)
            
            # Split by chapters
            result_files = self.split_by_chapters(content, file_path)
            
            return result_files
        except Exception as e:
            raise Exception(f"拆分文件失败: {str(e)}")


class TxtSplitterApp:
    def __init__(self, root):
        self.root = root
        self.language_manager = LanguageManager()
        self.root.title(self.language_manager.get_text("app_title"))
        self.root.geometry("650x750")  # Slightly larger to accommodate language selection
        self.root.resizable(True, True)
        
        self.splitter = TxtSplitter()
        self.files_to_process = []
        self.processing = False
        self.output_dir = None  # Output directory
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language selection
        language_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("language_selection"), padding="5")
        language_frame.pack(fill=tk.X, pady=5)
        
        self.language_var = tk.StringVar(value=self.language_manager.current_language)
        ttk.Radiobutton(language_frame, text="English", variable=self.language_var, 
                       value="english", command=self.change_language).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(language_frame, text="中文", variable=self.language_var, 
                       value="chinese", command=self.change_language).pack(side=tk.LEFT, padx=10)
        
        # File selection area
        file_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("file_selection"), padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text=self.language_manager.get_text("select_files"), 
                  command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text=self.language_manager.get_text("clear_list"), 
                  command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # Output directory selection
        output_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("output_directory"), padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_dir_var = tk.StringVar(value=self.language_manager.get_text("default_output"))
        ttk.Label(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text=self.language_manager.get_text("select_directory"), 
                  command=self.select_output_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text=self.language_manager.get_text("reset_to_default"), 
                  command=self.reset_output_dir).pack(side=tk.LEFT, padx=5)
        
        # File list
        list_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("files_to_process"), padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox
        self.file_listbox = tk.Listbox(list_frame)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Chapter recognition settings
        settings_frame = ttk.LabelFrame(main_frame, text=self.language_manager.get_text("split_settings"), padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Custom chapter regular expression
        ttk.Label(settings_frame, text=self.language_manager.get_text("custom_chapter_regex")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.custom_pattern_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.custom_pattern_var).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Default split size
        ttk.Label(settings_frame, text=self.language_manager.get_text("default_split_size")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.split_size_var = tk.StringVar(value="8000")
        ttk.Entry(settings_frame, textvariable=self.split_size_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Text cleaning options
        self.clean_text_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text=self.language_manager.get_text("enable_text_cleaning"), 
                       variable=self.clean_text_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        # Status label
        self.status_var = tk.StringVar(value=self.language_manager.get_text("ready"))
        ttk.Label(main_frame, textvariable=self.status_var).pack(anchor=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text=self.language_manager.get_text("start_processing"), 
                  command=self.start_processing).pack(side=tk.RIGHT, padx=5)
    
    def change_language(self):
        """Change the application language with manual restart instruction"""
        new_language = self.language_var.get()
        if new_language != self.language_manager.current_language:
            # Show manual restart instruction dialog
            if new_language == "english":
                message = "To apply English interface, the application needs to be restarted.\n\nThe application will now close. Please manually restart it to see the changes."
                chinese_message = "要应用英文界面，应用程序需要重新启动。\n\n应用程序将立即关闭。请手动重新启动以查看更改。"
            else:
                message = "要应用中文界面，应用程序需要重新启动。\n\n应用程序将立即关闭。请手动重新启动以查看更改。"
                chinese_message = message
            
            # Use appropriate message based on current language
            if self.language_manager.current_language == "english":
                display_message = message
            else:
                display_message = chinese_message
            
            result = messagebox.askokcancel(
                self.language_manager.get_text("language_selection"),
                display_message
            )
            
            if result:
                # Save the new language preference
                self.language_manager.set_language(new_language)
                
                # Show final confirmation and close the application
                if self.language_manager.current_language == "english":
                    final_message = "Language preference saved. The application will now close.\nPlease restart it manually to apply the changes."
                else:
                    final_message = "语言偏好已保存。应用程序将立即关闭。\n请手动重新启动以应用更改。"
                
                messagebox.showinfo(
                    self.language_manager.get_text("language_selection"),
                    final_message
                )
                
                # Close the application gracefully
                self.root.quit()
            else:
                # Revert the radio button selection
                self.language_var.set(self.language_manager.current_language)
    

    
    def update_ui_text(self):
        """Update all UI elements with current language translations"""
        # Update status label
        self.status_var.set(self.language_manager.get_text("ready"))
        
        # Update all LabelFrame texts
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        self.update_label_frame_text(child)
        
        # Update all button texts
        self.update_button_texts()
        
        # Update all label texts
        self.update_label_texts()
        
        # Update Checkbutton text
        self.update_checkbutton_text()
        
        # Update output directory label
        if self.output_dir:
            self.output_dir_var.set(self.output_dir)
        else:
            self.output_dir_var.set(self.language_manager.get_text("default_output"))
    
    def update_label_texts(self):
        """Update all label texts"""
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)):
                self.update_labels_in_frame(widget)
    
    def update_labels_in_frame(self, frame):
        """Update label texts in a specific frame"""
        for child in frame.winfo_children():
            if isinstance(child, ttk.Label):
                current_text = child.cget("text")
                
                # Map all possible label texts to translation keys
                text_to_key = {
                    # Split settings labels
                    "Custom Chapter Regular Expression:": "custom_chapter_regex",
                    "自定义章节正则表达式:": "custom_chapter_regex",
                    "Default Split Size (characters):": "default_split_size",
                    "默认拆分字数:": "default_split_size",
                    
                    # File list label
                    "Files to Process:": "files_to_process",
                    "待处理文件:": "files_to_process",
                    
                    # Output directory label
                    "Default: Use source file directory": "default_output",
                    "默认: 使用源文件目录": "default_output",
                    
                    # Status label
                    "Ready": "ready",
                    "就绪": "ready"
                }
                
                # Find the matching translation key
                translation_key = None
                for text_pattern, key in text_to_key.items():
                    if current_text == text_pattern:
                        translation_key = key
                        break
                
                # If no exact match found, try partial matching
                if translation_key is None:
                    for text_pattern, key in text_to_key.items():
                        if text_pattern in current_text or current_text in text_pattern:
                            translation_key = key
                            break
                
                if translation_key:
                    new_text = self.language_manager.get_text(translation_key)
                    child.config(text=new_text)
            elif isinstance(child, (ttk.Frame, ttk.LabelFrame)):
                # Recursively update labels in nested frames
                self.update_labels_in_frame(child)
    
    def update_checkbutton_text(self):
        """Update Checkbutton text"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Checkbutton):
                                current_text = grandchild.cget("text")
                                
                                # Map current Checkbutton text to translation keys
                                text_to_key = {
                                    "Enable text cleaning (remove extra blank lines, standardize punctuation, etc.)": "enable_text_cleaning",
                                    "启用文本整理（去除多余空行、统一标点符号等）": "enable_text_cleaning"
                                }
                                
                                if current_text in text_to_key:
                                    new_text = self.language_manager.get_text(text_to_key[current_text])
                                    grandchild.config(text=new_text)
    
    def update_label_frame_text(self, label_frame):
        """Update LabelFrame text based on its current text"""
        current_text = label_frame.cget("text")
        
        # Map current text to translation keys
        text_to_key = {
            "Language Selection": "language_selection",
            "语言选择": "language_selection",
            "File Selection": "file_selection", 
            "文件选择": "file_selection",
            "Output Directory": "output_directory",
            "输出目录": "output_directory",
            "Files to Process": "files_to_process",
            "待处理文件": "files_to_process",
            "Split Settings": "split_settings",
            "拆分设置": "split_settings"
        }
        
        if current_text in text_to_key:
            new_text = self.language_manager.get_text(text_to_key[current_text])
            label_frame.config(text=new_text)
    
    def update_button_texts(self):
        """Update all button texts"""
        # Update buttons in the main frame
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)):
                self.update_buttons_in_frame(widget)
    
    def update_buttons_in_frame(self, frame):
        """Update button texts in a specific frame"""
        for child in frame.winfo_children():
            if isinstance(child, ttk.Button):
                current_text = child.cget("text")
                
                # Map all possible button texts to translation keys
                text_to_key = {
                    # File selection buttons
                    "Select Files": "select_files",
                    "选择文件": "select_files",
                    "Clear List": "clear_list", 
                    "清除列表": "clear_list",
                    
                    # Output directory buttons
                    "Select Directory": "select_directory",
                    "选择目录": "select_directory",
                    "Reset to Default": "reset_to_default",
                    "重置为默认": "reset_to_default",
                    
                    # Start processing button
                    "Start Processing": "start_processing",
                    "开始拆分": "start_processing"
                }
                
                # Find the matching translation key
                translation_key = None
                for text_pattern, key in text_to_key.items():
                    if current_text == text_pattern:
                        translation_key = key
                        break
                
                # If no exact match found, try partial matching
                if translation_key is None:
                    for text_pattern, key in text_to_key.items():
                        if text_pattern in current_text or current_text in text_pattern:
                            translation_key = key
                            break
                
                if translation_key:
                    new_text = self.language_manager.get_text(translation_key)
                    child.config(text=new_text)
            elif isinstance(child, (ttk.Frame, ttk.LabelFrame)):
                # Recursively update buttons in nested frames
                self.update_buttons_in_frame(child)
    
    def select_files(self):
        """Select files"""
        files = filedialog.askopenfilenames(
            title=self.language_manager.get_text("select_txt_files"),
            filetypes=[(self.language_manager.get_text("text_files"), "*.txt")]
        )
        
        if files:
            for file in files:
                if file not in self.files_to_process:
                    self.files_to_process.append(file)
                    self.file_listbox.insert(tk.END, file)
    
    def clear_files(self):
        """Clear file list"""
        self.files_to_process = []
        self.file_listbox.delete(0, tk.END)
        
    def select_output_dir(self):
        """Select output directory"""
        directory = filedialog.askdirectory(title=self.language_manager.get_text("select_output_dir"))
        if directory:
            self.output_dir = directory
            self.output_dir_var.set(directory)
    
    def reset_output_dir(self):
        """Reset to default output directory"""
        self.output_dir = None
        self.output_dir_var.set(self.language_manager.get_text("default_output"))
    
    def update_progress(self, current, total):
        """Update progress bar"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.status_var.set(f"{self.language_manager.get_text('processing')} {current}/{total}")
        self.root.update_idletasks()
    
    def start_processing(self):
        """Start processing files"""
        if not self.files_to_process:
            messagebox.showwarning(
                self.language_manager.get_text("warning"),
                self.language_manager.get_text("warning_no_files")
            )
            return
        
        if self.processing:
            messagebox.showwarning(
                self.language_manager.get_text("warning"),
                self.language_manager.get_text("warning_processing")
            )
            return
        
        # Update settings
        custom_pattern = self.custom_pattern_var.get().strip()
        if custom_pattern:
            self.splitter.custom_pattern = custom_pattern
        
        try:
            split_size = int(self.split_size_var.get())
            if split_size > 0:
                self.splitter.default_split_size = split_size
        except ValueError:
            messagebox.showwarning(
                self.language_manager.get_text("warning"),
                self.language_manager.get_text("warning_invalid_size")
            )
            return
        
        # Set output directory
        self.splitter.output_dir = self.output_dir
        
        # Get text cleaning option status
        enable_clean = self.clean_text_var.get()
        
        # If output directory is selected, ensure it exists
        if self.output_dir and not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except Exception as e:
                messagebox.showerror(
                    self.language_manager.get_text("error"),
                    self.language_manager.get_text("error_create_dir", str(e))
                )
                return
        
        # Start processing thread
        self.processing = True
        threading.Thread(target=self.process_files).start()
    
    def process_files(self):
        """Process all files"""
        total_files = len(self.files_to_process)
        processed_files = 0
        result_files_count = 0
        
        try:
            for file_path in self.files_to_process:
                # Update status
                self.status_var.set(self.language_manager.get_text("processing_file", os.path.basename(file_path)))
                self.root.update_idletasks()
                
                # Split file
                result_files = self.splitter.split_file(file_path, enable_clean=self.clean_text_var.get())
                result_files_count += len(result_files)
                
                # Update progress
                processed_files += 1
                self.update_progress(processed_files, total_files)
            
            # Processing complete
            output_location = self.output_dir if self.output_dir else self.language_manager.get_text("default_output")
            self.status_var.set(self.language_manager.get_text("complete", processed_files, result_files_count, output_location))
            messagebox.showinfo(
                self.language_manager.get_text("success"),
                self.language_manager.get_text("success_complete", processed_files, result_files_count, output_location)
            )
        
        except Exception as e:
            messagebox.showerror(self.language_manager.get_text("error"), str(e))
            self.status_var.set(self.language_manager.get_text("error"))
        
        finally:
            self.processing = False


if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    app = TxtSplitterApp(root)
    root.mainloop()