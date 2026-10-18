# Das Dashboard ist optional

[Zurück](../README.md)

Die Zubereitung muss zuerst als Skript funktionieren. Ein Dashboard repariert
keine fehlende Cloud-Anmeldung, Fernstart-Freigabe oder falsche Entity-Auswahl.

## Einfach: normale Home-Assistant-Karten

Ein **neues leeres Dashboard** anlegen. Nicht die Rohkonfiguration eines vorhandenen
Dashboards mit anderen Ansichten überschreiben. Du kannst im visuellen Editor je
Favorit eine Schaltfläche anlegen: verständlicher Name, Aktion **Skript einschalten /
Ausführen**, passendes Favorit-Skript auswählen. Kein Toggle als Getränk-Stopp verwenden.

Alternativ die [quick_start.yaml](../dashboards/quick_start.yaml) in den
Rohkonfigurationseditor des **neuen** Dashboards kopieren. Sie enthält nur Standardkarten.
Die fünf `script.kaffee_auf_zuruf_…` sind Beispiel-IDs. Karten im Editor öffnen und
deine tatsächlichen Favoriten bei **Entität und Aktion-Ziel** auswählen. Nicht
blind davon ausgehen, dass Home Assistant die ID aus einem Anzeigenamen exakt so
gebildet hat. Nicht unterstützte Getränke als Karten entfernen.

Es gibt keine zwingenden Doppeltipp- oder Langdruck-Aktionen. Die Hauptaktionen
haben Textbeschriftungen. Die reale Screenreader-/Tastatur-Abnahme ist dennoch offen.

## Optional: Barista-Ansicht aus dem Original

Die [barista.template.yaml](../dashboards/barista.template.yaml) bewahrt die Bereiche
aus der Vorlage: Ein-/Ausschalten und Status, Quick-Start, direkte Geräteoptionen,
Getränkezähler sowie Verbindung/Wartung. Die Hauptaufgabe steht vor der Statistik.

Zusätzlich wird **Mushroom** benötigt, einschließlich
`custom:mushroom-legacy-template-card`. Diese Variante erhält die von der Vorlage
verwendeten `layout`-, `badge_icon`- und `icon_color`-Eigenschaften. Die einfache
Ansicht benötigt Mushroom nicht.

**Achtung:** Die Power-/Standby-Tasten und die direkten Geräteoptionen umgehen
nicht die Cloud, aber sie umgehen die Kaffee-Zentrale. Sie wirken auch dann,
wenn die Zentrale auf Trockenlauf steht. Sie sind nicht durch deren single-Modus
gesperrt. Direktregler können das ausgewählte oder aktive Programm betreffen;
für reproduzierbare Favoriten die Rezeptwerte im Favorit-Skript hinterlegen.

Die Barista-Vorlage enthält absichtlich Tokens wie `__POWER_ENTITY__`.
**Nicht unverändert importieren.** Statt vieler Wiederholungen wird jede ID einmal
in einer lokalen Mapping-Datei eingetragen:

```bash
mkdir -p local
cp examples/dashboard_entities.example.json local/dashboard_entities.json
```

In `local/dashboard_entities.json` die benötigten Werte durch eigene Entity-IDs
ersetzen. Diese Datei ist privat und über `.gitignore` vom Repository ausgeschlossen.
Dann (optional, Python 3.11 oder neuer, keine Zusatzpakete nötig):

```bash
python3 tools/render_dashboard.py --style barista   --mapping local/dashboard_entities.json --output local/barista.yaml
```

Der Renderer prüft fehlende Tokens, das Entity-ID-Format und die erforderlichen
Domains. Er prüft **nicht**, ob diese Entities in deiner Installation existieren.
Er überschreibt keine vorhandene Ausgabedatei. Zum erneuten Rendern einen neuen
Dateinamen wählen. Anschließend in einem neuen Dashboard importieren und visuell
sowie mit dem verwendeten Hilfsmittel prüfen.

Für dieselbe Ersetzung beim einfachen Dashboard `--style native` verwenden.
Dort reichen die fünf Script-Mappings. Den Renderer niemals mit Zugangsdaten füttern.

Die Statistiken sind Anzeigen von Geräte-/Integrationszählern. Unbelegte Liter-
und Bohnenmengen-Umrechnungen wurden entfernt. Eine Summierung der drei
Kaffee-Kategorien wird ausdrücklich nicht als vollständige Getränkesumme inklusive
Heißwasser bezeichnet. Zählerstände sind keine aktuellen Messungen des Tasseninhalts.
