# Abnahme vor dem ersten öffentlichen Release

**Noch offen.** Eine grüne lokale Simulation ist keine Erlaubnis, diese Liste als
erledigt zu markieren. Nur tatsächliche Beobachtungen eintragen.

## Testumgebung dokumentieren

- Datum, Home-Assistant-Version und Home-Connect-Alt-Version.
- Modellbezeichnung/E-Nummer ohne individuelle Seriennummer, Firmware soweit bekannt.
- Local-Übersetzungsmodus, tatsächlich vorhandene fünf Pflichtentitäten.
- Für UI-Abnahme Browser/App, Mushroom-Version und verwendetes Hilfsmittel.

## Ablauf

- [ ] Beide unveränderten Blueprints lassen sich in Home Assistant importieren.
- [ ] Eine Zentrale lässt sich mit den fünf korrekten Entitäten speichern.
- [ ] Ein fehlendes/anderes Gerät und unknown/unavailable führen zu verständlichem Abbruch.
- [ ] Favorit ohne Rezeptwerte läuft im Trockenlauf ohne Geräteaktion.
- [ ] Gewünschte Änderung an einem Favoriten bleibt getrennt vom Blueprint.
- [ ] Maschine von Hand eingeschaltet, sicher vorbereitet: ein Kaffee startet genau einmal.
- [ ] Run und nachfolgend Ready werden erkannt; Trace entspricht dem Ablauf.
- [ ] Zweiter Favorit während laufender Zentrale startet keine weitere Zubereitung.
- [ ] Bereits laufendes Getränk bei neuem Aufruf wird nicht als Warteschlange behandelt.
- [ ] Deaktivierter Fernstart / aktive lokale Bedienung / Pflegehinweis verhindern Start.
- [ ] Bewusst freigegebenes Einschalten funktioniert unter Berücksichtigung der Spülung.
- [ ] Je tatsächlich unterstütztem Getränk: Standard und ausdrücklich gewählte Werte prüfen.
- [ ] Kaffee-/Espresso-/Milchmengen entsprechen den gewählten, angebotenen Werten.
- [ ] Heißwasser separat prüfen; nicht unterstützte Getränke entfernen/dokumentieren.
- [ ] Ein Optionswechsel auf ein anderes Programm erzeugt keine irreführende Rezeptzusage.
- [ ] Native Dashboard-Tasten, Namen, Fokus und Screenreader-Ausgabe geprüft.
- [ ] Optionale Barista-Karten nur bei vorhandenen Entitäten und passender Mushroom-Version geprüft.
- [ ] HomeKit/Zigbee-Aufruf separat geprüft, falls als funktionierend beworben.
- [ ] Keine Zugangsdaten oder persönlichen Kennungen im veröffentlichten Inhalt.
- [ ] GitHub Actions einschließlich tatsächlichem HA-Schemajob erfolgreich.

Fehlerpfade mit Cloud-Unterbrechung nicht durch riskantes Manipulieren während
heißer Ausgabe erzwingen. Zum gezielten Fehler-/Race-Test eine geeignete Testumgebung
verwenden. Bei echten Geräten hat die sichere Handhabung Vorrang.

## Ergebnisvorlage

```text
Version/Commit:
Datum:
HA / Home Connect Alt:
Modell (ohne Seriennummer):
Getestete Programme:
Getestete Optionen/Grenzen:
Start / Run / Ready beobachtet:
Interfaces geprüft:
Noch offene Einschränkungen:
Testergebnis und freigegebener Umfang:
```

Erst daraus eine Kompatibilitätszusage für das tatsächlich getestete Modell ableiten.
