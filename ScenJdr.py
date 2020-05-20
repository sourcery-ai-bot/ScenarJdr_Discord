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
dico_fdp = {}
champ_par_ligne = 3
taille_wid = 20

#-------------------------------------------------------------
# fonction de suivi
#-------------------------------------------------------------

def printlog(monmsg):
    """Affiche monmsg par un print si la variable global log est True

    Args:
        monmsg (str): Message à afficher si global log est True
    """
    global log
    if log:
        print(monmsg)

def sauve_dico(mon_fichier, dico):
    """Enregistre en JSON UTF8 dans mon_fichier le dictionnaire dico,
       repertoire courant est utilisé en base

    Args:
        mon_fichier (str): Nom du fichier
        dico (dict): Dictionnaire complet à enregistrer dans mon_fichier
    """
    chemin = os.path.dirname(__file__)
    cheminfichier = os.path.join(chemin,mon_fichier)

    with open(cheminfichier , 'w', encoding='utf-8') as source:
                json.dump(dico,source, indent = 4)
 
#--------------------------------------------------------------------------

app = QtWidgets.QApplication(sys.argv)

#-------------------------------------------------------------
# déclaration fenetre GUI
#-------------------------------------------------------------
class FenChargement(QtWidgets.QWidget):
    """Fenetre de chargement qui correspond à la lecture et test des fichiers
       necessaire de l'application

    Args:
        QtWidgets (QWidget): rien de nécéssaire 
    """
    def __init__(self,app):
        """Initialisation de la fenetre de chargement

        Args:
            app (QtWidgets.QApplication(sys.argv)): QtWidgets.Qapplication 
        """
        super(FenChargement,self).__init__()

        self.setWindowTitle("Loadiiiiiiinnnng")
        self.resize(300,100)

        self.mon_layout = QtWidgets.QVBoxLayout(self)
        self.lbl_etape = QtWidgets.QLabel('début du chargement')

        self.mon_layout.addWidget(self.lbl_etape)

        self.val_etape = 0
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setRange(0,4)
        self.progressbar.setValue(self.val_etape)
        self.progressbar.setTextVisible(False)
        
        self.mon_layout.addWidget(self.progressbar)

        self.show()


        QtWidgets.QApplication.processEvents()

        self.chargement_style()
        self.chargement_config()
        self.chargement_fdp()
        self.chargement_source()

        self.close()
        
    def chargement_style(self):
        """Chargement du fichier style.css
           utilise un style vide en cas d'absence
        """
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Le faire avec\
             style')
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
        """ Chargement du fichier config.json
        défini les variables globales suivante:
        global dico_conf
        global token
        global id_chan
        global log
        global tpspool
        global champ_par_ligne

        A défaut, en créer un avec valeur neutre
        """
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Savoir \
            communiquer')
        self.update()
        time.sleep(ralentisseur)
        global dico_conf
        global token
        global id_chan
        global log
        global tpspool
        global champ_par_ligne

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
            champ_par_ligne = dico_conf["champ_par_ligne"]

            if tpspool <2:
                tpspool = 2

            
            self.progressbar.setValue(self.val_etape)
            self.update()
            time.sleep(ralentisseur)
            
        except:
            #-------------------------------------------------------------
            # si pas de config alors on en créer un
            #-------------------------------------------------------------
            token = "Your secret token here / ton token d'application secret\
                 ici"
            id_chan = "L'ID du canal ici "
            log = True
            tpspool = 4
            champ_par_ligne = 3

            printlog("Echec de lecture du fichier config, création \
                automatique")
            
            dico_conf= {}
            dico_conf["token"] = token
            dico_conf["id_chan"] = id_chan
            dico_conf["log"] = False
            dico_conf["tps_pool"] = tpspool
            dico_conf["champ_par_ligne"] = champ_par_ligne
            
            with open(cheminconfig, 'w') as source:
                json.dump(dico_conf,source, indent = 4)
            
    def chargement_fdp(self):
        """Chargement du fichier fdp.json
        défini la variable globale dico_fdp

        A défaut créer un fichier type fdp.json
        """
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+": s'en feuiller\
             précisément")
        self.update()
        time.sleep(ralentisseur)

        chemin = os.path.dirname(__file__)
        fichier = 'fdp.json'
        cheminfichier = os.path.join(chemin,fichier)

        global dico_fdp

        try:
            time.sleep(ralentisseur)
            with open (cheminfichier, "r", encoding='utf-8') as source:
                dico_fdp = json.load(source)     

            self.progressbar.setValue(self.val_etape)
            self.update()
            time.sleep(ralentisseur) 

            
            time.sleep(ralentisseur)
          
            
        except:
            #-------------------------------------------------------------
            # si pas de fichier source alors on en créer un bidon
            #-------------------------------------------------------------
            dico_compt = { "Spirale de la mort": [0,20] }

            dico_comp = { "Art de la guerre": 0,"Athlétisme": 0,\
        "Bagarre": 0, "Convaincre": 0, \
        "Dérober": 0, "Dissimulation": 0, \
        "Empathie": 0, "Equitation": 0, \
        "Erudition": 0, "Escrime": 0, \
        "Intimidation": 0, "Investigation": 0,\
        "Navigation": 0, "Représentation": 0, \
        "Subornation": 0, "Viser": 0}
            dico_carac={}
            dico_carac["Puissance"]=1
            dico_carac["Finesse"]=1
            dico_carac["Esprit"]=1
            dico_carac["Determination"]=1
            dico_carac["Panache"]=1
            
            systemD = {"Nom": "Nom"}
            systemD["Information"] = {'Nation':"Nul part"}
            systemD["Caractéristique"] = dico_carac
            systemD["Compétence"] = dico_comp
            systemD["Compteur"] = dico_compt

            dico_fdp = {}
            dico_fdp["7seaV2"] = systemD
            
            sauve_dico(fichier, dico_fdp)
     
    def chargement_source(self):
        """Charge le fichier source.json
        A défaut créer le fichier source.json
        avec valeurs neutres
        """
        self.val_etape +=1
        self.lbl_etape.setText('Etape '+ str(self.val_etape)+': Savoir de\
             quoi on parle !')
        self.update()
        time.sleep(ralentisseur)

        chemin = os.path.dirname(__file__)
        fichier = 'source.json'
        cheminfichier = os.path.join(chemin,fichier)

        global dico_pj

        try:
            time.sleep(ralentisseur)
            with open (cheminfichier, "r", encoding='utf-8') as source:
                dico_pj = json.load(source)     

            self.progressbar.setValue(self.val_etape)
            self.update()
            time.sleep(ralentisseur) 

            self.lbl_etape.setText('Etape '+ str(self.val_etape)+": Savoir\
                 s'arreter")
            self.update()    
            time.sleep(ralentisseur)
          
            
        except:
            #-------------------------------------------------------------
            # si pas de fichier source alors on en créer un bidon
            #-------------------------------------------------------------
            dico_comp = {}
            dico_comp['Escrime']= 1
            dico_comp['Parade']= 1
            dico_carac={}
            dico_carac["Puissance"]=1
            dico_carac["Finesse"]=1
            dico_carac["Esprit"]=1
            dico_carac["Determination"]=1
            dico_carac["Panache"]=1
            pj1 = {}
            pj1["Nom"] = "Noob"
            pj1["Information"] = {'Nation':"Noobland"}
            pj1["Caractéristique"] = dico_carac
            pj1["Compétence"] = dico_comp
            
            dico_pj={}
            dico_pj["system"] = "7seaV2"
            dico_pj["pj1"] = pj1
            dico_pj["pj2"] = pj1
            dico_pj["pj2"]["Nom"] = "Noob2"
        
            sauve_dico(fichier, dico_pj)

