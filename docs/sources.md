# Quellen und Abgrenzung

Prüfdatum der Dokumentation/Quellstellen: **18. Oktober 2026**.

## Vom Autor bereitgestellter Projektstand

`scripts.yaml` und `kaffee.yaml`, in der Projektbesprechung als aktuelle Vorlage
bereitgestellt. Daraus stammen die ursprüngliche Startlogik, die fünf Getränke,
Mushroom-Dashboard-Struktur und der Referenzname Siemens TP516DX3. Private Originale
werden nicht im Repository abgelegt. [Befunde und bewusste Änderungen](source-review.md)

## Primärquellen für die technische Prüfung

- [Home Connect Alt: Einrichtung, Local/Server-Übersetzung, dynamische Gerätefähigkeiten](https://github.com/ekutner/home-connect-hass/blob/master/README.md)
- [Home Connect Alt: Action-Felder und Optionsformat](https://github.com/ekutner/home-connect-hass/blob/master/custom_components/home_connect_alt/services.yaml), geprüfter Datei-Blob `e09034e5e294f4f07ae80013540e67cce5685cf0`.
- [Home Connect Alt: Weiterleitung von start_program an die Clientbibliothek](https://github.com/ekutner/home-connect-hass/blob/master/custom_components/home_connect_alt/services.py), geprüfter Datei-Blob `9f89c17afe1f8a28588fa16f70c9d4a84387aeb4`.
- [Home Assistant: Blueprint-Schema und Input-Sektionen](https://www.home-assistant.io/docs/blueprint/schema/)
- [Home Assistant: Entity- und andere Selektoren](https://www.home-assistant.io/docs/blueprint/selectors/)
- [Home Assistant: Skripte, Laufzeit-Defaults, direkte Aufrufe und script.turn_on](https://www.home-assistant.io/integrations/script/)
- [Home Assistant: Script-Syntax, Waits und Stop-Aktionen](https://www.home-assistant.io/docs/scripts/)
- [Home Assistant: Import und Reimport von Blueprints](https://www.home-assistant.io/docs/automation/using_blueprints/)
- [Home Assistant: HomeKit Bridge](https://www.home-assistant.io/integrations/homekit/)
- [Home Assistant: MCP Server](https://www.home-assistant.io/integrations/mcp_server/)
- [Mushroom: Legacy Template Card](https://github.com/piitaya/lovelace-mushroom/blob/main/docs/cards/legacy-template.md)
- [Home Assistant Core 2026.10.2: echte Script-Schema-Implementierung](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/script/config.py)
- [Home Assistant Core 2026.10.2: echte Blueprint-Schema-Implementierung](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/blueprint/schemas.py)
- [Home Assistant Core 2026.10.2: Paket-/Python-Anforderungen](https://github.com/home-assistant/core/blob/2026.10.2/pyproject.toml)

Die Prüfung der Action-Schnittstelle beweist nicht die tatsächlich akzeptierten
Programmkombinationen, Optionsgrenzen oder das Laufzeitverhalten jeder Maschine.
Externe Dokumentation kann sich verändern; ein Link allein ist kein bestandener Test.
