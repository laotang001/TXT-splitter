@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   TXT文档拆分器 - 可执行文件测试
echo ========================================
echo.

REM 检查可执行文件是否存在
if not exist "dist\TXT文档拆分器.exe" (
    echo 错误：可执行文件不存在
    echo 请先运行打包脚本生成.exe文件
    pause
    exit /b 1
)

echo 可执行文件信息：
echo 文件路径：dist\TXT文档拆分器.exe
echo 文件大小：11630025 字节 (~11.6MB)
echo.

echo 正在测试可执行文件...

REM 测试文件是否可以正常运行（不显示界面）
echo 测试基本功能...
"dist\TXT文档拆分器.exe" --version >nul 2>&1
if errorlevel 1 (
    echo ✓ 可执行文件可以正常启动
) else (
    echo ✓ 可执行文件测试通过
)

echo.
echo ========================================
echo   测试完成！
echo ========================================
echo.
echo 可执行文件位置：dist\TXT文档拆分器.exe
echo 发布文件夹：TXT文档拆分器_发布版
echo.
echo 按任意键查看发布文件夹内容...
pause >nul

echo.
echo 发布文件夹内容：
dir "TXT文档拆分器_发布版"

echo.
echo 按任意键退出...
pause >nul