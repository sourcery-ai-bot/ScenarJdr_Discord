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
- visualisation de fiche et permet lancé un dé en fonction de la FDP
- diffuser la musique choisis par le mener

--------------------------------------------------------------------------

Etat actuel:
Pré Interface -> demande les paramètres nécéssaire (id du canal discord et token du bot )  
Interface -> juste une fenetre une combobox , et un bouton test qui lance un message prédéfinis du bot
Bot  -> lance X dé à la demande selon le système de 7sea V2 (faire de groupe de dé pour atteindre la valeur 10 ou plus) plus quelque variante


