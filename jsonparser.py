import json
import re

f = open("test.json")

data = json.load(f)

f.close()


class JSON_Parser:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.parsed_text = self.handle_json(self.lines)

    def handle_json(self, lines):
        original_text = list(lines)
        if("#0" not in lines[0]):
            lines[0] += "#0"
        variables = []
        variables_index = {}
        last_line = int()
        line_counter = int()
        for i, line in enumerate(lines):
            if "#" in line:
                if line.count("#") > 1:
                    indices = [m.start() for m in re.finditer('#', line)]
                    nums = []
                    for idx in indices:
                        nums.append(idx+3)
                    split_line = [line[v1:v2] for v1, v2 in zip([0]+nums, nums+[None])]
                    while("") in split_line:
                        split_line.remove("")
                    for idx, partline in enumerate(split_line):
                        num = partline[partline.find("#")+1]
                        if num not in variables:
                            variables.append(num)
                            variables_index[num] = [[i*10+idx+10, partline]]
                            #print(i*10+idx)
                        else:
                            variables_index[num].append([i*10+idx+10, partline])

                else:
                    num = line[line.find("#")+1]
                    if num not in variables:
                        variables.append(num)
                        variables_index[num] = [[i*10+10, line]]
                    else:
                        variables_index[num].append([i*10+10, line])
            else:
                if "None" not in variables:
                    variables.append("None")
                    inb = line[line.find("{")+len("{"):line.rfind("}")]
                    mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "{enter}\n"
                    variables_index["None"] = [[i*10, mod_line]]
                else:
                    inb = line[line.find("{")+len("{"):line.rfind("}")]
                    if (i != len(lines)-1):
                        mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "{enter}\n"
                    else:
                        mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}") + "\n"
                    variables_index["None"].append([i*10+10, mod_line])
        #print(variables_index)            
        indent_counter = 0
        #print(variables_index)
        for i, key in enumerate(variables_index):
            for j, var in enumerate(variables_index[key]):
                #print(var[1])
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
                    if key != "None" and str(int(key)-1) in variables_index:
                        if str(variables_index[key][0][0])[0] == str(variables_index[str(int(key)-1)][0][0])[0]:
                            enter_part = "Send {backspace}{}}\n"
                    else:
                        enter_part = "Send {backspace}{}}{enter}\n"
                        
                        
                    var[1] = "Send " + var[1].replace("{#" + key + "}", 
                        "{{}\nInput, Text" + key + ", V, {tab}\n" + enter_part)
    #                 "Send {backspace}{}}{enter}\n")
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
        if zero_index == 0:
            zero_index_text = len(ordered[i][1]) - 2 - ordered[i][1].rfind("#0")

            print(ordered[i][1])
            print(zero_index_text)
        for item in ordered_list:
            if "#0" in item[1]:
                item[1] = item[1].replace("#0", "")

        lines_after_zero = len(ordered_list[zero_index+1:])
        
        print(zero_index)
        print(ordered_list[zero_index][1])
        if (len(ordered_list[zero_index][1]) != 5) and (zero_index != 0):
            print(len(ordered_list[zero_index][1]))
            ordered_list.append([str(int(ordered[-1][0])+1), "Send {home}{up " + str(lines_after_zero) + "}{end}{enter}"])
            ordered_list.append([str(int(ordered[-1][0])+1), "\n" + ordered_list[zero_index][1]])
        else:
            if (len(ordered_list) > 2):
                #print(ordered_list[-1][0][0])
                #TODO: check if last index equals previous index i.e. 11=12 True (based on first number) if so, do not send home
                #print(str(variables_index[key][0][0])[0])
                #print(ordered_list[-2][0][0])
                if (ordered_list[-1][0][0] != ordered_list[-2][0][0]):
                    ordered_list.append([str(int(ordered[-1][0])+1), "Send {home}"])
            else:
                ordered_list.append([str(int(ordered[-1][0])+1), "\n" + ordered_list[zero_index][1]])
                ordered_list.append([str(int(ordered[-1][0])+2), "\nSend {left " + str(zero_index_text) + "}"])
        
        ordered_list.pop(zero_index)
        #print(ordered_list)
        
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
    json_parser = JSON_Parser(macro["text"])
    f.write(json_parser.parsed_text)
    f.write("\n}\n")
f.close()