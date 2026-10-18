# Eigene Rezepte ohne Änderung der Logik

[Zurück](../README.md)

Ein Favorit ist ein eigenes Skript mit einer Auswahl der Zentrale, einem Getränk
und optionalen Rezeptwerten. Zum Ändern unter **Skripte** den Favoriten öffnen und
die Blueprint-Einstellungen bearbeiten. Nicht „Kontrolle übernehmen“ verwenden,
solange der Favorit seine Verbindung zum Blueprint behalten soll.

## Erster Favorit: möglichst wenig einstellen

**Füllmenge 0**, **Bohnenstärke leer** und **Kaffeetemperatur leer** bedeuten:
keine ausdrückliche Vorgabe an den Startaufruf. Dabei werden **nicht** automatisch
die momentanen Werte der alten Dashboard-Regler ausgelesen oder konserviert.
Welche Vorgaben ohne Optionen gelten, entscheidet die Integration/das Gerät.

Für ein reproduzierbares Rezept nur die für **dieses Gerät und dieses Getränk**
erlaubten Werte ausdrücklich angeben. Die Zentrale sendet sie gemeinsam mit dem
Programmschlüssel in einer `home_connect_alt.start_program`-Aktion; es gibt keine
separate Folge konkurrierender Optionen-Änderungen beim Start.

## Füllmenge

Ganze Milliliter eingeben. `0` im Favoriten ist der Schalter „keine Vorgabe“ und wird
nicht als Null-Milliliter-Getränk gesendet. Der Eingabebereich bis 1000 ml ist eine
Formular-/Validierungsgrenze, **keine Zusage**, dass irgendeine Maschine 1000 ml pro
Getränk unterstützt. Das tatsächliche Minimum, Maximum und Raster sind
programm- und geräteabhängig.

## Stärke und Temperatur

Unter Entwicklerwerkzeuge → Zustände den entsprechenden Select ansehen und im
Attribut **options** einen angebotenen **rohen Enumwert** kopieren. Die zugehörigen
Entitäten endeten in der Vorlage auf `_option_beanamount` bzw.
`_option_coffeetemperature`. Falls die Auswahl von einem Programm abhängt, das
passende Programm zuerst auf dem normalen, beaufsichtigten Bedienweg auswählen.
Ein Wert aus einem anderen Getränk ist nicht automatisch übertragbar.

Die Werte beginnen mit:

```text
ConsumerProducts.CoffeeMaker.EnumType.BeanAmount.
ConsumerProducts.CoffeeMaker.EnumType.CoffeeTemperature.
```

Den vollständigen tatsächlich angebotenen Wert verwenden, nicht nur dieses Präfix.
Keine übersetzte Beschriftung wie „Stark“ und keinen erfundenen Celsiuswert eintragen.
Die Projektprüfung kontrolliert Struktur/Präfixe, nicht die vollständige Liste
der Fähigkeiten jeder Maschine. Die Backend-Anbindung muss den Aufruf ebenfalls
akzeptieren. `validate: true` bleibt gesetzt; laut Home Connect Alt prüft diese Option
insbesondere die aktuelle Verfügbarkeit des Programms.

## Heißwasser

Der ursprüngliche fünfte Programmtyp `HotWater` bleibt erhalten. In dieser Version
werden für Heißwasser nur optionale Füllmengen unterstützt. Kaffee-Stärke und
Kaffee-Temperatur müssen leer bleiben. Kein Versprechen für Tee-Temperaturprogramme
oder Sondergetränke, die die Vorlage nicht implementiert.

## Fortgeschritten: direkter Aufruf der Zentrale

Das ist ein **Schema-Beispiel**, kein getestetes Rezept für jede Maschine. Die
Skript-ID durch die tatsächlich vergebene ID ersetzen und die Menge nur verwenden,
wenn sie für das eigene Getränk erlaubt ist und das Gefäß passt.

```yaml
action: script.kaffee_auf_zuruf_zentrale
data:
  beverage_type: Coffee
  program_options:
    - key: ConsumerProducts.CoffeeMaker.Option.FillQuantity
      value: 150
```

Andere Interfaces rufen für den Alltag besser einen benannten Favoriten ohne
freie Parameter auf. So bleiben Rezept und Validierung an einer Stelle.
