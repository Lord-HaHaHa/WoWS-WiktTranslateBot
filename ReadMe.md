# WoWS-Wikitranslator

## Allgemeine Infos

Das Programm übersetzt eine Englische WoWS-Wiki Seite ins Deutsche und speichert den erzeugten Code in eine Textdatei.

## Setup

Vorraussetzungen:

- Python 3
- Modul *requests*
- Modul *deep_translator*

## How To Use

Der Übersetzter kann über die Kommandozeile wiefolgt gestartet werden:

`python3 WikiScrper.py <Eng Schiffsnamen>`

Voraussetzung hiefür ist dass man sich bereits in dem selben Verzeichniss befindet.  

Die erzeugte Textdatei befindet sich im Unterordner *Sites*

## ErrorFiles

Da bisher nicht alle Templates und Verlinkungen des Englischen Wiki´s, den Deutschen zugeordnet wurden kann es sein dass eine solche Zuordnung nicht möglich ist.
In diesem Fall wird die Englische Vorlage nicht ausgewechselt und bleibt in der Generierten Textdatei.
Zudem wird im Unterodner *ErrorFiles* eine Datei angelegt, welche die unbekannten Templates / Links beinhaltet.
