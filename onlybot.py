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


#-------------------------------------------------------------
# Variable "globale" bouh pas bien ! Je sais
#-------------------------------------------------------------

log = True
tpspool = 3
ralentisseur = 0
dico_pj = {}
dico_fdp = {}
champ_par_ligne = 3
taille_wid = 20
dico_action = {} 


com_etat = 0
com_parler = ""
com_maj_pj = 0
com_maj_conf = 0

arret_interne = False
majpj_interne = False

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
#-----------------------------------------------------------------------
# fonction de lecture écriture des fichiers
#-----------------------------------------------------------------------

def chargement_config():
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

    except Exception as mes:

        printlog('problème lecture config : '+ str(mes))
    
def chargement_source():
    global dico_pj

    chemin = os.path.dirname(__file__)
    fichier = 'source.json'
    cheminfichier = os.path.join(chemin,fichier)

    with open (cheminfichier, "r", encoding='utf-8') as source:
        dico_pj = json.load(source)  


def lecture_com():

    printlog('lecture com')
    chemin = os.path.dirname(__file__)
    config = 'com.json'

    cheminconfig = os.path.join(chemin, config)
    try:       
        with open(cheminconfig, "r") as source:
            dico_action = json.load(source)
        com_etat = dico_action["etat"]
        com_parler = dico_action["parler"]
        com_maj_pj = dico_action["maj_pj"]
        com_maj_conf = dico_action["maj_conf"]
        
    except Exception as mes:

        printlog('problème lecture ordre : '+ str(mes))

        com_etat = 0
        com_parler = "" 
        com_maj_pj = 0
        com_maj_conf = 0 
    finally:
        print((com_etat, com_parler, com_maj_pj, com_maj_conf))
        return (com_etat, com_parler, com_maj_pj, com_maj_conf)


def ecriture_com( com_etat, com_parler, com_maj_pj, com_maj_conf):

    chemin = os.path.dirname(__file__)
    config = 'com.json'
    cheminconfig = os.path.join(chemin, config)

    dico_action["etat"] = com_etat
    dico_action["parler"] = com_parler
    dico_action["maj_pj"] = com_maj_pj
    dico_action["maj_conf"] = com_maj_conf

    try:
        with open(cheminconfig, "w") as source:
            json.dump(dico_action,source, indent = 4)
    except:
        printlog('échec écriture support de com')
    

def lecture_dico(nom_dico):
    return nom_dico
 
 



#-------------------------------------------------------------
# création du client discord
#-------------------------------------------------------------
client = discord.Client()
chargement_source()
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
    global arret_interne
    global dico_pj

    if message.author == client.user:
        return   # pour ne pas se répondre à soi-même

    if message.content.startswith('$jetequit'):
        arret_interne = True
    elif message.content.startswith('$give'):
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
            if recupnom is None:
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

    elif message.content.startswith('$majpj'):
        chargement_source()
        await message.channel.send('MAJ faites')
        

@client.event
async def my_background_task():
    """Tache de fond:
    Message de bienvenue, Message de toujours vivant
    """ 
    global client
    await client.wait_until_ready()
    global id_chan
    global justearrived 
    global tpspool
    global dico_conf

    channel = client.get_channel(int(id_chan))
    await asyncio.sleep(tpspool) 

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

        printlog("boucle de vie : "+str(count))
        count += 1
        modif = False
        (com_etat, com_parler, com_maj_pj, com_maj_conf)=lecture_com()
        if com_parler != "":
            await channel.send(com_parler)
            com_parler = ""
            modif = True
        
        if com_etat == 1 or arret_interne:
            await channel.send('Bye Bye')
            await client.close()
            com_etat = 2
            modif = True

        if com_maj_pj == 1 or majpj_interne:
            chargement_source()
            await channel.send("M.A.J. PJ ")

        if count % int(600/tpspool) == 0:
            
            random.shuffle(liste_blague)
            await channel.send(liste_blague[0])
            

        if modif:
            ecriture_com(com_etat, com_parler, com_maj_pj, com_maj_conf)
          
        
        
        await asyncio.sleep(tpspool) # relance la surveillance dans tpspool seconde
               
#-------------------------------------------------------------
# création de class pour thread
#-------------------------------------------------------------


printlog('debut run')

chargement_config()

client.loop.create_task(my_background_task())
client.run(token)

printlog('testnfin')

