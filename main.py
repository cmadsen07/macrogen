# File: main.py
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6 import QtGui
from PySide6.QtCore import QFile, QIODevice
import json
import re
import jsonparser    
import os
import traceback

class ActionHandler():
    def __init__(self, window):
        self.window = window

        # define elements
        self.macroBtn = window.pushButtonMacro
        self.list = window.listWidget
        self.name = window.lineEditName
        self.trigger = window.dropdownTrigger
        self.hotsring = window.lineEditHotstring
        self.textedit = window.textEdit
        self.saveFile = window.actionSave_File
        self.loadFile = window.actionLoad_File
        self.saveAHK = window.actionSave_AHK
        self.editortext = window.editorText
        self.removeBtn = window.removeButton
        self.saveJSON = window.actionSave_JSON
        self.newBtn = window.actionNew_File

        self.macroBtn.setShortcut("Ctrl+Shift+N")
        self.removeBtn.setShortcut("Ctrl+Shift+Del")


        # connect functions
        self.macroBtn.clicked.connect(self.add_macro)
        self.list.itemClicked.connect(self.select_macro)
        self.name.textChanged.connect(self.change_name)
        self.trigger.currentIndexChanged.connect(self.change_trigger)
        self.hotsring.textChanged.connect(self.change_hotstring)
        self.textedit.textChanged.connect(self.change_textedit)
        self.saveFile.triggered.connect(self.save_files)
        self.loadFile.triggered.connect(self.load_json)
        self.saveAHK.triggered.connect(self.save_AHK)
        self.editortext.textChanged.connect(self.change_editor)
        self.removeBtn.clicked.connect(self.remove_macro)
        self.saveJSON.triggered.connect(self.save_json_file)
        self.newBtn.triggered.connect(self.new_file)

        # variables
        self.counter = 0
        self.macros = []
        self.editors = []
        self.currentFile = None
    
    def add_macro(self):
        placeholder = "Macro" + str(self.counter)
        self.list.addItem(placeholder)
        self.counter += 1
        self.macros.append({"name": placeholder, "trigger": "`t", "hotstring": "", "text": ""})

        self.list.setCurrentRow(self.list.count()-1)
        self.select_macro(self.list.currentItem())
        self.name.setFocus()
        self.name.selectAll()

        self.change_title("*")
    
    def select_macro(self, item):
        self.name.setText(item.text())
        index = 0
        trigger_string = self.macros[self.list.currentRow()]["trigger"]
        match trigger_string:
            case "`t":
                index = 0
            case " ":
                index = 1
            case "":
                index = 2
        self.trigger.setCurrentIndex(index)
        self.hotsring.setText(self.macros[self.list.currentRow()]["hotstring"])
        self.textedit.setPlainText(self.macros[self.list.currentRow()]["text"])

        self.change_title("*")

    
    def change_name(self, string):
        self.list.currentItem().setText(string)
        self.macros[self.list.currentRow()]["name"] = string

        self.change_title("*")
    
    def change_trigger(self, index):
        trigger_text = "`t"
        match index:
            case 0:
                trigger_text = "`t"
            case 1:
                trigger_text = " "
            case 2:
                trigger_text = ""
        self.macros[self.list.currentRow()]["trigger"] = trigger_text

        self.change_title("*")
    
    def change_hotstring(self, string):
        self.macros[self.list.currentRow()]["hotstring"] = string

        self.change_title("*")

    def change_textedit(self):
        self.macros[self.list.currentRow()]["text"] = self.textedit.toPlainText()

        self.change_title("*")

    def save_files(self):
        name = self.save_json_file()
        s = (name[0].replace(".json", ".ahk"), "AHK (*.ahk)")
        self.save_ahk_file(saveName=s)
        
    
    def load_json(self):
        self.list.clear()

        name = QFileDialog.getOpenFileName(self.window, "Open File", "", "JSON (*.json)")
        file = open(name[0], "r")
        contents = json.load(file)
        file.close()
        self.editors = contents["editors"]
        self.macros = contents["macros"]
        
        for macro in self.macros:
            self.list.addItem(macro["name"])
        editor_string = ""
        for editor in self.editors:
            editor_string += editor + "\n"
        self.editortext.setPlainText(editor_string)

        self.currentFile = name
        #self.window.setWindowTitle("LaTex Macro generator for AHK (" + name[0].split("/")[-1] + ")")
    
    def save_AHK(self, save_as_given=False):
        self.save_ahk_file(saveName=save_as_given)
    
    def change_editor(self):
        editor_string = self.editortext.toPlainText()
        self.editors = [l for l in editor_string.split('\n') if l.strip()]
        
        self.change_title("*")

    def remove_macro(self):
        self.macros.pop(self.list.currentRow())
        self.list.takeItem(self.list.currentRow())

        self.name.clear()
        self.trigger.setCurrentIndex(0)
        self.hotsring.clear()
        self.textedit.clear()
        
        self.currentFile = None
        self.change_title("*")
    
    def check_editors(self):
        if self.editors == []:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Please note that for the generateed AHK script to function, you need to enter at least one editor in the field labeled editors.")
            msgBox.setWindowTitle("Editor field error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            #msgBox.buttonClicked.connect(msgButtonClick)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                #print('OK clicked')
                return
    
    def save_ahk_file(self, saveName=False):
        self.check_editors()

        if saveName == False:
            name = QFileDialog.getSaveFileName(self.window, "Save File", "", "AHK (*.ahk)") 
            if name == ("", ""):
                return
        else:
            name = saveName

        self.currentFile = name

        f = open(name[0], "w")
        f.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
        ; #Warn  ; Enable warnings to assist with detecting common errors.
        SendMode Input  ; Recommended for new scripts due to its superior speed and reliability
        SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
        SetTitleMatchMode 2  ; 2: A window's title can contain WinTitle anywhere inside it to be a match. \n""")
        for editor in self.editors:
            f.write("GroupAdd, LatexEditors, " + editor + "\n")
        f.write("#IfWinActive ahk_group LatexEditors\n")
        f.write('Hotstring("EndChars", "")' + "\n")
        for macro in self.macros:
            if (macro["text"] != ""):
                f.write("::" + macro["hotstring"] + macro["trigger"] + "::\n" + macro["name"].replace(" ", "_") + "() {\n")
                try:
                    json_parser = jsonparser.JSON_Parser(macro["text"])
                except:
                    traceback.print_exc()
                    print(macro["name"])
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("There was an error generating the AHK script, please send the JSON file to the developer.")
                    msgBox.setWindowTitle("Error generating ahk script")
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    #msgBox.buttonClicked.connect(msgButtonClick)

                    returnValue = msgBox.exec()
                    if returnValue == QMessageBox.Ok:
                        #print('OK clicked')
                        return
                    break
                f.write(json_parser.parsed_text)
                f.write("\n}\n")
        f.close()
        os.remove(name[0])

        self.change_title("")

    def save_json_file(self):
        self.check_editors()

        save_dict = {}
        save_dict["editors"] = self.editors
        save_dict["macros"] = self.macros
        json_object = json.dumps(save_dict, indent=4)

        if self.currentFile == None:
            name = QFileDialog.getSaveFileName(self.window, "Save File", "", "JSON (*.json)")
            if name == ("", ""):
                return
        else:
            name = self.currentFile

        self.currentFile = name

        #print(save_dict)

        file = open(name[0], "w")
        file.write(json_object)
        file.close()

        self.change_title("")

        return name
    
    def new_file(self):
        self.currentFile = None
        self.change_title("")
        self.name.clear()
        self.trigger.setCurrentIndex(0)
        self.hotsring.clear()
        self.textedit.clear()
        self.list.clear()


        

    def change_title(self, change):
        #print(self.currentFile)
        #print("change")
        if self.currentFile != None:
            self.window.setWindowTitle("LaTex Macro generator for AHK (" + self.currentFile[0].split("/")[-1] + change + ")")
        else:
            self.window.setWindowTitle("LaTeX Macro generator for AHK (" + change + ")")
        
    


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "layout.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    action_handler = ActionHandler(window)

    app.setWindowIcon(QtGui.QIcon('ahk_logo.ico'))
    
    window.show()

    sys.exit(app.exec())