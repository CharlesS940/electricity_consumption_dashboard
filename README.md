## Setup du projet avec Poetry

1. Installez [Poetry](https://python-poetry.org/docs/#installation) si ce n'est pas déjà fait :
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Installez les dépendances du projet :
    ```bash
    poetry install
    ```

## Lancer l'application


Pour lancer le serveur Django:
```bash
poetry run python hwjob/manage.py runserver
```

Pour accéder à la page admin il faudra créer un superuser:
```bash
poetry run python hwjob/manage.py create superuser
```

## Migrations et base de données

Une copie de la base de données originale (`db.sqlite3.backup`) est incluse dans le repo pour permettre de tester les migrations:
Si vous souhaitez appliquer les migrations sur cette base remplacez la db avec le backup:
```bash
cp hwjob/db.sqlite3.backup hwjob/db.sqlite3
```
Et appliquez les migrations:
```bash
poetry run python hwjob/manage.py migrate
```

J'explique certains choix et features de l'application ci-dessous:

## Logique de détection d'anomalie et de chauffage électrique

**Détection du chauffage électrique** :
  On compare la consommation d'électricité des mois d'hiver (décembre, janvier, février) à celle des mois d'été (juin, juillet, août).
  Si la consommation hivernale est significativement supérieure (par défaut, plus de 2 fois), le client est considéré comme ayant un chauffage électrique.

**Détection d'anomalie** :
  Une anomalie est détectée si la variation de consommation d'un mois à l'autre dépasse un certain seuil (par défaut 50%) ET une variation absolue de plus de 200 kWh.
  Pour les clients avec chauffage électrique, des règles spécifiques s'appliquent en décembre où on s'attend à une forte hausse et en mars où on s'attend à une forte baisse. Dans ce cas on qualifie d'anomalie une baisse en décembre et une hausse en mars quel que soit l'ampleur de la variation.

  Cette méthode n'est pas parfaite car on observe que les changements de consommation arrivent parfois avant ou après ces mois ce qui peut être normal et résulte dans de fausses anomalies. Un autre moyen serait d'éviter de signaler des anomalies pour toute la période de novembre à avril parce que la consommation sera plus variable pendant cette période mais on pourrait alors éviter de signaler de vraies anomalies. 

## Calcul automatique dans la vue de consommation

La vue `consumption_view` vérifie si les informations d'anomalie ou de chauffage électrique sont absentes pour un client.
Si c'est le cas, elles sont automatiquement calculées et enregistrées dans la base de données à l'affichage de la page.

## Statut de santé basé sur les anomalies récentes

Le statut "Health" affiché dans l'application est basé sur la présence d'anomalies récentes (`has_recent_anomaly`) et non sur toutes les anomalies historiques.
Ce choix permet de mieux refléter l'état actuel du client.

Les instructions originales sont situées ci-dessous:

## Votre mission

Votre objectif est de mettre en place un dashboard simplifié de diagnostic énergétique.
Le projet possède déjà une base de données contenant les informations de consommation d'électricité de 5000 clients depuis 2015.

Le site comporte actuellement 3 pages:
- Une page d'accueil `/`: Permet de rechercher les clients (actuellement la recherche ne fonctionne que par id)
- Une page client `/consumption/<id>`: Affiche la courbe de consommation de l'année des 12 derniers mois, et informe en cas de chauffage électrique ou de dysfonctionnement. (vide pour le moment)
- Une page admin `/admin/clients`: Une liste de clients accessible uniquement au staff qui permet de rapidement voir les clients avec un chauffage électrique ou un dysfonctionnement. 

Votre mission, si vous l'acceptez est d'ajouter ce qui manque sur ces pages. C'est à dire:

- Sur le dashboard `/consumption/<id>`:
    - Afficher la courbe de consommation des 12 derniers mois.
    - Identifier et afficher si le client a un chauffage électrique ou non (indice: en hiver la consommation électrique est bien plus importante en cas de chauffage électrique).
    - Détecter et afficher un dysfonctionnement: cela se traduit par un changement brusque de la consommation d'un mois à l'autre. En cas de dysfonctionnement, indentifier le mois et l'année où le dysfonctionnement est survenu.
- Sur le dashboard `/admin/clients`:
    - Mettre à jour les colonnes `Heating` et `Health` de la liste des clients (`/admin/clients`).
- Sur la page d'accueil `/`:
    - (Optionnel) Rechercher par nom et/ou prénom

Quelques informations sur nos utilisateurs:
- Une partie de nos utilisateurs est sur mobile.
- La base de donnée de production contiendra des dizaines de milliers de clients.

Pour l'exercice, n'importe quel utilisateur peut accéder au dashboard de tout le monde. Nous n'attendons pas qu'un système d'authentification et d'autorisation soit ajouté.

Vous êtes libre de changer complètement l'application. Amusez-vous !

## Mise en place

- Si vous n'êtes pas familier avec Django, prenez un peu de temps pour lire le [guide de démarrage](https://www.djangoproject.com/)
- Cloner ce dépo (ne pas en faire un fork)
- Installer les dépendances se trouvant dans requirements.txt
- Démarrer le serveur: `$ python manage.py runserver`

## Librairies à votre disposition

Seul [Django](https://www.djangoproject.com/) et [black](https://github.com/psf/black) sont listés en dépendances Python.
En front [eva-icons](https://github.com/akveo/eva-icons#how-to-use) est installée.

Vous êtes libre d'installer d'autres dépendances si besoin,
que ce soit des dépendances Python (drf, ...),
javascript (React, Vue, Svelte, ...),
css (tailwindcss, bootstrap, ...).
