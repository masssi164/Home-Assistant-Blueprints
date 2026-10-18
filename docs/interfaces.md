# Dasselbe Rezept, unterschiedliche Interfaces

[Zurück](../README.md)

Alle hier beschriebenen Wege starten **denselben benannten Favoriten**. Die
Geräteanbindung bleibt Home Connect Alt über die Home-Connect-Cloud. Ein lokaler
Zigbee-Taster macht die Verbindung zum Kaffeevollautomaten nicht cloudfrei.

## Apple Home und Siri (optional)

In Home Assistant **HomeKit Bridge** verwenden, nicht **HomeKit Device**. Bei einer
vorhandenen Bridge deren Einbindung anpassen, nicht parallel dieselbe Bridge noch
in YAML duplizieren. Nur die gewünschten Favorit-Skripte für HomeKit freigeben.

Die [HomeKit-Bridge-Dokumentation](https://www.home-assistant.io/integrations/homekit/)
führt Skripte als Schalter auf. In Apple Home kann daraus eine eindeutig benannte
Szene entstehen, zum Beispiel „Kaffee bitte“, die den Favoriten einschaltet.
Den gewünschten Siri-Aufruf anschließend am eigenen System testen. Ein abgeschalteter
Skript-Schalter ist **kein** verifizierter Stoppbefehl für ein laufendes Getränk.

Die Zentrale bleibt unter Umständen bis zum Laufende aktiv. Ein Sprachinterface
kann vorher sein eigenes Zeitlimit erreichen; keine unmittelbare Siri-Erfolgszusage
für „Kaffee fertig“ erwarten und bei unklarer Antwort nicht wiederholt auslösen.

## Zigbee-Fernbedienung

Die Fernbedienung zunächst in der verwendeten Integration einrichten (zum Beispiel
ZHA oder Zigbee2MQTT). In Home Assistant eine Automation erstellen:
**Auslöser:** der tatsächlich angebotene Tastendruck dieses Geräts.
**Aktion:** das vorhandene Favorit-Skript ausführen.

Es gibt hier keine universell gültige Zigbee-Geräte-ID oder Tastencode-Liste.
Keine erfundenen Event-Namen kopieren. Das physische Interface lässt sich frei
wählen, ohne eine neue Kopie der Zubereitungslogik zu erzeugen.

## Andere Automationen

Im Aktionseditor ein Favorit-Skript auswählen. Ein direkter Aufruf von
`script.DEIN_FAVORIT` wartet und reicht Fehler weiter. `script.turn_on` startet
hingegen im Hintergrund; dessen erfolgreicher Aufruf bestätigt nicht, dass das
Getränk erfolgreich ausgegeben wurde. [Home-Assistant-Skriptdokumentation](https://www.home-assistant.io/integrations/script/)

Keine Zeitautomation für unbeaufsichtigte Heißgetränke aus diesem Beispiel ableiten.

## KI-Agenten über MCP (optional, keine Voraussetzung)

Der [Home-Assistant-MCP-Server](https://www.home-assistant.io/integrations/mcp_server/)
kann passend freigegebene Funktionen für Agenten bereitstellen. Nur geprüfte
benannte Favoriten freigeben, nicht pauschal alle Aktoren und nach Möglichkeit nicht
die frei parametrisierbare Zentrale. Berechtigungen und Bestätigungsregeln im
verwendeten Agentensystem separat prüfen. Zugriff nicht öffentlich ungeschützt
bereitstellen. Diese Vorabfassung enthält keinen getesteten MCP-/Agenten-Workflow.
