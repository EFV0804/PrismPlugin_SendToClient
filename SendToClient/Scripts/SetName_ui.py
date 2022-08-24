# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetMediaName.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_setMediaNameDlg(object):
    def setupUi(self, setMediaNameDlg):
        if not setMediaNameDlg.objectName():
            setMediaNameDlg.setObjectName(u"setMediaNameDlg")
        setMediaNameDlg.resize(384, 181)
        self.verticalLayout_2 = QVBoxLayout(setMediaNameDlg)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.l_mediaName = QLabel(setMediaNameDlg)
        self.l_mediaName.setObjectName(u"l_mediaName")

        self.horizontalLayout_2.addWidget(self.l_mediaName)

        self.e_mediaName = QLineEdit(setMediaNameDlg)
        self.e_mediaName.setObjectName(u"e_mediaName")

        self.horizontalLayout_2.addWidget(self.e_mediaName)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l_mediaFolder = QLabel(setMediaNameDlg)
        self.l_mediaFolder.setObjectName(u"l_mediaFolder")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_mediaFolder.sizePolicy().hasHeightForWidth())
        self.l_mediaFolder.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.l_mediaFolder)

        self.c_mediaFolders = QComboBox(setMediaNameDlg)
        self.c_mediaFolders.setObjectName(u"c_mediaFolders")

        self.horizontalLayout_3.addWidget(self.c_mediaFolders)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.b_explorer = QPushButton(setMediaNameDlg)
        self.b_explorer.setObjectName(u"b_explorer")

        self.horizontalLayout.addWidget(self.b_explorer)

        self.buttonBox = QDialogButtonBox(setMediaNameDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        
        self.retranslateUi(setMediaNameDlg)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), setMediaNameDlg.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), setMediaNameDlg.reject)
        QMetaObject.connectSlotsByName(setMediaNameDlg)
        
    # setupUi

    def retranslateUi(self, setMediaNameDlg):
        setMediaNameDlg.setWindowTitle(QCoreApplication.translate("setMediaNameDlg", u"Dialog", None))
        self.l_mediaName.setText(QCoreApplication.translate("setMediaNameDlg", u"Media Name", None))
        self.l_mediaFolder.setText(QCoreApplication.translate("setMediaNameDlg", u"Media Folder", None))
        self.b_explorer.setText(QCoreApplication.translate("setMediaNameDlg", u"Open in Explorer", None))
    # retranslateUi

