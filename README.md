# Kaffee auf Zuruf

**Sprache statt Touch – oder genau das Interface, das zu dir passt.**

Steuere deinen Home-Connect-Kaffeevollautomaten mit Home Assistant: über ein
Dashboard, Siri/HomeKit, eine Zigbee-Fernbedienung oder Automationen. Zwei
Skript-Blueprints trennen die gemeinsame Maschinensteuerung von deinen Lieblingsrezepten.
Die Verbindung zur Maschine läuft über **Home Connect Alt und die Home-Connect-Cloud**.

**Öffentliche Beta: `v1.0.0-beta.1`.** Der End-to-End-Ablauf mit den Blueprints ist
mit einem **Siemens TP516DX3** getestet. Rückmeldungen zu weiteren Modellen und
Verbesserungsvorschläge sind willkommen.

[Beta-Release](https://github.com/masssi164/Home-Assistant-Blueprints/releases/tag/v1.0.0-beta.1) ·
[Einrichtung](docs/installation.md) ·
[Fehler melden](https://github.com/masssi164/Home-Assistant-Blueprints/issues/new/choose) ·
[CI](https://github.com/masssi164/Home-Assistant-Blueprints/actions/workflows/validate.yml)

## Voraussetzungen

- **Home Assistant ab 2026.10.0**; die Schema-Tests laufen gegen 2026.10.2.
- Ein Home-Connect-Kaffeevollautomat mit aktiviertem Fernstart und per API
  verfügbarem Getränk. Welche Programme und Rezeptwerte funktionieren, hängt vom Modell ab.
- **Home Connect Alt** (`home_connect_alt`) aus HACS, fertig eingerichtet mit
  Home-Connect-Account und Entwickleranwendung. Gemeint ist nicht die eingebaute
  Integration `home_connect`.
- **Übersetzungsmodus Local** in Home Connect Alt, damit die internen Enumwerte
  verfügbar bleiben. Deine Home-Assistant-Oberfläche darf weiterhin Deutsch sein.

Das Repository enthält Blueprints und Dashboard-Vorlagen, keine zusätzliche
HACS-Integration. Python, Git, Mushroom und Apple-Geräte sind für die
Blueprint-Einrichtung nicht erforderlich.

## Beide Blueprints importieren

Die folgenden Links importieren die feste Version **`v1.0.0-beta.1`**, nicht den
jeweils neuesten Entwicklungsstand von `main`:

**[1. Zentrale importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmasssi164%2FHome-Assistant-Blueprints%2Fblob%2Fv1.0.0-beta.1%2Fblueprints%2Fscript%2Fcoffee_control%2Fprepare_coffee.yaml)**

**[2. Favorit importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmasssi164%2FHome-Assistant-Blueprints%2Fblob%2Fv1.0.0-beta.1%2Fblueprints%2Fscript%2Fcoffee_control%2Fcoffee_recipe.yaml)**

Alternativ in Home Assistant unter **Einstellungen → Automatisierungen & Szenen →
Blueprints → Blueprint importieren** die jeweilige GitHub-Datei-URL einfügen:
[Zentrale](https://github.com/masssi164/Home-Assistant-Blueprints/blob/v1.0.0-beta.1/blueprints/script/coffee_control/prepare_coffee.yaml) ·
[Favorit](https://github.com/masssi164/Home-Assistant-Blueprints/blob/v1.0.0-beta.1/blueprints/script/coffee_control/coffee_recipe.yaml).

## Zum ersten Kaffee

### 1. Eine Zentrale pro Maschine

Aus **Kaffee auf Zuruf – Zentrale** ein Skript erstellen und diese fünf Entitäten
**derselben Maschine** aus Home Connect Alt auswählen:

| Auswahlfeld | Entität |
|---|---|
| Verbindung | `binary_sensor` – Connected |
| Ein-/Ausschalten | `select` – PowerState, nicht der gleichnamige Sensor |
| Betriebszustand | `sensor` – OperationState |
| Fernstart erlaubt | `binary_sensor` – RemoteControlStartAllowed |
| Bedienung am Gerät aktiv | `binary_sensor` – LocalControlActive |

**Keine Geräte-ID eintippen:** Die Zentrale ermittelt sie aus den Entitäten und
prüft die gemeinsame Gerätezuordnung. [Hilfe zur Entitätenauswahl](docs/entities.md)

### 2. Lieblingsgetränk anlegen

Aus **Kaffee auf Zuruf – Favorit** ein Skript erstellen, das gerade angelegte
Zentralenskript und dein Getränk auswählen. Optional Füllmenge, Stärke und Temperatur
festlegen. Stärke und Temperatur verwenden die internen Werte deiner Maschine,
nicht frei gewählte Grad-Celsius-Angaben. [Rezeptwerte](docs/recipes.md)

### 3. Testen und verwenden

Zunächst den voreingestellten **Trockenlauf** ausführen. Danach Maschine und Gefäß
vorbereiten, Trockenlauf in der Zentrale ausschalten und einen beaufsichtigten
Kaffee zubereiten. Weitere Favoriten verwenden dieselbe Zentrale.

**[Ausführliche Schritt-für-Schritt-Anleitung](docs/installation.md)**

## Bedienung nach deinen Bedürfnissen

Dashboard, Sprache, Taster und Automationen rufen dieselben benannten Favoriten auf.
Die Maschinenlogik bleibt an einer Stelle. Persönliche Entitäten und Rezepte werden
in den daraus erstellten Skripten gespeichert, nicht in den Blueprint-Dateien.

**[Einfaches Dashboard](dashboards/quick_start.yaml):** eingebaute Karten mit fünf
Favorit-Tasten. Die Beispiel-Skript-IDs im Karteneditor durch deine Skripte ersetzen.

**[Barista-Vorlage](dashboards/barista.template.yaml):** optionales
Mushroom-Dashboard mit Status, Geräteoptionen und Statistik. Zusätzliche Entitäten
und Mushroom sind nur für diese Variante nötig. [Dashboard-Einrichtung](docs/dashboard.md)

[Bestehende Skripte umstellen](docs/migration.md) ·
[Siri, Zigbee und MCP](docs/interfaces.md) ·
[Fehlersuche](docs/troubleshooting.md) ·
[Updates](docs/maintenance.md)

## Grenzen und Sicherheit

Kaffee, Espresso, Cappuccino, Latte Macchiato und Heißwasser sind als Programmtypen
vorgesehen. Verfügbarkeit und zulässige Rezeptwerte bestimmt die jeweilige Maschine.
Die Beta ist mit dem Siemens TP516DX3 getestet; daraus folgt keine universelle
Kompatibilitätszusage für andere Modelle.

Der Standard ist **Trockenlauf**, automatisches Einschalten ist zunächst **aus**.
Auch das Einschalten kann eine Spülung auslösen. Die Skripte erkennen keine Tasse,
keinen Milchschlauch und keine ausreichende Gefäßgröße. **Nicht unbeaufsichtigt testen.**

Alle Favoriten einer Maschine müssen dieselbe Zentrale benutzen. `mode: single`
verhindert parallele Läufe dieser Zentrale, solange sie läuft; es ist keine globale
Gerätesperre gegen Hersteller-App oder andere Skripte. Nach unklarer Cloud-Antwort
wird nicht automatisch erneut gestartet. Ein Home-Assistant-Neustart oder
Skript-Abbruch kann die lokale Sperre beenden und stoppt nicht automatisch das Getränk.

## Mitmachen und Entwicklung

Fehlerberichte bitte mit Modell, Softwareversionen, Getränk, erwarteter und
beobachteter Funktion. Keine Zugangsdaten, Seriennummern oder privaten HA-Exporte
veröffentlichen; Traces vor dem Teilen anonymisieren.

[Mitentwickeln](CONTRIBUTING.md) · [Änderungen](CHANGELOG.md) ·
[Teststand](docs/validation.md) · [Gerätetests](docs/acceptance.md) ·
[Veröffentlichung](PUBLISH.md) · [MIT-Lizenz](LICENSE) · [Quellen](docs/sources.md)
