# ScenarJdr_Discord
Gestionnaire de scénar de Jeu de rôle avec bot discord

Gestionnaire de Scénario de JDR, avec création d'un bot discord

Objectif:
le script interviens sur deux tableaux:
1) Interface meneur de jeu
2) Bot discord

Rôle de l'interface:
- Selectionner le système de jeu (rêgle de lancé de dé par exemple)
- Gestionnaire de fiche des PJ (FDP)
- Prise de note
- Faciliter le partage de document sur Discord
- Sauvegarde du contexte (pj, scénar , note etc)
- Selectionner la musique

Rôle du Bot:
- Lancé de Dé en fonction du système de regles choisis
- Visualisation de fiche et permet de lancer un dé en fonction de la FDP
- Diffuser la musique choisis par le mener

--------------------------------------------------------------------------

Etat actuel:

A)Interface
- Fenetre de chargement des fichiers nécéssaires (sources, style et config et fdp)
- Fentre principal en dark theme
- Lancement et arret bot
- modification des valeurs d'un PJ
- création / suprression d'un PJ

Bug connu:
pour le On Off, on peut démarrer et arreter une fois le bot et cela ne fonctionne plus ensuite

B)Bot
-> lance X dé à la demande selon le système de 7sea V2 (faire de groupe de dé pour atteindre la valeur 10 ou plus) plus quelques variantes
-> on peut s'attribuer un PJ pour voir apparraitre le nom sur les résultats du Lanceur
-> consultation fiche (Brut à améliorer pour lisibilité)




