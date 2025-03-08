# Get_Image_Brightness_Tool

# 打包指令
nuitka --standalone --onefile --windows-console-mode=disable --include-package=Common --include-package=Image  --include-data-dir=./ReportTemplate=ReportTemplate --include-module=image_brightness_init --include-package=PyQt5 --output-dir=dist --enable-plugin=pyqt5 --enable-plugin=upx image_brightness_run.py

nuitka --standalone --onefile --include-package=Common --include-package=Image  --include-data-dir=./ReportTemplate=ReportTemplate --include-module=image_brightness_init --include-package=PyQt5 --output-dir=dist --enable-plugin=pyqt5 --enable-plugin=upx image_brightness_run.py
