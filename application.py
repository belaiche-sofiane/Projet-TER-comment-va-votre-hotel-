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

@app.route('/')  # route qui a pour chemin / vers la page d'accueil
def recherche_1(): 
   print('/recherche_1')
   return render_template('base.html') # renvoie la page HTML base.html (c'est la page d'accueil)
@app.route('/recherche/accueil')
def accueil():
    return render_template('base.html')


@app.route('/recherche/', methods=['POST','GET'])
def recherche():
   if request.method           == 'POST':
        critere = request.form['critere']
         
        stockResultats =[] 
        resultats={}  
        FirstSentence = [] 
        dicADJ = {}
        dicAdj_Index_polarite = {}  
        liste_adverbes = [] 
        liste_adjectifs = []  
        LesNoms_Index = []
        liste_valeurs_adv =[] 
        Nouns  = [] 
        SecondSentence = [] 
        listeAdv_Index_valeurs = [] 
        listeAdj_Index_valeurs = []
        firstRound =[]
        secondRound =[]  
        dicADV = {} 
        verbesEtat =[] 
           
        LaNegation = [" ne "," n'"," non "," pas "] # pour la négation
        Liste_Rsultats_stockes =[] 
        import re
        morceaux = re.split(', | et |; | or | \. ',critere)  # conjonctions de coordinations utilisées pour séparer les morceaux
        criteres = critere.split()
        
        ListeCriteres = list(criteres)
        LesAdjectifs= [] 
        LesAdverbs = []
        tagList = []
        LesNoms = []
        Noms_Resultats = {}  
        ListeAdverbs = []
        ListeAdjectifs = [] 
        listeresultats = []  
        listeadv =[]
        LesVerbes =[] 
        dicResultats =[]
        avisPositif =[]
        avisNegatif =[] 
                      
        with open('Data/data.json') as json_data:  # ouverture de fichier des polarites pour les adjectifs
            Adjectif_dict = json.load(json_data)

        with open('Data/lexique.json') as data:  # ouverture de fichier lexique intensifieure pour les adverbes
            Adverbe_dict = json.load(data)     

        with open('Data/verbes_etat.json') as verbes_etat:  # fichier des verbes d'etat
            verbess = json.load(verbes_etat)
            
        
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
            for pos in avisPositif:
                avisPositif.remove(pos)
            for neg in avisNegatif:
                avisNegatif.remove(neg)
            
            
            tagss = pos_tag(morceau) # fonction pos_tag gére l'etiquettage des phrases
           
            print("\nmorceau:", morceau, "tagss:", tagss)
            tagList.append(tagss) 
            
            for tag in tagss:
                
                if tag[1] == "A":
                    LesAdjectifs.append(tag[0])  # ajout des adjectifs trouvés  dans une liste
                    ListeAdjectifs.append(tag[0]) # c'est une liste des adjectifs qu'on a utiliser pour l'affichage dans le navigateur
                elif tag[1] == "ADV" and tag[0] != "pas" and tag[0] != "ne" and tag[0] != "non" :   
                    LesAdverbs.append((index,tag[0])) # # ajout des adverbes trouvés  dans une liste
                    ListeAdverbs.append(tag[0])#c'est une liste des adverbes qu'on a utilisé pour l'affichage dans le navigateur
                   
                elif tag[1] == "N" and tag[0] != "or" :
                    LesNoms_Index.append((index, tag[0])) #ajout des noms avec leurs index dans une liste
                    LesNoms.append(tag[0])   # liste des noms qu'on a utilisé pour l'affichage
                    Nouns.append((index,tag[0]))
                elif tag[1] == "V":
                    LesVerbes.append(tag[0])  #  la liste des verbes

            for adjectif, polarite in Adjectif_dict.items(): # dictionnaire de fichier des mots polarisés                   
                for variable in LesAdjectifs:
                    if adjectif == variable:  #  si l'adjectif qu'on a saisi egale a l'adjectif qu'on a dans le fichier des mots polarisés
                        dicADJ.update({index:{adjectif:polarite}})  # dictionnaire de l'adjectif et sa valeur avec l'index
                                  
            for adverbe, valeur in Adverbe_dict.items():# dictionnaire de fichier lexique intensifieur
                for value in LesAdverbs:
                    if adverbe == value[1] : #  si l'adverbe qu'on a saisi egale a celui qu'on a dans le fichier des lexique intensifieur
                        if index == value[0]:
                            dicADV.update({index:{adverbe:valeur}}) 
                            listeadv.append((index,valeur))  # liste de l'index et la valeur de l'adverbe
                            
                        
            for indice, adjectif_polarite in dicADJ.items():
                for adjectif , sa_polarite in adjectif_polarite.items():
                    dicAdj_Index_polarite[indice] = sa_polarite   #  un dictionnaire de l'index et la polarite de l'adjectif
                   
            valeurAdj = 0
            
            for key , element in dicAdj_Index_polarite.items():
               if index == key: #  on récupére la polarite des adjectifs pour chaque index
                    valeurAdjectif = int(element)
                    valeurAdj = negation(valeurAdjectif) #application de la fonction negation sur la valeur de l'adjectif
                    listeAdj_Index_valeurs.append((key,valeurAdj)) #ajout de l'index et sa valeur dans la liste listeAdj_index_valeurs
                    listeAdj_Index_valeurs= list(set(listeAdj_Index_valeurs))  # suppression des doublons
                 
            for valeur in listeadv:
                if key == valeur[0]: #si l'adjectif et l'adverbe sont dans le meme morceau
                    liste_adjectifs.append((key,element)) # ajout de l'index et la valeur de l'adjectif dans la liste liste_adjectifs
                    liste_adjectifs = list(set(liste_adjectifs)) #suppression des doublons
                  
                    for adjectif in listeAdj_Index_valeurs:
                        for elem in liste_adjectifs:
                            if adjectif[0] == elem[0]:
                                listeAdj_Index_valeurs.remove(adjectif) # suppression des adjectifs qui sont dans le méme morceau que les adverbes de cette liste
                 
            valAdv = 0
            valAdj = 0
            totalAdv = 0
            totalAdj = 0
            res = 0

            for adv in listeadv:
                
                if index == adv[0]:  # pour chaque index on fait la somme des adverbes
                    valAdv = int(adv[1])
                    res = negation(valAdv) # utilisation la fonction negation
                    totalAdv += res 
            liste_valeurs_adv.append((index,totalAdv))  # l'ajout de total des valeurs des adverbes avec index dans une liste
            liste_valeurs_adv = list(set(liste_valeurs_adv))
            
            
            for adj in listeAdj_Index_valeurs:
                
                valAdj = int(adj[1])
                totalAdj += valAdj  #la somme des valeurs des adjectifs
               
            for verbe , value in verbess.items(): #fichier des verbes d'etat
                for vb in value:
                    if vb in morceau: # si y a un verbe d'etat dans le morceau traité
                        verbesEtat.append((index,vb))   # extraction des verbes d'etat
                        
            result = 0 
            val_adj = 0
            val_adv = 0
            total = 0          
            
            for adj in liste_adjectifs:
                val_adj = int(adj[1])
                
                for adv in liste_valeurs_adv:
                    val_adv = int(adv[1])
                    if adv[0] == adj[0]:   # si l'index de l'adjectif egale à l'index de la somme des adverbes on fait la multiplication(sommeadverbes * valeur adjectif)
                        total += val_adv * val_adj # multiplication des valeurs des adjectifs et adverbes si ils sont dans le méme morceau
             
                
            result = total  + totalAdj  # le total de tout
            
            listeresultats.append((index,result)) # la liste de l'index et resultats
            
            gf = 0
            variablle = 0
            resultat_premiere_phrase = 0
            resultat_seconde_phrase = 0
            resultat = 0
            a = 0
            for res in listeresultats:
                for veb in verbesEtat:
                    for nom in Nouns:
                        if res[0] < nom[0]:
                            if nom[0] == veb[0]:   #vérification la présence des verbes d'etat dans le morceau
                                
                                resultat_premiere_phrase = int(res[1] )  # résultat de premier morceau
                                
                    if res[0] >= nom[0]:
                        gf = int(res[1])
                        if nom[0] == veb[0]:  
                            
                            resultat_seconde_phrase = gf - resultat_premiere_phrase  #résultat de second morceau
                    
            for nom in Nouns:
                for rt in FirstSentence:
                    FirstSentence.remove(rt)  # suppression du contenu de la liste pour chaque index
                if nom[0] == 0:
                    FirstSentence.append((nom[1], resultat_premiere_phrase)) # la liste des noms avec leurs resultats final
                    FirstSentence= list(set(FirstSentence))
                    print("FirstPhrase ",FirstSentence)

                if nom[0] >= 0:
                    for phrase in SecondSentence:
                        SecondSentence.remove(phrase)# suppression du contenu de la liste pour chaque index
                    SecondSentence.append((nom[1], resultat_seconde_phrase ))# la liste des noms avec leurs resultats final
                    SecondSentence = list(set(SecondSentence)) 

            print("Secondphrase = ",SecondSentence)          
                       
                    
            print("result = ",result) 
            
                          
            for sentence in FirstSentence:
                Noms_Resultats[sentence[0]] = sentence[1]  # ajout des resultats de premier morceau dans un dictionnaire pour l'affichage dans le navigateur  
                 
            for phrase in SecondSentence:
                Noms_Resultats[phrase[0]] = phrase[1] # ajout des resultats de second morceau dans un dictionnaire pour l'affichage dans le navigateur 
                
            if index == 1:
                secondRound.append(resultat_seconde_phrase)
            if not LesAdjectifs:
                if not LesAdverbs:
                    for element in LesNoms_Index:
                        if index >= 0:
                            firstRound.append(element[1] )  # cette partie gére des phrases comme le jardin et la chambre sont propre
                           
            for first in firstRound:
                for second in secondRound:
                                  
                    Noms_Resultats[first] = second # ajout des resultats dans un dictionnaire pour l'affichage dans le navigateur
            
        with open('Data/dic.json') as ontologie:  #  ouverture de fichier ontologie
            ontologi = json.load(ontologie)
            fichier_ontologie = dict(ontologi)
        if isinstance(ontologi,dict):
            i = 0    
            for hi,gi in ontologi.items(): #hi est une clé , et gi est une valeur 
                if hi == 'hôtel':
                    for m in gi:
                        
                        if isinstance(m,dict):
                            for l,k in m.items():
                                for car, ko in Noms_Resultats.items():
                                    
                                    if car  == l:
                                        
                                        k.append(ko)
                                        i += ko 
                                        resultats[l] = ko        #toute cette partie pour parcourrir le fichier ontologie pour l'ajout des scores.
                                        
                                    for element in k:
                                        if isinstance(element,list):
                                            if car == element:
                                                for var in m.values():
                                                    if not var:
                                                        var.append(ko)
                                                        i += ko
                                                        resultats[element] = ko 
                                                     
                                        # elif isinstance(element,dict):
                                            
                                        #     for key , value in element.items():
                                        #         for b , n in Noms_Resultats.items():
                                        #                 if key == b:
                                        #                     if isinstance(value,list):
                                        #                         value.append(n)
                                        #                         value = list(set(value))
                                        #                         i += n

                                        #                         print("valllllllleeeeeue = ",value)
                                 
                                    else:    
                                        for x in k:
                                            if isinstance(x,dict):
                                                for n,a in x.items():
                                                   
                                                    for v, nr in Noms_Resultats.items():
                                                        if v == n:
                                                            if not a:
                                                                a.append(nr)
                                                                i += nr
                                                                resultats[n] = nr 
                                                        for element in a:
                                                            if v == element:
                                                                for variablle in x.values():
                                                                    if not variablle:
                                                                        variablle.append(nr)
                                                                        i += nr
                                                                        resultats[element]= nr 
                                                        else:
                                                            for v in a:
                                                                if isinstance(v,dict):
                                                                    for c,w in v.items():
                                                                        for tar,ju in Noms_Resultats.items():
                                                                            if tar  == c:
                                                                                if not w:
                                                                                    w.append(ju)
                                                                                    i += ju
                                                                                    resultats[c] = ju 
                                                                            for element in w:
                                                                                if tar == element:
                                                                                    for variable in v.values():
                                                                                        if not variable:
                                                                                            variable.append(ju)   
                                                                                            i += ju
                                                                                            resultats[element] = ju 
                                                                            else:
                                                                   
                                                                                for t in w: 
                                                                                    if isinstance(t,dict):
                                                                                        for cc,nn in t.items():   
                                                                                            for mar,nk in Noms_Resultats.items():
                                                                                                
                                                                                                if mar == cc:
                                                                                                    if not nn:
                                                                                                        nn.append(nk)
                                                                                                        i += nk
                                                                                                        resultats[cc] = nk 
                                                                                                for element in nn:
                                                                                                    if mar == element:
                                                                                                        for varia in t.values():
                                                                                                            if not (varia): 
                                                                                                                varia.append(nk)
                                                                                                                i += nk
                                                                                                                resultats[element] = nk 
       
        fichier_ontologie =  json.dumps(fichier_ontologie, indent=5, ensure_ascii=False).encode('utf8').decode()
        
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        d = client["TER_DataBase"] # creation d'une base de données
        col = d["customer"]
        dicResultats = dict(resultats) #ajout les resultats de traitement de chaque morceau dans un dictionnaire
        x = col.insert_one(dicResultats) #on insére le resultat dans la base de données
        for x in col.find():
            stockResultats.append(x) # ajout le résultat de la base de données dans une liste pour l'affichage dans le navigateur
                
        negatif = 0
        positif = 0
        r = 0
        for t in stockResultats:
            for key, value in t.items():
                if key == "_id":
                    tr = str(value)

            Liste_Rsultats_stockes.append(((tr,key,value))) # ajout de l'id + descripteur + score dans une liste
            Liste_Rsultats_stockes = list(set(Liste_Rsultats_stockes))
            
            for t in Liste_Rsultats_stockes:
                if t[1] == "_id" or t[2] == 0 :
                    Liste_Rsultats_stockes.remove(t)  # suppression des id de cette liste
        pos = 0
        neg = 0
        for n in Liste_Rsultats_stockes:    # séparation des avis positifs et négatifs
            if n[2] < 0:
                avisNegatif.append(n)
                avisNegatif = list(set(avisNegatif)) # la liste avec tous le scores des avis négatifs
                neg += n[2] # le total des avis négatifs
                negatif = len(avisNegatif) # pour calculer le nombre d'avis négatifs

            elif n[2] > 0:
                avisPositif.append(n) # la liste avec tous les scores des avis positifs
                avisPositif = list(set(avisPositif))
                pos += n[2] # le total des avis positifs
                positif = len(avisPositif) # le nombre d'avis positifs
        
        tot = 0
        tot = pos + neg #le total des avis positifs et négatifs
        negativevalue = neg * -1
              
            
        return render_template('recherche_1.html', pos=pos,neg=neg,tot=tot,Liste_Rsultats_stockes=Liste_Rsultats_stockes, negativevalue=negativevalue, tagList=tagList,dicADJ=dicADJ,dicADV=dicADV,i=i,positif=positif,negatif=negatif,Noms_Resultats=Noms_Resultats,LesVerbes = LesVerbes,fichier_ontologie=fichier_ontologie,ListeCriteres=ListeCriteres,LesNoms =LesNoms , ListeAdjectifs=ListeAdjectifs,ListeAdverbs=ListeAdverbs,LesNoms_Index=LesNoms_Index)
                  
app.run(debug=True)












