# Veröffentlichung, CI und Releases

## Aktuelle Beta

Version: **`v1.0.0-beta.1`**, veröffentlicht als **GitHub-Pre-Release**, nicht als
stabile Version. Der reale End-to-End-Ablauf ist mit dem Siemens TP516DX3 getestet.
Der Testumfang steht unter [Teststand](docs/validation.md).

## Continuous Integration

**Actions → Validate coffee blueprints** prüft Pushes und Pull Requests:

1. YAML/JSON, Templates, simulierte Abläufe, Dashboards und Datenschutzheuristiken
   mit Python 3.13.
2. Echte Home-Assistant-2026.10.2-Schemas mit Python 3.14.

Diese Tests benötigen keine Home-Connect-Zugangsdaten und steuern keine Maschine.
Die bestehende Validierungs-CI bleibt auf `contents: read` beschränkt.

## Beta veröffentlichen

Der Workflow **Publish beta release** startet auf `main`, wenn `VERSION`, eine
Datei unter `releases/` oder der Release-Workflow geändert wird. Zusätzlich ist
**Run workflow** auf `main` möglich. Andere Branches und Forks veröffentlichen nicht.

Für eine weitere Beta in einem gemeinsamen Commit/PR:

1. `VERSION` auf die nächste Beta setzen, beispielsweise `v1.0.0-beta.2`.
2. Passende Notizen unter `releases/v1.0.0-beta.2.md` hinzufügen.
3. README-Importlinks, Blueprint-`source_url` und Dokumentationslinks auf diesen
   Tag aktualisieren; Changelog und den tatsächlich geprüften Testumfang ergänzen.
4. Änderungen nach erfolgreichen PR-Checks nach `main` übernehmen.

Der Release-Workflow führt beide Prüfjobs erneut auf genau dem zu veröffentlichenden
Commit aus. Erst danach erstellt der Veröffentlichungsjob den Tag und einen
GitHub-Pre-Release mit `--prerelease --latest=false`. Die beiden Blueprints und das
native Quick-Start-Dashboard werden angehängt; GitHub bietet zusätzlich Quellarchive an.

Nur dieser Veröffentlichungsjob erhält `contents: write` und verwendet das kurzlebige
`GITHUB_TOKEN`. Es werden keine persönlichen Tokens oder Cloud-Zugangsdaten benötigt.
Bestehende Releases werden nicht überschrieben und vorhandene Tags nicht verschoben.
Eine abweichende vorhandene Tag-Referenz ohne Release führt zum Abbruch.

Der Workflow akzeptiert ausschließlich Beta-Versionen. Eine spätere stabile
Veröffentlichung ist eine separate, bewusste Freigabe.

## Fehlerbehandlung

Bei fehlgeschlagenen Tests wird kein Release erstellt. Fehler beheben und die Checks
erneut ausführen. Bei einem Veröffentlichungsfehler den betroffenen Actions-Lauf
prüfen und erneut ausführen. Ein vorhandener Release wird dabei unverändert belassen.

Die festen Importlinks setzen einen erfolgreich veröffentlichten Versions-Tag voraus.
Vor der Ankündigung die Release-Seite und beide verlinkten YAML-Dateien prüfen.

## Sicherheit und Feedback

Keine privaten HA-Exporte, Credentials, Tokens, Seriennummern oder persönlichen
Geräte-IDs einchecken. Traces vor dem Teilen anonymisieren. Die CI-Heuristiken sind
kein Ersatz für diese Prüfung. Weitere Gerätemodelle nur mit dem tatsächlich
beobachteten Testumfang dokumentieren. [Gerätetests](docs/acceptance.md)
