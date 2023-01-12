#this program reads the fst files in the form of {key which is the state we are in, list of list where each list
#consist of the out going state, lower string, and upperstring}
#We can also construct the upperstring and lower string depending on which method is called


import sys
from itertools import combinations
import numpy as np


FST = {} #emptey dictionary 

def readFST(filename):
    
    global numStates
    global alphabet
    new_dict = dict() 
    fileList = []
    tmp_list = []
    List23 = []
    transition = []
    lowerElements = []
    result2 = []
    statesList2 = []
    stateIn = []
    
    #open the file and read all lines into variable "List24"
        
    with open(filename) as f:
        List24 = open(filename).readlines()
        for element in List24:
            #strip the list of emptey spaces and newline characters
            List23.append(element.strip())
            result2.append(element.replace("\n", ""))
        result2 = [item.replace(' ', '') for item in result2]
        List23 = [item.replace(' ', '') for item in List23]
        
        List23 = List23[1:]
        
    
        #getting all the upper elements from the list
        upperElements = List23[1:]
        upperElements = list(filter(None, upperElements))
        upperElements = [item[0] for item in upperElements]
        upperElements = ' '.join(upperElements).replace('2','').replace('1','').split()
        length = len(List23[2])
        #getting all of the lower elements from the list
        for element in List23:
            if(len(element) >= length  ):
                lowerElements.append(element)
        #lowerElements =lowerElements[1:]
        #lowerElements = list(filter(None, lowerElements))
        lowerElements = [item[1] for item in lowerElements]
        lowerElements = ' '.join(lowerElements).replace('N','').replace('F','').split()
        
        lengthLower = len(lowerElements) 
        lengthUpper = len(upperElements)
        lengthTotal = lengthLower + lengthUpper
        for element in List23:
            if(len(element) >= 2):
                transition.append(element)
        #getting all of the transitions from the list
        transition = [item[2:] for item in transition]
        transition = ' '.join(transition).replace('F','').split()
        transition = ' '.join(transition).replace('N','').split()
        
        #changing the transition value to a single diget rather that a pair of digets if needed
        for i in range(len(transition)):
            if transition[i] == '21':
                transition[i] = '3'
            if transition[i] == '12':
                transition[i] = '2'
            if transition[i] == '11':
                transition[i] = '1'
            if transition[i] == '22':
                transition[i] = '4'
        
        check = 'F'
        check2 ='N'
        #getting which states are final and not final states and removing the state number from the list elements
        statesList = [idx for idx in List23 if idx.lower().endswith(check.lower()) or idx.lower().endswith(check2.lower())]
        for i in statesList:
            stateIn.append(i[0:2])
            statesList2.append(i[-1])
        
        stateIn = ' '.join(stateIn).replace('N','').replace('F','').split()
        
        #changing the key value to a single digit rather than a pair of digets
        for i in range(len(stateIn)):
            if stateIn[i] == '21':
                stateIn[i] = '3'
            if stateIn[i] == '12':
                stateIn[i] = '2'
            if stateIn[i] == '11':
                stateIn[i] = '1'
            if stateIn[i] == '22':
                stateIn[i] = '4'
        
        
        for line in f:
            line = line.rstrip("\n")
            if line == "":
                fileList.append(tmp_list)
            else:
                tmp_list.extend(line.split())
        
            
    numStates = [tmp_list[0]] #get the number of states from the file
    numStates = ''.join(numStates) # convert the variable to a string
    numStates = int(numStates) #convert to an int to later be used
    listOfStates = list(range(1, numStates+1)) # all the possible states that we can be in
    
    
    k = list(zip(transition, upperElements, lowerElements))
    
    lengthLower = (lengthLower +1 )//numStates
    
   
    
    k1 = [k[i:i + (lengthLower)] for i in range(0, len(k), (lengthLower))]
    
    
    i = 0
    p = 1
    w = 0
    while(p < numStates+1):
        #state = statesList2[w] #check if the state is a final state or not
        startState = stateIn[w]
        count = len(result2[p])
        count = count //3
        # adding everything to dictionary
        new_dict[startState] = (k1[i],statesList2[i])
        
        #incrementing all counters that I used
        i=i+1
        p = p +1
        w = w + 1
    
        
    #return a sorted dictionary of the FST
    new_dict = dict(sorted(new_dict.items()))
    
    return (new_dict)


