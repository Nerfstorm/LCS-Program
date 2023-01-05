from turtle import clear
from typing import List
from unicodedata import name

ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','t','f'] 
BinConnectors = ['=','$','|','&']
AtomicProps = dict()
ComplexPropsValues = []
PropOps = []
PropOpsAux=[]
v= True
MaxRank = 0


class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.rank = None
        self.leftChild = None
        self.rightChild = None
        self.operation = None
        self.value = None
        self.vanity = 0
    
    def PrintTree(self):
        if self.leftChild:
          self.leftChild.PrintTree()

        if self.rank == 0:
            print(self.rank,self.data,"("+str(self.operation)+")")
        elif self.parent.leftChild == self:
            print(" "*(self.parent.vanity)+" "*self.rank*9,"/",self.rank,self.data,"{"+str(self.operation)+"}")
        else:
            print(" "*(self.parent.vanity)+" "*self.rank*9,"\\",self.rank,self.data,"{"+str(self.operation)+"}")

        if self.rightChild:
            self.rightChild.PrintTree()

    def ComputeValue(self):
        for key in AtomicProps:
            if key == self.rightChild.data:
                self.rightChild.value = AtomicProps[key]

        if self.operation == "!":
            
            self.value = (self.rightChild.value*-1)+1
        else:
            for key in AtomicProps:
                if key == self.leftChild.data:
                    self.leftChild.value = AtomicProps[key]
            
            if self.operation == "&":

                self.value = self.leftChild.value * self.rightChild.value
            elif self.operation == "|":

                self.value = (self.leftChild.value+self.rightChild.value)
                if self.value > 1:
                    self.value -= 1

            if self.operation == "=":
                if self.leftChild.value == self.rightChild.value:
                    self.value = 1
                else:
                    self.value = 0

            if self.operation == "$":
                if self.leftChild.value == 0:
                    self.value = 1
                elif self.rightChild.value == 1:
                    self.value = 1
                else:
                    self.value = 0

    def ReturnNodes(self):
        if self.leftChild:
            self.leftChild.ReturnNodes()      

        if self.rightChild:
            self.rightChild.ReturnNodes()

        if self.data not in PropOps and len(self.data)>1 and self.data != "end":
            PropOps.append(self.data)

    
    def ReturnRowVallues(self):
        #print(PropOpsAux)
        #print (self.data)
        if self.leftChild:
            self.leftChild.ReturnRowVallues()      

        if self.rightChild:
            self.rightChild.ReturnRowVallues()

        if self.data not in PropOpsAux and len(self.data)>1 and self.data != "end":
            PropOpsAux.append(self.data)
            self.ComputeValue()
            ComplexPropsValues.append(self.value)
    

def AddLeftChild(node,i,):

    node.leftChild = Node(node.data[1:i])
    node.leftChild.rank = node.rank + 1
    node.leftChild.parent = node
    node.vanity = int(node.parent.vanity) + int(len(node.data))

def AddLeftNone(node):

    node.leftChild = Node("end")
    node.leftChild.rank = node.rank + 1
    node.leftChild.parent = node
    node.vanity = int(node.parent.vanity) + int(len(node.data))

def AddRightChild(node,i):

    node.rightChild = Node(node.data[i+1:-1])
    node.rightChild.rank = node.rank + 1
    node.rightChild.parent = node
    node.vanity = int(node.parent.vanity) + int(len(node.data))

def CreateChildren(node):

    global MaxRank
    if node.rank>MaxRank:
        MaxRank = node.rank

    if(node.data[0] == '(' and node.data[-1] == ")" ):
        rang = -1
        for i in range(0,len(node.data)):
            if node.data[i] == "(":
                rang +=1
            elif node.data[i] == ")":
                rang -=1
            elif node.data[i] in BinConnectors and rang == 0:
                node.operation = node.data[i]
                AddLeftChild(node,i)
                CreateChildren(node.leftChild)
                AddRightChild(node,i)
                CreateChildren(node.rightChild)
                break
            elif node.data[i] == "!" and rang == 0:
                node.operation = "!"
                node.value = node.data[i]
                AddLeftNone(node)
                AddRightChild(node,i)
                CreateChildren(node.rightChild)
                break
    elif (len(node.data) == 1):
        if node.data in ALPHABET:
            AtomicProps[node.data] = None
    else:
        global v
        v = False

def Rewriting(Sentence):
    Sentence = Sentence.replace("⇔", "=")
    Sentence = Sentence.replace("⇒", "$") 
    Sentence = Sentence.replace("∧", "&")
    Sentence = Sentence.replace("∨", "|")
    Sentence = Sentence.replace("¬", "!")
    Sentence = Sentence.replace(" ", "")
    Sentence = Sentence.replace("⊥", "f")
    Sentence = Sentence.replace("⊤", "t")
    return(Sentence)

def BKT(i):
    for j in range (0,2):
        PropVarAux[i] = j
        if(i==len(PropVarAux)-1):
            #print(PropVarAux) ### trebe continuat cu restul tabelului
            PrintRow()
        else:
            BKT(i+1)

def PrintRow():
    SVanity = 0
    i=0
    print(end="|")
    SVanity += 1
    for key in AtomicProps:
        AtomicProps[key] = PropVarAux[i] #useful
        print(end = str(AtomicProps[key])+"|")
        SVanity+= 3
        i+=1
    ComplexPropsValues.clear()
    PropOpsAux.clear()
    root.ReturnRowVallues()
    #print(AtomicProps) #Verifying
    for nr in range(0, len(ComplexPropsValues)-1):
        vanityy = len(PropOps[nr])//2
        SVanity += len(PropOps[nr])
        print(end=" "*(vanityy-1)+str(ComplexPropsValues[nr])+" "*(vanityy+(len(PropOps[nr])%2))+"|")
    vanityy = len(PropOps[-1])//2 + len(PropOps[-1]) % 2
    SVanity += len(PropOps[-1]) 
    print(end=" "*(vanityy-1)+str(ComplexPropsValues[-1])+" "*(vanityy+(len(PropOps[-1])%2))+"")
    #print(ComplexPropsValues)
    print("||")
    print("-"*SVanity)
    i=0
    



InputSentence = input()
print(">>>")
InputSentence = Rewriting(InputSentence)
print("Standardized:",InputSentence)
print(">>>")
root = Node(InputSentence)
root.rank = int(0)
root.parent = Node("NOT FOUND")
root.vanity = 0

CreateChildren(root)

if(len(AtomicProps) == 0 or v == False):
    print ("Error : Input is not WFF")

else:
    print (">>> Binary Tree >>>")
    root.PrintTree()            ### Binary tree
    print(">>>")

    print(">>>Variables>>>")
    print(AtomicProps) ### Atomic Propositions
    print(">>> TABLE >>>")
    
    PropVarAux = list(AtomicProps)
    root.ReturnNodes()   
    PropSentences = PropVarAux+PropOps
    print(end="|")
    for i in range(0,len(PropSentences)):
        if i==len(PropSentences)-1:
            print(PropSentences[i],end="|",)
            print()
        else:
            print (PropSentences[i],end="|")
    #print(PropOps)
    PropKey = list(AtomicProps)
    BKT(0)
    print("**Table estethics are work in progress**") # the svanityy is work in progress,
    print(">>>")
    print(PropKey, "MaxRank = ", str(MaxRank))

    root.ReturnNodes()
