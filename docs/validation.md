# Prüfstand der Vorabfassung

Stand: 18. Oktober 2026 · Vorabfassung `0.1.0-preview.1`.

## Tatsächliches lokales Ergebnis

**102 Tests bestanden, 2 Tests lokal ausdrücklich übersprungen.**

Ausgeführt: `python -m pytest -q` im Repository.
Umgebung: Python 3.13.5, PyYAML 6.0.3, Jinja2 3.1.6, pytest 9.0.2.
Zusätzlich: Python-Dateien kompilierbar. Das ehemalige Skript zur erstmaligen Repository-Erstellung entfällt; die GitHub-Publikation erfolgt separat.

Der abschließende Quellvergleich hat keine individuellen Gerätekennungen aus den
beiden bereitgestellten Originaldateien im öffentlichen Dateisatz gefunden.
Die separate private Vorkonfiguration gehört nicht zum Repository/ZIP.

## Umfang der bestandenen Tests

Die Tests lesen die tatsächlich ausgelieferten YAML-Dateien. Geprüft werden:
YAML/JSON und doppelte Schlüssel; Auflösen aller Blueprint-Inputs; Jinja-Syntax;
Laufzeit-Defaults und Typen; erlaubte Getränke/Optionen; Gerätezuordnung;
Trockenlauf; Einschalten; Verbindung, Remote-Freigabe, lokale Bedienung und
Betriebszustände; simulierte Wartezeit-/Fehlerpfade; genau eine Startanfrage;
Rezeptweitergabe; Dashboard-Mapping, Statistikfälle, interne Dokumentationslinks
und eine Datenschutzheuristik. Auch spät eintreffende Zustände nach abgelaufener
Wartezeit werden nicht als erfolgreicher Abschluss gewertet.

Beim Testen wurden ein Problem mit der Typprüfung vor der nativen Jinja-Konvertierung
sowie die Ganzzahl-Normalisierung der Füllmenge erkannt und korrigiert.

Die Zustandsabläufe verwenden einen kleinen expliziten **Test-Doppelgänger**.
Er ersetzt weder die HA-Template-Engine vollständig noch Runtime, Eventloop,
Cloud-API, Zeitmessung oder parallele Aufrufe. Die Tests beweisen insbesondere
**keine reale globale Sperrwirkung** und keine tatsächliche Getränkeausgabe.

## CI-Ergebnis auf GitHub

Am 18. Oktober 2026 liefen auf GitHub beide Jobs erfolgreich:

- `static-and-simulated`: **102 bestanden**, Python 3.13.
- `homeassistant-schema`: **2 bestanden** gegen echte Home-Assistant-2026.10.2-Schemas unter Python 3.14.

Nachweis: [GitHub-Actions-Lauf 39162471240](https://github.com/masssi164/Home-Assistant-Blueprints/actions/runs/39162471240), Commit `365aca55d33f917d6fc465958bb287bada760ddf`.
Die ursprünglichen CI-Läufe waren rot, weil die HA-Schematests erst einen echten HomeAssistant-Kontext im Eventloop benötigten. Dieser Testaufbau wurde korrigiert; die Skriptlogik musste nicht geändert werden.

## Noch nicht durchgeführt
- Import/Speichern der Vorabfassung in Home Assistant und reale Ausführung dort.
- Cloud-/Maschinenaufrufe, zeitliche Rennen und Sperrverhalten im HA-Eventloop.
- Frontend-, VoiceOver-, HomeKit-, Zigbee- oder MCP-Abnahme.

Das Home-Assistant-Paket konnte in der Arbeitsumgebung nicht nachinstalliert werden
(Netzwerk-/Namensauflösung nicht verfügbar); außerdem ist dort Python 3.13.5 vorhanden,
während der vorgesehene HA-Schemajob Python ab 3.14.2 benötigt.
Die CI hat die **Home-Assistant-2026.10.2**-Schemas mit Python 3.14
tatsächlich erfolgreich geprüft. Der Schemajob prüft jedoch nicht die reale
Geräteanbindung oder die Bedienung im Home-Assistant-Frontend.

Die Version bleibt bis zur tatsächlichen Abnahme eine **Vorabfassung**, nicht ein
bereits freigegebenes Release. Der aktuelle Stand wird auf GitHub als Preview bereitgestellt. Die genannte CI-Ausführung war erfolgreich; spätere Commits benötigen eigene grüne CI-Läufe.

[Abnahmeplan](acceptance.md) · [Quellen](sources.md)
