# Mitentwickeln

Die normale Einrichtung benötigt kein Python. Die folgenden Schritte sind nur für
Entwicklung, Tests und Vorbereitungen zur Veröffentlichung.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Die lokalen Tests lesen die tatsächlich ausgelieferten YAML-Dateien, prüfen
Blueprint-Eingaben, rendern ihre Jinja-Ausdrücke und simulieren ausgewählte
Zustandswechsel/Fehler. Die Simulation ist **kein** Home Assistant, keine echte
Nebenläufigkeitsprüfung und kein Geräte-/Cloud-Test.

Für die zusätzliche echte Home-Assistant-Schemaprüfung ist Python **3.14.2 oder neuer**
und das festgelegte Core-Paket erforderlich (eine separate virtuelle Umgebung verwenden):

```bash
python -m pip install -r requirements-ha.txt
REQUIRE_HOME_ASSISTANT=1 python -m pytest -m homeassistant -q
```

Ohne `REQUIRE_HOME_ASSISTANT=1` werden diese HA-Schematests bewusst übersprungen.
Mit der Variable müssen Import und Schema tatsächlich funktionieren; ein fehlendes
Paket darf dann nicht stillschweigend als Erfolg zählen.

Die CI ist vorbereitet, aber bis zur Veröffentlichung und einem tatsächlichen Lauf
nicht als bestanden zu bezeichnen. Sie ersetzt auch dann keine Hardware-Abnahme.

Bitte Änderungen klein halten: zuerst reproduzierbarer Test/Trace, dann Logikänderung,
danach Dokumentation und Changelog. Keine Geräte-IDs, Zugangsdaten oder vollständigen
privaten Exporte in Issues/PRs. Tests müssen synthetische Entitäten verwenden.

Neue Getränke erfordern echte API-Programm-Keys und belegte Gerätekompatibilität,
nicht nur einen zusätzlichen Namen im Auswahlfeld.