class QHLine(QtWidgets.QFrame):
    """OQobjet pour faire des lignes Horizontales

    Args:
        QtWidgets (QtWidgets.QFrame):RAS
    """
    def __init__(self):
           super(QHLine, self).__init__()
           self.setFrameShape(QtWidgets.QFrame.HLine)
           self.setFrameShadow(QtWidgets.QFrame.Sunken)

class QVLine(QtWidgets.QFrame):
    """OQobjet pour faire des lignes Verticales

    Args:
        QtWidgets (QtWidgets.QFrame):RAS
    """
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class MaFen(QtWidgets.QMainWindow):
    """Fenetre principale de l'application ]

    Args:
        QtWidgets (QtWidgets.QMainWindow): RAS
    """
    def __init__(self,mon_style):
        """Initialise la fenetre en chargeant le style 'mon_style'

        Args:
            mon_style (lecture d'un fichier CSS): Feuille de style css
        """
        super(MaFen, self).__init__()
        self.etat_bot = False
        
        # création des Widgets
        self.ma_fenetre_principal(mon_style)
        self.ma_barre_de_menu()

        #pour memoriser les widget à effacer
        self.liste_wid_page = []

        # Création des layouts et affectation Widget
        
        self.mes_layouts()   
        self.page_pj(self.fendroite,'pj1')
     
    def test(self):
        """demande gentiment au bot de dire test
        """
        global action
        if action == (0,0):
            action = (1,'test')

    def lanceboton(self):
        """lance le thread du bot
        """

        global action
        if self.etat_bot == False:
            self.etat_bot = True
            self.mon_bot = Class1()
            printlog(str(self.mon_bot))

            try:
                self.mon_bot.start()
                self.lbl_etat_bot.setText("On cherche le bot")
                global action
                action = (2, self)
            except Exception as pourquoi:
                printlog('ZeVeuxPo :' + str(pourquoi))
        else:
                self.lbl_etat_bot.setText("Bot déjà actif")
                printlog(str(self.mon_bot))          

    def lancebotof(self): 
        """envoi un messafe au bot pour qu'il s'arrete et mettent fin au
             thread
        """
        global action

        #self.mon_bot.quit()
        if action == (0,0):
            action = (3,self)
            
    def ma_barre_de_menu(self):
        """Définis la barre de menu
        """
        global dico_pj
        self.main_Menu = self.menuBar()
        self.Camp_Menu = self.main_Menu.addMenu("Campagne")
        
        self.PJ_Menu = self.main_Menu.addMenu("PJ")
        self.act_gest_pj = QtWidgets.QAction('Gestion Pjs')
        self.act_gest_pj.triggered.connect(partial(self.affiche_pageX,\
            'gest pj'))
        self.PJ_Menu.addAction(self.act_gest_pj)
        self.list_action = []
        i = 0
        for key in dico_pj:
            if key != 'system':
                self.list_action.append(QtWidgets.QAction('&'+str(dico_pj[key]['Nom'])))
                self.list_action[i].triggered.connect(partial(self.affiche_pageX,'pj',key))
                self.PJ_Menu.addAction(self.list_action[i])
                i += 1
                
        self.Bot_Menu = self.main_Menu.addMenu("BOT")
        self.act_A_Boton = QtWidgets.QAction('Bot On')
        self.act_A_Boton.triggered.connect(self.lanceboton)
        self.Bot_Menu.addAction(self.act_A_Boton)

        self.act_A_Botof = QtWidgets.QAction('Bot Off')
        self.act_A_Botof.triggered.connect(self.lancebotof)
        self.Bot_Menu.addAction(self.act_A_Botof)

        self.Aide_Menu = self.main_Menu.addMenu("Options")
        self.act_config = QtWidgets.QAction("Configuration")
        self.Aide_Menu.addAction(self.act_config)
        self.act_config.triggered.connect(partial(self.affiche_pageX,\
            'config'))
        self.act_A_propos = QtWidgets.QAction('A propos')
        self.act_A_propos.triggered.connect(self.dial_a_propos)
        self.Aide_Menu.addAction(self.act_A_propos)
    
    def actualise_menu(self):
        """actualise le menu en fonction de la liste de PJ
        """
        global dico_pj
        try:

            for action in self.list_action:
                action.deleteLater()
        except:
            pass

        i = 0
        self.list_action = []
        for key in dico_pj:
            if key != 'system':
                self.list_action.append(QtWidgets.QAction('&'+\
                    str(dico_pj[key]['Nom'])))
                self.list_action[i].triggered.connect(partial(\
                    self.affiche_pageX,'pj',key))
                self.PJ_Menu.addAction(self.list_action[i])
                i += 1    
        
    def ma_fenetre_principal(self, monstyle):
        """ définit la taille de base de l'application
        et applique le style
        """
        self.resize(700,500)
        self.setWindowTitle('Enjoy your campagne')
        self.setStyleSheet(mon_style)  

    def mes_layouts(self):
        """définit les layouts de l'application
        """
        self.mon_scroll = QtWidgets.QScrollArea()
        self.main_widget = QtWidgets.QWidget()    
        self.grille = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.grille)
        self.mon_scroll.setWidget( self.main_widget)
        self.mon_scroll.setWidgetResizable(True)   
        self.setCentralWidget(self.mon_scroll)
        self.fendroite = QtWidgets.QVBoxLayout()
        self.grille.addLayout(self.fendroite)
         
    def destruct_page(self):
        """détuit tout les Widgets de la liste
        """
        for wid in self.liste_wid_page:
            wid.deleteLater()
        self.liste_wid_page = []
    
    def affiche_pageX(self,quelpage,complement=''):
        """affiche_pageX : detruit la page actuelle pour afficher
         la page demandée

        Args:
            quelpage ([type]): [description]
            complement ([type]): [description]
        """
        try:
            self.destruct_page()
        except:
            pass
        if quelpage == 'pj':
            self.page_pj(self.fendroite,complement)
        elif quelpage == 'gest pj':
            self.page_gestionpj(self.fendroite)
        elif quelpage == 'config':
            self.page_config(self.fendroite)
        else:
            print("doesn't work 404")

    def page_pj(self, layout, pj_voulu):
        """affiche la page de détaille du joueur pj_voulu dans la fenetre
        layout

        Args:
            layout (QtWidgets.QVBoxLayout: Layout où seront affiché les objets
            pj_voulu (str): Nom code du joueur ex: 'pj1' 
        """
        global dico_pj
        global champ_par_ligne
        global taille_wid
        self.liste_wid_page = []
        i= 0
        mon_pj = dico_pj[pj_voulu]
        for categorie in mon_pj:
            self.liste_wid_page.append(QtWidgets.QLabel(categorie))
       
            layout.addWidget(self.liste_wid_page[i])
            i += 1
            monglayout = QtWidgets.QGridLayout()
                    
            self.liste_wid_page.append(monglayout)
         
            i += 1
            r = 0
            nbkey = 0
            c = 0
            if categorie == 'Nom':
                self.liste_wid_page.append(QtWidgets.QLabel('Nom complet: '\
                     + mon_pj['Nom']))
            
                monglayout.addWidget(self.liste_wid_page[i],r,c)
                i += 1
                self.liste_wid_page.append(QtWidgets.QPushButton('Edit'))
                self.liste_wid_page[i].clicked.connect(partial(\
                    self.edittextpj,(pj_voulu,categorie)))
        
                monglayout.addWidget(self.liste_wid_page[i],r,c+1)
                i += 1
                self.liste_wid_page.append(QtWidgets.QLabel(' '))
                monglayout.addWidget(self.liste_wid_page[i],r,c+2)
          
                i += 1
            else:

                total_key = len( mon_pj[categorie])
                key_par_colone = total_key // champ_par_ligne
                if total_key % champ_par_ligne != 0 :
                    key_par_colone += 1
         
                for key in mon_pj[categorie]:
                    nbkey += 1
                    
                    if nbkey > key_par_colone:
                        c += 5
                        r = 0
                        nbkey = 1

                    if  isinstance(mon_pj[categorie][key],int):
                        self.liste_wid_page.append(QtWidgets.QLabel(key +\
                            ' : '+ str(mon_pj[categorie][key])))
                        monglayout.addWidget(self.liste_wid_page[i],r,c)
                     
                        i += 1

                        self.liste_wid_page.append(QtWidgets.QPushButton('+'))
                        self.liste_wid_page[i].clicked.connect(partial(\
                            self.plusmoinspj,(pj_voulu,categorie,key),1))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
                 
                        i += 1

                        self.liste_wid_page.append(QtWidgets.QPushButton('-'))
                        self.liste_wid_page[i].clicked.connect(partial(\
                            self.plusmoinspj,(pj_voulu,categorie,key),-1))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+2)
                    
                        i += 1

                        self.liste_wid_page.append(QVLine())
                        self.liste_wid_page[i].setObjectName('maligne')
                        monglayout.addWidget(self.liste_wid_page[i],r,c+3)
                    
                        i += 1

                        self.liste_wid_page.append(QtWidgets.QLabel(' '))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+4) 
                         
                        i += 1
                        r += 1
                    elif isinstance(mon_pj[categorie][key], list):
                        valcompt = mon_pj[categorie][key][0]
                        maxcompt = mon_pj[categorie][key][1]
                         
                        self.liste_wid_page.append(QtWidgets.QLabel(key +\
                            ' : '+ str(valcompt)+' / '+str(maxcompt)))
                        monglayout.addWidget(self.liste_wid_page[i],r,c)
                    
                        i += 1
                        self.liste_wid_page.append(QtWidgets.QPushButton('+'))
                        self.liste_wid_page[i].clicked.connect(partial(\
                            self.plusmoinspj,(pj_voulu,categorie,key),1))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
                   
                        i += 1
                        self.liste_wid_page.append(QtWidgets.QPushButton('-'))
                        self.liste_wid_page[i].clicked.connect(partial(\
                            self.plusmoinspj,(pj_voulu,categorie,key),-1))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+2)
                   
                        i += 1
                        self.liste_wid_page.append(QVLine())
                        self.liste_wid_page[i].setObjectName('maligne')
                        monglayout.addWidget(self.liste_wid_page[i],r,c+3)
               
                        i += 1
                        self.liste_wid_page.append(QtWidgets.QLabel(' '))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+4) 
                                   
                        i += 1
                        r += 1
                    else:
                        self.liste_wid_page.append(QtWidgets.QLabel(key +\
                            ' : '+ str(mon_pj[categorie][key])))
                        monglayout.addWidget(self.liste_wid_page[i],r,c)
                     
                        i += 1
                        self.liste_wid_page.append(QtWidgets.QPushButton(\
                            'Edit'))
                        self.liste_wid_page[i].clicked.connect(partial(\
                            self.edittextpj,(pj_voulu,categorie,key)))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
                      
                        i += 1
                        self.liste_wid_page.append(QVLine())
                        self.liste_wid_page[i].setObjectName('maligne')
                        monglayout.addWidget(self.liste_wid_page[i],r,c+3)
                       
                        i += 1
                        self.liste_wid_page.append(QtWidgets.QLabel(' '))
                        monglayout.addWidget(self.liste_wid_page[i],r,c+4)  
                                       
                        i += 1
                        r+= 1
            layout.addLayout(monglayout)
            self.liste_wid_page.append(QHLine())
            self.liste_wid_page[i].setObjectName('maligne')
            
            layout.addWidget(self.liste_wid_page[i])
            i += 1   
    
    def plusmoinspj(self,datas,increment):
        """ajoute la valeur de l'incrément à la datas
        sauvegarde le dico_pj dans le fichier source.json

        Args:
            datas (tuple(str,str,str)): nom code du pj, premier niveau de 
                                        clé dictionnaire, deuxième niveau 
                                        de clé
            increment (int): typiquement +1 ou -1 
        """
        global dico_pj
        (quel_pj,quel_categorie,quel_key) = datas
        valeur = dico_pj[quel_pj][quel_categorie][quel_key]
        if isinstance(valeur, list):
            valeur = dico_pj[quel_pj][quel_categorie][quel_key][0]
            cmptmax = dico_pj[quel_pj][quel_categorie][quel_key][1]
            valeur += increment
            if valeur >= 0 and valeur <= cmptmax:
                dico_pj[quel_pj][quel_categorie][quel_key] = [valeur,cmptmax]
                self.affiche_pageX('pj',quel_pj)
                sauve_dico('source.json',dico_pj)
        else:
            valeur += increment
            if valeur >= 0:
                dico_pj[quel_pj][quel_categorie][quel_key] = valeur
                self.affiche_pageX('pj',quel_pj)
                sauve_dico('source.json',dico_pj)

    def edittextpj(self, datas):
        """Ouvre un Qdialog, pour demander la saisie d'un texte
        et relie le bouton de cofirmation à la fonction self.modiftext()

        Args:
            datas (tuple(str,str,str)): nom code du pj, premier niveau de clé dictionnaire, deuxième niveau de clé
        """
        global dico_pj
        self.demande_texte = QtWidgets.QDialog(parent = self)
        self.demande_texte.setWindowTitle('Saisissez votre texte')
        monVlayout = QtWidgets.QVBoxLayout(self.demande_texte)
        champ_saisi = QtWidgets.QLineEdit(self.demande_texte)
        try:
            (pj_voulue,categorie,key) = datas
            champ_saisi.setText(dico_pj[pj_voulue][categorie][key])
        except:
            (pj_voulue,categorie) = datas
            champ_saisi.setText(dico_pj[pj_voulue][categorie])

        monVlayout.addWidget(champ_saisi)
        bouton_ok = QtWidgets.QPushButton('ok')
        bouton_ok.clicked.connect(partial(self.modiftext, champ_saisi,\
             self.demande_texte, datas))
        monVlayout.addWidget(bouton_ok)
        
        self.demande_texte.setLayout(monVlayout)
        self.demande_texte.show()

    def modiftext(self, champ,mondial, datas):
        """Vérifie que champs non vide et sauvegarde la valeur, pour
         ensuite fermer le Qdialog

        Args:
            champ (QtWidgets.QLineEdit): QlineEdit contenant la valeur à
                                         sauvegarder
            mondial (QtWidgets.QDialog): fenetre de Qdialog qui appellent la 
                                         fonction pour fermeture
            datas (tuple(str,str,str)): nom code du pj, premier niveau de clé
                                        dictionnaire, deuxième niveau de clé
        """
        global dico_pj
        mavaleur = str(champ.text()) 
        if mavaleur != '':
            try:
                (quel_pj,quel_categorie,quel_key) = datas
                
                dico_pj[quel_pj][quel_categorie][quel_key] = mavaleur
                self.affiche_pageX('pj',quel_pj)
                
            except:
                (quel_pj,quel_categorie) = datas
                dico_pj[quel_pj][quel_categorie] = mavaleur
                self.affiche_pageX('pj',quel_pj)
                self.actualise_menu()
            sauve_dico('source.json',dico_pj)
            mondial.close()

    def page_gestionpj(self,layout):
        """ initialise la page gestion des pjs
        """
        global dico_pj
        
        preliste_pj = []
        max_id = 0 
        #Mise en forme de la liste des pj pour affichage
        #recuperation du system en cours
        for pj in dico_pj:
            if pj == 'system':
                mon_system = dico_pj['system']
                mon_system = mon_system
            else:
                idpj = int(pj.split('pj')[1])
                if max_id < idpj:
                    max_id = idpj
                nompj = dico_pj[pj]['Nom']
                preliste_pj.append([idpj,nompj])
        #on viens recuperer les id (pjX) et le nom du perso
        #l'ID max rencontré
        liste_pj = []
        for poubelle in range(0,max_id+1):
            poubelle = poubelle 
            liste_pj.append('')
        #on créer une liste avec max_id element vide

        #que l'on rempli avec les noms des pjs
        for pj in preliste_pj:
            liste_pj[pj[0]] = pj[1]
        #on repasse sur la liste pour ressortir le premier élément vide
        #comme nouvelle ID
        unId = 0
        new_id = 0
        for pj in liste_pj:
            if unId == 0:
                pass
            else:
                if pj == '':
                    new_id = unId
                    break
            unId += 1
        if new_id == 0:
            new_id = max_id +1
        #maintenant on va pouvoir faire la liste des pj actuel (pour 
        #suppression) et proposer un nouvel ID

        i = 0
        
        self.liste_wid_page.append(QtWidgets.QLabel(\
            'Liste des personnages :'))
        layout.addWidget(self.liste_wid_page[i])
        i += 1

        num_pj = 0
        
        for elem in liste_pj:
            if elem != '':
                monHLayout = QtWidgets.QHBoxLayout()
                self.liste_wid_page.append(monHLayout)
                layout.addLayout(monHLayout)
                i += 1

                self.liste_wid_page.append(QtWidgets.QLabel(' '))
                monHLayout.addWidget(self.liste_wid_page[i])
                i += 1


                self.liste_wid_page.append(QtWidgets.QLabel('PJ'+\
                    str(num_pj)+' : ' +elem))
                monHLayout.addWidget(self.liste_wid_page[i])
                i += 1

                self.liste_wid_page.append(QtWidgets.QPushButton('x'))
                self.liste_wid_page[i].clicked.connect(partial(self.supprpj,\
                    'pj'+str(num_pj)))
                monHLayout.addWidget(self.liste_wid_page[i])
                i += 1
                self.liste_wid_page.append(QtWidgets.QLabel(' '))
                monHLayout.addWidget(self.liste_wid_page[i])
                i += 1

                
            num_pj += 1

        monHLayout = QtWidgets.QHBoxLayout()
        self.liste_wid_page.append(monHLayout)
        layout.addLayout(monHLayout)
        i += 1

        self.liste_wid_page.append(QtWidgets.QLabel(' '))
        monHLayout.addWidget(self.liste_wid_page[i])
        i += 1
        
        self.liste_wid_page.append(QtWidgets.QPushButton('New'))
        self.liste_wid_page[i].clicked.connect(partial(\
            self.nouveau_pj,new_id))
        monHLayout.addWidget(self.liste_wid_page[i])
        i += 1

        self.liste_wid_page.append(QtWidgets.QLabel(' '))
        monHLayout.addWidget(self.liste_wid_page[i])
        i += 1

    def supprpj(self,txtpj):
        """supprime le pj txtpj, et sauvegarde le fichier source
        """
        global dico_pj
        del dico_pj[txtpj]

        sauve_dico('source.json', dico_pj)
        self.destruct_page()
        self.actualise_menu()
        self.affiche_pageX('gest pj')

    def nouveau_pj(self,new_id):
        """Créer un nouveau pj en prennant le model dans dico_fdp

        Args:
            new_id (int): numéro du code de pj à créer
        """
      
        global dico_fdp
        global dico_pj
        if new_id > 0:
            Newpj = dico_fdp['7seaV2']
            dico_pj['pj'+str(new_id)]=Newpj
            sauve_dico('source.json', dico_pj)

            self.destruct_page()
            self.actualise_menu()
            self.affiche_pageX('gest pj')
    
    def dial_a_propos(self):
        """affiche le Qdialog du a propos
        """
        
        self.demande_texte = QtWidgets.QDialog(parent = self)
        self.demande_texte.setWindowTitle('CampDisc V1.0 - Béta')
        monVlayout = QtWidgets.QVBoxLayout(self.demande_texte)
        self.nomversion = QtWidgets.QLabel('CampDisc V1.0 - Béta')
        monVlayout.addWidget(self.nomversion)
        description = QtWidgets.QLabel('Réalisé par Pierre Nunez')
        monVlayout.addWidget(description)
        self.demande_texte.show()

    def page_config(self,layout):
        """initialise la page de configuration

        Args:
            layout (QtWidgets.QGridLayout): QGridLayout hebergeant la page
        """
        global dico_conf
        self.liste_wid_page = [] 
        i = 0
        r=0
        c=0

        monglayout = QtWidgets.QGridLayout()
        self.liste_wid_page.append(monglayout)
        i += 1

        self.liste_wid_page.append(QtWidgets.QLabel(''))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        r += 1

        self.liste_wid_page.append(QtWidgets.QLabel('Paramètres du Bot'))
        monglayout.addWidget(self.liste_wid_page[i],r,c, columnspan = 2)
        i += 1

        
        self.liste_wid_page.append(QtWidgets.QLabel(''))
        monglayout.addWidget(self.liste_wid_page[i],r,c+2)
        i += 1
        r += 1
        c = 1

        self.liste_wid_page.append(QtWidgets.QLabel('Token du Bot : ' + str(dico_conf['token'])))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        self.liste_wid_page.append(QtWidgets.QPushButton('Edit'))
        self.liste_wid_page[i].clicked.connect(partial(self.edit_param_config,'token'))
        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
        i += 1
        r += 1

        self.liste_wid_page.append(QtWidgets.QLabel('ID du canal Discord : ' + str(dico_conf['id_chan'])))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        self.liste_wid_page.append(QtWidgets.QPushButton('Edit'))
        self.liste_wid_page[i].clicked.connect(partial(self.edit_param_config,'id_chan'))
        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
        i += 1
        r += 1

        self.liste_wid_page.append(QtWidgets.QLabel('Réactivité du bot : ' + str(dico_conf['tps_pool'])))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        self.liste_wid_page.append(QtWidgets.QPushButton('Edit'))
        self.liste_wid_page[i].clicked.connect(partial(self.edit_param_config,'tps_pool'))
        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
        i += 1
        r += 1

        c = 0
        self.liste_wid_page.append(QtWidgets.QLabel("Paramètres d'apparence"))
        monglayout.addWidget(self.liste_wid_page[i],r,c, columnspan = 2)
        i += 1
        r += 1
        c = 1

        self.liste_wid_page.append(QtWidgets.QLabel('Nombre de colonnes: ' + str(dico_conf['champ_par_ligne'])))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        self.liste_wid_page.append(QtWidgets.QPushButton('Edit'))
        self.liste_wid_page[i].clicked.connect(partial(self.edit_param_config,'champ_par_ligne'))
        monglayout.addWidget(self.liste_wid_page[i],r,c+1)
        i += 1
        r += 1

        self.liste_wid_page.append(QtWidgets.QLabel(''))
        monglayout.addWidget(self.liste_wid_page[i],r,c)
        i += 1
        r += 1

        layout.addLayout(monglayout)

    def edit_param_config(self,param):
        global dico_conf
        self.demande_texte = QtWidgets.QDialog(parent = self)
        self.demande_texte.setWindowTitle('Saisissez votre texte')
        monVlayout = QtWidgets.QVBoxLayout(self.demande_texte)
        champ_saisi = QtWidgets.QLineEdit(self.demande_texte)
        champ_saisi.setText(str(dico_conf[param]))

        monVlayout.addWidget(champ_saisi)
        bouton_ok = QtWidgets.QPushButton('ok')
        bouton_ok.clicked.connect(partial(self.modiftextconf, champ_saisi, self.demande_texte, param))
        monVlayout.addWidget(bouton_ok)
        
        self.demande_texte.setLayout(monVlayout)
        self.demande_texte.show()

    def modiftextconf(self, champ,mondial, param):
        """Vérifie que champs non vide et sauvegarde la valeur, pour ensuite
         fermer le Qdialog

        Args:
            champ (QtWidgets.QLineEdit): QlineEdit contenant la valeur à 
                                         sauvegarder
            mondial (QtWidgets.QDialog): fenetre de Qdialog qui appellent la 
                                         fonction pour fermeture
            datas (tuple(str,str,str)): nom code du pj, premier niveau de clé 
                                        dictionnaire, deuxième niveau de clé
        """
        global dico_conf
        mavaleur = str(champ.text()) 
        if mavaleur != '':
            if param == 'token' or param == 'id_chan':               
                dico_conf[param] = mavaleur

            elif param == 'log':
                if mavaleur == 'False':
                    mavaleur = ''
                dico_conf[param] = bool(mavaleur)
            else:
                dico_conf[param] = int(mavaleur)

            sauve_dico('config.json',dico_conf)
            self.affiche_pageX('config')
            mondial.close()

    