def composeFST(F1,F2):
    FST1 = readFST(F1)
    FST2 = readFST(F2)
    numStates = len(FST1)
    numStates1 = len(FST2)
    numStatesTotal = numStates + numStates1 #total number of states in the composed fst
    new_dict = dict()
    new_dict2 = dict()
    
    statesAll = []
    p = 0
    k = 0

    
    while(p < numStates1):
        states = list(FST1.keys())[k]
        statesAll.append(states)
        p = p + 1
        k = k + 1
    k = 0 
    p = 0
    while(p <numStates1):
        states2 = list(FST2.keys())[k]
        statesAll.append(states2)
        p = p + 1
        k = k + 1
  
    #getting the keys from fst and creating the new combined state key
    allStatesCombo = list(combinations(statesAll, 2)) #getting the combinations of states
    allStatesCombo.sort() #sorting the states
    allStatesCombo = list(dict.fromkeys(allStatesCombo)) #getting rid of duplicate states

    p = 1
    k = 0 
        
    
    i = 0
    
    trial = []
    trial2 = []   
    
    #inialize the dictionary
    d = dict([(key, []) for key in allStatesCombo])
    
    
    #inialize all the counters and list
    n = 1
    w = 1
    t = 1
    f = 1

    res = []
    res2 = []
    oh = 0
    ya = 0
    
    g= 0
    j = 0
  
    
    listOfValues = list(FST1.values())
    listOfValues3 = list(FST2.values())
    listOfKeys = list((FST1.keys())) #list of keys of 1st FST
    listOfKeys2 = list((FST2.keys())) #list of keys of 1st FST
    listOfValues2 = listOfValues[oh]
    listOfValues4 = listOfValues3[ya]
    
    numOfvalues = (len(listOfValues2[0]) + len(listOfValues4[0])) //2
    
    
    
    f = open("composed.txt", "w") #write a composed file
    f.write(str(numStatesTotal)  + "\n") # the number of states
    f.write("11" + " " + listOfValues[0][-1] + "\n") # write the first state and if the state is final or not
    

    while(n< numStatesTotal*numOfvalues+1): # loop through all the values in all states
        trial = []
        #listOfValues = list(FST1.values())
        listOfValues2 = listOfValues[oh]
        #listOfValues2 = ([x for x in listOfValues2 if len(x) >= 3])
        res = listOfValues2
        result = res[0]
        
        fState = listOfValues[oh][-1] #the N or F of the state of FST1
        fState2 = listOfValues3[ya][-1] #the N or F of FST2
        
        if(i == numOfvalues):
            i = 0
        else:
            pass
            
        listOfValues4 = listOfValues3[ya]
        res2 = listOfValues4
        result2 = res2[0]
        
        variable2 = 0
        variable3 = 0
        inputStr = 0
        state1 = 1
        variable2 = result[i]
        variable3 = (variable2[2])
        inputStr = variable2[1]
        state1 = variable2[0]
            
            
        q = 0
        variable11 =0
        variable33 = 0
        variable44 = 0
        state = 0
        variable11 = result2[i]
        variable33 = variable11[1] 
        variable44 = variable11[2]
        state = variable11[0]
        if(variable33 == variable3):
            added = variable44
        else:
            q = 0
            q = i + 1
            variable11 = result2[q]
            variable33 = variable11[1]
            variable44 = variable11[2]
            state = variable11[0]
            if(variable33 == variable3):
                added = variable44
            else:
                q = i +1
                variable11 = result2[q]
                variable33 = variable11[1]
                variable44 = variable11[2]
                state = variable11[0]
        stateTotal = 0
        stateTotal = state1 + state
    
        trial.append((stateTotal, inputStr, added))
            
        
        i = i + 1
        
        l = listOfKeys[oh]
        r = listOfKeys2[ya]
        
        d[l,r].append(trial)
        
        if(n % numOfvalues == 0):
            if(fState == 'F' and fState2 == 'F'):
                d[l,r].append('F')
                #f.write('F' + "\n")
            else:
                d[l,r].append('N')
        
        if(g % numOfvalues == 0 and g != 0):
            if(fState == 'F' and fState2 == 'F'):
                f.write(str(oh + 1)+str(ya + 1) + " " + 'F' + "\n")
            else:
                f.write(str(oh + 1)+str(ya + 1) + " " + 'N' + "\n")
    
        if(w < numStates):
            w = w +1
        else:
            if(w == numStates and t == numStates1):
                w = 1
            else:
                t = t + 1
        if(n%numOfvalues == 0):      
            if(oh < 1):
                oh = oh +1
            else:
                if(oh == 1 and ya == 1):
                    oh = 0
                else:
                    ya = ya + 1
        n = n + 1
        g = g + 1
        j = j + 1
        
        
        f.write("  " + str(inputStr) + " " + str(added) + " " + str(stateTotal) + "\n")
        #d[l,r].append(trial)
    return ((d))
       
    
  
