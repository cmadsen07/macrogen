import json

f = open("sample.json")

data = json.load(f)

f.close()


def parse_text_field(text):
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
    indent_counter = 0
    for i, key in enumerate(variables_index):
        for j, var in enumerate(variables_index[key]):
            if "\t" in var[1]:
                if indent_counter < var[1].count("\t"):
                    for i in range(0, var[1].count("\t")):
                        var[1] = var[1].replace("\t", "{tab}")
                        indent_counter += 1
                elif indent_counter == var[1].count("\t"):
                    var[1] = var[1].replace("\t", "")
                elif indent_counter > var[1].count("\t"):
                    for i in range(0, (indent_counter-var[1].count("\t"))):
                        var[1] = var[1].replace("\t", "+{tab}")
            elif indent_counter > 0:
                for i in range(0, indent_counter):
                    var[1] = "+{tab}" + var[1]
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

f = open("latex_test.ahk", "w")
f.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode 2  ; 2: A window's title can contain WinTitle anywhere inside it to be a match. \n""")
for editor in data["editors"]:
    f.write("GroupAdd, LatexEditors, " + editor + "\n")
f.write("#IfWinActive ahk_group LatexEditors\n")
for macro in data["macros"]:
    f.write("#Hotstring " + macro["trigger"] + "\n")
    f.write("::" + macro["hotstring"] + "::\n" + macro["name"] + "() {\n")
    f.write(parse_text_field(macro["text"]))
    f.write("\n}\n")
f.close()