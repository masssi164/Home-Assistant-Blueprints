# Prüfung der bereitgestellten Ausgangsdateien

Grundlage: die für dieses Projekt überlassenen `scripts.yaml` und `kaffee.yaml`.
Die Originaldateien und privaten Kennungen sind **nicht** Teil des Repositorys.
Die Punkte unten trennen tatsächlichen Inhalt, daraus abgeleitete Probleme und
bewusste Änderungen dieser Vorabfassung.

## Übernommener Kern

Der Originalkern heißt `mach_kaffee_universal`. Er hat `mode: single`, ein Feld
`beverage_type` und die fünf Werte Coffee, Espresso, Cappuccino, LatteMacchiato,
HotWater. Er prüft Verbindung, schaltet bei Bedarf ein, wartet auf Fernstartfreigabe,
keine lokale Bedienung und den Betriebszustand Ready. Danach folgt
`home_connect_alt.start_program` mit `validate: true` und einem vollständigen
Programm-Key. Fünf benannte Wrapper rufen ihn auf. Diese Trennung war bereits
vorhanden und wurde nicht als neue Projektidee erfunden.

Das Dashboard besitzt Bereiche für Power/Status, Statistik, vier Quick-Start-Tasten,
Temperatur/Stärke/Füllmenge/Mehrfachgetränk sowie System/Wartung. Es nutzt Mushroom.

## Konkrete Befunde und Änderungen

1. **Feste persönliche IDs in beiden Dateien.** Sie wurden durch fünf konfigurierbare
   Blueprint-Entity-Inputs und Dashboard-Tokens ersetzt. Die Start-Geräte-ID wird
   anhand des gewählten Verbindungssensors ermittelt und auf konsistente Zuordnung
   geprüft, nicht aus dem alten privaten Präfix abgeleitet.

2. **Ein Skriptfeld-Default im Formular ist kein Laufzeit-Default.** Im Original wird
   `beverage_type` direkt in einen Template-String eingesetzt. Die neue Zentrale
   behandelt einen wirklich fehlenden Parameter ausdrücklich als Coffee und weist
   unbekannte übergebene Werte ab. Erforderlich/Default im Formular allein erzwingt
   das zur Laufzeit nicht (siehe Home-Assistant-Skriptdokumentation).

3. **Der Originalkern endet nach der Startanfrage.** Sein single-Modus schützt daher
   nicht automatisch die gesamte nachfolgende Zubereitungszeit. Die neue Zentrale
   wartet zusätzlich auf Run und anschließend Ready. Bei fehlender Bestätigung
   gibt es keine automatische Startwiederholung. Das ist weiterhin keine globale
   oder über Neustarts persistente Gerätesperre.

4. **Kein explizites Options-Paket im Original-Startaufruf.** Die Dashboard-Regler
   sind direkte Geräteoptionen. Es wird nicht behauptet, dass ein Programmwechsel
   diese Werte immer übernimmt. Optionale Favorit-Werte werden jetzt ausdrücklich
   in derselben Startanfrage mitgegeben. Ohne Vorgaben bleibt die Entscheidung
   bei Integration/Gerät. Mehrfachgetränk wird nicht als neues Favorit-Feature zugesagt.

5. **Zusätzliches Rückfrage-/Tassenskript mit externer Abhängigkeit.** Ein weiteres
   Originalskript ruft `script.eg_notify_send` auf; dessen Definition ist nicht
   enthalten. Seine Benachrichtigungsaktionen verwenden feste Action-Namen. Diese
   Companion-App-/Benachrichtigungsvariante wurde nicht als unabhängig installierbar
   übernommen. Die neue Fassung besitzt **keine** automatische Tassenerkennung und
   **keine** Bestätigungsfunktion als stillen Ersatz. Eine künftige optionale
   Bestätigung braucht ein eigenes, getestetes Konzept pro Aufruf.

6. **Themenfremde Skripte.** HomePod-Fanfare und Netzwerkauskunft gehören nicht zum
   Kaffeeprojekt und wurden nicht übernommen. Private Exporte bleiben privat.

7. **Statistik ohne belastbare Umrechnung.** `total * 0.15` würde 0,15 kg pro Bezug
   als Bohnenmenge ausgeben. Diese Konstante ist im Export nicht hergeleitet.
   Der Heißwasser-Zähler wurde außerdem durch 1000 geteilt und als Liter angezeigt,
   ohne dass der Export eine entsprechende Einheit belegt. Beide Umrechnungen
   wurden entfernt, statt eine andere willkürliche Konstante einzusetzen.

8. **Gleichstände im Lieblingsgetränk.** Der ursprüngliche else-Zweig zeigt auch
   bei Gleichstand der größten Kaffee-Kategorien Espresso an; bei drei Nullen
   ebenfalls. Die bereinigte Ansicht nennt Gleichstände, fehlende Werte und den
   Nullstand gesondert. Die Summe bleibt auf die drei tatsächlich addierten
   Kaffee-Kategorien beschränkt.

9. **Dashboard-Kompatibilität.** Die von der Quelle verwendeten Template-Eigenschaften
   gehören zur Mushroom-Legacy-Template-Card. Die optionale Ansicht benennt diesen
   Kartentyp explizit. Nicht-templatefähige `icon_color`-Ausdrücke in Entity-Karten
   wurden durch statische Farben ersetzt. Der reale Frontendtest ist noch offen.

10. **Bewusste abweichende Startvorgaben.** Das Original schaltet automatisch ein.
    Die Vorabfassung startet aus Sicherheits-/Einrichtungsgründen im Trockenlauf
    und verlangt eine bewusste Freigabe des automatischen Einschaltens. Diese
    Änderung ist dokumentiert und keine Behauptung über die bisherige Nutzung.

## Was aus den Dateien nicht nachgewiesen ist

Exakte Home-Assistant-/Home-Connect-Alt-Version der Installation; Firmware und
E-Nummer der physischen Maschine; erlaubte Optionslisten/Grenzen pro Getränk;
Erhalt der gewünschten Optionen über Programmwechsel; tatsächliche Cloud-Latenzen;
Zugänglichkeit jeder Karte im aktuellen Frontend; erfolgreiche Funktion der neuen
Fassung am Gerät. Der Referenzname TP516DX3 stammt aus den Entity-Namen, nicht aus
einer Prüfung des Typenschilds.

Die vorher diskutierte Anzeige „Kein Ziel festgelegt“ wird nicht pauschal als
Laufzeitfehler bewertet: Die ursprüngliche Power-Aktion übergibt `entity_id` in
`data`. Eine Editoranzeige allein beweist keinen fehlenden Geräteaufruf.

[Quellen](sources.md) · [Prüfstand](validation.md)
