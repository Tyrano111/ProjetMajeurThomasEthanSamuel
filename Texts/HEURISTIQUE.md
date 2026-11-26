**Exlication du fonctionnement de L'IA** :

**4 fonctions** :

-   **empty_space** : Elle vérifie simplement les colonnes où le jeton peut être placé.

-   **score_grid** : Elle permet d'évaluer le score de la grille en fonction du positionnement des jetons.
			     Il est borné entre -0.9 et 0.9 pour éviter d'atteindre -1 (victoire de l'humain) et 1 (victoire de l'IA).

			     On parcours toutes les fenêtres de 4 et on attribue un score à chacune d'entre elle,
			     pour par exemple 1, 2 ou 3 jetons alignés non bloqué pour l'IA, on attribue +1, +10 et +50 respectivement.
			     Si c'est en faveur de l'humain, c'est -1, -11 et -75, des scores plus importants pour que l'IA soit plus préocupée par la défense.
			     Une fenêtre de 4 avec aucun jeton ou plusieurs jetons des 2 couleurs (fenêtre bloquée), on n'attribue pas de score.

-   **minimax** : C'est une fonction vue en cours, par récursivité elle teste chaque coup possible,
			  en alternant jeton rouge et jaune, dans chaque colonne jusqu'à une profondeur fixée.
			  Si la grille est pleine pendant son exécution elle renvoie 0,
			  en cas de victoire elle renvoie -1 ou 1 auquel on soustrait ou ajoute la profondeur/1000 pour favoriser les victoires rapides sans revenir dans l'encadrement -0.9/0.9,
			  et sinon le plus souvent elle renvoie le score de la grille si la profondeur max est atteinte.
			  La profondeur est paire pour que l'IA considère en dernier son coup, ça évite qu'elle joue trop défensivement.

			  C'est elle qui fait la majorité du temps de calcul de l'IA car il y a 7^(n) coups à tester (7 colonnes au début et n la profondeur de l'IA).
			  Le temps de calcul se réduit en fin de partie.

			  On l'optimise avec du alpha beta pruning, une fenêtre de valeur entre alpha (l'IA va choisir ce qui maximise son score) et beta (l'humain minimise son score)
			  En considérant que l'humain et l'IA vont jouer parfaitement, si une branche du graphe de score ne permet forcément pas
			  un score plus favorable pour l'un des 2 joueurs, on peut ne pas l'explorer et on réduit le temps de calcul.

-   **best_placement** : Elle renvoie le meilleur coup à jouer entre les colonnes disponibles.
				    Pour chacune de ces colonnes, on place un jeton, on lance minimax, on le retire,
				    puis on renvoie la colonne avec la meilleure valeur.

				    Deux optimisations rapides:
				    Si on peut gagner ou perdre en un coup on joue sur cette colonne directement.
				    On évalue les positions les plus proches du centre centre en premier puisque ce sont les plus favorables,
				    c'est une heuristique intuitive au puissance 4.