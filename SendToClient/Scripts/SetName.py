try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

import SetName_ui

class SetName(QDialog, SetName_ui.Ui_setMediaNameDlg):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)