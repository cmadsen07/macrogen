import json
import re
import traceback

# f = open("full.json")

# data = json.load(f)

# f.close()


class JSON_Parser:
    def __init__(self, text):
        self.lines = text.split("\n")
        self.parsed_text = self.handle_json(self.lines)

    def handle_json(self, lines):
        original_text = list(lines)
        #print("#0" in lines[0])
        if(not any("#0" in s for s in lines)):
            lines[0] += "#0"
        variables = []
        variables_index = {}
        #print(lines)
        last_line = int()
        line_counter = 0
        for i, line in enumerate(lines):
            #print(i)
            if "#" in line:
                #print(line.count("#"))
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
                            variables_index[num] = [[str(i*10+idx+10).zfill(3), partline]]
                            #print(i*10+idx)
                        else:
                            variables_index[num].append([str(i*10+idx+10).zfill(3), partline])
                else:
                    num = line[line.find("#")+1]
                    #print(num)
                    if num not in variables:
                        variables.append(num)
                        variables_index[num] = [[str(i*10+10).zfill(3), line]]
                    else:
                        variables_index[num].append([str(i*10+10).zfill(3), line])
            else:
                #print("here")
                if "None" not in variables:
                    variables.append("None")
                    mod_line = line
                    for j in range(0, line.count("}")):
                        if j > 0:
                            inb = line[line.rfind("{")+len("{"):line.rfind("}")]
                            mod_line = mod_line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                        else:
                            inb = line[line.find("{")+len("{"):line.find("}")]
                            mod_line = mod_line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                    mod_line += "{enter}\n"
                    variables_index["None"] = [[str(i*10+10).zfill(3), mod_line]]
                else:
                    #print(line.count("}"))
                    mod_line = line
                    for j in range(0, line.count("}")):
                        if j > 0:
                            inb = line[line.rfind("{")+len("{"):line.rfind("}")]
                            if (j != len(lines)-1):
                                mod_line = mod_line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                            else:
                                mod_line = mod_line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                        else:
                            inb = line[line.find("{")+len("{"):line.find("}")]
                            if (i != len(lines)-1):
                                mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                            else:
                                mod_line = line.replace("{" + inb + "}", "{{}" + inb + "{}}")
                    if (i != len(lines)-1):
                        mod_line += "{enter}\n"
                    else:
                        mod_line += "\n"
                    variables_index["None"].append([str(i*10+10).zfill(3), mod_line])
        #print("indexes")
        #print(variables_index)            
        indent_counter = 0

        for i, key in enumerate(variables_index):
            for j, var in enumerate(variables_index[key]):
                #print(var[1])
                # if "\t" in var[1]:
                #     if indent_counter < var[1].count("\t"):
                #         for k in range(0, var[1].count("\t")):
                #             var[1] = var[1].replace("\t", "{tab}")
                #             indent_counter += 1
                #     elif indent_counter == var[1].count("\t"):
                #         var[1] = var[1].replace("\t", "")
                #     elif indent_counter > var[1].count("\t"):
                #         for k in range(0, (var[1].count("\t"))):
                #             var[1] = var[1].replace("\t", "+{tab}")
                #             indent_counter -= 1
                # elif indent_counter > 0:
                #     var[1] = "+{tab}"*(indent_counter) + var[1]
                #     # for k in range(0, indent_counter):
                #     #     var[1] = "+{tab}" + var[1]
                #     #     indent_counter -= 1
                #     indent_counter = 0
                if "!" in var[1]:
                    var[1] = var[1].replace("!", "{!}")
                if "^" in var[1]:
                    var[1] = var[1].replace("^", "{^}")
                if j > 0:
                    #print(j)
                    var[1] = "Send " + var[1].replace("#" + key, "%Text" + key + "%")
                    var[1] = var[1].replace("{%Text" + key + "%}", "{{}%Text" + key + "%{}}\n") 
                else:
                    #print("KEEEYY: ")
                    #print(j)
                    #if key != "None": print(variables_index[key])
                    if key != "None" and str(int(key)-1) in variables_index:
                        #print(key)
                        #print(str(int(key)-1) in variables_index)
                        # TODO: needs to check first two characters, or add leading zero when smaller than 100
                        if str(variables_index[key][0][0])[0:2] == str(variables_index[str(int(key)-1)][0][0])[0:2]:
                            #print("here")
                            enter_part = "Send {}}\n"
                        else:
                            enter_part = "Send {}}{enter}\n"
                    else:
                        enter_part = "Send {}}{enter}\n"
                        
                    if key != "0":
                        var[1] = "Send " + var[1].replace("{#" + key + "}", 
                            "{{}\nText" + key + ":=get_input()\nSend %Text" + key + "%\n" + enter_part)
                    else:
                        var[1] = "Send " + var[1].replace("{#" + key + "}", 
                            "{{}#" + key + "{}}")
                        #"{{}\nInput, Text" + key + ", V, {tab}\n" + enter_part)
    #                 "Send {backspace}{}}{enter}\n")
        final_text = ""
        #print("============")
        #print(variables_index)
        
        variables_strings = []
        for key in list(variables_index.values()):
            for item in key:
                variables_strings.append(item)
        variables_dict = {}
        for string in variables_strings:
            variables_dict[str(string[0])] = string[1]
        ordered = sorted(variables_dict.items(), key=lambda x: int(x[0]))
        # print("===")
        # print("list")
        # print(list(variables_dict.items()))
        # print("")
        # print(ordered)
        zero_index = None
        ordered_list = []
        for i in range(0, len(ordered)):
            ordered_list.append(list(ordered[i]))
            if ("#0" in ordered[i][1]):
                zero_index = i
        
        #print(zero_index)
        if zero_index == 0:
           # print(ordered[i][1].rfind("#0"))
            #print(ordered[i][1].rfind("{}}"))
            if (ordered[i][1].rfind("{}}")-ordered[i][1].rfind("#0") == 2):
                zero_index_text = len(ordered[i][1]) - 2 - ordered[i][1].rfind("#0") - 2
            else:
                zero_index_text = len(ordered[i][1]) - 2 - ordered[i][1].rfind("#0")
        elif zero_index == None:
            #print(ordered[i][1])
            zero_index = len(ordered[i][1])-1
        #print(ordered[i][1])
        # print(zero_index)
        # print("text")
        #print(zero_index_text)

            #print(ordered[i][1])
            #print(zero_index_text)
        
        indent_counter = 0
        for item in ordered_list:
            # INDENT HANLING
            indent_num = item[1].count("\t")-indent_counter
            #print(item[1])
            #print(indent_num)
            #print(item[1].count("\t"))
            mod_line = item[1]
            if (indent_num > 0):
                for i in range(0, item[1].count("\t")):
                    #print("remove tab 1")
                    mod_line = mod_line.replace("\t", "")
                #print("{tab}"*indent_num)
                mod_line = mod_line.replace("Send ", "Send " + "{tab}"*indent_num)
            elif (indent_num < 0):
                for i in range(0, item[1].count("\t")):
                    #print("remove tab 3")
                    mod_line = mod_line.replace("\t", "")
                #print("+{tab}"*abs(indent_num))
                mod_line = mod_line.replace("Send ", "Send " + "+{tab}"*abs(indent_num))
            elif indent_num == 0:
                for i in range(0, item[1].count("\t")):
                    #print("remove tab 4")
                    mod_line = mod_line.replace("\t", "")
            #print(mod_line)
            #print("="*5)
            indent_counter = item[1].count("\t")
            item[1] = mod_line
            # var = item
            # if "\t" in var[1]:
            #     print("====")
            #     print(indent_counter)
            #     print(var[1].count("\t"))
            #     print(var[1].count("\t")-indent_counter)
            #     print(var[1])
            #     print("=====")
            #     if indent_counter < var[1].count("\t"):
            #         for k in range(0, var[1].count("\t")-indent_counter):
            #             var[1] = var[1].replace("\t", "{tab}")
            #             indent_counter += 1
            #     elif indent_counter == var[1].count("\t"):
            #         for k in range(0, var[1].count("\t")):
            #             var[1] = var[1].replace("\t", "")
            #     elif indent_counter > var[1].count("\t"):
            #         for k in range(indent_counter, var[1].count("\t")):
            #             var[1] = var[1].replace("\t", "+{tab}")
            #             indent_counter -= 1
            # elif indent_counter > 0:
            #     #var[1] = "+{tab}"*(indent_counter) + var[1]
            #     mod_line = var[1].replace("Send ", "")
            #     var[1] = "Send " + "+{tab}"*indent_counter + mod_line
            #     # for k in range(0, indent_counter):
            #     #     var[1] = "+{tab}" + var[1]
            #     #     indent_counter -= 1
            #     indent_counter = 0



            if "#0" in item[1]:
                item[1] = item[1].replace("#0", "")

        #print(zero_index)
        # print(ordered_list[0])
        # print(zero_index)
        # print("======")
        
        lines_after_zero = len(ordered_list[zero_index+1:])
        #print(ordered_list[zero_index][1])
        if (len(ordered_list[zero_index][1]) != 5) and (zero_index != 0):
            #print(len(ordered_list[zero_index][1]))
            ordered_list.append([str(int(ordered[-1][0])+1), "Send {home}{up " + str(lines_after_zero) + "}{end}{enter}"])
            ordered_list.append([str(int(ordered[-1][0])+1), "\n" + ordered_list[zero_index][1]])
        else:
            if (len(ordered_list) > 1):
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

        if ("\n" in ordered_list[0][1]):
            ordered_list[0][1] = ordered_list[0][1].lstrip()
            #print(ordered_list[0])
        
        return_string = ""
        for item in ordered_list:
            #print(item[1])
            if "    \end" not in item[1] and item[1]:
                return_string += item[1]
            elif item[1]:
                return_string += item[1].replace("  \end", "\end")
        return return_string



