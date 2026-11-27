# Puissance 4.5

Un Puissance 4 en Python avec pygame, enrichi de **sorts** que les joueurs peuvent utiliser pendant la partie. Projet réalisé dans le cadre du Majeur Info.

## Description

Le jeu propose deux modes :

- **Solo** : le joueur affronte une IA (algorithme minimax avec élagage alpha-bêta). L'IA joue toujours les jetons jaunes.
- **Joueur contre joueur (Jcj)** : deux joueurs s'affrontent sur le même ordinateur, avec des sorts utilisables pendant la partie.

## Plateformes supportées

- Windows 10 et 11 (testé)

## Prérequis

- **Python 3.13** (la version est fixée dans le `Pipfile`)
- **Git** pour récupérer le projet
- **pipenv** pour installer les dépendances

Dépendances Python, installées automatiquement par pipenv :

| Bibliothèque | Version | Rôle |
|---|---|---|
| pygame-ce | 2.5.x | Affichage, sons, gestion des événements |

## Installation

1. **Cloner le dépôt** (dans un dossier hors OneDrive) :
   ```
   git clone https://github.com/Tyrano111/ProjetMajeurThomasEthanSamuel.git
   cd ProjetMajeurThomasEthanSamuel
   ```

2. **Installer pipenv** :
   ```
   pip install pipenv
   ```

3. **Créer l'environnement virtuel et installer les dépendances** :
   ```
   python -m pipenv install
   ```
   Cette commande lit le fichier `Pipfile.lock` et installe exactement les mêmes versions pour tout le monde.

> Sous Windows, la commande `pipenv` seule n'est parfois pas reconnue. Écrire `python -m pipenv` à la place fonctionne dans tous les cas.

## Lancer le jeu

Depuis la **racine du projet** (là où se trouvent `Pipfile` et le dossier `Assets/`) :

```
python -m pipenv run python Scripts/main.py
```

Il faut lancer le jeu depuis la racine : les images sont chargées avec des chemins relatifs (`Assets/...`).

## Commandes

| Action | Commande |
|---|---|
| Placer un jeton | Clic gauche sur une colonne de la grille |
| Utiliser un sort | Clic sur le bouton du sort, à droite (mode Jcj) |
| Ouvrir le menu pause | Touche `Échap` |

## Structure du projet

```
.
├── README.md
├── Pipfile
├── Pipfile.lock
├── Assets/            Images du jeu (grille, jetons, boutons de sorts)
├── Scripts/
│   ├── main.py        Point d'entrée : boucle principale du jeu
│   ├── Jeu.py         Logique de la partie
│   ├── Grille.py      Logique de lié à la grille 
│   ├── UI.py          Interface (menus, grille, boutons)
│   ├── IA.py          Adversaire du mode solo
│   └── ConstantesEtVariable.py   Constantes partagées
└── Texts/            Règles et documentation
```


## Dépannage

| Problème | Solution |
|---|---|
| `pipenv` n'est pas reconnu | Utiliser `python -m pipenv ...` |
| Erreur « Python 3.13 not found » | Installer Python 3.13 depuis python.org (cocher *Add Python to PATH*) |
| Les images ne s'affichent pas | Lancer le jeu depuis la racine du projet |
| `ModuleNotFoundError: pygame` | Lancer avec `python -m pipenv run python ...` pour utiliser le bon environnement |

## Auteurs

- Thomas
- Ethan
- Samuel