# -*- coding: utf-8 -*-

import os
import sys 
import json
import random  #gestion des aléas des dés
import time

from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore

import discord #module discord
import asyncio #gestion d'évènenment asynchrone pour discord
from threading import Thread # pour programmation parallèle

#-------------------------------------------------------------
# Variable "globale"
#-------------------------------------------------------------

log = False
action = (0,0)
tpspool = 3


#-------------------------------------------------------------
# fonction de suivi
#-------------------------------------------------------------

def printlog(monmsg):
    global log
    if log:
        print(monmsg)

#--------------------------------------------------------------------------
mon_style = '''
                            QWidget {
                                background-color : #202020;
                                color : #DFDFDF;
                                border-color : #7F7F7F;
                                }
                            QPushButton {
                                border-style: outset;
                                border-width: 1px;
                                border-radius: 10px; 
                                border-color: #7F7F7F;
                                font: bold 14px;
                                min-width: 3em;
                                padding: 6px;
                                }
                            QPushButton:pressed{
                                background-color: #777777;
                                color : black;
                                border-style: inset;
                                }
                            QComboBox {
                                color : #505050 ;
                                border: 1px solid ;
                                border-color: #7F7F7F; 
                                border-radius: 3px;
                                padding: 6px;
                                min-width: 6em;
                                }
                            QComboBox:enabled{
                                color : #DFDFDF ;
                                border: 1px solid ;
                                border-color: #7F7F7F; 
                                border-radius: 3px;
                                padding: 6px;
                                min-width: 6em;
                                }
                            QProgressBar {
                                background-color : #202020;
                                color : #7F7F7F;
                                border: 1px solid ;
                                border-color: #7F7F7F; 
                                border-radius: 3px;
                                padding: 6px;
                                }
                            QLineEdit {                
                                border: 1px solid ;
                                border-color: #7F7F7F; 
                                border-radius: 3px;
                                }
                            QCheckbox{
                                border: 1px solid ;
                                border-color: #7F7F7F; 
                                border-radius: 3px;
                                }'''

app = QtWidgets.QApplication([])

#-------------------------------------------------------------
# déclaration fenetre de préconfiguration et de lancement
#-------------------------------------------------------------
  

class premiere_config(QtWidgets.QWidget):
    def __init__(self, dico_conf, mon_style):
        
        super(premiere_config, self).__init__()
        
        self.setStyleSheet(mon_style)     
        self.resize(300,200)
        self.setWindowTitle("Assistant de configuration")
        
        self.dico_conf = dico_conf
        r = c = 0
        
        self.grille = QtWidgets.QGridLayout(self)#exist en Hlayout et Vlayout

        
        self.lbl_1 = QtWidgets.QLabel('Etape de configuration, Merci de renseigner les informations demandés ',self)
        self.grille.addWidget(self.lbl_1, r,c,1,1)
        r+=1

        self.lbl_2 = QtWidgets.QLabel("Token du bot de l'appli à vérifier dans la secton developpeur:")
        self.grille.addWidget(self.lbl_2, r,c,1,1)           
        r+=1
        
        self.le_token = QtWidgets.QLineEdit()
        self.le_token.setText(self.dico_conf["token"])
        self.grille.addWidget(self.le_token, r,c,1,1)           
        r+=1

        self.lbl_3 = QtWidgets.QLabel("Id du channel Discord:")
        self.grille.addWidget(self.lbl_3, r,c,1,1)           
        r+=1
        
        self.le_idchan = QtWidgets.QLineEdit()
        self.le_idchan.setText(self.dico_conf["id_chan"])
        self.grille.addWidget(self.le_idchan, r,c,1,1)           
        r+=1

        self.valid = False
        self.btn_valid = QtWidgets.QPushButton('Ok',self)     
        self.btn_valid.clicked.connect(self.clique)
        self.grille.addWidget(self.btn_valid, r,c,1,1)           
        r+=1

        QtWidgets.QShortcut(QtGui.QKeySequence('Esc'), self, self.close)

    def clique(self):
        self.close()
  

class choix_system(QtWidgets.QWidget):
    def __init__(self, mon_style):
      
        super(choix_system, self).__init__()
        
        self.setStyleSheet(mon_style)     
        self.resize(300,50)
        self.setWindowTitle("Choix crucial!")
        self.choix = 0
        self.r = self.c = 0

        self.grille = QtWidgets.QGridLayout(self)#exist en Hlayout et Vlayout

        self.lbl_1 = QtWidgets.QLabel('Que voullez-vous faire ? ',self)
        self.grille.addWidget(self.lbl_1, self.r,self.c,1,2)
        self.r += 1

        self.rad_new = QtWidgets.QRadioButton('Nouvelle campagne', self)
        self.rad_new.toggled.connect(self.bascul)
        self.grille.addWidget(self.rad_new, self.r,self.c,1,1)
        self.rad_old = QtWidgets.QRadioButton('Poursuivre', self)
        self.rad_old.setChecked(True)
        self.grille.addWidget(self.rad_old, self.r,self.c+1,1,1)
        self.r += 1

        self.cmb_1 = QtWidgets.QComboBox()
        self.cmb_1.addItems(['7seaV2','DK²'])
        self.cmb_1.setCurrentIndex(0)
        self.cmb_1.setEnabled(False)
        #self.cmb_1.setVisible(False)
        self.grille.addWidget(self.cmb_1, self.r,self.c,1,2)
        self.r += 1

    def bascul(self):
        recup = self.sender()
        self.cmb_1.setEnabled(recup.isChecked())
  

