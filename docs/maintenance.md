# Wartung ohne individuelle YAML-Forks

## Vertrag zwischen Logik und Konfiguration

Die Zentrale besitzt stabile Blueprint-Input-Namen für fünf Entitäten, Test-/Power-
Verhalten und Zeitgrenzen. Der Aufrufvertrag lautet `beverage_type` plus optional
`program_options`. Ein Favorit speichert seine zentrale Script-Entity-ID und
Rezeptwerte getrennt von der Logik. Eine zweite Maschine bekommt eine eigene Zentrale;
mehrere Favoriten derselben Maschine dürfen nicht je eine eigene Zentrale erzeugen.

Neue optionale Blueprint-Inputs erhalten Defaults. Bestehende Inputs und die fünf
Programmbezeichner nicht ohne Migration umbenennen. Änderungen an Defaults können
vorhandene Instanzen mit nicht ausdrücklich gesetzten Werten betreffen und gehören
in das Changelog. Inkompatible Änderungen bekommen eine neue Hauptversion und eine
Migration, erforderlichenfalls einen separaten Blueprint-Dateipfad.

## Update auf einer Installation

1. Home-Assistant-Backup und Kopie der verwendeten Blueprint-Version erstellen.
2. Changelog/Abnahme des Updates lesen. Nie eine laufende Kaffee-Zentrale neu laden.
3. Aktualisierung über dieselbe Blueprint-Datei bzw. denselben Importpfad durchführen.
   Ein Wechsel zwischen lokalem `coffee_control/...`-Pfad und GitHub-Import kann einen
   anderen lokalen Pfad erzeugen; dann Instanzen bewusst umhängen, nicht beide kopieren.
4. Skripte neu laden, Inputs und Zuordnungen prüfen, Trockenlauf und einen sicheren
   beaufsichtigten Funktionstest durchführen. Erst dann weitere Interfaces testen.

Ein Blueprint-Update lässt die getrennt gespeicherten persönlichen Inputs nicht
absichtlich verschwinden; eine inkompatible Änderung kann dennoch Skripte brechen.
„Kontrolle übernehmen“ erzeugt eine unabhängige Kopie und beendet den normalen
Blueprint-Updatepfad. Für Alltagsanpassungen stattdessen Favorit-Inputs benutzen.

## Freigabeprozess

Diese Vorabfassung ist als **0.1.0-preview.1** bezeichnet, aber noch kein GitHub-Tag
oder Release. Vorgesehen: Änderungen in einem Branch/PR → lokale Tests → GitHub CI
mit HA-Schema → gerätebezogene Abnahme → Changelog → Tag/Release → Hauptvideo-Link.

Nur tatsächlich absolvierte Tests in [validation.md](validation.md) und der
[Abnahme](acceptance.md) als erfolgreich vermerken. Eine Versionsnummer allein ist
keine Freigabe. Die erste öffentliche stabile Importverknüpfung soll auf den
abgenommenen Tag zeigen, nicht blind auf die laufende Entwicklung in `main`.

Releases tragen dokumentierte Home-Assistant-/Integration-Versionen, bestätigte
Modelle/Getränke und bekannte Grenzen. Ein gemeldetes neues Modell wird erst nach
den entsprechenden Beobachtungen als unterstützt geführt. Nicht bei jeder Meldung
alle Defaults für bestehende Nutzer ändern.

## CI und Datenschutz

Die vorbereiteten Workflows haben nur Lese-Berechtigungen. Sie sprechen keine
Maschine an und benötigen keine Home-Connect-Zugangsdaten. Action-Versionen sind
auf Commit-SHAs fixiert; Dependabot kann Updates vorschlagen. Es gibt keinen
verdeckten Auto-Release und kein `pull_request_target` mit fremdem Code.

Lokale Mapping-Dateien liegen in `local/` oder außerhalb des Repositorys. Vor jedem
Push `git diff --cached` kontrollieren. Keine kompletten privaten HA-Exporte einchecken.
