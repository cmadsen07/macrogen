# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layout.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 604)
        MainWindow.setStyleSheet(u"")
        self.actionSave_File = QAction(MainWindow)
        self.actionSave_File.setObjectName(u"actionSave_File")
        self.actionLoad_File = QAction(MainWindow)
        self.actionLoad_File.setObjectName(u"actionLoad_File")
        self.actionSave_AHK = QAction(MainWindow)
        self.actionSave_AHK.setObjectName(u"actionSave_AHK")
        self.actionChange_editors = QAction(MainWindow)
        self.actionChange_editors.setObjectName(u"actionChange_editors")
        self.actionSave_JSON = QAction(MainWindow)
        self.actionSave_JSON.setObjectName(u"actionSave_JSON")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_3.addWidget(self.listWidget)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.editorText = QPlainTextEdit(self.centralwidget)
        self.editorText.setObjectName(u"editorText")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editorText.sizePolicy().hasHeightForWidth())
        self.editorText.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.editorText)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelName = QLabel(self.centralwidget)
        self.labelName.setObjectName(u"labelName")

        self.horizontalLayout_6.addWidget(self.labelName)

        self.lineEditName = QLineEdit(self.centralwidget)
        self.lineEditName.setObjectName(u"lineEditName")

        self.horizontalLayout_6.addWidget(self.lineEditName)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelTrigger = QLabel(self.centralwidget)
        self.labelTrigger.setObjectName(u"labelTrigger")

        self.horizontalLayout_4.addWidget(self.labelTrigger)

        self.dropdownTrigger = QComboBox(self.centralwidget)
        self.dropdownTrigger.addItem("")
        self.dropdownTrigger.addItem("")
        self.dropdownTrigger.addItem("")
        self.dropdownTrigger.setObjectName(u"dropdownTrigger")

        self.horizontalLayout_4.addWidget(self.dropdownTrigger)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelHotstring = QLabel(self.centralwidget)
        self.labelHotstring.setObjectName(u"labelHotstring")

        self.horizontalLayout_3.addWidget(self.labelHotstring)

        self.lineEditHotstring = QLineEdit(self.centralwidget)
        self.lineEditHotstring.setObjectName(u"lineEditHotstring")

        self.horizontalLayout_3.addWidget(self.lineEditHotstring)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_2.addWidget(self.textEdit)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonMacro = QPushButton(self.centralwidget)
        self.pushButtonMacro.setObjectName(u"pushButtonMacro")

        self.horizontalLayout_2.addWidget(self.pushButtonMacro)

        self.removeButton = QPushButton(self.centralwidget)
        self.removeButton.setObjectName(u"removeButton")

        self.horizontalLayout_2.addWidget(self.removeButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSave_File)
        self.menuFile.addAction(self.actionLoad_File)
        self.menuFile.addAction(self.actionSave_AHK)
        self.menuFile.addAction(self.actionSave_JSON)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LaTeX Macro generator for AHK", None))
        self.actionSave_File.setText(QCoreApplication.translate("MainWindow", u"Save Files", None))
#if QT_CONFIG(shortcut)
        self.actionSave_File.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoad_File.setText(QCoreApplication.translate("MainWindow", u"Open File", None))
#if QT_CONFIG(shortcut)
        self.actionLoad_File.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_AHK.setText(QCoreApplication.translate("MainWindow", u"Export AHK as", None))
#if QT_CONFIG(shortcut)
        self.actionSave_AHK.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionChange_editors.setText(QCoreApplication.translate("MainWindow", u"Change editors", None))
        self.actionSave_JSON.setText(QCoreApplication.translate("MainWindow", u"Save JSON as", None))
#if QT_CONFIG(shortcut)
        self.actionSave_JSON.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Macros", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Editors (One per line)", None))
        self.labelName.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.labelTrigger.setText(QCoreApplication.translate("MainWindow", u"Trigger key", None))
        self.dropdownTrigger.setItemText(0, QCoreApplication.translate("MainWindow", u"Tab", None))
        self.dropdownTrigger.setItemText(1, QCoreApplication.translate("MainWindow", u"Space", None))
        self.dropdownTrigger.setItemText(2, QCoreApplication.translate("MainWindow", u"No trigger", None))

        self.labelHotstring.setText(QCoreApplication.translate("MainWindow", u"Hotstring", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Macro text", None))
        self.pushButtonMacro.setText(QCoreApplication.translate("MainWindow", u"Add macro", None))
        self.removeButton.setText(QCoreApplication.translate("MainWindow", u"Remove macro", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

