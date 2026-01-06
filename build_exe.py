#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT文档拆分器 - 打包脚本
用于将Python程序打包成Windows可执行文件(.exe)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ PyInstaller安装失败")
        return False

def create_spec_file():
    """创建PyInstaller spec文件"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.datastruct import TOC
from PyInstaller.building.osx import BUNDLE

block_cipher = None

# 主程序分析
a = Analysis(
    ['txt_splitter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 添加必要的隐藏导入
hiddenimports = ['chardet', 'tkinter', 'tkinter.filedialog', 'tkinter.ttk', 'tkinter.messagebox']
for imp in hiddenimports:
    try:
        __import__(imp)
        a.hiddenimports.append(imp)
    except ImportError:
        pass

# 添加Tcl/Tk数据文件
import tkinter
import os
tk_root = tkinter.Tk()
tk_root.withdraw()

# 获取Tcl/Tk库路径
tcl_library = tk_root.tk.exprstring('$tcl_library')
tk_library = tk_root.tk.exprstring('$tk_library')

# 添加Tcl/Tk数据文件到打包中
if os.path.exists(tcl_library):
    a.datas.append((tcl_library, "_tcl_data"))
if os.path.exists(tk_library):
    a.datas.append((tk_library, "_tk_data"))

tk_root.destroy()

# 创建PYZ文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TXT文档拆分器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # 如果有图标文件的话
)
"""
    
    with open('txt_splitter.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✓ Spec文件创建成功")

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    # 使用PyInstaller直接构建，添加更多选项确保Tkinter正常工作
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=TXT文档拆分器",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 窗口程序（不显示控制台）
        "--add-data=preferences.json;.",  # 包含配置文件
        "--add-data=C:/Users/tonyt/miniconda3/Library/lib/tcl8.6;tcl8.6",
        "--add-data=C:/Users/tonyt/miniconda3/Library/lib/tk8.6;tk8.6",
        "--collect-all", "tkinter",
        "--collect-all", "_tkinter",
        "--hidden-import=chardet",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "txt_splitter.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✓ 可执行文件构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 可执行文件构建失败: {e}")
        return False

def cleanup():
    """清理临时文件"""
    print("正在清理临时文件...")
    
    # 删除构建目录
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # 删除spec文件
    if os.path.exists('txt_splitter.spec'):
        os.remove('txt_splitter.spec')
    
    print("✓ 临时文件清理完成")

def create_distribution_folder():
    """创建发布文件夹"""
    print("正在创建发布文件夹...")
    
    dist_dir = Path("dist")
    release_dir = Path("TXT文档拆分器_发布版")
    
    # 创建发布文件夹
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制可执行文件
    exe_file = dist_dir / "TXT文档拆分器.exe"
    if exe_file.exists():
        shutil.copy2(exe_file, release_dir / "TXT文档拆分器.exe")
    
    # 复制必要的文件
    files_to_copy = ["README.md", "README_EN.md"]
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, release_dir / file)
    
    # 创建使用说明
    create_usage_guide(release_dir)
    
    print(f"✓ 发布文件夹创建完成: {release_dir}")

def create_usage_guide(release_dir):
    """创建使用说明文件"""
    guide_content = """TXT文档拆分器 - 使用说明
============================

## 软件介绍
这是一款专业的TXT文档拆分软件，专为AI书籍处理和本地知识库创建而设计。

## 系统要求
- Windows 7/8/10/11 (64位)
- 无需安装Python

## 使用方法
1. 双击运行 "TXT文档拆分器.exe"
2. 在界面中点击"选择文件"按钮，选择需要拆分的TXT文件
3. 可选择输出目录（可选，默认使用源文件目录）
4. 点击"开始拆分"按钮开始处理

## 功能特点
- 智能章节识别（支持中英文）
- 按章节或按大小拆分
- 多编码支持
- 批量处理多个文件
- 用户友好界面

## 注意事项
- 软件会创建preferences.json文件保存用户设置
- 处理大文件时请耐心等待
- 如有问题，请查看README.md文件获取详细信息
"""
    
    with open(release_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)

def main():
    """主函数"""
    print("TXT文档拆分器 - 打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("txt_splitter.py"):
        print("错误：请在包含txt_splitter.py的目录中运行此脚本")
        return
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return
    
    # 构建可执行文件
    if not build_executable():
        return
    
    # 创建发布文件夹
    create_distribution_folder()
    
    # 清理临时文件
    cleanup()
    
    print("\n" + "=" * 50)
    print("✓ 打包完成！")
    print("可执行文件位置: dist/TXT文档拆分器.exe")
    print("发布文件夹: TXT文档拆分器_发布版")
    print("=" * 50)

if __name__ == "__main__":
    main()