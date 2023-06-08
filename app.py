from flask import Flask, render_template, request
import subprocess
import os
import time
from threading import Thread
import fileinput
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.debug = True
UPLOAD_FOLDER = os.path.join(os.getcwd(), '/home/pi/RaspiWiFi/data')

@app.route('/')
def index():
    wifi_ap_array = scan_wifi_networks()
    return render_template('app.html', wifi_ap_array = wifi_ap_array, ip ="")

@app.route('/ipFixo', methods= ['GET','POST'])
def ipFixo():
    address = request.form.get('address')
    broadcast = request.form.get('broadcast')
    netmask = request.form.get('netmask')
    gateway = request.form.get('gateway')
    dns = request.form.get('dns')

    wifi_ap_array = scan_wifi_networks()
    fixar_ip(address, broadcast, netmask, gateway, dns)
    return render_template('app.html', wifi_ap_array = wifi_ap_array, ip='Agora seu IP é '+ address)

@app.route('/alias_bluetooth')
def alias_bluetooth():
    return render_template('alias_bluetooth.html')

@app.route('/nomeBluetooth', methods=['GET', 'POST'])
def setar_nome():
    bluetooth = request.form.get('bluetooth')
    mudar_nome_bluetooth(bluetooth)
    return render_template('informacao.html', informacao='Álias do Bluetooth Alterado')

@app.route('/save_credentials', methods = ['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']

    create_wpa_supplicant(ssid, wifi_key)
    
    # Call set_ap_client_mode() in a thread otherwise the reboot will prevent
    # the response from getting to the browser
    def sleep_and_start_ap():
        time.sleep(2)
        set_ap_client_mode()
    t = Thread(target=sleep_and_start_ap)
    t.start()
    return render_template('save_credentials.html', ssid = ssid)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload_arquivo', methods=['GET',"POST"])
def upload_arquivo():
    file = request.files['file']
    if file:
        savePath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(savePath)
        return render_template('informacao.html', informacao='Upload de arquivo concluído')
    else:
        return 'Nenhum arquivo enviado!'

######## FUNCTIONS ##########

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)

    return ap_array

def create_wpa_supplicant(ssid, wifi_key):
    temp_conf_file = open('wpa_supplicant.conf.tmp', 'w')

    temp_conf_file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('network={\n')
    temp_conf_file.write('	ssid="' + ssid + '"\n')

    if wifi_key == '':
        temp_conf_file.write('	key_mgmt=NONE\n')
    else:
        temp_conf_file.write('	psk="' + wifi_key + '"\n')

    temp_conf_file.write('	}')

    temp_conf_file.close

    os.system('mv wpa_supplicant.conf.tmp /etc/wpa_supplicant/wpa_supplicant.conf')

def fixar_ip(address, broadcast, netmask, gateway, dns):
    if not os.path.exists('/etc/network/interfaces.original'):
        os.system('mv /etc/network/interfaces /etc/network/interfaces.original')
    with open('/etc/network/interfaces', 'w') as arquivo:
        arquivo.write('source /etc/network/interfaces.d/*\n\nauto lo\niface lo inet loopback\n\nallow-hotplug wlan0\niface wlan0 inet static\naddress ' +address +'\nbroadcast ' +broadcast +'\nnetmask ' +netmask +'\ngateway ' +gateway +'\ndns-nameservers ' +dns) 

def mudar_nome_bluetooth(alias):
    os.system('bluetoothctl system-alias ' +alias)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')