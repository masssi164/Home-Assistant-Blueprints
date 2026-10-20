# Gerätetests und Kompatibilität

## Getesteter Stand

**v1.0.0-beta.1: End-to-End-Ablauf mit Siemens TP516DX3 erfolgreich getestet.**
Die Blueprints sind in Home Assistant eingerichtet; Kaffee wird über die neuen
Zentralen- und Favoriten-Skripte am realen Gerät zubereitet.

Die folgende Checkliste dient weiteren Gerätemodellen, neuen Funktionen und
Regressionstests. Ihre leeren Kästchen sind eine wiederverwendbare Testvorlage,
keine Rücknahme des bereits erfolgten End-to-End-Tests.

## Testumgebung

Datum, Blueprint-Version/Commit, Home-Assistant- und Home-Connect-Alt-Version sowie
Modell/E-Nummer und Firmware soweit bekannt festhalten. Keine Seriennummern oder
persönlichen Gerätekennungen veröffentlichen. Für UI-Tests zusätzlich Browser/App,
optionale Mushroom-Version und verwendete Bedienhilfen notieren.

## Checkliste für weitere Tests

- [ ] Beide Blueprints importieren und Zentrale mit fünf Entitäten derselben Maschine speichern.
- [ ] Favorit anlegen; persönliche Rezeptwerte bleiben getrennt vom Blueprint.
- [ ] Trockenlauf ohne Geräteaktion und beaufsichtigten realen Start prüfen.
- [ ] Start, Run und anschließendes Ready im Trace mit dem Gerät abgleichen.
- [ ] Zweiter Favorit während eines laufenden Zentralenskripts startet keine weitere Zubereitung.
- [ ] Bereits laufendes Getränk, lokale Bedienung oder fehlende Fernstartfreigabe verhindern einen weiteren Start.
- [ ] Fehlerhafte Gerätezuordnung und unknown/unavailable führen zu einem verständlichen Abbruch.
- [ ] Optionales Einschalten mit der Spülung der Maschine sicher testen.
- [ ] Jedes beworbene Getränk mit Standardwerten und den verwendeten Rezeptoptionen prüfen.
- [ ] Füllmengen, Stärke und Temperaturgrenzen pro Getränk dokumentieren; Heißwasser separat prüfen.
- [ ] Verwendete Dashboard-, Sprach- und Taster-Interfaces separat prüfen.
- [ ] Home-Assistant-Schema- und Simulations-CI für den jeweiligen Stand erfolgreich.
- [ ] Geteilte Traces und Testberichte enthalten keine Zugangsdaten oder privaten Kennungen.

Fehlerpfade mit Cloud-Unterbrechung oder zeitlichen Rennen nur in einer geeigneten
Testumgebung prüfen. Nicht während heißer Ausgabe riskant am Gerät manipulieren.

## Ergebnisvorlage

```text
Version/Commit:
Datum:
Home Assistant / Home Connect Alt:
Modell und Firmware (ohne Seriennummer):
Getestete Programme und Rezeptoptionen:
Start / Run / Ready beobachtet:
Verwendete Interfaces:
Ergebnis und Einschränkungen:
```

[Fehler oder Modellrückmeldung melden](https://github.com/masssi164/Home-Assistant-Blueprints/issues/new/choose) ·
[Teststand](validation.md)