#-------------------------------------------------------------
# On regarde où on est
#-------------------------------------------------------------

chargeeeeer = FenChargement(app)

#-------------------------------------------------------------
# création du client discord
#-------------------------------------------------------------
client = discord.Client()

justearrived = True # pour générer un message à la connexion
affectation = {} #pour mémoriser qui à pris un pj
# = 0
#-------------------------------------------------------------
# fonction outils pour bot discord
#-------------------------------------------------------------

#lance nb D10 si explose est valide, chaque 10 rajoute un D10 suplémentaire, (max 20) 
#retourne les résultats sous forme de liste
def brouette(nb, explose):
    """Lance 'nb' D10 si 'explose' est valide, chaque 10 rajoute un D10 
    suplémentaire, (max 20) 
    retourne les résultats sous forme de liste

    Args:
        nb (int): nombre de dé lancé
        explose (bool): Valide ou non si un dé explose ou non

    Returns:
        [list]: liste de resultat des dé
    """
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
def nbmise(liste_de, difficulte):
    """Calcul le nombre de mises d'une liste de dé 10

    Args:
        liste_de (liste): liste de resultat de 1 à 10
        difficulte (int): valeur de la mise a cosntituer avec les dés

    Returns:
        [tuple(int, str)]:(Nombre de mise constitué, détails des mises 
                          constituées)
    """
    liste_de.sort() #on tri du plus petit au plus grand
    liste_mise = [] 
    
    nb_de_mise = 0
    while len(liste_de)>0: #tant qu'il y a des dés...
        plusfort = int (liste_de.pop()) #on prend le plus fort des dé en fin\
                                        #de liste
        mise_encours = plusfort #on créer la somme de la premiere mise (pas 
                                      #forcement complete)
        mise = [] # on crée la liste de dé de la mise pour vérification
        mise.append(plusfort) # on y rajoute le premier dé
       
        while mise_encours < difficulte and len(liste_de)>0: #tant que la mise
                                                     # n'atteint pas son seuil
                                                     # et tant qu'il y a des dé
            plusfaible = int(liste_de.pop(0)) # on recupere le plus faible
            mise_encours += plusfaible #on cumul pour connaitre la valeur de 
                                       #la mise encours
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
    """action effectuée quand le bot est loggué
    """
    monmsg = ('We have logged in as {0.user}'.format(client))
    printlog(monmsg)

