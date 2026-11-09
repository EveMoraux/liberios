"""Citations du jour LibERIOS : repliques cultes de jeux video, films, series et culture geek.

Chaque entree : (citation, qui, oeuvre, annee, genre). Repliques courtes, en VF quand
elle est connue. La rotation change chaque jour et d'une page a l'autre.
"""
from __future__ import annotations

import datetime as dt

CITATIONS: list[tuple[str, str, str, int, str]] = [
    # Jeux video
    ("Il est dangereux d'y aller seul ! Prends ceci.", "Le vieil homme", "The Legend of Zelda", 1986, "Jeu vidéo"),
    ("Le gâteau est un mensonge.", "Inscription murale", "Portal", 2007, "Jeu vidéo"),
    ("Hey ! Listen !", "Navi", "Ocarina of Time", 1998, "Jeu vidéo"),
    ("It's-a me, Mario !", "Mario", "Super Mario 64", 1996, "Jeu vidéo"),
    ("La guerre… La guerre ne change jamais.", "Le narrateur", "Fallout", 1997, "Jeu vidéo"),
    ("Rien n'est vrai, tout est permis.", "Le Credo", "Assassin's Creed", 2007, "Jeu vidéo"),
    ("Un homme choisit, un esclave obéit.", "Andrew Ryan", "BioShock", 2007, "Jeu vidéo"),
    ("All your base are belong to us.", "CATS", "Zero Wing", 1991, "Jeu vidéo"),
    ("Finish him !", "L'annonceur", "Mortal Kombat", 1992, "Jeu vidéo"),
    ("Fais un tonneau !", "Peppy Hare", "Star Fox 64", 1997, "Jeu vidéo"),
    # Films
    ("Que la Force soit avec toi.", "Han Solo", "Star Wars", 1977, "Film"),
    ("Fais-le, ou ne le fais pas. Il n'y a pas d'essai.", "Yoda", "L'Empire contre-attaque", 1980, "Film"),
    ("Hello there.", "Obi-Wan Kenobi", "La Revanche des Sith", 2005, "Film"),
    ("Vers l'infini et au-delà !", "Buzz l'Éclair", "Toy Story", 1995, "Film"),
    ("Houston, nous avons un problème.", "Jim Lovell", "Apollo 13", 1995, "Film"),
    ("Je reviendrai.", "Le Terminator", "Terminator", 1984, "Film"),
    ("Hasta la vista, baby.", "Le Terminator", "Terminator 2", 1991, "Film"),
    ("Il n'y a pas de cuillère.", "L'enfant", "Matrix", 1999, "Film"),
    ("Je s'appelle Groot.", "Groot", "Les Gardiens de la Galaxie", 2014, "Film"),
    ("Un grand pouvoir implique de grandes responsabilités.", "Oncle Ben", "Spider-Man", 2002, "Film"),
    ("Tu ne passeras pas !", "Gandalf", "La Communauté de l'anneau", 2001, "Film"),
    ("Un magicien n'est jamais en retard. Il arrive précisément à l'heure prévue.", "Gandalf", "La Communauté de l'anneau", 2001, "Film"),
    ("Mon précieux.", "Gollum", "Les Deux Tours", 2002, "Film"),
    ("Courage, fuyons !", "Le roi Arthur", "Monty Python : Sacré Graal !", 1975, "Film"),
    ("Hakuna matata !", "Timon et Pumbaa", "Le Roi lion", 1994, "Film"),
    ("La vie, c'est comme une boîte de chocolats : on ne sait jamais sur quoi on va tomber.", "Forrest Gump", "Forrest Gump", 1994, "Film"),
    ("Je suis Batman.", "Batman", "Batman", 1989, "Film"),
    ("Le monde se divise en deux catégories : ceux qui ont un pistolet chargé et ceux qui creusent.", "Blondin", "Le Bon, la Brute et le Truand", 1966, "Film"),
    ("T'as d'beaux yeux, tu sais.", "Jean", "Quai des brumes", 1938, "Film"),
    ("Ce sont nos choix qui montrent ce que nous sommes vraiment, beaucoup plus que nos aptitudes.", "Albus Dumbledore", "Harry Potter et la Chambre des secrets", 2002, "Film"),
    ("Puisse le sort vous être favorable.", "Effie Trinket", "Hunger Games", 2012, "Film"),
    ("Nous sommes tous fous ici.", "Le Chat du Cheshire", "Alice au pays des merveilles", 1951, "Film"),
    # Series
    ("C'est pas faux.", "Perceval", "Kaamelott", 2005, "Série"),
    ("Le gras, c'est la vie.", "Karadoc", "Kaamelott", 2005, "Série"),
    ("L'hiver vient.", "Ned Stark", "Game of Thrones", 2011, "Série"),
    ("Tu ne sais rien, Jon Snow.", "Ygritte", "Game of Thrones", 2012, "Série"),
    ("C'est la voie.", "Les Mandaloriens", "The Mandalorian", 2019, "Série"),
    ("Vous avez essayé de l'éteindre et de le rallumer ?", "Roy", "The IT Crowd", 2006, "Série"),
    ("Bazinga !", "Sheldon Cooper", "The Big Bang Theory", 2007, "Série"),
    ("D'oh !", "Homer Simpson", "Les Simpson", 1989, "Série"),
    ("Wubba lubba dub dub !", "Rick Sanchez", "Rick et Morty", 2013, "Série"),
    ("Allons-y !", "Le Docteur", "Doctor Who", 2005, "Série"),
    ("C'est plus grand à l'intérieur !", "Les compagnons du Docteur", "Doctor Who", 1963, "Série"),
    ("La vérité est ailleurs.", "Le générique", "X-Files", 1993, "Série"),
    ("Longue vie et prospérité.", "Spock", "Star Trek", 1967, "Série"),
    ("Je suis celui qui frappe.", "Walter White", "Breaking Bad", 2011, "Série"),
    # Livres et culture geek
    ("La réponse est 42.", "Pensées Profondes", "Le Guide du voyageur galactique", 1979, "Livre"),
    ("N'oubliez pas votre serviette.", "Le Guide", "Le Guide du voyageur galactique", 1979, "Livre"),
    ("Ce n'est pas un bug, c'est une fonctionnalité.", "Proverbe de développeur", "Folklore informatique", 1980, "Geek"),
    ("Il y a 10 types de personnes : celles qui comprennent le binaire et les autres.", "Blague de développeur", "Folklore informatique", 1990, "Geek"),
]


def citation_du_jour(day: dt.date, slot: int = 0) -> tuple[str, str, str, int, str]:
    """Une citation par jour et par emplacement, sans doublon dans un meme numero."""
    step = 7  # premier avec la taille de la liste : les emplacements ne se croisent pas
    index = (day.toordinal() * 3 + slot * step) % len(CITATIONS)
    return CITATIONS[index]
