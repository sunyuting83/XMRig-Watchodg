# -*- coding: utf-8 -*-
import sys
import os
from public import DEV

if __name__ == "__main__":
    program_name = os.path.basename(sys.argv[0])
    if DEV:
        program_name = "python.exe"
    filePath = os.path.abspath(sys.argv[0])
    programPath = os.path.dirname(filePath)
    from Utils.utils import checkFirst, CheckConfigFile
    yamlpath = os.path.join(programPath, "config.yaml")
    yamlData = CheckConfigFile(yamlpath)
    from Utils.icon import CheckOrMakeIcon
    CheckOrMakeIcon(programPath)
    if checkFirst(program_name, DEV):
        from PyQt5.QtWidgets import QApplication
        from UI.controller import MainController
        app = QApplication(sys.argv)
        main = MainController(programPath, program_name, yamlData)
        sys.exit(app.exec_())
    else:
        sys.exit(0)