

#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os, json, re # import des modules 
import codecs
os.system("clear")  # effacer la ligne de commande


      
dic= {}
# dic['lexique']=  { mot: { 'polarite': polarite}}
# dic['lexique'][mot]=  { 'polarite': polarite}

dm = codecs.open('data.txt' , 'r', encoding='utf-8')

for ligne in dm.readlines():
    morceaux = ligne.split(":")
    mot = morceaux[0]
    polarite = morceaux[1].strip()
    print('mot:',mot, 'polarite: ',polarite)

    # dic['lexique'][mot]= polarite
    dic[mot] = polarite
    # dic['lexique'][mot]['polarite']=  polarite
print('dic:',dic)
with open('data.json', 'w') as jsonOut:
    json.dump(dic, jsonOut, indent=4)