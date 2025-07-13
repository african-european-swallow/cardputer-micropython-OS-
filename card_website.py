import network
import cardputerlib as card
import socket
import machine
import ure  # MicroPython's regex module for parsing
card.setfont('8x8')
# Wi-Fi credentials
SSID = card.imput('Wifi: ', [0,60], [0,255,0])
PASSWORD = card.imput('Password: ', [0,70], [0,255,0])
card.setfont('16x16')

# Setup Wi-Fi in Station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
while not wlan.isconnected():
    pass

card.prinS("Connected to WiFi. IP: " + str(wlan.ifconfig()[0]), [0,0],[100,0,0])



# Function to parse RGB input
def parse_rgb(rgb_str):
    try:
        decoded_rgb = rgb_str.replace('%2C', ',').replace('+', ' ')
        r, g, b = map(int, decoded_rgb.split(','))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return [r, g, b]
    except ValueError:
        pass
    return None

# Function to parse dot coordinates
def parse_dot(dot_str):
    try:
        decoded_dot = dot_str.replace('%2C', ',').replace('+', ' ')
        x, y = map(int, decoded_dot.split(','))
        if 0 <= x <= 135 and 0 <= y <= 240:
            return [x, y]
    except ValueError:
        pass
    return None

# HTML Page with Improved UI
def generate_html(message="", rgb="", dot="", led_status=""):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Cardputer Controller</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f4;
          text-align: center;
          padding: 20px;
        }}
        h1, h2, h3 {{
          color: #333;
        }}
        .container {{
          max-width: 400px;
          margin: auto;
          background: white;
          padding: 20px;
          border-radius: 10px;
          box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        }}
        input, button {{
          width: 90%;
          padding: 10px;
          margin: 10px 0;
          border: 1px solid #ddd;
          border-radius: 5px;
        }}
        button {{
          background-color: #28a745;
          color: white;
          border: none;
          cursor: pointer;
        }}
        button:hover {{
          background-color: #218838;
        }}
        .led-status {{
          font-size: 18px;
          color: { 'green' if led_status == 'ON' else 'red' };
          font-weight: bold;
        }}
      </style>
    </head>
    <body>

      <div class="container">
        <h1>Cardputer Controller</h1>
        <img src="https://codehs.com/uploads/17fb1f56d419c7ba2e85bcdcefadfe30">
        <h2>Send Message</h2>
        <form action="/send_message" method="get">
          <input type="text" name="message" placeholder="Type something..."/>
          <button type="submit">Send to Screen</button>
        </form>
        <h3>Last Message: {message}</h3>

        <h2>Set Background Color</h2>
        <form action="/set_rgb" method="get">
          <input type="text" name="rgb" placeholder="Enter RGB as r,g,b"/>
          <button type="submit">Set RGB</button>
        </form>
        <h3>Current RGB: {rgb}</h3>

        <h2>Place a Dot</h2>
        <form action="/set_dot" method="get">
          <input type="text" name="cord" placeholder="Enter coordinates as x,y"/>
          <button type="submit">Place Dot</button>
        </form>
        <h3>Last placed dot: {dot}</h3>

        <h2>Screen Control</h2>
        <form action="/clear_screen" method="get">
          <button type="submit" style="background-color: #dc3545;">Clear Screen</button>
        </form>

      </div>

    </body>
    </html>
    """

# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

current_rgb = [0, 0, 0]  # Default RGB value
current_dot = [0, 0]  # Default dot position

while True:
    conn, addr = s.accept()
    print("Connection from", addr)
    request = conn.recv(1024).decode()
    print(request)

    message = ""

    # Check if the request is to turn LED on/off
    

    if "GET /send_message" in request:
        print("Handling /send_message request...")

        match = ure.search(r"message=([^& ]+)", request)
        if match:
            message = match.group(1).replace("+", " ")  # Replace '+' with spaces
            card.clear()
            card.prinS(message, [0,0], [200,200,200])
    
    # Handle RGB input
    elif "GET /set_rgb" in request:
        print("Handling /set_rgb request...")

        match = ure.search(r"rgb=([^& ]+)", request)
        if match:
            rgb_str = match.group(1)
            rgb = parse_rgb(rgb_str)
            if rgb:
                current_rgb = rgb
                card.clear()
                card.fill([rgb[0], rgb[1], rgb[2]])  # Set background color
                 # Display text in contrast color
            else:
                print("Invalid RGB value!")

    # Handle dot placement
    elif "GET /set_dot" in request:
        print("Handling /set_dot request...")

        match = ure.search(r"cord=([^& ]+)", request)
        if match:
            dot_str = match.group(1)
            dot = parse_dot(dot_str)
            if dot:
                current_dot = dot
                card.dot([dot[1],dot[0]])  # Call dot() with only coordinates
            else:
                print("Invalid Position!")

    # Handle clearing the screen
    elif "GET /clear_screen" in request:
        print("Clearing screen...")
        card.clear()

    response = "HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n"
    response += generate_html(message, str(current_rgb), str(current_dot))
    
    conn.sendall(response)
    conn.close()

