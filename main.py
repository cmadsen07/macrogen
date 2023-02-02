# File: main.py
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QInputDialog
from PySide6.QtCore import QFile, QIODevice
import json

def parse_json(text):
    lines = text.split("\n")
    original_text = list(lines)
    variables = []
    variables_index = {}
    last_line = int()
    line_counter = int()
    for i, line in enumerate(lines):
        if "#" in line:
            num = line[line.find("#")+1]
            if num not in variables:
                variables.append(num)
                variables_index[num] = [[i, line]]
            else:
                variables_index[num].append([i, line])
        else:
            if "None" not in variables:
                variables.append("None")
                inb = line[line.find("{")+len("{"):line.rfind("}")]
                mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "{enter}\n"
                variables_index["None"] = [[i, mod_line]]
            else:
                inb = line[line.find("{")+len("{"):line.rfind("}")]
                if (i != len(lines)-1):
                    mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "{enter}\n"
                else:
                    mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "\n"
                variables_index["None"].append([i, mod_line])
    for i, key in enumerate(variables_index):
        for j, var in enumerate(variables_index[key]):
            if "\t" in var[1]:
                var[1] = var[1].replace("\t", "{tab}")
            if "!" in var[1]:
                var[1] = var[1].replace("!", "{!}")
            if j > 0:
                var[1] = "Send " + var[1].replace("#" + key, "%Text" + key + "%")
                var[1] = var[1].replace("{%Text" + key + "%}", "{{}%Text" + key + "%{}}\n") 
            else:
                var[1] = "Send " + var[1].replace("{#" + key + "}", 
                    "{{}\nInput, Text" + key + ", V, {tab}\n" +
                    "Send {backspace}{}}{enter}\n")
    final_text = ""
    
    variables_strings = []
    for key in list(variables_index.values()):
        for item in key:
            variables_strings.append(item)
    variables_dict = {}
    for string in variables_strings:
        variables_dict[str(string[0])] = string[1]
    ordered = sorted(variables_dict.items())
    zero_index = None
    ordered_list = []
    for i in range(0, len(ordered)):
        ordered_list.append(list(ordered[i]))
        if ("#0" in ordered[i][1]):
            zero_index = i
    for item in ordered_list:
        if "#0" in item[1]:
            item[1] = item[1].replace("#0", "")

    lines_after_zero = len(ordered_list[zero_index+1:])
    
    if (len(ordered_list[zero_index][1]) != 5):
        ordered_list.append([str(int(ordered[-1][0])+1), "Send {home}{up " + str(lines_after_zero) + "}{end}{enter}"])
        ordered_list.append([str(int(ordered[-1][0])+1), "\n" + ordered_list[zero_index][1]])
    else:
        ordered_list.append([str(int(ordered[-1][0])+1), "Send {home}"])
    
    ordered_list.pop(zero_index)
    
    return_string = ""
    for item in ordered_list:
        if "    \end" not in item[1]:
            return_string += item[1]
        else:
            return_string += item[1].replace("  \end", "\end")
    return return_string
    

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


        # connect functions
        self.macroBtn.clicked.connect(self.add_macro)
        self.list.itemClicked.connect(self.select_macro)
        self.name.textChanged.connect(self.change_name)
        self.trigger.currentIndexChanged.connect(self.change_trigger)
        self.hotsring.textChanged.connect(self.change_hotstring)
        self.textedit.textChanged.connect(self.change_textedit)
        self.saveFile.triggered.connect(self.save_json)
        self.loadFile.triggered.connect(self.load_json)
        self.saveAHK.triggered.connect(self.save_AHK)
        self.editortext.textChanged.connect(self.change_editor)
        self.removeBtn.clicked.connect(self.remove_macro)

        # variables
        self.counter = 0
        self.macros = []
        self.editors = []
    
    def add_macro(self):
        placeholder = "Macro" + str(self.counter)
        self.list.addItem(placeholder)
        self.counter += 1
        self.macros.append({"name": placeholder, "trigger": "`t", "hotstring": "", "text": ""})
    
    def select_macro(self, item):
        self.name.setText(item.text())
        index = 0
        trigger_string = self.macros[self.list.currentRow()]["trigger"]
        match trigger_string:
            case "`t":
                index = 0
            case "*0":
                index = 1
            case "*":
                index = 2
        self.trigger.setCurrentIndex(index)
        self.hotsring.setText(self.macros[self.list.currentRow()]["hotstring"])
        self.textedit.setPlainText(self.macros[self.list.currentRow()]["text"])

    
    def change_name(self, string):
        self.list.currentItem().setText(string)
        self.macros[self.list.currentRow()]["name"] = string
    
    def change_trigger(self, index):
        trigger_text = "`t"
        match index:
            case 0:
                trigger_text = "`t"
            case 1:
                trigger_text = "*0"
            case 2:
                trigger_text = "*"
        self.macros[self.list.currentRow()]["trigger"] = trigger_text
    
    def change_hotstring(self, string):
        self.macros[self.list.currentRow()]["hotstring"] = string

    def change_textedit(self):
        self.macros[self.list.currentRow()]["text"] = self.textedit.toPlainText()

    def save_json(self):
        save_dict = {}
        save_dict["editors"] = self.editors
        save_dict["macros"] = self.macros
        json_object = json.dumps(save_dict, indent=4)

        name = QFileDialog.getSaveFileName(self.window, "Save File", "", "JSON (*.json)")

        file = open(name[0], "w")
        file.write(json_object)
        file.close()
    
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
    
    def save_AHK(self):
        name = QFileDialog.getSaveFileName(self.window, "Save File", "", "AHK (*.ahk)") 

        f = open(name[0], "w")
        f.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
        ; #Warn  ; Enable warnings to assist with detecting common errors.
        SendMode Input  ; Recommended for new scripts due to its superior speed and reliability
        SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
        SetTitleMatchMode 2  ; 2: A window's title can contain WinTitle anywhere inside it to be a match. \n""")
        for editor in self.editors:
            f.write("GroupAdd, LatexEditors, " + editor + "\n")
        f.write("#IfWinActive ahk_group LatexEditors\n")
        for macro in self.macros:
            f.write("#Hotstring " + macro["trigger"] + "\n")
            f.write("::" + macro["hotstring"] + "::\n" + macro["name"] + "() {\n")
            f.write(parse_json(macro["text"]))
            f.write("\n}\n")
        f.close()
    
    def change_editor(self):
        editor_string = self.editortext.toPlainText()
        self.editors = [l for l in editor_string.split('\n') if l.strip()]
        print(self.editors)

    def remove_macro(self):
        self.macros.pop(self.list.currentRow())
        self.list.takeItem(self.list.currentRow())
        
    


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
    
    window.show()

    sys.exit(app.exec())