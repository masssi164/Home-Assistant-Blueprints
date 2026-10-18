# Bestehende Kaffee-Skripte sicher umstellen

[Zurück](../README.md)

Die Ausgangsdatei enthält neben Kaffee auch HomePod-/Netzwerkskripte. Sie wird
**niemals komplett ersetzt**. Auch das bestehende Dashboard bleibt zunächst erhalten.

## Zuerst parallel testen

1. Eine Sicherung der bestehenden Skripte und des Dashboards erstellen.
2. Beide Blueprints lokal kopieren oder nach Veröffentlichung importieren.
3. Zentrale und Favoriten mit **neuen** IDs `kaffee_auf_zuruf_…` anlegen.
   Bei vorhandenen gleichnamigen Einträgen andere Namen/IDs wählen.
4. Den Trockenlauf über die neuen Favoriten prüfen; danach den beaufsichtigten
   Gerätetest aus [Abnahme](acceptance.md) durchführen.
5. Erst danach bestehende Dashboard-/HomeKit-/Automationszuordnungen ändern.
   Während der Tests alte und neue Startwege nicht gleichzeitig benutzen.

## Alte Namen behalten

Das Beispiel [legacy_aliases.yaml](../examples/legacy_aliases.yaml) zeigt die fünf
alten Aufrufnamen. Es leitet sie auf die neue gemeinsame Zentrale um. Damit können
Dashboard und bestehende Siri-/Automationszuordnungen grundsätzlich bei den alten
Entitäts-IDs bleiben, sofern diese beim Bearbeiten erhalten bleiben.

**Nicht einfach an `scripts.yaml` anhängen:** Wenn `mach_kaffee` usw. bereits
existieren, würde das doppelte YAML-Schlüssel erzeugen. Stattdessen nach erfolgreicher
Abnahme die bestehenden Skripte einzeln bearbeiten und ihre Sequenz umstellen.
Im UI-Editor eines einzelnen Skripts gehören weder `mach_kaffee:` als äußere Ebene
noch andere Skripteinträge dazu. Nur Inhalt dieses einen Skripts bearbeiten.

Die Ziel-ID `script.kaffee_auf_zuruf_zentrale` ist ein Beispiel; die tatsächlich
vergebene ID wählen. Die Vorlage enthält bewusst keine persönlichen Rezeptwerte.
Diese können in einem neuen Favoriten konfiguriert werden. Ein alter Alias kann
alternativ genau diesen Favoriten direkt aufrufen.

Die alte universelle Implementierung erst entfernen, wenn keine Aufrufer sie mehr
benötigen. Das Rückfrage-Skript mit `eg_notify_send` bleibt außerhalb dieses Projekts;
es wird weder ungefragt entfernt noch als bereits ersetzt ausgegeben. Es darf nicht
parallel die neue Zentrale umgehen, wenn deren lokale Sperre wirken soll.

## Unterschiede bewusst übernehmen

Die neue Zentrale startet im Trockenlauf und schaltet standardmäßig nicht selbst ein.
Sie wartet nach einem echten Start auf Zustandsrückmeldungen. Das sind beabsichtigte
Änderungen, keine identische Kopie des alten Laufzeitverhaltens. Einzelheiten stehen
in [Änderungen gegenüber der Vorlage](source-review.md).

Ein Home-Assistant-Neustart oder Skript-Reload während eines Getränks ist kein
sicherer Migrationsschritt. Die Skriptsperre ist nicht dauerhaft und ein bereits
laufendes Getränk wird dadurch nicht automatisch gestoppt.