@client.event
async def on_message(message):
    """Action du bot effectuée sur apparition de message dans le canal

    Args:
        message (voir module discord): [description]

    Returns:
        Rien : Queue de Chique, Nada, Neant 
    """
    global justearrived
    if message.author == client.user:
        return   # pour ne pas se répondre à soi-même
    

    if message.content.startswith('$give'):
        requete = message.content
        decortique = requete.split()

        recup = dico_pj.get(decortique[1])
        if recup != None:
            affectation[str(message.author)[0:-5]] = recup['Nom']
            monmessage = str(message.author)[0:-5] + \
                ', vous êtes maintenant : ' + recup['Nom']
            await message.channel.send(monmessage)

    elif message.content.startswith('$hello'):
        monmessage = 'Coucou pret à lancer vos dés !'
        await message.channel.send(monmessage)

    elif message.content.startswith('$help'):
        await message.channel.send('''
        Pour lancer un set de 7 dés il faut taper '$n 7' sans les guillemets
        - $n pour un jet normal (sans relance des 10)
        - $nd pour un jet normal (sans relance des 10) avec des groupes'''+\
        ''' de 15 pour 1 mise
        - $ne pour un jet explosif (avec 1D en plus pour chaque 10)
        - $ned pour un jet explosif (avec 1D en plus pour chaque 10) avec'''+\
        ''' des groupes de 15 pour 1 mise
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
                
            resultat = recupnom + ', vous avez ' + str(nb) + \
                ' mise(s), ( | '+texte+')'
            
            await message.channel.send(resultat)

        else:
            await message.channel.send('pas compris !')

    elif message.content.startswith('$pj'):
        requete = message.content
        if requete == '$pj':
                    
            texte_li_pj = 'liste des Pj: \n'
            for key in dico_pj:
                if key != "system":
                    nompj = dico_pj[key]
                    texte_li_pj += key + ' : ' + nompj['Nom'] + '\n'
            await message.channel.send(texte_li_pj)

        elif len(requete) > 3 :
            num_pj = requete[3:len(requete)]
            
            monmessage = str(dico_pj['pj'+num_pj])
            await message.channel.send(monmessage)
        else:
            await message.channel.send('''$pj d'accord mais $pj combien  ?''')
        
