# -*- coding: utf-8 -*-

import os
import sys 
import json
import random 
import time

from functools import partial
from PySide2 import QtWidgets, QtGui, QtCore

import discord #module discord
import asyncio #gestion d'évènenment asynchrone pour discord
from threading import Thread # pour programmation parallèle

#-------------------------------------------------------------
# Variable "globale" bouh pas bien ! Je sais
#-------------------------------------------------------------

log = False
action = (0,0)
tpspool = 3
ralentisseur = 0
dico_pj = {}

#-------------------------------------------------------------
# fonction de suivi
#-------------------------------------------------------------

def printlog(monmsg):
    global log
    if log:
        print(monmsg)

#--------------------------------------------------------------------------

app = QtWidgets.QApplication([])

#-------------------------------------------------------------
# déclaration fenetre GUI
#-------------------------------------------------------------
class fen_chargement(QtWidgets.QWidget):
    def __init__(self,app):
        super(fen_chargement,self).__init__()

        self.setWindowTitle("Loadiiiiiiinnnng")
        self.resize(300,100)

        self.mon_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_etape = QtWidgets.QLabel('début du chargement')

        self.mon_layout.addWidget(self.lbl_etape)

        self.val_etape = 0
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setRange(0,3)
        self.progressbar.setValue(self.val_etape)
        self.progressbar.setTextVisible(False)
        
        self.mon_layout.addWidget(self.progressbar)

        self.show()


        QtWidgets.QApplication.processEvents()

        self.chargement_style()
        self.chargement_config()
        self.chargement_source()
        self.close()
        
    
    def chargement_style(self):
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Le faire avec style')
        time.sleep(ralentisseur)
        self.update()
        global mon_style
        config = 'style.css'
        chemin = os.path.dirname(__file__)
        cheminconfig = os.path.join(chemin, config)
        try:
            with open(cheminconfig, "r") as fstyle:
                mon_style = fstyle.read()

            self.progressbar.setValue(self.val_etape)
            time.sleep(ralentisseur)
            self.update()
            
   
        except:
            mon_style = ''  

    def chargement_config(self):
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Savoir communiquer')
        self.update()
        time.sleep(ralentisseur)
        global dico_conf
        global token
        global id_chan
        global log
        global tpspool
        
        chemin = os.path.dirname(__file__)
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

            
            self.progressbar.setValue(self.val_etape)
            self.update()
            time.sleep(ralentisseur)
            
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
            
    def chargement_source(self):
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Savoir de quoi on parle !')
        self.update()
        time.sleep(ralentisseur)

        chemin = os.path.dirname(__file__)
        fichier = 'source.json'
        cheminfichier = os.path.join(chemin,fichier)

        global dico_pj

        try:
            time.sleep(ralentisseur)
            with open (cheminfichier, "r") as source:
                dico_pj = json.load(source)     

            self.progressbar.setValue(self.val_etape)
            self.update()
            time.sleep(ralentisseur) 

            self.lbl_etape.setText('Etape '+ str(self.val_etape)+": Savoir s'arreter")
            self.update()    
            time.sleep(ralentisseur)
          
            
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
            pj1["info"] = {'nation':"Noobland"}
            pj1["carac"] = dico_carac
            pj1["comp"] = dico_comp

            dico_pj={}
            dico_pj["system"] = "7seaV2"
            dico_pj["pj1"] = pj1
            dico_pj["pj2"] = pj1
            dico_pj["pj2"]["nom"] = "Noob2"
        
            with open(cheminfichier , 'w') as source:
                json.dump(dico_pj,source, indent = 4)
 
