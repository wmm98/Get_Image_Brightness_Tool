# Get_Image_Brightness_Tool

# 显示窗口
nuitka --standalone --onefile --include-package=Common --include-package=Image  --include-data-dir=./ReportTemplate=ReportTemplate --include-module=image_brightness_init --include-module=run --include-data-files=ui_config.yaml=ui_config.yaml --include-package=PyQt5 --output-dir=dist --enable-plugin=pyqt5 --enable-plugin=upx image_brightness_run.py

# (不显示窗口)
nuitka --standalone --onefile --windows-console-mode=disable --include-package=Common --include-package=Image  --include-data-dir=./ReportTemplate=ReportTemplate --include-module=image_brightness_init --include-module=run --include-data-files=ui_config.yaml=ui_config.yaml --include-package=PyQt5 --output-dir=dist --enable-plugin=pyqt5 --enable-plugin=upx image_brightness_run.py