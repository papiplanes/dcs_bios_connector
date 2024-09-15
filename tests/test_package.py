from dcs_bios_connector import DcsBiosEventListener

def test_dcs_bios_event_listener():
    dcsBios = DcsBiosEventListener()
    dcsBios.connect()
    
    assert listener is not None
