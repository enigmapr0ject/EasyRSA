"""
Main Driver Code for EasyRSA
"""

# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////
# Made by Bartosz Rzepka (DevPanada), Leighton Brooks (enigmapr0ject)
# 21477187 / 21472005
# Theme by Zeno Rocha: https://zenorocha.com/
# noinspection PyUnresolvedReferences
import json
# noinspection PyUnresolvedReferences
import os
# noinspection PyUnresolvedReferences
import platform
# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
import webbrowser
# noinspection PyUnresolvedReferences
import pyperclip
# noinspection PyUnresolvedReferences
import rsa
# noinspection PyUnresolvedReferences
from PySide6 import QtGui, QtWidgets, QtCore
# noinspection PyUnresolvedReferences
from PySide6.QtWidgets import QMainWindow
# noinspection PyUnresolvedReferences
from modules import *

# warnings.filterwarnings('ignore')
# os.environ['QT_DEBUG_PLUGINS'] = "1"
os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%
title = "EasyRSA"
description = "RSA made simple."


class MainWindow(QMainWindow):
    """
    Dashboard
    """

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        widgets = self.ui
        self.rt: RepeatedTimer | None = None
        self.model: QtWidgets.QFileSystemModel | None = None
        self.dragPos = None
        Settings.ENABLE_CUSTOM_TITLE_BAR = titleBarFlag
        # APPLY TEXTS
        self.setWindowTitle(title)
        # widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_filespace.clicked.connect(self.buttonClick)
        widgets.btn_passwords.clicked.connect(self.buttonClick)
        widgets.btn_account.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)
        widgets.closeAppBtn.clicked.connect(self.buttonClick)
        widgets.extraLabel.setText("Bartosz/Leighton")

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            """
            Open/Close Extra Left Box
            :return:
            """
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            """
            Open/Close Extra Right Box
            :return:
            """
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)
        widgets.btn_logout.clicked.connect(self.buttonClick)
        widgets.btn_help.clicked.connect(self.buttonClick)
        widgets.btn_report.clicked.connect(self.buttonClick)
        widgets.btn_credits.clicked.connect(self.buttonClick)
        # SHOW APP
        self.show()
        widgets.btn_more.clicked.connect(self.buttonClick)

        """
        themeFile = "themes\\Hookmark.qss"

        # SET THEME AND HACKS
        UIFunctions.theme(self, themeFile, True)
        AppFunctions.setThemeHack(self)
        """
        # Search for config file
        stem = os.getcwd()
        stem += "\\config\\config.json"
        if not os.path.exists(stem):
            # Create JSON object
            data = {"defaultSDLocation": os.getcwd()}
            with open(stem, "w") as f:
                json.dump(data, f)
                f.close()
        else:
            with open(stem, "r") as f:
                self.configArray = json.load(f)
                f.close()

        # SET HOME PAGE AND SELECT MENU
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        # Home Screen
        self.ui.credits.hide()

        # Main Page functionality

        # Generate Key Pair
        (self.publicKey, self.privateKey) = rsa.newkeys(512)
        self.ui.publicKeyDisplay.setPlainText(str(self.publicKey))
        self.ui.privateKeyDisplay.setPlainText("PrivateKey(***********)")

        # Private Key Checkbox Tick
        self.ui.privateKeyCheckbox.stateChanged.connect(self.privateKeyCheckboxTick)

        # Copy Private Key
        self.ui.copyPrivateKeyButton.clicked.connect(self.buttonClick)

        # Filespace Page functionality

        # Multiview Checkbox Tick
        self.ui.multiviewCheckbox.stateChanged.connect(self.buttonClick)
        self.ui.openDirectory.clicked.connect(self.buttonClick)
        self.ui.defaultLocation.clicked.connect(self.buttonClick)
        self.ui.goToDefault.clicked.connect(self.buttonClick)


        # Multiview disabled by default
        self.ui.defaultLocation.hide()
        self.ui.driveInfo.hide()
        self.ui.driveInfoTitle.hide()
        self.ui.fileBrowserTree.hide()
        self.ui.goToDefault.hide()
        self.ui.openDirectory.hide()
        self.ui.parentDrive.hide()
        self.ui.parentDriveSpace.hide()
        self.ui.parentDriveTitle.hide()
        self.ui.filepathBox.show()
        self.ui.openFilepathButton.show()

    # BUTTON CLICK
    def buttonClick(self):
        """
        Button Click event handler
        :return:
        """
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        match btnName:
            # SHOW NEW PAGE
            case "closeAppBtn":
                try:
                    self.rt.stop()
                    self.close()
                    sys.exit(0)
                except AttributeError:
                    self.close()
                    sys.exit(0)
                except Exception as e:
                    print(repr(e))
            case "btn_home":
                self.ui.titleLeftDescription.setText("Dashboard")  # SET PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)  # RESET ANOTHERS BUTTONS SELECTED
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            case "btn_filespace":
                self.ui.titleLeftDescription.setText("Filespace")
                self.ui.stackedWidget.setCurrentWidget(self.ui.filespace)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            case "btn_passwords":
                self.ui.titleLeftDescription.setText("Page 3")
                self.ui.stackedWidget.setCurrentWidget(self.ui.page3)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            case "btn_account":
                self.ui.titleLeftDescription.setText("Page 4")
                self.ui.stackedWidget.setCurrentWidget(self.ui.page4)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            case "btn_exit":
                self.close()
            case "btn_logout":
                self.close()
            case "btn_credits":
                # Check if the credits are already showing
                if self.ui.credits.isHidden():
                    self.ui.credits.show()
                else:
                    self.ui.credits.hide()
            case "btn_help":
                webbrowser.get().open("https://github.com/enigmapr0ject/EasyRSA")
            case "btn_report":
                webbrowser.get().open("https://github.com/enigmapr0ject/EasyRSA/issues")
            case "btn_more":
                webbrowser.get().open("https://github.com/enigmapr0ject")
            case "copyPrivateKeyButton":
                pyperclip.copy(self.ui.privateKeyDisplay.toPlainText())
            case "multiviewCheckbox":
                if self.ui.multiviewCheckbox.isChecked():
                    self.ui.filepathBox.hide()
                    self.ui.openFilepathButton.hide()
                    self.ui.defaultLocation.show()
                    self.ui.driveInfo.show()
                    self.ui.driveInfoTitle.show()
                    self.ui.fileBrowserTree.show()
                    self.ui.goToDefault.show()
                    self.ui.openDirectory.show()
                    self.ui.parentDrive.show()
                    self.ui.parentDriveSpace.show()
                    self.ui.parentDriveTitle.show()
                    self.model = QFileSystemModel()
                    self.model.setRootPath(os.getcwd())
                    self.ui.fileBrowserTree.setModel(self.model)  # Set the model
                    try:
                        self.ui.fileBrowserTree.setRootIndex(
                            self.model.index(self.configArray['defaultSDLocation']) if self.configArray[
                                                                                           'defaultSDLocation'] != "" else
                            self.model.index(
                                os.getcwd()))  # Set the first displaying directory
                    # If directory in defaultSDLocation doesn't exist on the current machine, use current directory
                    except FileNotFoundError:
                        self.ui.fileBrowserTree.setRootIndex(self.model.index(os.getcwd()))
                        self.model.index(os.getcwd())
                    self.ui.fileBrowserTree.setAlternatingRowColors(False)  # Set the alternating row colors
                    self.ui.fileBrowserTree.setSortingEnabled(True)  # Set the sorting
                    self.ui.fileBrowserTree.setColumnWidth(0, 200)
                    self.ui.fileBrowserTree.setColumnWidth(1, 150)
                    self.ui.fileBrowserTree.setColumnWidth(2, 200)
                    self.ui.fileBrowserTree.setColumnWidth(3, 200)
                    # Set the context menu
                    self.ui.fileBrowserTree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
                    # (right clicking)
                    self.ui.fileBrowserTree.customContextMenuRequested.connect(self.contextMenu)  # Custom right click
                    # menu
                    # self.ui.fileBrowserTree.doubleClicked.connect() # Double-clicking on a file has a special effect
                    drivestats = DriveStatistics()
                    self.ui.parentDrive.setText("Parent Drive: %s" % drivestats.parentDrive)
                    self.ui.parentDriveSpace.setValue(drivestats.parentDriveSpace)
                    self.ui.driveInfo.setText(drivestats.driveInformation)
                    self.rt = RepeatedTimer(5, self.driveStatistics)
                    self.rt.start()
                else:
                    self.rt.stop()
                    self.ui.defaultLocation.hide()
                    self.ui.driveInfo.hide()
                    self.ui.driveInfoTitle.hide()
                    self.ui.fileBrowserTree.hide()
                    self.ui.goToDefault.hide()
                    self.ui.openDirectory.hide()
                    self.ui.parentDrive.hide()
                    self.ui.parentDriveSpace.hide()
                    self.ui.parentDriveTitle.hide()
                    self.ui.filepathBox.show()
                    self.ui.openFilepathButton.show()

    # Multiview drive statistics
    def driveStatistics(self):
        """
        Drive statistics for multiview, in realtime
        """
        drivestats = DriveStatistics()
        self.ui.parentDrive.setText("Parent Drive: %s" % drivestats.parentDrive)
        self.ui.parentDriveSpace.setValue(drivestats.parentDriveSpace)
        self.ui.driveInfo.setText(drivestats.driveInformation)

    # Private Key Checkbox Tick
    def privateKeyCheckboxTick(self):
        """
        Private Key Checkbox Tick event
        :return:
        """
        if self.ui.privateKeyCheckbox.isChecked():
            self.ui.privateKeyDisplay.setPlainText(str(self.privateKey))
        else:
            self.ui.privateKeyDisplay.setPlainText("PrivateKey(***********)")

    # Custom Context Menu
    def contextMenu(self):
        """
        Custom Context Menu
        :return:
        """
        menu = QtWidgets.QMenu()
        menu.setStyleSheet(
            "QMenu {background-color: rgb(33, 37, 43); font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249);}"
            "QMenu::item:selected {color: rgb(255, 255, 255); background-color: rgb(254, 120, 198); border-style: "
            "solid; border-radius: 4px;} "
            "QMenu::item {color: rgb(254, 120, 198); background-color: rgb(40, 44, 52; border-style: solid; "
            "border-radius: 4px;}")
        encrypt = menu.addAction("Encrypt File")
        decrypt = menu.addAction("Decrypt File")
        rename = menu.addAction("Rename File")
        move = menu.addAction("Move File")
        delete = menu.addAction("Delete File")
        """
        encrypt.triggered.connect(self.encryptFile)
        decrypt.triggered.connect(self.decryptFile)
        rename.triggered.connect(self.renameFile)
        delete.triggered.connect(self.deleteFile)
        """
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    # RESIZE EVENTS
    def resizeEvent(self, event):
        """
        Resize event
        :param event:
        :return:
        """
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        """
        Mouse press event
        :param event:
        :return:
        """
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


if __name__ == "__main__":
    match platform.system():  # Check the OS
        case "Windows":  # If Windows
            import ctypes  # Windows exclusive library

            myappid = 'theenigmaproject.crypto.easyRSA.001'  # arbitrary string, can be anything
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # Set the AppID. Needed for
            # taskbar icon and window icons to work.
            titleBarFlag = True  # Variable holding the value for if we have a custom titlebar or not. This is broken
            # on any other OS.
        case other:
            titleBarFlag = False
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())