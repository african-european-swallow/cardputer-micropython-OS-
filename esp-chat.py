import network
import espnow
import _thread
import cardputerlib as card
import time

PEERS_FILE = "peers.txt"

card.clear()
NAME = "Cardputer"
chat_log = []
chat_pro = []
stop = False
sending = ''
last_drawn_lines = []
last_drawn_color = []

def mac_bytes_to_str(mac_bytes):
    return ''.join(f'{b:02x}' for b in mac_bytes)

def mac_str_to_bytes(mac_str):
    return bytes.fromhex(mac_str)

def read_peer_file_raw(path="peers.txt"):
    try:
        with open(path, "r") as f:
            lines = f.read().splitlines()
        # Return non-empty lines only
        return ','.join([line.strip() for line in lines if line.strip()])
    except OSError:
        print("⚠️ Could not read peers.txt")
        return []


def load_peers():
    try:
        with open(PEERS_FILE, 'r') as f:
            lines = f.readlines()
        peers = [mac_str_to_bytes(line.strip()) for line in lines if line.strip()]
        print(f"Loaded peers from file: {peers}")
        return peers
    except Exception as e:
        print(f"Could not load peers file: {e}")
        return []

def save_peers(peers):
    try:
        with open(PEERS_FILE, 'w') as f:
            for mac in peers:
                f.write(mac_bytes_to_str(mac) + '\n')
        print("Peers saved to file.")
    except Exception as e:
        print(f"Failed to save peers file: {e}")

# Load peers at startup
PEER_MACS = load_peers()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.config(channel=1)

e = espnow.ESPNow()
e.active(True)

# Add all peers initially
for mac in PEER_MACS:
    try:
        e.esp_now_del_peer(mac)
    except:
        None
    try:
        e.add_peer(mac)
    except Exception as xe:
        card.clear()
        card.prinS(f'ERROR: {xe}: {mac}',[0,0],[255,0,0])
        time.sleep(1)
        card.clear()

def add_peer_mac(friend_code):
    global PEER_MACS
    try:
        # Convert hex string to bytes
        mac = bytes.fromhex(friend_code.strip())

        if mac not in PEER_MACS:
            PEER_MACS.append(mac)
            e.add_peer(mac)
            save_peers(PEER_MACS)
            print(f"✅ Added peer: {mac_bytes_to_str(mac)}")
        else:
            print(f"⚠️ Peer already exists: {mac_bytes_to_str(mac)}")
    except ValueError:
        print(f"❌ Invalid MAC format: {friend_code}")


def remove_peer_mac(friend_code):
    global PEER_MACS
    try:
        # Convert hex string to bytes
        mac = bytes.fromhex(friend_code.strip())

        if mac in PEER_MACS:
            PEER_MACS.remove(mac)
            e.del_peer(mac)
            save_peers(PEER_MACS)
            print(f"🗑️ Removed peer: {mac_bytes_to_str(mac)}")
        else:
            print(f"⚠️ Peer not found: {friend_code}")
    except ValueError:
        print(f"❌ Invalid MAC format: {friend_code}")


def listen():
    global chat_log,chat_pro , stop
    while not stop:
        peer, msg = e.recv()
        if msg:
            if not msg.startswith(b'!'):
                try:
                    decoded = msg.decode()
                    send_reasz('!'+decoded)
                    chat_log.append(decoded)
                    chat_pro.append('white')
                    if len(chat_log) > 50:
                        chat_log.pop(0)
                        chat_pro.pop(0)
                except:
                    chat_log.append("[binary message]")
                    chat_pro.append('red')
            elif msg.startswith(b'!'):
                try:
                    decoded = msg[1:].decode()
                    for i, val in enumerate(chat_log):
                        if decoded == val and chat_pro[i] != 'white':
                            chat_pro[i] = 'white'
                            break
                except:
                    pass
        time.sleep(0.01)

_thread.start_new_thread(listen, ())

def send_chat(msg):
    full = "{}: {}".format(NAME, msg)
    for mac in PEER_MACS:
        e.send(mac, full.encode())
    chat_log.append(full)
    chat_pro.append('red')
    if len(chat_log) > 50:
        chat_log.pop(0)
        chat_pro.pop(0)
        
def send_reas(msg):
    full = "{}: {}".format(NAME, msg)
    for mac in PEER_MACS:
        e.send(mac, full.encode())
def send_reasz(msg):
    full = str(msg)
    for mac in PEER_MACS:
        e.send(mac, full.encode())
        
def draw_chat():
    global last_drawn_lines, last_drawn_sending, last_drawn_color, chat_pro
    card.rect(0, 135 - 8, 240, 8, [0, 0, 0], fill=True)
    card.prinS("> " + sending, [0, 135 - 8], [0, 255, 0])

    current_lines = chat_log[-15:]
    current_color = chat_pro[-15:]
    
    if current_color != last_drawn_color:
        last_drawn_color[:] = current_color
        y=0
        for x,line in enumerate(current_lines):
            card.prinS(line, [0, y], [255, 255, 255] if chat_pro[x] == 'white' else [255,0,0])
            y += 8
    if current_lines == last_drawn_lines:
        return

    last_drawn_lines[:] = current_lines
    last_drawn_sending = sending

    card.clear()
    y = 0
    for x,line in enumerate(current_lines):
        card.prinS(line, [0, y], [255, 255, 255] if chat_pro[x] == 'white' else [255,0,0])
        y += 8


while True:
    draw_chat()
    if card.pressing(['`', 'ESC']):
        stop = True
        e.active(False)
        break
    elif card.pressing(['ENT']):
        send_chat(sending)
        sending = ''
    elif card.pressing(['BSPC']):
        sending = sending[:-1]
    elif card.pressing(['OPT']):
        time.sleep(0.1)
        while True:
            card.clear()
            mac_bytes = wlan.config('mac')
            mac_str = ''.join('{:02x}'.format(b) for b in mac_bytes)
            card.prinS(f'Device code: {mac_str}', [0, 0], [255, 255, 255])
            card.prinS(f'Peers: {read_peer_file_raw()}', [0, 8], [255, 255, 255])
            cmd = card.imput('Type: add/rem {code} or ..: ', [0, 111], [255, 255, 255])

            if cmd.strip() == '..':
                card.clear()
                break
            parts = cmd.strip().split()
            if len(parts) == 2:
                action, code = parts
                if action == 'add':
                    add_peer_mac(code)
                elif action == 'rem':
                    remove_peer_mac(code)
    else:
        temp = [c for c in card.pressed() if c not in ['`', 'ESC', 'ENT', 'BSPC']]
        sending += ''.join(temp)
    time.sleep(0.1)
