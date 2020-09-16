# Projet LSIN 608: Simulateur d'une machine de Turing

Auteurs: Helmi Abed, Tahar Azouaoui, Louis Leskow, Mohamed Louiba, Farah Mahrez,
Ahmed Saadi, Wissem Sassi, Martin Sohier

## Organisation des dossiers:

Le code se trouve dans le dossier ```simulateur```, les tests unitaires
dans le dossier ```tests```.

Les fichiers ```__init__.py``` sont là pour permettre une organisation
en module dans des fichiers différents. Ils sont vides sauf pour celui
dans le ```derouleur```, les variables globales du derouleur s'y trouvent.

## Premiers tests:

Pour vérifier qu'il n'y a pas de problème d'import. A l'intérieur du dossier ```simulateur```, entrer:

```bash
python3 hello.py
```

Les tests unitaires sont exécutés à l'aide du module unittest.
Des exemples de tests sont donnés dans le dossier ```tests```, pour les lancers (à l'intérieur du dossier ```tests```):

```bash
python3 -m unittest # lance tout les tests
python3 -m unittest test_verificateur.py # pour un fichier de tests spécifique.
```

## Programmation en Python:

### Style:

* [Conventions de style](https://www.python.org/dev/peps/pep-0008/)
* [Conventions de style pour les docstrings](https://www.python.org/dev/peps/pep-0257/) (Les docstrings sont les commentaires constituant la documentation d'une classe/fonction entre """)

### Annotations de type: typing

Par défaut le typage en Python est implicite, nous utilisons le
module ```typing``` pour le rendre explicite, la majorité des tutoriels sur
Python n'utilise pas les annotations de type, et l'aspect du code peut
donc paraitre assez différent.

[La documentation](https://docs.python.org/fr/3/library/typing.html#module-typing)

### Tutoriels

* [Issue de la documentation officiel](https://docs.python.org/fr/3/tutorial/)

## Utilisation du dépôt, workflow par fonctionnalités:

* Récupérer le projet:

```bash
git clone https://gitlab.com/llproj/turing_simulateur.git
```

* Récupérer et fusionner

```bash
git pull origin master
```

* Créer une branche et la rejoindre:

```bash
git checkout −b fonctionnalite
```

* Fusion

```bash
git checkout master
git merge fonctionnalite
```

* Envoyer les modifications

```bash
git push origin master
```
