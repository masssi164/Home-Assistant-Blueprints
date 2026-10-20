# Änderungen

## 1.0.0-beta.1 – 20. Oktober 2026

Erste öffentliche Beta.

- End-to-End-Kaffeezubereitung mit den Blueprint-Skripten am Siemens TP516DX3 getestet.
- README und Testdokumentation auf einen einheitlichen Beta-Stand gebracht.
- Importlinks und Blueprint-Quellverweise auf `v1.0.0-beta.1` festgelegt.
- Veröffentlichung als GitHub-Pre-Release nach beiden erfolgreichen CI-Prüfungen.
- Zentrale, Favorit und natives Dashboard als einzelne Release-Dateien.
- Keine Änderung an Zubereitungslogik, persönlichen Skripten oder Standardwerten.

[Release-Notizen](releases/v1.0.0-beta.1.md)

## 0.1.0-preview.1 – interne Vorabfassung, nicht als Release veröffentlicht

Aus den ursprünglichen Kaffee-Skripten und dem Barista-Dashboard abgeleitet:

- Zwei Script-Blueprints: gemeinsame Zentrale pro Maschine und konfigurierbare Favoriten.
- Fünf Entitäten-Auswahllisten mit automatischer Gerätezuordnung.
- Laufzeit-Defaults und Validierung für Getränk und optionale Rezeptparameter.
- Gemeinsamer single-Modus bis zur beobachteten Rückkehr nach Ready; kein Start-Retry.
- Trockenlauf als Standard, automatisches Einschalten nur nach bewusster Freigabe.
- Native Quick-Start-Ansicht und bereinigte optionale Mushroom-Barista-Vorlage.
- Lokales Dashboard-Mapping statt privater Geräte-IDs im öffentlichen Repository.
- Einrichtungs-, Rezept-, Interface-, Migrations-, Fehlersuch- und Testdokumentation.
- Statische, Template-, Simulations- und Home-Assistant-Schema-Tests.
