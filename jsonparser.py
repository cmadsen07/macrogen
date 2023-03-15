import json
import re
import traceback

# f = open("full.json")

# data = json.load(f)

# f.close()

class JSON_Parser:
    def __init__(self, text):
        self.text = text
        self.parsed_text = self.handle_json()

    def find_occurrences(self, s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def handle_json(self):
        if "#0" not in self.text:
            self.text += "\n#0"
        occurences_idx = self.find_occurrences(self.text, "#")
        occurences = []
        for occ in occurences_idx:
            occurences.append(self.text[occ+1])
        occ_sorted, occ_idx_sorted = zip(*sorted(zip(occurences, occurences_idx)))
        
        return_text = """ClipSaved := ClipboardAll()
A_Clipboard := "
(
""" + self.text + """   
)"
Send '^v'     
"""
        for i in range(0, len(occ_sorted)):
            if occ_sorted[i] != "0" and occ_sorted[i] != occ_sorted[i-1]:
                if int(occ_sorted[i]) > 1:
                    if occ_idx_sorted[i] > occ_idx_sorted[i-1]:
                        return_text += "Send '{left " + str(len(self.text)-occ_idx_sorted[i]-2) + "}'\nSend '{backspace 2}'\nText" + occ_sorted[i] + " := get_input()\nSend '{backspace}'\n"
                        return_text += "Send '{right " + str(len(self.text)-occ_idx_sorted[i]-2) + "}'\n"
                    else:
                        add_string = ""
                        for j in range(1, int(occ_sorted[i])):
                            add_string += "+StrLen(Text" + occ_sorted[j] + ")-2"
                        return_text += "MoveInt := " + str(len(self.text)-occ_idx_sorted[i]-2)  + add_string + "\n"
                        return_text += "Send '{left ' . MoveInt . '}'\nSend '{backspace 2}'\nText" + occ_sorted[i] + " := get_input()\nSend '{backspace}'\n"
                        return_text += "Send '{right ' . MoveInt . '}'\n"
                else:
                    return_text += "Send '{left " + str(len(self.text)-occ_idx_sorted[i]-2*int(occ_sorted[i])) + "}'\nSend '{backspace 2}'\nText" + occ_sorted[i] + " := get_input()\nSend '{backspace}'\n"
                    return_text += "Send '{right " + str(len(self.text)-occ_idx_sorted[i]-2*int(occ_sorted[i])) + "}'\n"
            elif occ_sorted[i] == occ_sorted[i-1] and len(occ_sorted) > 1:
                return_text += "Send '{left " + str(len(self.text)-occ_idx_sorted[i]-2*int(occ_sorted[i])) + "}'\nSend '{backspace 2}'\nSend Text" + occ_sorted[i] + "\n"
                return_text += "Send '{right " + str(len(self.text)-occ_idx_sorted[i]-2*int(occ_sorted[i])) + "}'\n"
        if "0" in occ_sorted:
            zero_idx = occ_idx_sorted[occ_sorted.index("0")]
            greater_idxs = []
            for i in range(0, len(occ_sorted)):
                if occ_sorted[i] != "0":
                    if occ_idx_sorted[i] > zero_idx:
                        greater_idxs.append([occ_sorted[i], occ_idx_sorted[i]])
            if len(greater_idxs) > 0:
                add_string = ""
                for idx in greater_idxs:
                    add_string += "+StrLen(Text" + idx[0] + ")-2"
                return_text += "MoveInt := " + str(len(self.text)-occ_idx_sorted[0]-2) + add_string + "\n"
                return_text += "Send '{left ' . MoveInt . '}'\nSend '{backspace 2}'"
            else:
                return_text += "Send '{left " + str(len(self.text)-occ_idx_sorted[0]-2) + "}'\nSend '{backspace 2}'"
        
        return_text += '\nSleep 10\nA_Clipboard := ClipSaved\nClipSaved := ""'
        return return_text


# for macro in data["macros"]:
#     try:
#         json_parser = JSON_Parser(macro["text"])
#     except:
#         traceback.print_exc()
#         print(macro["name"])
#         break
#     json_parser.handle_json()


# f = open("latex_test.ahk", "w")
# f.write("SetTitleMatchMode 2\n")
# for editor in data["editors"]:
#     f.write("GroupAdd 'LatexEditors', '" + editor + "'\n")
# f.write("""get_input() 
# {
# ih := InputHook("V", "{tab}")
# ih.Start()
# ErrorLevel := ih.Wait()
# if (ErrorLevel = "EndKey")
#     ErrorLevel .= ":" ih.EndKey
# OutputVar := ih.Input
# return OutputVar
# }
# """)
# f.write("HotIfWinActive 'LatexEditors'\n")
# f.write('Hotstring("EndChars", "")' + "\n")
# for macro in data["macros"]:
#     #f.write(":*O:" + macro["hotstring"] + " "+ "::\n" + macro["name"] + "() {\n")
#     #f.write("#Hotstring EndChars " + macro["trigger"]  + "\n")
#     print(macro["hotstring"])
#     f.write(":*O:" + macro["hotstring"] + macro["trigger"]  + "::\n{\n")
#     try:
#         json_parser = JSON_Parser(macro["text"])
#     except:
#         traceback.print_exc()
#         print(macro["name"])
#         break
#     f.write(json_parser.parsed_text)
#     f.write("\n}\n")
# f.close()