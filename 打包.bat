@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   TXT文档拆分器 - 打包工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未检测到Python，请先安装Python
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在安装必要的依赖包...
pip install chardet
if errorlevel 1 (
    echo 错误：chardet安装失败
    pause
    exit /b 1
)

echo 正在安装PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo 错误：PyInstaller安装失败
    pause
    exit /b 1
)

echo.
echo 正在构建可执行文件...

REM 使用PyInstaller打包
pyinstaller --onefile --windowed --name "TXT文档拆分器" ^
    --add-data "preferences.json;." ^
    --hidden-import chardet ^
    --hidden-import tkinter ^
    --hidden-import tkinter.filedialog ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    txt_splitter.py

if errorlevel 1 (
    echo.
    echo 错误：打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 可执行文件位置：dist\TXT文档拆分器.exe
echo.
echo 按任意键退出...
pause >nul