class mafen(QtWidgets.QMainWindow):
    def __init__(self,mon_style):
        super(mafen, self).__init__()
        self.etat_bot = False
        
        # création des Widgets
        self.ma_fenetre_principal(mon_style)
        self.ma_barre_de_menu()
        self.mon_pied_de_page()

        # Création des layouts et affectation Widget
        coord = (0,0)
        coord = self.mes_layouts(coord)   
        self.page_pj(self.fendroite,'pj1')
    def test(self):
        #my_background_task()
        global action
        if action == (0,0):
            action = (1,'test')
            
    def lanceboton(self):
        global action
        if self.etat_bot == False:
            self.etat_bot = True
            self.mon_bot = class1()
            print(str(self.mon_bot))

            try:
                self.mon_bot.start()
                self.lbl_etat_bot.setText("On cherche le bot")
                global action
                action = (2, self)
            except Exception as pourquoi:
                print('ZeVeuxPo :' + str(pourquoi))
        else:
                self.lbl_etat_bot.setText("Bot déjà actif")
                print(str(self.mon_bot))          

    def lancebotof(self): 
        global action

        #self.mon_bot.quit()
        if action == (0,0):
            action = (3,self)
            
    def ma_barre_de_menu(self):
        global dico_pj
        self.main_Menu = self.menuBar()
        self.PJ_Menu = self.main_Menu.addMenu("PJ")
        self.PJ_Menu.addAction("Gestion Pjs")
        self.list_action = []
        i = 0
        for key in dico_pj:
            if key != 'system':
                self.list_action.append(QtWidgets.QAction('&'+str(dico_pj[key]['nom'])))
                self.list_action[i].triggered.connect(partial(self.essaiboutonmenu,key))
                self.PJ_Menu.addAction(self.list_action[i])
                i += 1
                
            
        self.Camp_Menu = self.main_Menu.addMenu("Campagne")
        self.Conf_Menu = self.main_Menu.addMenu("Configuration")
        self.Aide_Menu = self.main_Menu.addMenu("?")
        self.Aide_Menu.addAction("Aide")
        self.Aide_Menu.addAction("A propos")

    def ma_fenetre_principal(self, monstyle):
        self.resize(600,300)
        self.setWindowTitle('Enjoy your campagne')
        self.setStyleSheet(mon_style)  
        
    def mon_pied_de_page(self):

        self.btn_boton = QtWidgets.QPushButton('Boton',self ) #Flat = True   
        self.btn_boton.clicked.connect(self.lanceboton)
        
        self.btn_botof = QtWidgets.QPushButton('Botof',self ) #Flat = True     
        self.btn_botof.clicked.connect(self.lancebotof)

        self.lbl_etat_bot = QtWidgets.QLabel("le bot est Off", self)

    def mes_layouts(self, coord):
        (r,c) = coord
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.grille = QtWidgets.QGridLayout(self.main_widget) #exist en Hlayout et Vlayout
        
        self.fendroite = QtWidgets.QVBoxLayout()
        self.grille.addLayout(self.fendroite,r,c,1,2)
        r +=1 

        self.pieddepage = QtWidgets.QHBoxLayout()
        self.grille.addLayout(self.pieddepage,r,c,1,2)
        r +=1  


        #affectation widget
        self.pieddepage.addWidget(self.btn_boton)
        self.pieddepage.addWidget(self.btn_botof)
        self.pieddepage.addWidget(self.lbl_etat_bot)
        
        return (r,c)

    def page_pj(self, layout, pj_voulu):
        global dico_pj
        self.liste_wid_page = []
        i= 0
        mon_pj = dico_pj[pj_voulu]
        for categorie in mon_pj:
            if categorie == 'nom':
                self.liste_wid_page.append(QtWidgets.QLabel('Nom : ' + mon_pj['nom']))
                layout.addWidget(self.liste_wid_page[i])
                i+=1
            else:
                self.liste_wid_page.append(QtWidgets.QLabel(categorie))
                layout.addWidget(self.liste_wid_page[i])
                i += 1
                monhlayout = QtWidgets.QHBoxLayout()
                self.liste_wid_page.append(monhlayout)
                i += 1
                for key in mon_pj[categorie]:
                    self.liste_wid_page.append(QtWidgets.QLabel(key +' : '+ str(mon_pj[categorie][key])))
                    monhlayout.addWidget(self.liste_wid_page[i])
                    i += 1
                layout.addLayout(monhlayout)
        for wid in self.liste_wid_page:
            print(str(wid))

    def destruct_page(self):
        for wid in self.liste_wid_page:
            wid.deleteLater()

    def essaiboutonmenu(self,txtpj):
        try:
            self.destruct_page()
        except:
            pass
        self.page_pj(self.fendroite,txtpj)

#-------------------------------------------------------------
# On regarde où on est
#-------------------------------------------------------------


#test fenetre chargement

chargeeeeer = fen_chargement(app)


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
    global client
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
                    '''Inserez une blague ici''',\
                    '''De ceux qui n'ont rien à dire, les meilleurs sont ceux qui se taisent''']

    liste_intro=['''Je viens d'arriver, je ne vous ai pas manqué ?''',\
            '''Poypoy ! Pour rappel on me parle avec des $ ''',\
            '''Faites $help pour apprendre à me parler''',\
            '''Et Lanceur est arrivééé, sans se préceeeeerrrr...''']
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
            monmessage = str(corps)
            await channel.send(monmessage)
            action = (0,0)
        elif requete == 2:
            corps.lbl_etat_bot.setText('Je suis actif!')
            action = (0,0)
        elif requete == 3:            
            action = (0,0)
            corps.lbl_etat_bot.setText('Le bot fait Dodo')
            corps.etat_bot = False
            action = (0,0)
            print('client close')
            await client.close()
            client = discord.Client()
            
            
        elif count % int(600/tpspool) == 0:
            
            random.shuffle(liste_blague)
            await channel.send(liste_blague[0])
             
        
        
        await asyncio.sleep(tpspool) # task runs every 60 seconds
               
#-------------------------------------------------------------
# création de class pour thread
#-------------------------------------------------------------

class class1(Thread):

    def __init__(self):
        Thread.__init__(self) 
        print('init class1')

    def run(self):
        print('debut run')
        global client
        client.loop.create_task(my_background_task())
        global dico_conf
        codesecret = dico_conf['token']
        client.run(codesecret)
        
        print('testnfin')
        
    

fen = mafen(mon_style)
fen.show()
app.exec_()

printlog('end of line')
