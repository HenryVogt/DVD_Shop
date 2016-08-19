# DVD Shop

Für das Modul Web-basierte Anwendungen an der Hochschule RheinMain wurde ein DVD Shop in Python implementiert. Basierend auf einer Kundendatenbank sollten einige einfache Oberflächen und kurze Prozessschritte realisiert werden. Die Zielgruppe sind dabei hauptsächlich Mitarbeiter und auch Kunden.


# Hinweise
Als Datenbestand wird die [Dellstore](http://linux.dell.com/dvdstore/) Datenbank genutzt. Das SQL Script zum erzeugen der Datenbank ist im Ordner [db_stuff](https://github.com/HenryVogt/DVD_Shop/tree/master/db_stuff). Zusätzlich gibt es noch ein SQL Script für App spezifische Views. Beide Scripte können mit folgenden Kommandos ausgeführt werden:
````
psql -h db_host -U db_user db_name < dellstore.sql
psql -h db_host -U db_user db_name < create_views.sql
````

In der App muss die datei [config.py](https://github.com/HenryVogt/DVD_Shop/blob/master/app/config.py) mit den datenbankspezifischen Daten befüllt werden
````
DB_HOSTNAME = "db.examplehost.com"
DB_NAME = "db.name"
DB_USER = "db.user"
DB_PASSWORD = "db.password"
````


Zum ausführen der Admin App muss folgende WSGI Datei genutzt werden:
````
dvdshop.wsgi
````
Zum ausführen der Kunden App muss folgende WSGI Datei genutzt werden:
````
dvdorder.wsgi
````

# Screenshot
###### Admin App
![Admin View](https://github.com/HenryVogt/DVD_Shop/blob/master/admin_view.png)
###### Kunden App
![Customer View](https://github.com/HenryVogt/DVD_Shop/blob/master/customer_view.png)
