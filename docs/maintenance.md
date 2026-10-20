# Wartung ohne individuelle YAML-Forks

## Vertrag zwischen Logik und Konfiguration

Die Zentrale besitzt Blueprint-Inputs für fünf Entitäten, Test-/Einschaltverhalten
und Zeitgrenzen. Der Aufrufvertrag lautet `beverage_type` plus optional
`program_options`. Favoriten speichern Zentralenskript und Rezeptwerte getrennt
von der Logik. Jede Maschine bekommt eine Zentrale; alle ihre Favoriten verwenden
sie gemeinsam.

Neue optionale Inputs erhalten Defaults. Bestehende Inputs und Programmbezeichner
nicht ohne Migration umbenennen. Änderungen an Defaults können vorhandene Instanzen
betreffen und gehören ins Changelog. Inkompatible Änderungen benötigen eine
Migrationsanleitung, nötigenfalls einen separaten Blueprint-Dateipfad.

## Versionierte Imports

Die Importlinks und `source_url`-Angaben für **v1.0.0-beta.1** zeigen auf den festen
Versions-Tag. Sie folgen nicht automatisch den Änderungen von `main`. Ein erneuter
Import derselben Quelle bleibt auf dieser Beta. Für eine neuere Beta bewusst die
neue Version wählen und deren Release-Notizen lesen.

## Update auf einer Installation

1. Home-Assistant-Backup und Kopie der verwendeten Blueprint-Version erstellen.
2. Changelog und Teststand lesen. Nie eine laufende Kaffee-Zentrale neu laden.
3. Neue Blueprint-Version unter dem bisherigen lokalen Blueprint-Dateipfad ersetzen
   oder Skriptinstanzen bewusst auf den neuen Importpfad umstellen. Ein Wechsel
   zwischen lokalem `coffee_control/...`-Pfad und GitHub-Import kann einen anderen
   lokalen Pfad erzeugen. Nicht versehentlich zwei Zentralen parallel verwenden.
4. Skripte neu laden, Inputs und Zuordnungen prüfen, Trockenlauf und einen sicheren
   beaufsichtigten Funktionstest durchführen. Danach weitere Interfaces testen.

Persönliche Inputs bleiben außerhalb der Blueprint-Dateien gespeichert; eine
inkompatible Änderung kann dennoch eine Migration erfordern. „Kontrolle übernehmen“
erzeugt eine unabhängige Kopie statt einer weiter an den Blueprint gebundenen Instanz.
Alltagsanpassungen deshalb über Favorit-Inputs vornehmen.

## Weitere Beta-Releases

Änderungen in Branch/PR prüfen, den tatsächlichen Gerätetestumfang dokumentieren,
`VERSION`, Release-Notizen und Versionslinks gemeinsam aktualisieren und nach `main`
übernehmen. **Publish beta release** prüft den Commit erneut und veröffentlicht erst
danach als Pre-Release. Vorhandene Tags und Releases bleiben unverändert.

Die vollständige Anleitung und Fehlerbehandlung stehen in [PUBLISH.md](../PUBLISH.md).
Eine stabile Version wird nicht automatisch aus einer Beta erzeugt.

## CI und Datenschutz

Die Validierungsjobs haben nur Leserechte und sprechen keine Maschine an. Nur der
Veröffentlichungsjob erhält `contents: write` für Tag und GitHub-Release; er läuft
nicht für Pull Requests oder Forks. Actions sind auf Commit-SHAs fixiert.

Lokale Mapping-Dateien liegen in `local/` oder außerhalb des Repositorys. Keine
privaten HA-Exporte, Zugangsdaten oder individuellen Gerätekennungen einchecken.
