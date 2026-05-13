# Wichtige Linux Kommandozeilenbefehle

1. Aktuelles Arbeitsverzeichnis ausgeben
- pwd

2. Geben Sie den Inhalt des aktuellen Verzeichnisses aus.
- ls

3. Neues Verzeichnis /home/<Benutzer>/test erstellen  //Benutzer ist nur ein Placeholder
- mkdir /home/pi/test

4. In das neu erstellte Verzeichnis wechseln
- cd /home/pi/test

5. Neue Textdatei im Verzeichnis erstellen und verändern
- nano dateiname.txt

6. Hostnamen des Computers abfragen
- hostname //Zeigt nur den Namen an
- hostnamectl //Gibt weitere Information, wie Kernel, Maschine ID, etc. an

7. Eigene IP-Adresse ausgeben
- ip a oder ifconfig //Lokale IP Adresse ausgeben 
- curl ifconfig.me //Öffentliche IP Adresse ausgeben

8. Systemauslastung anzeigen
- top
- htop