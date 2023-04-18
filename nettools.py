import network


SSID = 'Palliative-Chair'
PASSWORD = '88888888'

def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=PASSWORD)

    while ap.active() == False:
        pass
    
    print("Access Point Configured Successfully")

