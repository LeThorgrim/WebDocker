# WebDocker
*https://github.com/LeThorgrim/WebDocker* <br><br>
WebDocker est un projet d'utilisation de docker dans le cadre de mes études, il simule un scénario où une organisation aurai besoin de lier de manière modulaire leurs différentes applications webs (Django & NodeJS par exemple), à une BDD unique tout en pouvant surveiller celle-ci avec un outil de gestion (dans mon projet: Adminer); tout cela de manière rapide et organisé autour d'un docker-compose.
<br><br>
Le projet comporte quatre modules indépendants (bien que les deux app aient besoin de la BDD) :

* App Django (Python), DriveDuWish adapté pour l'occasion
* App nodeJS, un simple site pour verifier si un utilisateur existe
* BDD PostgreSQL, auto-configuré par le fichier docker-compose
* Adminer (PHP), lui aussi auto-configuré par le fichier docker-compose

<br>

> *si vous voulez aussi allez voir la version originale de mon ancien projet DriveDuWish* <br>
>*https://github.com/LeThorgrim/DriveDuWish*

<br><br>

# Comment utiliser le projet ? 
<br>

* Django : http://127.0.0.1:8000/ ou http://localhost:8000/
> Sur l'appli Django, c'est là que vous pouvez créer/supprimer des comptes sur la database ainsi qu'utiliser le Drive personnel comme sur mon projet DriveDuWish.
* NodeJS : http://127.0.0.1:8001/ ou http://localhost:8001/
> C'est une simple app NodeJS qui sert de démonstration sur la versatilité du projet docker, il est relié à la même BDD que l'appli Django et sert simplement à verifier si un compte existe avec comme élement de recherche son pseudonyme.
* Adminer : http://127.0.0.1:8080/ ou http://localhost:8080/
> Adminer (anciennement phpMinAdmin), pour l'utiliser remplissez ces infos: <br>
> Système : PostgreSQL <br>
> Serveur : db <br>
> Utilisateur : db_admin<br>
> Mot de passe : db_password<br>
> Base de données : docker_db

<br>
<br>


<br><br>

# Comment lancer WebDocker avec docker 🐬 ?

## Ressources nécessaires :
>Docker Desktop <br>
>Invite de Commande

<br>

## Tutoriel :

*Pour chacune de ces opérations, allez à la racine de WebDocker.*
<br>

### Premier lancement
```
> docker-compose build
> docker-compose up
```
### Lancer le projet
```
> docker-compose up
ou
> docker-compose up -d (mode détaché)
```
### Eteindre le projet (si en mode détaché)
```
> docker-compose down
```
### Remettre le projet à zero
```
> docker-compose down -v
```