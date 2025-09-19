import os
import re
import chardet
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import threading

class TxtSplitter:
    def __init__(self):
        # 默认章节识别模式
        self.chapter_patterns = [
            r'^第[0-9一二三四五六七八九十百千]+[章回节]',  # 第X章、第X回、第X节
            r'^第[0-9一二三四五六七八九十百千]+[卷]',      # 第X卷
            r'^[0-9一二三四五六七八九十百千]+[、.]',       # X、或X.
            r'^[第]?[0-9]+[章节回]',                     # 第1章、1章
            r'^[第]?[0-9]+',                           # 第1、1
            r'.*（[一二三四五六七八九十]+）',              # XXX（一）
            r'.*\([一二三四五六七八九十]+\)'              # XXX(一)
        ]
        self.custom_pattern = None
        self.default_split_size = 8000  # 默认按8000字符拆分
        self.encoding = None
        self.output_dir = None  # 输出目录，默认为None表示使用源文件目录
        
    def detect_encoding(self, file_path):
        """检测文件编码"""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']
    
    def read_file(self, file_path):
        """读取文件内容"""
        try:
            # 检测编码
            self.encoding = self.detect_encoding(file_path)
            if not self.encoding:
                self.encoding = 'utf-8'  # 默认使用UTF-8
            
            # 使用二进制模式读取，避免编码问题
            with open(file_path, 'rb') as f:
                content_bytes = f.read()
                
            # 尝试解码
            try:
                content = content_bytes.decode(self.encoding, errors='replace')
            except UnicodeDecodeError:
                # 如果解码失败，尝试其他常见编码
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
    
    def find_chapters(self, content):
        """识别章节"""
        lines = content.split('\n')
        chapters = []
        
        # 合并所有模式
        patterns = self.chapter_patterns.copy()
        if self.custom_pattern:
            patterns.append(self.custom_pattern)
        
        # 查找所有章节
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
        """按章节拆分"""
        chapters, lines = self.find_chapters(content)
        
        # 如果没有找到章节，则按字数拆分
        if not chapters:
            return self.split_by_size(content, file_path)
        
        # 按章节拆分
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # 使用指定的输出目录或源文件目录
        output_dir = self.output_dir if self.output_dir else os.path.dirname(file_path)
        
        result_files = []
        for i in range(len(chapters)):
            start_idx = chapters[i][0]
            # 如果是最后一章，结束索引为文件末尾
            if i == len(chapters) - 1:
                end_idx = len(lines)
            else:
                end_idx = chapters[i+1][0]
            
            # 提取章节内容
            chapter_content = '\n'.join(lines[start_idx:end_idx])
            chapter_title = lines[start_idx].strip()
            
            # 检查章节内容长度是否超过1万字
            if len(chapter_content) > 10000:
                # 计算需要拆分的部分数量
                parts_count = (len(chapter_content) + 9999) // 10000  # 向上取整
                
                # 按照大约相等的长度拆分章节
                part_size = len(chapter_content) // parts_count
                
                for part_idx in range(parts_count):
                    start_pos = part_idx * part_size
                    end_pos = min((part_idx + 1) * part_size, len(chapter_content))
                    part_content = chapter_content[start_pos:end_pos]
                    
                    # 使用章节名+数字作为文件名
                    safe_title = re.sub(r'[\\/*?:"<>|]', '_', chapter_title)  # 移除不允许的文件名字符
                    output_file = os.path.join(output_dir, f"{safe_title}_{part_idx+1}.txt")
                    
                    with open(output_file, 'wb') as f:
                        f.write(part_content.encode(self.encoding, errors='replace'))
                    
                    result_files.append(output_file)
            else:
                # 章节内容不超过1万字，直接保存
                # 使用章节名作为文件名
                safe_title = re.sub(r'[\\/*?:"<>|]', '_', chapter_title)  # 移除不允许的文件名字符
                output_file = os.path.join(output_dir, f"{safe_title}.txt")
                
                with open(output_file, 'wb') as f:
                    f.write(chapter_content.encode(self.encoding, errors='replace'))
                
                result_files.append(output_file)
        
        return result_files
    
    def split_by_size(self, content, file_path):
        """按字数拆分"""
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # 使用指定的输出目录或源文件目录
        output_dir = self.output_dir if self.output_dir else os.path.dirname(file_path)
        
        # 计算需要拆分的文件数
        total_chars = len(content)
        num_files = max(1, (total_chars + self.default_split_size - 1) // self.default_split_size)
        
        result_files = []
        for i in range(num_files):
            start_idx = i * self.default_split_size
            end_idx = min((i + 1) * self.default_split_size, total_chars)
            
            # 提取内容
            part_content = content[start_idx:end_idx]
            
            # 保存文件
            output_file = os.path.join(output_dir, f"{base_name}_{i+1}.txt")
            with open(output_file, 'wb') as f:
                f.write(part_content.encode(self.encoding, errors='replace'))
            
            result_files.append(output_file)
        
        return result_files
    
    def split_file(self, file_path, progress_callback=None):
        """拆分文件"""
        try:
            # 读取文件
            content = self.read_file(file_path)
            
            # 按章节拆分
            result_files = self.split_by_chapters(content, file_path)
            
            return result_files
        except Exception as e:
            raise Exception(f"拆分文件失败: {str(e)}")


class TxtSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TXT文档拆分工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.splitter = TxtSplitter()
        self.files_to_process = []
        self.processing = False
        self.output_dir = None  # 输出目录
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="选择文件", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="清除列表", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # 输出目录选择
        output_frame = ttk.LabelFrame(main_frame, text="输出目录", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_dir_var = tk.StringVar(value="默认使用源文件目录")
        ttk.Label(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="选择目录", command=self.select_output_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text="重置为默认", command=self.reset_output_dir).pack(side=tk.LEFT, padx=5)
        
        # 文件列表
        list_frame = ttk.LabelFrame(main_frame, text="待处理文件", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建列表框
        self.file_listbox = tk.Listbox(list_frame)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        # 章节识别设置
        settings_frame = ttk.LabelFrame(main_frame, text="拆分设置", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # 自定义章节正则表达式
        ttk.Label(settings_frame, text="自定义章节正则表达式:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.custom_pattern_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.custom_pattern_var).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # 默认拆分字数
        ttk.Label(settings_frame, text="默认拆分字数:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.split_size_var = tk.StringVar(value="8000")
        ttk.Entry(settings_frame, textvariable=self.split_size_var).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(main_frame, textvariable=self.status_var).pack(anchor=tk.W, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="开始拆分", command=self.start_processing).pack(side=tk.RIGHT, padx=5)
    
    def select_files(self):
        """选择文件"""
        files = filedialog.askopenfilenames(
            title="选择TXT文件",
            filetypes=[("文本文件", "*.txt")]
        )
        
        if files:
            for file in files:
                if file not in self.files_to_process:
                    self.files_to_process.append(file)
                    self.file_listbox.insert(tk.END, file)
    
    def clear_files(self):
        """清除文件列表"""
        self.files_to_process = []
        self.file_listbox.delete(0, tk.END)
        
    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir = directory
            self.output_dir_var.set(directory)
    
    def reset_output_dir(self):
        """重置为默认输出目录"""
        self.output_dir = None
        self.output_dir_var.set("默认使用源文件目录")
    
    def update_progress(self, current, total):
        """更新进度条"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.status_var.set(f"处理中... {current}/{total}")
        self.root.update_idletasks()
    
    def start_processing(self):
        """开始处理文件"""
        if not self.files_to_process:
            messagebox.showwarning("警告", "请先选择要处理的文件！")
            return
        
        if self.processing:
            messagebox.showwarning("警告", "正在处理文件，请稍候！")
            return
        
        # 更新设置
        custom_pattern = self.custom_pattern_var.get().strip()
        if custom_pattern:
            self.splitter.custom_pattern = custom_pattern
        
        try:
            split_size = int(self.split_size_var.get())
            if split_size > 0:
                self.splitter.default_split_size = split_size
        except ValueError:
            messagebox.showwarning("警告", "默认拆分字数必须是正整数！")
            return
        
        # 设置输出目录
        self.splitter.output_dir = self.output_dir
        
        # 如果选择了输出目录，确保目录存在
        if self.output_dir and not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"创建输出目录失败: {str(e)}")
                return
        
        # 启动处理线程
        self.processing = True
        threading.Thread(target=self.process_files).start()
    
    def process_files(self):
        """处理所有文件"""
        total_files = len(self.files_to_process)
        processed_files = 0
        result_files_count = 0
        
        try:
            for file_path in self.files_to_process:
                # 更新状态
                self.status_var.set(f"正在处理: {os.path.basename(file_path)}")
                self.root.update_idletasks()
                
                # 拆分文件
                result_files = self.splitter.split_file(file_path)
                result_files_count += len(result_files)
                
                # 更新进度
                processed_files += 1
                self.update_progress(processed_files, total_files)
            
            # 处理完成
            output_location = self.output_dir if self.output_dir else "源文件所在目录"
            self.status_var.set(f"处理完成！共处理 {processed_files} 个文件，生成 {result_files_count} 个拆分文件，保存在: {output_location}")
            messagebox.showinfo("完成", f"所有文件处理完成！\n\n共处理 {processed_files} 个文件\n生成 {result_files_count} 个拆分文件\n保存在: {output_location}")
        
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status_var.set("处理出错！")
        
        finally:
            self.processing = False


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    app = TxtSplitterApp(root)
    root.mainloop()