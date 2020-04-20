# -*- coding: utf-8 -*-

import os
import sys 
import json
import random  #gestion des aléas des dés
import time

import tkinter
from tkinter import ttk

import discord #module discord

import asyncio #gestion d'évènenment asynchrone pour discord
from threading import Thread # pour programmation parallèle


log = False
action = (0,0)
tpspool = 3


def printlog(monmsg):
    global log
    if log:
        print(monmsg)




class premiere_config(tkinter.Tk):
    def __init__(self, dico_conf):
        super().__init__() 
        self.dico_conf = dico_conf
        r = c = 0
        self.label1 = tkinter.Label(self,  text="Etape de configuration, Merci de renseigner les informations demandés ") #
        self.label1.grid(column = c, row = r)
        
        r+=1
        self.label2 = tkinter.Label(self,  text="Token du bot de l'appli à vérifier dans la secton developpeur:") #
        self.label2.grid(column = c, row = r) 
        
        r+=1
        self.CToken = tkinter.StringVar()
        self.CToken.set(self.dico_conf["token"])
        self.E_token = tkinter.Entry(self, textvariable = self.CToken, width = 65)
        self.E_token.grid(column = c, row = r)

        r+=1
        self.label3 = tkinter.Label(self,  text="Id du channel Discord ") #
        self.label3.grid(column = c, row = r) 
        
        r+=1
        self.CIdChan = tkinter.StringVar()
        self.CIdChan.set(self.dico_conf["id_chan"])
        self.E_IdChan = tkinter.Entry(self, textvariable = self.CIdChan, width = 65)
        self.E_IdChan.grid(column = c, row = r)




chemin = os.path.dirname(__file__)

#-------------------------------------------------------------
#test d'accès au fichier config 
#-------------------------------------------------------------
config = 'config.json'
cheminconfig = os.path.join(chemin, config)
try:
    with open(cheminconfig, "r") as source:
        dico_conf = json.load(source)
    token = dico_conf["token"]
    id_chan = dico_conf["id_chan"]
    log = dico_conf["log"]
    tpspool = dico_conf["tps_pool"]
    if tpspool <2:
        tpspool = 2
    printlog("Lecture fichier config réussi")

    
except:
    token = "Your secret token here / ton token d'application secret ici"
    id_chan = "L'ID du canal ici "
    log = True
    tpspool = 4

    printlog("Echec de lecture du fichier config, création automatique")
    
    dico_conf= {}
    dico_conf["token"] = token
    dico_conf["id_chan"] = id_chan
    dico_conf["log"] = False
    dico_conf["tps_pool"] = tpspool
    
    with open(cheminconfig, 'w') as source:
        json.dump(dico_conf,source, indent = 4)
    
prems = premiere_config(dico_conf)
prems.mainloop()

#-------------------------------------------------------------
#test d'accès au fichier pj
#-------------------------------------------------------------


chemin = os.path.dirname(__file__)
fichier = 'source.json'
cheminfichier = os.path.join(chemin,fichier)
try:
    with open (cheminfichier, "r") as source:
        dico_pj = json.load(source)
    printlog("chargement liste Pj")

    
except:
    dico_comp = {}
    dico_comp['escrime']= 1
    dico_comp['parade']= 1
    dico_carac={}
    dico_carac["Puissance"]=1
    dico_carac["Finesse"]=1
    dico_carac["Esprit"]=1
    dico_carac["Determination"]=1
    dico_carac["Panache"]=1
    pj1 = {}
    pj1["nom"] = "Noob"
    pj1["nation"] = "Noobland"
    pj1["carac"] = dico_carac
    pj1["comp"] = dico_comp

    dico_pj={}
    dico_pj["pj1"] = pj1
    dico_pj["pj2"] = pj1

    printlog("Absence de fichier PJ création automatique de source.json")
    printlog(str(dico_pj))
    with open(cheminfichier , 'w') as source:
        json.dump(dico_pj,source, indent = 4)
    

# création du client discord
client = discord.Client()

justearrived = True # pour générer un message à la connexion
affectation = {} #pour mémoriser qui à pris un pj
j = 0

#lance nb D10 si explose est valide, chaque 10 rajoute un D10 suplémentaire, (max 20) 
#retourne les résultats sous forme de liste
def brouette(nb, explose):
    nb = nbtot = min(10,nb)
    liste_de = []
            
    while nb > 0:
        nouveau_de = random.randint(1,10)
        liste_de.append(nouveau_de)
        if explose and nouveau_de == 10 and nbtot <=20 :
            nb +=1  
            nbtot +=1         
        nb -= 1
    
    return liste_de

#Calcul le nombre de mises d'une liste de dé 10
def nbmise (liste_de, difficulte):
    liste_de.sort() #on tri du plus petit au plus grand
    liste_mise = [] 
    
    nb_de_mise = 0
    while len(liste_de)>0: #tant qu'il y a des dés...
        plusfort = int (liste_de.pop()) #on prend le plus fort des dé en fin qe liste
        mise_encours = plusfort #on créer la somme de la premiere mise (pas forcement complete)
        mise = [] # on crée la liste de dé de la mise pour vérification
        mise.append(plusfort) # on y rajoute le premier dé
       
        while mise_encours < difficulte and len(liste_de)>0: #tant que la mise n'atteint pas son seuil
            # et tant qu'il y a des dé
            plusfaible = int(liste_de.pop(0)) # on recupere le plus faible
            mise_encours += plusfaible #on cumul pour connaitre la valeur de la mise encours
            mise.append(plusfaible) #on rajoute a la liste de verif


        if mise_encours >= difficulte:
            mise.sort()
            for de in mise:
                if mise_encours - de >= difficulte:
                    mise.remove(de)
                    mise_encours -= de
                    liste_de.append(de)
                    liste_de.sort()

            nb_de_mise += 1
        
        liste_mise.append(mise)
        
    texte_mise = ''
    for mise in liste_mise:
        for de in mise:
            texte_mise += str(de) + ' '
        texte_mise += '| '

        

    return nb_de_mise, texte_mise


