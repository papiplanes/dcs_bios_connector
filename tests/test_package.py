from dcs_bios_connector import DcsBiosConnector

def test_dcs_bios_event_listener():
    api = DcsBiosConnector()
    api.connect()
    
    assert api is not None
