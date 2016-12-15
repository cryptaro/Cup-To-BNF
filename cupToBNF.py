#!/usr/bin/python3
import os, sys
import re

## CUP File ##
cupFile=""

if len(sys.argv) > 1:
    cupFile = sys.argv[1]
else:
	cupFile = input("Entrez un chemin de fichier .cup : ");

fichierCUP = open(cupFile, "r");
allCupLines = fichierCUP.readlines();
fichierCUP.close();

cupContent = ""

beginFlag = False;
for line in allCupLines :
	if(beginFlag):
		cupContent+=line;
	else:
		# print(line)
		beginFlag = line.startswith("start with")

## CUP File ##
flexFile=""

if len(sys.argv) > 2:
    flexFile = sys.argv[2]
else:
	flexFile = input("Entrez un chemin de fichier .flex : ");

fichierFlex = open(flexFile, "r");
allFlexLines = fichierFlex.readlines();
fichierFlex.close();

flexContent = ""

beginFlag = False;
for line in allFlexLines :
	if(beginFlag):
		if(not line.startswith("%")):
			flexContent+=line;
	else:
		beginFlag = line.startswith("%eofval}")

## END File Parsing ##


# BEGIN REPLACE IN CUP #
BNF = cupContent
BNF = re.sub("{:(.|\s)*?:}", "", BNF) # on enleve les définitions des resultats
BNF = re.sub("\%.*", "", BNF) # on enleve les définitions des resultats
BNF = re.sub("//.*", "", BNF)
BNF = re.sub("/\*.*\*/", "", BNF)
BNF = re.sub("[\t ]*([\w\_\d]+):[\w\_\d]+[\t ]*", r"<\1> ", BNF) #enleve les espaces
BNF = re.sub("([\w\_\d]+)\s*::=\s*", r"<\1> ::= ", BNF) 
BNF = re.sub("(\n|\r)+\s*(\n|\r)*", r"\n", BNF) 
BNF = re.sub("(\n\|)\s*", "\n | ", BNF) 

# check for token replace #


flexContent = re.sub("//.*", "", flexContent)
flexContent = re.sub("/\*.*\*/", "", flexContent)
marker = "&&&&-->"
flexContent = re.sub("\n\"(.*?)\"\s*{((.|\s)*?)\(((.|\s)*?)\,((.|\s)*?)\.((.|\s)*?)(,((.|\s)*?))*?\)(.*?)}",r"\n\1 "+marker+" \8" ,flexContent)
# flexContent = re.sub("\n\"(.*?)\"\s*{(.*?)\((.*?)\)(.*?)}",r"\n\1 \3" ,flexContent)
# print(flexContent)

listToken = []
for line in flexContent.split("\n"):
	if(marker in line):
		print(line+"\n")

# print(BNF)