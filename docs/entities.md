# Entitäten, IDs und interne Werte

[Zurück](../README.md)

## Wo finde ich die passenden Entitäten?

Unter **Einstellungen → Geräte & Dienste → Home Connect Alt** das Gerät öffnen.
Die Entitäten dieser Maschine ansehen; möglicherweise deaktivierte Entitäten prüfen.
Die benötigten Status-/Steuerentitäten müssen vorhanden und aktiviert sein.
Anzeigenamen können lokalisiert oder selbst umbenannt sein. In den Einstellungen
jeder Entität steht die technische **Entity-ID**.

Für die Zentrale reichen Auswahllisten. Die technische ID braucht man vor allem
zur Fehlersuche oder für das optionale Dashboard-Mapping. Lange IDs nicht abschreiben,
sondern kopieren oder die Entität auswählen.

In **Entwicklerwerkzeuge → Zustände** die betreffende Entität öffnen. Entscheidend
ist dort der interne Zustand, nicht nur die freundlich übersetzte Anzeige einer Karte.
Die Entwicklerwerkzeuge dienen hier ausschließlich zum Nachsehen. **„Zustand setzen“
nicht als Test verwenden**: Eine veränderte Zustandsanzeige bedient die Maschine nicht
und kann die Vorbedingungen verfälschen.

| Zweck | Domain | Typisches Ende der ursprünglichen ID | Erwarteter Rohzustand |
|---|---|---|---|
| Verbindung | `binary_sensor` | `_connected` | `on` bei bestehender Verbindung |
| Stromzustand/Steuerung | `select` | `_bsh_common_setting_powerstate` | `BSH.Common.EnumType.PowerState.On` |
| Betriebszustand | `sensor` | `_bsh_common_status_operationstate` | `BSH.Common.EnumType.OperationState.Ready` |
| Fernstart erlaubt | `binary_sensor` | `_bsh_common_status_remotecontrolstartallowed` | `on` zum Starten |
| Lokale Bedienung aktiv | `binary_sensor` | `_bsh_common_status_localcontrolactive` | `off` zum Starten |

Die Endungen sind Suchhilfen aus der Vorlage, kein universelles Namensschema.
Geänderte Entity-IDs und abweichende Modelle sind möglich. Keinen privaten
Gerätepräfix per globalem Suchen-und-Ersetzen in fremden Code einbauen.

## Geräte-ID, Entity-ID und Client-ID sind verschiedene Dinge

**Entity-ID:** zum Beispiel `select.meine_kaffeemaschine_powerstate`; bezeichnet
 eine einzelne Funktion in Home Assistant.

**Geräte-ID:** interne Kennung des Geräts in Home Assistant. Die Zentrale verwendet
`device_id()` auf dem Verbindungssensor. Sie wird nicht durch Abschneiden eines
Entity-Präfixes oder aus einer Seriennummer gebildet.

**HAID:** Gerätekennung der Home-Connect-Seite; nicht mit der HA-Geräte-ID verwechseln.
Sie wird von der Integration behandelt, nicht in dieses Blueprint eingetragen.

**Client-ID / Client-Secret:** gehören zur eigenen Home-Connect-Entwickleranwendung.
Nur in der Integration einrichten. Keine dieser Zugangsdaten gehört in einen
Favoriten, ein Dashboard, ein GitHub-Issue oder eine Videoaufnahme.

## Optionale Dashboard-Entitäten

Die vollständige Zuordnung steht in
[dashboard_entities.example.json](../examples/dashboard_entities.example.json).
Für das einfache Dashboard werden nur die fünf dortigen `*_SCRIPT`-Einträge benötigt.

Für die Barista-Ansicht zusätzlich: Power-Select, OperationState, Verbindung,
Fernstart, Kindersicherung, Temperatur-Select, Stärke-Select, Füllmengen-Number,
Mehrfachgetränk-Switch und die vier ursprünglichen Getränkezähler.
Nicht jedes Modell stellt alle davon bereit. Fehlende Karten entfernen oder beim
einfachen Dashboard bleiben; keine zufällige andere Entität als Ersatz auswählen.

Wird eine Entity-ID später umbenannt, die Auswahl in der Zentrale bzw. die
Dashboard-Zuordnung erneut prüfen. Favoriten benötigen nur die zentrale Skript-ID.
Die Zentrale nicht versehentlich löschen und mit einer neuen ID anlegen, ohne die
Favoriten umzuhängen.
