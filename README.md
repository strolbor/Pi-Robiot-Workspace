# Adeept Mars Rover Erweiterung

## Neues 2. Dashboard
Unter localhost:5000/dashboard zu finden.

## Neue Modi:
* YOLO 1+2
* Raum scannen
* fahrender Raum Scanner
* Alarm
* Sammeln

## Neue Funktionen:
* Rechts- und Links-Kurve
* Konstant vor und zurück fahren
* Kreisfahrmodus

## Modi

### YOLO 1
Der zu suchende Gegenstand muss vor der Kamera stehen, damit der Roboter hinfährt

### YOLO 2
Der zu suchende Gegenstand muss im Raum stehen, damit der Roboter hinfährt

### Raum Scanner
Der Roboter registeriert alle ihm bekannte Objekte und speichert sie.
Dabei macht er nach dem ersten Intervall eine 180° Drehung

### Fahrender Raum Scanner
Der Roboter fährt und scannt im 180° Winkel alle ihm bekannte Objekte.
#### Logik
Ist ein meter vor dir frei? -> fahre grade aus.
Aonst fahre nach rechts bzw. links.

### Alarm
Wenn der Roboter den trigger hat, wird dem Besitzer eine Nachricht per (E-Mail) gesendet.

### Sammeln
Fahre zum Objekt hin, bewege dich zurück und fahre zum nächsten Objekt hin.
*Voraussetzung*: YOLO 2