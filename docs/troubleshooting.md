# Fehlersuche

[Zurück](../README.md)

## Nichts passiert

Zuerst in den Home-Assistant-Benachrichtigungen nachsehen: **Trockenlauf** ist
absichtlich voreingestellt. Eine Trockenlaufmeldung ist kein Fehler. Für einen
beaufsichtigten echten Test den Schalter in der **Zentrale** ändern.

Unter **Einstellungen → Automatisierungen & Szenen → Skripte** zuerst den Favoriten,
dann die Zentrale öffnen und den letzten **Trace / Ablauf** ansehen. Bei einem
Aufruf über `script.turn_on` können Fehler nur im gestarteten Skript erscheinen.

## Die Entität fehlt in der Auswahl

Prüfen, ob wirklich **Home Connect Alt**, nicht `home_connect`, verwendet wird.
Auf der Geräteseite nach deaktivierten Entitäten suchen. Die Integration entdeckt
Gerätefähigkeiten dynamisch. Wurde das relevante Programm überhaupt am Gerät
verfügbar? Nicht willkürlich eine ähnlich benannte fremde Entität auswählen.
Fehlende Pflichtzustände werden nicht stillschweigend weggelassen.

## Fehler „Alle fünf Entitäten müssen zum selben Gerät gehören“

Die ausgewählten Entitäten prüfen, besonders bei mehreren gleichartigen Maschinen.
Der Power-Select und ein Power-Sensor können ähnlich heißen. Der Verbindungssensor
muss zum Gerät gehören, nicht zu einem globalen Status der Integration.

## Fehler zu rohen Enumwerten / Local

Die Home-Connect-Alt-Übersetzung auf **Local** prüfen. Im Server-Modus ändern sich
auch die internen Zustandswerte mit der Sprache. Die UI-Sprache darf Deutsch bleiben.
Vorsicht bei vorhandenen eigenen Automationen, die noch übersetzte Werte vergleichen.

## Timeout beim Einschalten / Ready

Ist die Maschine online? Fernstart erlaubt? Wird sie gerade am Gerät bedient?
Zeigt sie einen Pflege-, Wasser- oder Behälterhinweis? Lief schon ein Programm?
Die Zentrale wartet nicht auf das Ende eines bei Aufruf bereits laufenden Getränks,
um anschließend unbemerkt noch eines zu starten. Eine Maschine mit `Run`, `Pause`
oder `DelayedStart` wird beim Einstieg abgewiesen.

Zeitgrenzen nur nach Beobachtung anpassen, nicht als Ersatz für eine fehlende
Vorbedingung. Die Zentrale bricht bei fehlender Bereitschaft ohne Programmstart ab.

## Start wurde gesendet, aber Rückmeldung ist unklar

**Nicht erneut auslösen.** Die Cloud kann eine Anfrage ausgeführt haben, obwohl
Home Assistant ihre Rückmeldung noch nicht kennt. Die Zentrale versucht den Start
nicht automatisch erneut. Wird nach dem Aufruf kein `Run` beobachtet, meldet sie
den unklaren Ausgang und hält ihre lokale single-Sperre noch für die konfigurierte
Lauf-/Sperrzeit. Danach ist dennoch eine menschliche Prüfung nötig.

Bricht die eigentliche API-Aktion mit einem Fehler ab, propagiert der Fehler;
die nachfolgenden Warteaktionen laufen dann nicht mehr. Auch hier gibt es keinen
Wiederholungsversuch und keine Garantie, dass der Fehler vor jeder Gerätewirkung
auftrat. Ein laufendes Skript nicht blind abbrechen und sofort erneut starten.

`single` ist keine persistente, cloudweite Exactly-once-Garantie. Andere Skripte,
Apps, mehrere Zentralen und Neustarts können diesen lokalen Schutz umgehen.

## Die Menge oder Stärke entspricht nicht dem alten Dashboard

Der bereitgestellte Universal-Startaufruf enthielt ursprünglich keine expliziten
Optionen. Die Original-Regler setzen Optionen des ausgewählten/aktiven Programms;
bei einem anderen gestarteten Programm ist die Übernahme nicht garantiert.
Rezeptwerte ausdrücklich im Favoriten konfigurieren und nur tatsächlich angebotene
Werte desselben Programms verwenden. `validate: true` ersetzt keinen Tassen-Check.

## „Custom element doesn't exist“ / Barista sieht anders aus

Für Barista muss Mushroom inklusive Legacy Template Card geladen sein. Ressource
und Browser-Neuladen prüfen. Die native Quick-Start-Ansicht benötigt keine solche
Ressource. Für das optionale Dashboard bleiben ein echter Frontendtest und die
Prüfung mit VoiceOver/anderen Hilfsmitteln erforderlich.

## Was in eine Fehlermeldung gehört

Modell, Home-Assistant-/Home-Connect-Alt-Version, gewähltes Getränk, Fehlertext und
ein **bereinigter** Trace-Ausschnitt. Keine Tokens, Secrets, HAID, Seriennummer,
Geräte-IDs, persönliche Entity-Präfixe oder vollständigen privaten Exporte posten.

## Ein anderer Lauf beginnt während der Bereitschaftsphase

Beobachtet die Zentrale während dieses Wartens `Run`, `Pause` oder `DelayedStart`,
bricht sie ab, statt nach einem fremden Lauf automatisch noch ein Getränk zu starten.
Ein Gerät kann solche Zustände möglicherweise auch beim Aufheizen/Spülen melden.
In diesem Fall zunächst selbst einschalten, Spülung abwarten und erst im tatsächlichen
Ready-Zustand aufrufen. Das genaue Einschaltverhalten muss am Referenzgerät abgenommen
werden. Eine abgelaufene Wartezeit gilt auch bei spät eintreffender Zustandsmeldung
nicht nachträglich als erfolgreich.