# f = open("latex_test.ahk", "w")
# f.write("""#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
# ; #Warn  ; Enable warnings to assist with detecting common errors.
# SendMode Input  ; Recommended for new scripts due to its superior speed and reliability
# SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
# SetTitleMatchMode 2  ; 2: A window's title can contain WinTitle anywhere inside it to be a match.
# """)
# for editor in data["editors"]:
#     f.write("GroupAdd, LatexEditors, " + editor + "\n")
# f.write("""get_input() {
# Input, Text1, V, {tab}
# Send +^{Left}
# clipboard := ""
# Send ^c
# ClipWait, 1
# my_Text := regexreplace(clipboard, "\s+$")
# return my_text
# }
# """)
# f.write("#IfWinActive ahk_group LatexEditors\n")
# f.write('Hotstring("EndChars", "")' + "\n")
# for macro in data["macros"]:
#     #f.write(":*O:" + macro["hotstring"] + " "+ "::\n" + macro["name"] + "() {\n")
#     #f.write("#Hotstring EndChars " + macro["trigger"]  + "\n")
#     f.write(":*O:" + macro["hotstring"] + macro["trigger"]  + "::\n" + macro["name"].replace(" ", "_") + "() {\n")
#     try:
#         json_parser = JSON_Parser(macro["text"])
#     except:
#         traceback.print_exc()
#         print(macro["name"])
#         break
#     f.write(json_parser.parsed_text)
#     f.write("\n}\n")
# f.close()