class mafen(QtWidgets.QWidget):
    def __init__(self,mon_style):
        super(mafen, self).__init__()
        self.resize(300,150)
        self.setWindowTitle('Enjoy your campagne')
        self.setStyleSheet(mon_style)  

        global dico_pj

        r=c=0
        
        
        self.grille = QtWidgets.QGridLayout(self)#exist en Hlayout et Vlayout


        
        self.lbl_1 = QtWidgets.QLabel("Mon gestionnaire de campagne de la môôôôôôôrt !",self)
        self.grille.addWidget(self.lbl_1, r,c,1,5)
        r += 1

        self.cmb_1 = QtWidgets.QComboBox()
        for key in dico_pj: 
            if not key == "system":
                print(str(key))
                self.cmb_1.addItem(str(key))
        self.cmb_1.setCurrentIndex(0)
        self.grille.addWidget(self.cmb_1, r,c,1,2)
        r+=1


        self.btn_test = QtWidgets.QPushButton('test',self ) #Flat = True     
        self.btn_test.clicked.connect(self.test)
        self.grille.addWidget(self.btn_test, r,c,1,2)
        r+=1
        

    def test(self):
        #my_background_task()
        global action
        if action == (0,0):
            action = (1,'test')
            
        
    

#-------------------------------------------------------------
# On regarde où on est
#-------------------------------------------------------------

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
    #-------------------------------------------------------------
    # si pas de config alors on en créer un
    #-------------------------------------------------------------
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
    
    fenetre = premiere_config(dico_conf,mon_style)
    fenetre.show()
    app.exec_()


#-------------------------------------------------------------
#test d'accès au fichier pj
#-------------------------------------------------------------


chemin = os.path.dirname(__file__)
fichier = 'source.json'
cheminfichier = os.path.join(chemin,fichier)


fenetre = choix_system(mon_style)
fenetre.show()
app.exec_()

try:
    with open (cheminfichier, "r") as source:
        dico_pj = json.load(source)
    printlog("chargement liste Pj")

    
except:
    #-------------------------------------------------------------
    # si pas de fichier source alors on en créer un bidon
    #-------------------------------------------------------------
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
    dico_pj["system"] = "7seaV2"
    dico_pj["pj1"] = pj1
    dico_pj["pj2"] = pj1

    printlog("Absence de fichier PJ création automatique de source.json")
    printlog(str(dico_pj))
    with open(cheminfichier , 'w') as source:
        json.dump(dico_pj,source, indent = 4)
    
#-------------------------------------------------------------
# création du client discord
#-------------------------------------------------------------
client = discord.Client()

justearrived = True # pour générer un message à la connexion
affectation = {} #pour mémoriser qui à pris un pj
j = 0
#-------------------------------------------------------------
# fonction outils pour bot discord
#-------------------------------------------------------------

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

#-------------------------------------------------------------
# fonction asyncio de bot discord
#-------------------------------------------------------------

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
        - $ned pour un jet explosif (avec 1D en plus pour chaque 10) avec des groupes de 15 pour 1 mise
        Pour agir avec les PJ:
        - $pj pour voir la liste des pj
        - $give pj1 recevoir un pj
        ''')
        
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
        requete = message.content
        if requete == '$pj':
                    
            texte_li_pj = 'liste des Pj: \n'
            for key in dico_pj:
                if not key == "system":
                    nompj = dico_pj[key]
                    print(nompj)
                    texte_li_pj += key + ' : ' + nompj['nom'] + '\n'
            await message.channel.send(texte_li_pj)

        elif len(requete) > 3 :
            num_pj = requete[3:len(requete)]
            
            monmessage = str(dico_pj['pj'+num_pj])
            await message.channel.send(monmessage)
        else:
            await message.channel.send('''$pj d'accord mais $pj combien  ?''' )
        

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
    await asyncio.sleep(tpspool) #

    liste_blague = ['''Staying alive, staying a live. Ah, ah ah....''',\
                    '''Inserez une blageu ici''',\
                    '''Pour ce que j'en dit il faudrais mieux que je me taise''']

    liste_intro=['''Je viens d'arriver, je ne vous ai pas manqué ?''',\
            '''Poypoy ! Pour rappel on me parle avec des $ ''',\
            '''Faites $help pour apprendre à me parler''',\
            '''Eh Lanceur est arrivééé, sans se préceeeeerrrr...''']
    if justearrived :

       
        random.shuffle(liste_intro)
        await channel.send(liste_intro[0])
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
        if count % int(600/tpspool) == 0:
            
            random.shuffle(liste_blague)
            await channel.send(liste_blague[0])
             
        
        
        await asyncio.sleep(tpspool) # task runs every 60 seconds
      
            
#-------------------------------------------------------------
# création de class pour thread
#-------------------------------------------------------------

class class1(Thread):

    def __init__(self):
        Thread.__init__(self) 
        

    def run(self):
        global client
        client.loop.create_task(my_background_task())
        global dico_conf
        codesecret = dico_conf['token']
        print('007')
        client.run(codesecret)


# Création des threads
thread_1 = class1()


# Lancement des threads
thread_1.start()



fen = mafen(mon_style)
fen.show()
app.exec_()
# Attend que les threads se terminent
thread_1.join()

print('end of line')
