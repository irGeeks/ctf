from __future__ import print_function
import websocket
### irGeeks
### SharifCTF{2f7a87d9afd14d7f6de27546e8084168}
questions = []

class Q():
    def __init__(self, q):
        self.q = q
        self.fails = []
        self.wins = []
        
def find(str):
    for x in questions:
        if(x.q == str):
            return x
    return None


def print_menu(msg):
    s = msg.split("#")
    for i in range(len(s)):
        print("{0}: {1}".format(i,s[i]))

def add(list, str):
    if(not str in list):
        list.append(str)
                
def analyse_him(asking, msg, ans, stat):
    fail = True if stat == "00" else False
    q = find(msg)
    if(q == None):
        q = Q(msg)
        questions.append(q)    

    if(asking):
        if(fail):
            add(q.wins, ans)
        else:
            add(q.fails, ans)
            
    else:
        if(fail):
            add(q.fails, ans)
        else:
            add(q.wins, ans)
            
def strOf(idx, options):
    s = options.split("#")
    return s[idx]    
    
def indexOf(str, strOptions):
    s = strOptions.split("#")
    
    if(not str in strOptions):
        return None
    
    for i in range(len(s)):
        if(s[i] == str):
            return i

def validOptions(qs, fail):
    s = set(fail)
    all = qs.split("#")
    temp = [x for x in all if x not in s] 
    res = ""
    for t in temp:
        res+= " {0}".format(indexOf(t,qs))
    return res

def answer(msg, strOptions): # returns  str of index if found otherwise list of valid options 
        
    q = find(msg)
    if (q == None):
        return ""#, "" #validOptions(strOptions,[])
    
    if(len(q.wins) > 0 ):
        for win in q.wins:
            if win in strOptions:
                return str(indexOf(win,strOptions))#,"" #validOptions(strOptions, [])
            else:
                return ""#, "" #validOptions(strOptions, q.fails)
                

def read(options):
    return "0"
    r = len(options.split("#"))
    while(True):
        try:
            x = int(raw_input("Which:"))
            if(x <r):
                return str(x)
        except:
            pass
                
        print("Invalid")

s = websocket.create_connection("ws://213.233.175.130:4010")

ready = False
r = 0

while(True):
    
    if (not ready):
        stat = s.recv()
        print(stat)
    ready = False
    
    if ("lost" in stat.lower()):
        r+=1
        print("round {0}".format(r))
        continue
    elif ("flag" in stat.lower()):
        exit()
    
    if(stat == "01"):
        qs = s.recv()
        print(qs)
        qs = qs[1:]
        print_menu(qs)
        ans = read(qs)
        s.send(ans)
        his_ans = s.recv()
        print(his_ans)
        stat = s.recv()
        print(stat)
        analyse_him(True, strOf(int(ans), qs), his_ans[1:], stat)
        ready = True
        
    elif(stat == "00"):
        q = s.recv()
        print(q)
        q = q[1:]
        options = s.recv()
        print(options)
        options = options[1:]
        ans = answer(q, options)
        
        if (ans == "" or ans == None):
            print("\nQ:{0}".format(q))
            print_menu(options)
            #print("Suggestions:{0}".format(suggestions))
            ans = read(options)
            ans = "0"
        s.send(ans)
        stat = s.recv()
        print(stat)
        analyse_him(False, q, strOf(int(ans), options), stat)
        ready = True
            
