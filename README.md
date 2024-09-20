# uneviedefourmi M1 Project La Plateforme

## To do list

-

- Use different colors for multiple paths w/ a loop

- fix color palette on graphs

- save in an image folder the gif for each antshill

- ajouter capture d'écran à chaque étape

- Retourne erreur lors du dl du fichier txt si il manque Sv Sd ou s'il n'y a pas de chemin

- rajouter formule pour calculer nombre de chemin à emprunter par rapport à la distance totale du chemin et la prévision du nombre d'étape



### Bonus

- Version jeu éducatif


### Notes temporaires A DELETE
Avancée max par étape
Quelle proportion de la tâche accomplie t on en envoyant le max de débit dans un tel chemin ?

point de conflit - embouteillage





1. Envoie le max dans le meilleur chemin(1)
2. Si nombre d'étape nécessaire pour terminer chemin(2) > quantité début d'étape fourmies - débit


starting f 30
f step+1 for path 1 would mean 27 for path 2 to take into consideration

3 - 3 - 3 - 3  (    9     )
1 - 1 - 1 - 1 - 1 - 1 - 1 (  2  )
1 - 1 - 1 - 1 - 1 - 1 - 1 - 1 - 1


LEN DIFF : 3
FOR PATHS Meilleurs que path actuel
  IF len(new_path) - max( parmis lens(previous_paths)) * flow_rate >=
                 (    4     )                  *     3


previous f/2+len diff


if previous f diff(3)/


for path in paths[1:]
  if débit 1* (len(chemin1)-1) + débit 2* (len(chemin2)-1) < f de début d'étape/2:
    déplacer fourmi 3e chemin


for path in paths[1:]
  if débit 1* (len(chemin1)-1) e< f de début d'étape/2:
    déplacer fourmi 3e chemin










if f début d'étape - len(chemin2)*débit chemin2 - len(chemin1)*débit chemin1 > 0:
  on envoie dans le 2e chemin
