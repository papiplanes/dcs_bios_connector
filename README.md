# DCS Bios Connector [Python Library]

This is a python library that allows you to listen to DCS Bios events. This can be imported into any python and used for projects.

This library uses [DCS Bios Skunkworks](https://github.com/DCS-Skunkworks/dcs-bios)

A helpful tool is [DCS Bort](https://github.com/DCS-Skunkworks/Bort/releases/tag/v0.3.0) to see button/switch names for each piece of data for a given aircraft. In the `Usage` section below, I am using the `FLAPS_SW` for the `F/A-18_Hornet`. Bort helps you see the name in DCS Bios for every piece of data, it also shows the values in realtime to help debug and see what data you are looking for.

# Requirments
1.[ DCS Bios ](https://github.com/DCS-Skunkworks/dcs-bios) installed on your PC and configured with DCS 

# Installation
PIP Package [Link](https://pypi.org/project/dcs-bios-connector/)

`pip install dcs-bios-connector`

## Usage
```
from dcs_bios_connector import DcsBiosConnector
bios = DcsBiosConnector()
bios.connect()

# ============= Example: Detect when flap switch changes and its new value =====================
def handle_flaps_change(value, controlInformation, dataInformation):
    print("Flaps have been changed to: ", value)

bios.on("FLAP_SW", handle_flaps_change)


# ============= Example: Callback method to run when flaps are set to 2 =====================
def handle_flaps_lowered():
    print("That flaps have been lowered! Yeah")

bios.on("FLAP_SW:0", handle_flaps_lowered)


# ================= Example: Setting flap switch to position 2 (Flaps to auto) ==========================
bios.send("FLAP_SW 2")
```