@client.event
async def my_background_task():
    """Tache de fond:
    Message de bienvenue, Message de toujours vivant
    """ 
    global client
    await client.wait_until_ready()
    global id_chan
    global action
    global justearrived 
    global tpspool
    global dico_conf
    channel = client.get_channel(int(id_chan))
    await asyncio.sleep(tpspool) #

    liste_blague = ['''Staying alive, staying a live. Ah, ah ah....''',\
                    '''Inserez une blague ici''',\
                    '''De ceux qui n'ont rien à dire, les meilleurs sont'''+\
                    ''' ceux qui se taisent''']

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
            #corps.lbl_etat_bot.setText('Je suis actif!')
            action = (0,0)
        elif requete == 3:            
            action = (0,0)
            #corps.lbl_etat_bot.setText('Le bot fait Dodo')
            corps.etat_bot = False
            action = (0,0)
            await client.close()
            client = discord.Client()
            
            
        elif count % int(600/tpspool) == 0:
            
            random.shuffle(liste_blague)
            await channel.send(liste_blague[0])
             
        
        
        await asyncio.sleep(tpspool) # task runs every 60 seconds
               
#-------------------------------------------------------------
# création de class pour thread
#-------------------------------------------------------------

class Class1(Thread):
    """Class1 permet de créer et lancer un thread

    Args:
        Thread (Thread du module thread): voir module Thread
    """

    def __init__(self):
        """initialise le thread
        """
        Thread.__init__(self) 
        printlog('init thread')

    def run(self):
        """Affecte la tache de fond au client discord
        et lance la connexion du client
        """
        printlog('debut run')
        global client
        client.loop.create_task(my_background_task())
        global dico_conf
        codesecret = dico_conf['token']
        client.run(codesecret)
        
        printlog('testnfin')
        
fen = MaFen(mon_style)
fen.show()
app.exec_()