def reconstructUpper(l, F):
    #Print the set of upper strings associated with lower string l by FST F.
    
    FST = readFST(F)
    
    listOfValues = list(FST.values()) #getting a list of all values
    
    u = ""
    
    k = 0
    
    state = 1 #always start in the first state
    
    
   
    
    count = 0 # number of transitions
    
    
    while(l != ""): # loop through until l is emptey
    
        listOfValues2 = listOfValues[int(state) - 1]# starting is state one and going foward in states when the transducer moves
        listOfValues2 = listOfValues2[0]
        numListOfValues2 = len(listOfValues2) #how many values that are associated with the given key
        if(k>(numListOfValues2 - 1)):
            #return("The set of upper strings is not in the language of the transducer")
            break
        else:
            list3 = listOfValues2[k][1]#always getting the lower string from a l/u pair
    
        q = listOfValues2[-1]#the final state of the state that we are in
    
    
        #the lower string is emptey and we are in a final state
        if(not l and q == "F"):
            return (u)
            
        #the lower string is emptey and we are not in a final state
        elif(not l and q != "F"):
            return
        
        else:
            first = l[0]
            if(first == list3):
                add = listOfValues2[k][2]
                u = u + add
                state = listOfValues2[k][0]
                l = l[1:]
                k = 0
                count = count + 1 #increment the number of transitions
                
            else:
                k = k + 1
    
    return((u))  
    
    

def reconstructLower(u, F):
    #Print the set of lower strings associated with upper string l by FST F.
    
    FST = readFST(F)
    
    listOfValues = list(FST.values()) #getting a list of all values
    
    numListOfValues = len(listOfValues)
    
    l = ""
    
    state = 1 #always start in state 1
    
    k = 0
    
    count = 0 # number of transitions
    
    while(u != ""): # loop through until l is emptey
    
        listOfValues2 = listOfValues[int(state) - 1 ]# starting is state one and going foward in states when the transducer moves
        listOfValues2 = listOfValues2[0]
        numListOfValues2 = len(listOfValues2) #how many values that are associated with the given key
        if(k>(numListOfValues2-1)):
        #if(k >= len(listOfValues[int(state)-1])):
            return("The set of upper strings is not in the language of the transducer")
            break
        else:
            list3 = listOfValues2[k][2]#always getting the upper string from a l/u pair
    
        q = listOfValues2[-1]#the final state of the state that we are in
    
    
        if(not u and q == "F"): #upperstring is emptey and we are in a final state
            return (l)
            
        elif(not u and q != "F"): #upperstring is emptey but we are not in a final state
            return
        
        else:
            first = u[0]
            if(first == list3):
                add = listOfValues2[k][1] #add the lower element to the string
                l = l + add
                state = listOfValues2[k][0]
                u = u[1:]
                k = 0
                count = count + 1 #increment the number of transitions
                
            else:
                k = k + 1
    
    return(l)  
    





        
       
   
i = 3  
j = 1

#taking the lexical forms or the surface form depending on the command line argument
#also reading the word.lex and word.srf file depending on the command line
#doing different things depending on if one one file is entered commared to 
#if multiple files are entered in the command line

if(sys.argv[1] == 'lexical'):
    f = open(sys.argv[2], 'r')
    line = f.readlines()
    lengthWordLex = len(line)
    if(len(sys.argv) == 4):
        while(j < lengthWordLex+1):
            line2 = line[j-1]
            mine3 = reconstructUpper(line2,F = sys.argv[3])
            print("Surface form:" + line2  +"Reconstructed lexical forms:" + mine3 +"\n")
            j = j + 1
    if(len(sys.argv) >= 4):
        f = open(sys.argv[2], 'r')
        line = f.readlines()
        lengthWordLex = len(line)
        #while(i <= length):
    else:
        line2 = composeFST(F1 = sys.argv[3], F2 = sys.argv[-1])
        mine3 = reconstructLower(line2,F = line2)
        print("Surface form:" + line2 + "\n" + "Reconstructed lexical forms:" + mine3 +"\n")
        #i = i + 1

     
if(sys.argv[1] == 'surface'):
    f = open(sys.argv[2], 'r')
    line = f.readlines()
    lengthWordLex = len(line)
    if(len(sys.argv) == 4):
        while(j < lengthWordLex):
            line2 = line[j].strip()
            mine3 = reconstructLower(line2,F = sys.argv[3])
            print("Lexical form:" + line2 + "\n" + "Reconstructed Surface forms:" + mine3 +"\n")
            
            j = j + 1
    if(len(sys.argv) >= 4):
        f = open(sys.argv[2], 'r')
        line = f.readlines()
        lengthWordLex = len(line)
        #while(i <= length):
    else:
        line2 = composeFST(F1 = sys.argv[3], F2 = sys.argv[-1])
        mine3 = reconstructLower(line2,F = line2)
        print("Lexical form:" + line2 + "\n" + "Reconstructed Surface forms:" + mine3 +"\n")
            #i = i + 1


#test functions to see if the methods were working
 
'''
mine = readFST("vcuPlu.fst")
mine1 = readFST("composed.txt")
mine2 = composeFST(F1 = "test1.fst",F2 = "test2.fst") 
mine3 = reconstructUpper(l = "tosPtpS",F = "delplu1.fst")
mine4 = reconstructLower("tp-tpS", F = "delplu1.fst")
print (mine2)
#print (mine1)
'''
