# Einrichtung: erst ein funktionierender Favorit

[Zurück zur Übersicht](../README.md)

## 1. Die Geräteanbindung muss vorher funktionieren

Home Assistant muss mit der Maschine über **Home Connect Alt** verbunden sein.
Installiere diese Integration über HACS nach ihrer
[Installationsanleitung](https://github.com/ekutner/home-connect-hass#installation-instructions).
Dort sind die Registrierung der Entwickleranwendung, der OAuth-Redirect und die
Anmeldung beschrieben. Client-ID und Client-Secret nur in Home Assistant hinterlegen,
niemals in dieses Repository oder ein Issue kopieren. Home Assistant muss die Cloud
erreichen können; das ist keine rein lokale Geräteanbindung.

Prüfe, dass das Gerät in der Home-Connect-App eingerichtet ist und dass Fernstart
für dein Modell erlaubt/aktiviert ist. Schalte es für den ersten Test selbst ein.
Warte das Ende einer eventuellen Spülung ab. Stelle ein ausreichend großes Gefäß
unter den passenden Auslauf; Milchgetränke benötigen zusätzlich den passenden
Milchanschluss. Beachte dafür die Geräteanleitung.

Öffne **Einstellungen → Geräte & Dienste → Home Connect Alt → Konfigurieren**
(je nach Version auch über das Menü des Integrationseintrags). Stelle
**Translation Mode / Übersetzungsmodus = Local** ein. Das stellt nicht die ganze
Home-Assistant-Oberfläche auf Englisch um. Alte Automationen, die übersetzte
Zustände verwenden, müssen bei einem Wechsel zu Local ebenfalls angepasst werden.

## 2. Beide Script-Blueprints bereitstellen

### Import aus dem öffentlichen GitHub-Repository

In der [README](../README.md) die beiden Importlinks verwenden oder die URL der
jeweiligen YAML-Datei aus GitHub kopieren. In Home Assistant:
**Einstellungen → Automatisierungen & Szenen → Blueprints → Blueprint importieren**.
Voransicht prüfen und importieren. Jeweils für Zentrale und Favorit wiederholen.

Bei einem privaten Repository kann Home Assistant die öffentlichen URLs nicht lesen.
Keinen GitHub-Token in eine Import-URL einbauen.

### Alternativ: lokaler Import, auch offline

Im Home-Assistant-Konfigurationsverzeichnis diese Struktur anlegen:

```text
/config/blueprints/script/coffee_control/
├── prepare_coffee.yaml
└── coffee_recipe.yaml
```

Die zwei Dateien aus `blueprints/script/coffee_control/` hierhin kopieren, zum
Beispiel mit dem bereits verwendeten Datei-Editor oder Dateizugriff deiner Installation.
`/config` bezeichnet das HA-Konfigurationsverzeichnis; je nach Installationsart heißt
der sichtbare Ordner nur `config`. Nicht in `www`, `custom_components` oder direkt
in `scripts.yaml` kopieren. Blueprints/Skripte neu laden; falls die Liste die neuen
Dateien nicht aufnimmt, Home Assistant geplant neu starten. Die Importfunktion
ist eine URL-Importfunktion, kein Upload-Dialog für lokale Dateien.

## 3. Genau eine Zentrale pro Maschine anlegen

In der Blueprint-Liste **Kaffee auf Zuruf – Zentrale** auswählen und daraus ein
**Skript** erstellen. Falls die Liste keinen direkten Knopf zeigt:
**Skripte → Skript erstellen → Blueprint verwenden** und diese Vorlage wählen.

Die fünf Felder ausfüllen. Alle müssen aus Home Connect Alt und von derselben
Maschine stammen:

| Feld | Gesuchte Entität |
|---|---|
| Verbindung | `binary_sensor`, Connected |
| Ein-/Ausschalten | `select`, PowerState – nicht der gleichnamige Sensor |
| Betriebszustand | `sensor`, OperationState |
| Fernstart erlaubt | `binary_sensor`, RemoteControlStartAllowed |
| Bedienung am Gerät aktiv | `binary_sensor`, LocalControlActive |

Die [ID-Hilfe](entities.md) beschreibt die Suche und Rohzustände genauer.
**Eine Geräte-ID musst du nicht kopieren.** Die Zentrale ermittelt sie über den
Verbindungssensor und prüft, dass die übrigen vier Entitäten zum selben Gerät gehören.

**Trockenlauf eingeschaltet lassen**, automatisches Einschalten zunächst ausgeschaltet.
Zum Beispiel als **Kaffee auf Zuruf Zentrale** speichern. Notiere die tatsächlich
vergebene Entity-ID. Der Anzeigename und die Entity-ID sind nicht dasselbe;
Home Assistant kann bei Namenskonflikten eine Ziffer anhängen.

## 4. Den ersten Favoriten anlegen

Mit **Kaffee auf Zuruf – Favorit** ein weiteres Skript erstellen. Als Zentrale
**das gerade angelegte Skript**, nicht diesen oder einen anderen Favoriten wählen.
Zunächst **Kaffee** auswählen und alle optionalen Rezeptwerte unverändert lassen.
Als **Kaffee auf Zuruf Kaffee** speichern.

Den Favoriten über **Ausführen** starten. Es darf jetzt kein Wasser laufen und
keine Maschine eingeschaltet werden. In den Home-Assistant-Benachrichtigungen
erscheint eine Trockenlaufmeldung oder eine konkrete Konfigurationsfehlermeldung.

**Eine erfolgreiche Trockenlaufmeldung bestätigt keinen echten API-Aufruf und
keine Kompatibilität des Getränks.** Sie prüft nur die Auswahl, Eingabestruktur und
gelesenen Ausgangszustände.

## 5. Einmal beaufsichtigt wirklich zubereiten

Maschine bereit, Gefäß vorhanden und Auslauf passend? In der **Zentrale** den
Trockenlauf ausschalten und speichern. Den Favoriten genau einmal ausführen.
Die Zentrale sendet eine Startanfrage und wartet auf `Run` und anschließend `Ready`.
Währenddessen bleibt sie aktiv und nimmt keinen weiteren parallelen Skriptlauf an.

Bei einer Fehlermeldung oder unklaren Rückmeldung **nicht mehrfach drücken**.
Am Gerät prüfen, was tatsächlich passiert ist, und den Skript-Trace öffnen.
Ein Netzwerkfehler kann bedeuten, dass der Befehl angekommen ist, obwohl die
Rückmeldung fehlt. [Fehlersuche](troubleshooting.md)

## 6. Erst danach erweitern

Weitere Favoriten aus derselben Favorit-Vorlage anlegen und immer dieselbe Zentrale
wählen. Du musst die fünf Maschinen-Entitäten nicht erneut eingeben.

[Eigenes Rezept](recipes.md) → [Dashboard](dashboard.md) →
[Siri oder Zigbee](interfaces.md). Automatisches Einschalten erst bewusst aktivieren,
wenn du den Spülablauf deiner Maschine sicher berücksichtigt hast.

Vor einer Weitergabe an andere die [Abnahmeliste](acceptance.md) durcharbeiten.
