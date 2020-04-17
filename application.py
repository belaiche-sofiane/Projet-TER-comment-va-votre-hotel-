#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import json
import re
import nltk
from flask import Flask, render_template, request  # importation des class de flask

from nltk.tag import StanfordPOSTagger

app = Flask(__name__)
os.system("clear")

root_path = "/home/e20160010106/projet teR NOUVEAU/StanfordTagguer/"
# instance de la classe StanfordPOSTagger en UTF-8
pos_tagger = StanfordPOSTagger(root_path + "/models/french.tagger",
                               root_path + "/stanford-postagger.jar", encoding='utf8')


def pos_tag(sentence):
    # je transforme la phrase en tokens => si vous avez un texte avec plusieurs phrases, passez d'abord par nltk pour récupérer les phrases
    tokens = nltk.word_tokenize(sentence)
    tags = pos_tagger.tag(tokens)  # lance le tagging
    print(tags)
    return tags

@app.route('/')  # route qui a pour chemin /
def recherche_1(): 
   print('/recherche_1')
   return render_template('recherche_1.html') # renvoie la page HTML recherche_1.html


@app.route('/recherche/', methods=['POST','GET'])
def recherche():
   if request.method           == 'POST':
        critere = request.form['critere']
          
         
        FirstPhrase = [] 
        dicADJ = {}
        dicAdj_Index_polarite = {}  
        dicADV_Index_Intensifieur = {}
        
        liste_adverbes = [] 
        liste_adjectifs = []  
        LesNoms_Index = []
     
        Nouns  = [] 
        SecondPhrase = [] 
         
        listeAdv_Index_valeurs = [] 
        listeAdj_Index_valeurs = []
 
        firstRound =[]
        secondRound =[]  
          
        LaNegation = [" ne "," n'"," non "," pas "] # pour la négation
        
        import re
        
        morceaux = re.split(', | et |; | or | par contre  ',critere)
        
        
        
        criteres = critere.split()
        
        ListeCriteres = list(criteres)
         
        dicADV = {} 
        LesAdjectifs= [] 
        LesAdverbs = []
        tagList = []
        LesNoms = []
        Noms_Resultats = {}  
        
        ListeAdverbs = []
        ListeAdjectifs = [] 
         
         
        listeresultats = []  
               
        with open('Data/data.json') as json_data:  # ouverture de fichier des polarites pour les adjectifs
            data_dict = json.load(json_data)

        with open('Data/lexique.json') as data:  # ouverture de fichier lexique intensifieure pour les adverbes
            dictt = json.load(data)     

        with open('Data/verbes_etat.json') as verbes_etat:  # fichier des verbes d'etat
            verbes = json.load(verbes_etat)
        
        index = 0

        for index, morceau in enumerate(morceaux): # morceau et son index

            def negation(variable):  #c'est une fonction qui gére la négation
                
                v = 0
                val = int(variable)
                for var in LaNegation:
                    if var in morceau: # morceau = c'est une phrase séparée par un ou deux conjonctions de coordination
                        v = val * -1
                    else:
                        v = val * 1
                return v  #retourne la valeur négative ou positive

            for adj in LesAdjectifs:
                LesAdjectifs.remove(adj) # suppression du contenu de la liste pour le 2émé morceau(phrase)
            for adv in LesAdverbs:
                LesAdverbs.remove(adv)  # //  //   //
            for nom in LesNoms_Index:
                LesNoms_Index.remove(nom) # // //   //
            
        
            
            tagss=pos_tag(morceau) # fonction pos_tag gére l'etiquettage des phrases
           
            print("\nmorceau:", morceau, "tagss:", tagss)
            tagList.append(tagss) 
            
            for tag in tagss:
                
                if tag[1] == "A":
                    LesAdjectifs.append(tag[0])  # ajout des adjectifs trouvées  dans une liste
                    ListeAdjectifs.append(tag[0]) # c'est une liste des adjectifs qu'on a utiliser pour l'affichage dans le navigateur
                elif tag[1] == "ADV" and tag[0] != "pas" and tag[0] != "ne" and tag[0] != "non" :   
                    LesAdverbs.append(tag[0]) # # ajout des adverbes trouvées  dans une liste
                    ListeAdverbs.append(tag[0])#c'est une liste des adverbes qu'on a utiliser pour l'affichage dans le navigateur
                   
                elif tag[1] == "N" :
                    LesNoms_Index.append((index, tag[0])) #ajout des noms avec leurs index dans une liste
                    LesNoms.append(tag[0])   # liste des noms
                    print("nommmmmmmmmmmmmmmsssss=",LesNoms )
                    Nouns.append((index,tag[0]))
                

            

            for varr, nombre in data_dict.items():                    
                for val in LesAdjectifs:
                    if varr == val:
                        dicADJ.update({index:{varr:nombre}})  # dictionnaire de l'adjectif et sa valeur avec l'index
                        print("dicADJ===",dicADJ)
                                      
            for key, valeur in dictt.items():
                for value in LesAdverbs:
                    if key == value:
                        dicADV.update({index:{key:valeur}}) # dictionnaire de l'adverbe et sa valeur et son index
             
            for r , a in dicADJ.items():
                for tt , uu in a.items():
                    dicAdj_Index_polarite[r] = uu   #  un dictionnaire de l'index et la valeur de l'adjectif
                    
            
            for tt, oo in dicADV.items():
                for aa, ww in oo.items():
                    dicADV_Index_Intensifieur[tt] = ww   # un dictionnare de l'index et la valeur de l'adverbe
            
            valeurAdj = 0
            valeurAdv = 0
           
            
            for key , element in dicAdj_Index_polarite.items():
                if index == key:
                    yy = int(element)
                    valeurAdj = negation(yy) #application de la fonction negation sur la valeur de l'adjectif
                    listeAdj_Index_valeurs.append((key,valeurAdj)) #ajout de l'index et sa valeur dans la liste tweleve
                    listeAdj_Index_valeurs= list(set(listeAdj_Index_valeurs))
            



                for cle , valeur in dicADV_Index_Intensifieur.items():
                    if index == cle:
                        yy = int(valeur)
                        valeurAdv = negation(yy) # application de la fonction negation sur la valeur de l'adverbe
                        listeAdv_Index_valeurs.append((cle,valeurAdv)) #ajout de l'index et sa valeur dans la liste eleven  
                        listeAdv_Index_valeurs = list(set(listeAdv_Index_valeurs))

                    if key == cle: #si l'adjectif et l'adverbe sont dans le meme morceau
                        if index == cle:
                            f = int(valeur)
                            cc = negation(f) # application de la fonction negation sur la valeur de l'adverbe 

                            liste_adverbes.append((cle,cc))
                            liste_adverbes = list(set(liste_adverbes))
                       
                    
                        
                        liste_adjectifs.append((key,element)) # ajout de l'index et la valeur de l'adjecrif dans la liste
                        liste_adjectifs = list(set(liste_adjectifs))
                     
                    for el in listeAdv_Index_valeurs:
                        for sec in liste_adverbes:
                            if el[0] == sec[0]:
                                 
                                listeAdv_Index_valeurs.remove(el) # suppression des doublons
                                
                    for adjectif in listeAdj_Index_valeurs:
                        for elem in liste_adjectifs:
                            if adjectif[0] == elem[0]:
                                listeAdj_Index_valeurs.remove(adjectif) # suppression des doublons
                                
            valAdv = 0
            valAdj = 0
            totalAdv = 0 
            totalAdj = 0
           
            for adv in listeAdv_Index_valeurs:
                valAdv = int(adv[1])
                totalAdv += valAdv  # total des valeurs des adverbes
                
            for adj in listeAdj_Index_valeurs:
                valAdj = int(adj[1])
                
                totalAdj += valAdj # total des valeurs des adjectifs
             
            result = 0 
            val_adj = 0
            val_adv = 0
            total = 0          
            
            for adj in liste_adjectifs:
                for adv in liste_adverbes:
                    if adj[0] == adv[0]:
                        val_adj = int(adj[1])
                        val_adv = int(adv[1]) 
                        total += val_adj * val_adv # total des valeurs des adjectifs et des adverbes si ils sont dans la méme morceau
                            
                        
            result = total + totalAdv + totalAdj  # le total de tout
            print("result ==== ",result)
            
            listeresultats.append((index,result)) # la liste de l'index et resultats
            
            gf = 0
            variablle = 0
            resultat_premiere_phrase = 0
            resultat_seconde_phrase = 0
            resultat = 0
            i = 0
            
            for res in listeresultats:
                for nom in Nouns:
                    if res[0] < nom[0]:
                        resultat_premiere_phrase = int(res[1])  # resultats de la premiere phrase
                         
                    if res[0] >= nom[0]:
                        gf = int(res[1])
                        resultat_seconde_phrase = gf -  resultat_premiere_phrase # resultats des autres phrases
                     
            g = 0            
            for nom in Nouns:
                for rt in FirstPhrase:
                    FirstPhrase.remove(rt)
                if nom[0] == 0:
                    FirstPhrase.append((nom[1], resultat_premiere_phrase)) # la liste des noms avec leurs resultats final
                    FirstPhrase = list(set(FirstPhrase))
                    print("FirstPhrase ",FirstPhrase)

                if nom[0] >= 0:
                    for pom in SecondPhrase:
                        SecondPhrase.remove(pom)
                    SecondPhrase.append((nom[1], resultat_seconde_phrase ))# la liste des noms avec leurs resultats final
                    SecondPhrase = list(set(SecondPhrase)) 

            print("Secondphrase = ",SecondPhrase)          
                       
                    
            print("result = ",result) 
            
                          
            for pm in FirstPhrase:
                
                Noms_Resultats[pm[0]] = pm[1]  # ajout des resultats dans un dictionnaire pour l'affichage dans le navigateur  
                   
            for ls in SecondPhrase:
                
                Noms_Resultats[ls[0]] = ls[1] # ajout des resultats dans un dictionnaire pour l'affichage dans le navigateur 
            if index == 1:
                secondRound.append(resultat_seconde_phrase)
            if not LesAdjectifs:
                if not LesAdverbs:
                    for element in LesNoms_Index:
                        if index >= 0:
                            firstRound.append(element[1] )  # cette partie gére des phrases comme le jardin et la chambre sont propre
                           
            for tr in firstRound:
                for hg in secondRound:
                                  
                    Noms_Resultats[tr] = hg # ajout des resultats dans un dictionnaire pour l'affichage dans le navigateur
                


            
                                    

        with open('Data/dic.json') as ontologie:  #  ouverture de fichier ontologie
            ff = json.load(ontologie)
            mm = dict(ff)
        if isinstance(ff,dict):
            i = 0    
            for hi,gi in ff.items(): #hi est une clé , et gi est une valeur 
                if hi == 'hôtel':
                    for m in gi:
                        
                        if isinstance(m,dict):
                            for l,k in m.items():
                                for car, ko in Noms_Resultats.items():
                                    
                                    if car  == l:
                                        
                                        k.append(ko)
                                        i += ko                             # tous ca c'est un code pour parcourrir la hiérarchie du fichier ontologie
                                        
                                    for element in k:
                                        if isinstance(element,list):
                                            if car == element:
                                                for var in m.values():
                                                    if not var:
                                                        var.append(ko)
                                                        i += ko
                                        
                                 
                                    else:    
                                        for x in k:
                                            if isinstance(x,dict):
                                                for n,a in x.items():
                                                   
                                                    for v, nr in Noms_Resultats.items():
                                                        if v == n:
                                                            if not a:
                                                                a.append(nr)
                                                                i += nr
                                                        for element in a:
                                                            if v == element:
                                                                for variablle in x.values():
                                                                    if not variablle:
                                                                        variablle.append(nr)
                                                                        i += nr
                                                        else:
                                                            for v in a:
                                                                if isinstance(v,dict):
                                                                    for c,w in v.items():
                                                                        for tar,ju in Noms_Resultats.items():
                                                                            if tar  == c:
                                                                                if not w:
                                                                                    w.append(ju)
                                                                                    i += ju
                                                                            for element in w:
                                                                                if tar == element:
                                                                                    for variable in v.values():
                                                                                        if not variable:
                                                                                            variable.append(ju)   
                                                                                            i += ju
                                                                            else:
                                                                   
                                                                                for t in w: 
                                                                                    if isinstance(t,dict):
                                                                                        for cc,nn in t.items():   
                                                                                            for mar,nk in Noms_Resultats.items():
                                                                                                
                                                                                                if mar == cc:
                                                                                                    if not nn:
                                                                                                        nn.append(nk)
                                                                                                        i += nk
                                                                                                for element in nn:
                                                                                                    if mar == element:
                                                                                                        for varia in t.values():
                                                                                                            if not (varia): 
                                                                                                                varia.append(nk)
                                                                                                                i += nk
       
       
       
       
                    
       
        mm =  json.dumps(mm, indent=5, ensure_ascii=False).encode('utf8').decode()
                                                                                           
                                                                                        
                                                                                
                                                                               
                                                                                       
                                    
            

        return render_template('recherche_1.html', tagList=tagList,dicADJ=dicADJ,dicADV=dicADV,i=i, Noms_Resultats=Noms_Resultats, mm=mm,ListeCriteres=ListeCriteres,LesNoms =LesNoms , ListeAdjectifs=ListeAdjectifs,ListeAdverbs=ListeAdverbs,LesNoms_Index=LesNoms_Index)
                  
# else:
        # return render_template('recherche_1.html')
      
                  
app.run(debug=True)