@client.event
async def on_ready():
    monmsg = ('We have logged in as {0.user}'.format(client))
    printlog(monmsg)

@client.event
async def on_message(message):
    global justearrived
    if message.author == client.user:
        return   # pour ne pas se répondre à soi-même
    

    if message.content.startswith('$give'):
        requete = message.content
        decortique = requete.split()

        recup = dico_pj.get(decortique[1])
        if recup != None:
            affectation[str(message.author)[0:-5]] = recup['nom']
            monmessage = str(message.author)[0:-5] + ', vous êtes maintenant : ' + recup['nom']
            await message.channel.send(monmessage)

    elif message.content.startswith('$hello'):
        monmessage = 'Coucou pret à lancer vos dés !'
        await message.channel.send(monmessage)

    elif message.content.startswith('$help'):
        await message.channel.send('''
        Pour lancer un set de 7 dés il faut taper '$n 7' sans les guillemets
        - $n pour un jet normal (sans relance des 10)
        - $nd pour un jet normal (sans relance des 10) avec des groupes de 15 pour 1 mise
        - $ne pour un jet explosif (avec 1D en plus pour chaque 10)
        - $ned pour un jet explosif (avec 1D en plus pour chaque 10) avec des groupes de 15 pour 1 mise''')
        
    elif message.content.startswith('$n'):
        

        requete = message.content
        decortique = requete.split()


        if decortique[0] == "$n":
            explose = False
            difficulte = 10
        elif decortique[0] == "$nd":

            explose = False
            difficulte = 15
        elif decortique[0] == "$ne":
            explose = True
            difficulte = 10
        elif decortique[0] == "$ned":
            explose = True
            difficulte = 15


        if len(decortique)>1:
            
            nb = int(decortique[1])
            liste_de = brouette(nb, explose)

            nb , texte = nbmise(liste_de, difficulte)
            recupnom = affectation.get(str(message.author)[0:-5])
            if recupnom == None:
                recupnom = str(message.author)[0:-5]
                
            resultat = recupnom + ', vous avez ' + str(nb) + ' mise(s), ( | '+texte+')'
            
            await message.channel.send(resultat)

        else:
            await message.channel.send('pas compris !')

    elif message.content.startswith('$pj'):
        
        texte_li_pj = 'liste des Pj: \n'
        for key in dico_pj:
            nompj = dico_pj[key]
            texte_li_pj += key + ' : ' + nompj['nom'] + '\n'

        
        await message.channel.send(texte_li_pj)


@client.event
async def my_background_task():
    await client.wait_until_ready()
    global id_chan
    global action
    global justearrived 
    global tpspool
    global dico_conf
    print(id_chan)
    channel = client.get_channel(int(id_chan))
    await asyncio.sleep(tpspool) # task runs every 60 seconds

    if justearrived :
        monmessage = '''Je viens d'arriver, je ne vous ai pas manqué ?'''
        await channel.send(monmessage)
        monmessage = '''Pour rappel on me parle avec des $ et pour savoir si je suis pret '''
        await channel.send(monmessage)
        monmessage = '''faites $hello, sinon $help pour apprendre à me parler'''
        await channel.send(monmessage)
        justearrived = False

    count = 0
    while not client.is_closed():
        printlog("scrute : "+str(count))
        count += 1
        requete , corps = action
        if requete == 1:
            print(corps)
            monmessage = str(corps)
            await channel.send(monmessage)
            action = (0,0)
        
        
        await asyncio.sleep(tpspool) # task runs every 60 seconds


class mafen(tkinter.Tk):
    def __init__(self):
        super().__init__() 

        global dico_pj
        c=0
        r=0

        self.label1 = tkinter.Label(self,  text="Mon gestionnaire de campagne de la môôôôôôôrt !")
        self.label1.grid(column = c, row = r,columnspan = 5) 

        r +=1
        self.var1 = () 
        for key in dico_pj: 
            self.var1 = self.var1 + (key,)
        
        self.var2 = tkinter.StringVar() #permet de récuperer la station selectionnée 
        self.combo1 = ttk.Combobox(self, width=30, textvariable=self.var2,\
                                   values=self.var1, state ='readonly') #combobox de présentation des pj
        self.combo1.grid(column = 0, row = 1)
        r+=1

        self.btbefore = tkinter.Button(self,text="test", width = 2, command=self.test)
        self.btbefore.grid(row=r,column = c)

    def test(self):
        #my_background_task()
        global action
        if action == (0,0):
            action = (1,'test')

class class1(Thread):

    def __init__(self):
        Thread.__init__(self) 
        

    def run(self):
        global client
        client.loop.create_task(my_background_task())
        global dico_conf
        codesecret = dico_conf['token']
        client.run(codesecret)
        
class class2(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        self.fen = mafen()
        self.fen.mainloop()

# Création des threads
thread_1 = class1()
thread_2 = class2()

# Lancement des threads
thread_1.start()
thread_2.start()

# Attend que les threads se terminent
thread_1.join()
thread_2.join()
