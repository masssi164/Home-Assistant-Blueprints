# Veröffentlichung, CI und Releases

Dieses Repository liegt auf GitHub unter **[masssi164/Home-Assistant-Blueprints](https://github.com/masssi164/Home-Assistant-Blueprints)**. Eine neue Repo-Erstellung ist nicht erforderlich.

## Continuous Integration

Unter **Actions → Validate coffee blueprints** laufen automatisch bei Push und Pull Request:

1. Statische YAML-/JSON-Prüfung, Template-/Datenschutztests und simulierte Abläufe mit Python 3.13.
2. Prüfungen gegen echte Home-Assistant-2026.10.2-Schemas unter Python 3.14.

Beide Jobs benötigen keine Zugangsdaten zur Home-Connect-Cloud und greifen nicht auf deine Maschine zu. Dependency-Updates erfolgen als Dependabot-PRs. Actions haben `contents: read` und keine Schreibrechte.

Eine grüne CI bedeutet **nicht**, dass eine echte Maschine das Getränk sicher und korrekt ausgegeben hat. Die [Abnahmecheckliste](docs/acceptance.md) muss separat abgeschlossen werden.

## Release-Politik

Der Stand ist `0.1.0-preview.1`, ausdrücklich **ohne Hardware-Freigabe**. Kein automatisches Tag, keine automatische öffentliche GitHub-Release-Seite und keine automatische Veröffentlichung in HACS.

Ein Release erfolgt erst nach manueller Abnahme:

1. Anforderungen, offene Fehler, Sicherheit und unterstützte Gerätefunktionen dokumentieren.
2. CI auf dem freizugebenden Commit vollständig grün bestätigen.
3. Release-Notizen und Kompatibilitätszusagen mit gemessener Evidenz versehen.
4. Einen Versions-Tag auf den geprüften Commit setzen; GitHub Release von Hand veröffentlichen.

Die Blueprints können bis dahin direkt vom `main`-Branch importiert werden, sind aber nicht stabil versioniert. Ein späteres Release sollte feste Tag-URLs für verlässliche Importe anbieten.

## Sicherheitsregeln

Niemals `scripts.yaml`, `kaffee.yaml`, `.storage`, `secrets.yaml`, API-Credentials, Tokens, persönliche Geräte-IDs, Logauszüge oder personenbezogene Daten hochladen. Die CI enthält lediglich ergänzende Heuristiken, keine vollständige Geheimnisprüfung. Feedback nur mit anonymisierten Traces.
