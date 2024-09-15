# DCS Bios Connector [Python Library]

This is a python library that allows you to listen to DCS Bios events. This can be imported into any python and used for projects.

This library uses [DCS Bios Skunkworks](https://github.com/DCS-Skunkworks/dcs-bios)

A helpful tool is [DCS Bort](https://github.com/DCS-Skunkworks/Bort/releases/tag/v0.3.0) to see button/switch names for each piece of data for a given aircraft. In the `Usage` section below, I am using the `FLAPS_SW` for the `F/A-18_Hornet`. Bort helps you see the name in DCS Bios for every piece of data, it also shows the values in realtime to help debug and see what data you are looking for.

# Installation
`pip install dcs-bios-connector`

## Usage
```
from dcs_bios_connector import DcsBiosConnector
bios = DcsBiosConnector()
bios.connect()

# Example: Detect when the FLAP_SW in the F/A-18 Hornet goes to position 1
bios.on("FLAP_SW:1", lambda: print("Flaps are at position 1"))

# Example of calling a function anytime the FLAP_SW changes
def  handle_flaps_switch_moved(dcsValue, controlInformation, dataInformation):
	print("Detected flap switch changed: ", dcsValue, controlInformation, dataInformation)
bios.on("FLAP_SW", handle_flaps_switch_moved)
```

