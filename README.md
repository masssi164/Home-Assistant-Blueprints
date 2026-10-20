# Kaffee auf Zuruf

**Sprache statt Touch – oder genau das Interface, das zu dir passt.**

Mit Home Assistant, Home Connect Alt und eigenen Skripten lässt sich ein kompatibler
Kaffeevollautomat über ein Dashboard, Siri/HomeKit, eine Zigbee-Fernbedienung oder
Automationen bedienen. Das Interface ist austauschbar; die Geräteanbindung bleibt
von der Home-Connect-Cloud abhängig. Die Hersteller-App wird damit nicht als
unzugänglich dargestellt.

**Status: Praxiseinsatz beim Autor bestätigt; weiterhin Vorabfassung.** Die Blueprints
sind in der Home-Assistant-Installation des Autors eingerichtet; laut Rückmeldung
funktioniert die bisherige Kaffee-Steuerung weiterhin. Zusätzlich wurde die Logik
mit YAML-/Template-Tests und simulierten Zuständen geprüft. Ein vollständiger,
dokumentierter End-to-End-Test sämtlicher Blueprint-Abläufe und eine Freigabe für
andere Gerätemodelle stehen noch aus. [Prüfstand](docs/validation.md) · [Abnahme](docs/acceptance.md)

[CI: Validate coffee blueprints](https://github.com/masssi164/Home-Assistant-Blueprints/actions/workflows/validate.yml)

Die Ausgangskonfiguration stammt von einem **Siemens TP516DX3** (Modellbezeichnung
in den bereitgestellten Entity-IDs). Das ist keine Zusage für sämtliche
Home-Connect-Maschinen. Der gemeldete Praxiseinsatz ersetzt keine dokumentierte
Hardware-Abnahme aller Blueprint-Funktionen.

## Für den ersten Kaffee

Du brauchst:

- Einen Home-Connect-Kaffeevollautomaten, der das gewünschte Getränk per API starten
  lässt; Fernstart am Gerät aktivieren und sichere Vorbereitung laut Geräteanleitung.
- Eine funktionierende Home-Assistant-Installation. Diese Vorabfassung richtet sich
  vorläufig an **2026.10.x**; ältere Versionen sind nicht freigegeben.
- **Home Connect Alt** (`home_connect_alt`) aus HACS, einen Home-Connect-Account und
  eine eigene Entwickleranwendung für deren OAuth/API-Zugang. Nicht mit der
  eingebauten Integration `home_connect` verwechseln.
- Bei Home Connect Alt den **Übersetzungsmodus Local**. Deine Oberfläche darf
  weiterhin Deutsch sein. Die Skripte brauchen die unveränderten internen Enumwerte.

**Dieses Repository ist eine Blueprint-/Dashboard-Sammlung, keine neue HACS-Integration.**
HACS wird für Home Connect Alt und bei Bedarf Mushroom verwendet. Die beiden
Skriptvorlagen werden über die Blueprint-Funktion eingerichtet.

Kein Python, kein Git, kein Mushroom und kein Apple-Gerät sind für den normalen
Blueprint-Einrichtungsweg erforderlich. Ein Raspberry Pi ist ebenfalls keine
besondere Voraussetzung dieses Projekts.

**Ablauf:** Zwei Blueprints importieren → eine Zentrale mit fünf Entitäten anlegen →
einen Favoriten anlegen → Trockenlauf → beaufsichtigter Test → weitere Interfaces.
Die erstmalige Einrichtung von HACS/Cloud-Anmeldung kommt gegebenenfalls noch dazu;
es wird keine unrealistische Zwei-Minuten-Installation versprochen.

**[Schritt-für-Schritt-Anleitung](docs/installation.md)**

### Blueprints

| Vorlage | Aufgabe |
|---|---|
| [Zentrale](blueprints/script/coffee_control/prepare_coffee.yaml) | Einmal pro Maschine: Verbindung, Einschalten, Bereitschaft, Start und Rückmeldungen |
| [Favorit](blueprints/script/coffee_control/coffee_recipe.yaml) | Beliebig viele benannte Rezepte, alle mit derselben Zentrale |

Diese GitHub-Datei-URLs können unter
**Einstellungen → Automatisierungen & Szenen → Blueprints → Blueprint importieren**
verwendet werden:

- [Zentrale importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmasssi164%2FHome-Assistant-Blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fcoffee_control%2Fprepare_coffee.yaml)
- [Favorit importieren](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fmasssi164%2FHome-Assistant-Blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fcoffee_control%2Fcoffee_recipe.yaml)

**Die Blueprints sind beim Autor eingerichtet; die bestehende Steuerung funktioniert
laut Rückmeldung weiterhin.** Die öffentliche Fassung bleibt bis zur dokumentierten
End-to-End-Abnahme eine Vorabversion. Die Links zu `main` können sich ändern;
eine stabile Release-Verknüpfung folgt nach der Abnahme.

## Was getrennt bleibt

```text
Dashboard / Siri / Zigbee-Taster / Automation / optional KI-Agent
                         ↓
                  benannte Favoriten
                         ↓
           eine gemeinsame Kaffee-Zentrale
                         ↓
              Home Connect Alt → Cloud → Maschine
```

Eigene Geräte-Entitäten und Rezeptwerte werden in den daraus angelegten Skripten
konfiguriert, nicht in den Blueprint-Dateien. Ein Update soll keine persönlichen
IDs oder Favoriten überschreiben. Inkompatible Änderungen erfordern trotzdem eine
Migration; sie werden nicht automatisch auf eine laufende Installation angewendet.

Kaffee, Espresso, Cappuccino, Latte Macchiato und Heißwasser entsprechen den fünf
Programmtypen der Ausgangsskripte. Die tatsächliche Verfügbarkeit sowie Mengen,
Stärken und Temperaturen bestimmt das konkrete Gerät. Ein Kaffee-Temperaturwert
ist hier ein Hersteller-Enum, nicht beliebig einstellbare Grad Celsius.

## Dashboards und Erweiterungen

**[Einfaches Dashboard](dashboards/quick_start.yaml):** eingebaute Karten, fünf
Favorit-Tasten. Die Beispiel-Skript-IDs im Karteneditor auf deine Skripte einstellen.

**[Barista-Vorlage](dashboards/barista.template.yaml):** aus dem bereitgestellten
Mushroom-Dashboard abgeleitet, mit Status, Schnellstart, Geräteoptionen und
bereinigter Statistik. Sie benötigt zusätzliche Entitäten und Mushroom; sie ist
nicht Voraussetzung für den ersten Kaffee. [Einrichtung beider Varianten](docs/dashboard.md)

[Bestehende Installation umstellen](docs/migration.md) · [Entitäten und IDs](docs/entities.md) · [Rezepte](docs/recipes.md) ·
[Siri, Zigbee und MCP](docs/interfaces.md) · [Fehlersuche](docs/troubleshooting.md) ·
[Änderungen gegenüber der Vorlage](docs/source-review.md)

## Grenzen und Sicherheit

Der Standard ist **Trockenlauf**, automatisches Einschalten ist zunächst **aus**.
Auch das Einschalten kann eine Spülung auslösen. Die Skripte erkennen keine Tasse,
keinen Milchschlauch und keine ausreichende Gefäßgröße. **Nicht unbeaufsichtigt testen.**

Alle Favoriten einer Maschine müssen dieselbe Zentrale benutzen. `mode: single`
verhindert parallele Läufe dieser Zentrale, solange sie läuft; es ist **keine globale
Gerätesperre** gegen Hersteller-App, andere Skripte oder weitere Zentralen.
Nach einer unklaren Cloud-Antwort wird nicht automatisch erneut gestartet.
Neustarts/Abbruch von Home Assistant können die lokale Sperre beenden. Ein
Skript-Abbruch stoppt nicht automatisch das Getränk.

## Entwicklung und Veröffentlichung

[Mitentwickeln](CONTRIBUTING.md) · [Updates und Releases](docs/maintenance.md) ·
[GitHub Actions & Releases](PUBLISH.md) · [Lizenz](LICENSE) · [Quellen](docs/sources.md)

Das Projekt enthält weder API-Zugangsdaten noch private Geräte-IDs oder die
vollständigen Home-Assistant-Exporte des Autors. Eine Community-Veröffentlichung
begleitet das geplante Hauptvideo; hier werden keine bereits verfügbaren Videos
oder Releases behauptet.
