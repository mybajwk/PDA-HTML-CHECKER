import sys
import re

class PDA:
    def __init__(self, states, input_symbols, stack_symbols, initial_state, initial_stack, accepting_states, is_pda_accept_empty_stack):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.initial_state = initial_state
        self.current_state = initial_state
        self.initial_stack = initial_stack
        self.stack = []
        self.stack.append(initial_stack)
        self.accepting_states = accepting_states
        self.is_pda_accept_empty_stack = is_pda_accept_empty_stack
        self.transitions = {}
        
        
    def add_transition(self, curr_state, symbol, top_of_stack, next_state, final_stack):
        key = (curr_state, symbol, top_of_stack)
        self.transitions[key] = (next_state, final_stack)
        
    def check(self, input_arr):
        currLine = 1
        for token in input_arr:
            if (token == "\n"):
                currLine = currLine + 1
                continue
            
            print("token: ", token)
            
            top_stack = self.stack[-1]
            key = (self.current_state, token, top_stack)
            print("stack 0:", self.stack)
            print("key 0:", key)
            
            if key not in self.transitions:
                return (False, currLine)
            
            while key in self.transitions:
                print("stack :", self.stack)
                print("key :", key)
                (next_state, final_stack) = self.transitions[key]
                old_state = self.current_state
                self.current_state = next_state
                
                self.stack.pop()
                
                for el in final_stack[::-1]:
                    if (el != "e"):
                        self.stack.append(el)
                
                print("stack2: ", self.stack)
                if (top_stack == self.stack[-1] and self.current_state == old_state):
                    break
                top_stack = self.stack[-1]
                key = (self.current_state, token, top_stack)
                print("key2: ", key)
        
        if (self.is_pda_accept_empty_stack and len(self.stack) == 1 and self.stack[0] == self.initial_stack):
            return (True, -1)
        
        if (not self.is_pda_accept_empty_stack and self.current_state in self.accepting_states):
            return (True, -1)
            
        return (False, currLine)
        
def read_html_from_file(file_path, array_symbol):
    with open(file_path, 'r') as file:
        str = file.read()
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    array_html = []
    
    print(str)
    
    index = 0
    
    length = len(str)
    
    currentW = ""
    
    
    insideQuot = False
    strQuot = ""
    # pertama = False
    
    # match = re.search(r'>([\s\S]*)<', str)
    
    # print(map(match.groups()))
    
    while (index < length):
        # print("char: ", str[index])
        if (str[index] == "\n"):
            array_html.append("\n")
            index = index + 1
            continue
        
        if (str[index] == " "):
            index = index + 1
            continue
        
        if (str[index] == '"' and insideQuot):
            insideQuot = False
        
        if (insideQuot):
            strQuot = strQuot + str[index]            
            index = index + 1
            continue
        
        
        if (str[index] == "<"):
            if (len(currentW) > 0):
                if (currentW not in array_symbol):
                    for c in currentW:
                        array_html.append("*")
                    currentW = ""
        
        if (str[index:index+4] == "<!--"):
            index+=7
            array_html.append("<!--")
            while(str[index-3:index] !="-->" and str[index] != "\n"):
                index+=1
            
            array_html.append(str[index-3:index])
            currentW = ""
            continue
            
        # print("cword: ", currentW)
        currentW += str[index]
        
        if (currentW in array_symbol):
            if (currentW == "<" and str[index + 1] != " "):
                index = index + 1
                continue
                
            if (currentW == '"' and not insideQuot):
                print("str:", strQuot)
                if (strQuot in array_symbol):
                    str_prev = array_html[-1]
                    array_attr_special = ['type="', 'method="']
                    if (str_prev in array_attr_special):
                        array_html.append(strQuot)
                array_html.append('"')
                currentW = ""
                index = index + 1
                strQuot = ""
                
                continue
            
            if (currentW == "<b" and (str[index + 1] == "o" or str[index + 1] == "u")):
                index = index + 1
                continue
            array_html.append(currentW)
            currentW = ""
            
        
        if (str[index] == '"' and not insideQuot):
            insideQuot = True
            index = index + 1
            continue
            
        
        index = index + 1
        
    return (array_html, lines)

def read_pda_definition_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    
    states = lines[0].replace("\n","").split(" ")
    input_symbols = lines[1].replace("\n","").split(" ")
    stack_symbols = lines[2].replace("\n","").split(" ")
    
    initial_state = lines[3].replace("\n","")
    initial_stack = lines[4].replace("\n","")
    accepting_states = lines[5].replace("\n","").split(" ")
    is_pda_accept_empty_stack = lines[6][0] == "E"        

    
    pda = PDA(states, input_symbols, stack_symbols, initial_state, initial_stack, accepting_states, is_pda_accept_empty_stack)
    
    for line in lines[7:]:
        [curr_state, symbol, top_of_stack, next_state, final_stack] = line.replace("\n","").split(" ")
        
        pda.add_transition(curr_state, symbol, top_of_stack, next_state, final_stack.replace("\n","").split(","))
    
    return pda

def main(pda_file_path, html_file_path):
    print("start")
    print(pda_file_path)
    print(html_file_path)
    pda = read_pda_definition_from_file(pda_file_path)
    # key = ('Q', '</html>', '<html')
    # print(pda.transitions)
    
    
    array_html, lines = read_html_from_file(html_file_path, pda.input_symbols)
    print(array_html)
    
    result, currLine = pda.check(array_html)
    if (result):
        print("ACCEPTED")
    else:
        print("ERROR IN LINE ", currLine, " : ", lines[currLine - 1])
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    
    
