@echo off
chcp 65001 >nul
echo ========================================
echo   SeqDiff Visualizer 打包工具
echo ========================================
echo.

echo [1/3] 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [2/3] 开始打包（约2-5分钟）...
C:\Users\Dell\AppData\Local\Programs\Python\Python312\python.exe -m PyInstaller build.spec --clean --noconfirm

echo.
echo [3/3] 复制 MAFFT 到发布目录...
if exist dist\SeqDiff (
    xcopy /E /I /Y mafft-win dist\SeqDiff\mafft-win
    echo.
    echo ========================================
    echo   打包完成！
    echo   发布目录: dist\SeqDiff\
    echo   运行: dist\SeqDiff\SeqDiff.exe
    echo ========================================
) else (
    echo 打包失败，请检查错误信息
)

echo.
pause
