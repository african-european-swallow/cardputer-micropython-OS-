import cardputerlib as card
import urequests
import time
import re
import network

# Connect to Wi-Fi
def connect_wifi():
    card.clear()
    card.setfont('8x8')
    card.prinS("Connect to Wi-Fi", [20, 10], [0, 255, 255])
    ssid = card.imput("SSID: ", [40, 40], [255, 255, 255])
    password = card.imput("Password: ", [70, 60], [255, 255, 255])

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    card.clear()
    card.prinS("Connecting...", [0, 30], [0, 255, 0])
    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(0.5)

    if wlan.isconnected():
        card.prinS("Connected!", [0, 50], [0, 255, 0])
        time.sleep(1)
        return True
    else:
        card.prinS("Connection Failed!", [0, 50], [255, 0, 0])
        time.sleep(2)
        return False

# Remove <script>...</script> blocks
def remove_scripts(html):
    while True:
        start = html.find("<script")
        end = html.find("</script>", start)
        if start == -1 or end == -1:
            break
        html = html[:start] + html[end+9:]
    return html

# Extract plain text and links from HTML
def extract_text_and_links(html):
    links = []
    html = remove_scripts(html)

    i = 0
    while True:
        match = re.search(r'<a\s+href=["\'](.*?)["\'].*?>(.*?)</a>', html)
        if not match:
            break
        href, text = match.group(1), match.group(2)
        placeholder = f"[{i}] {text}"
        html = html.replace(match.group(0), placeholder, 1)
        links.append(href)
        i += 1

    text = re.sub(r'<[^>]+>', '', html)
    return text, links

# Fetch and parse HTML
def fetch_page(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        r = urequests.get(url)
        return extract_text_and_links(r.text)
    except Exception as e:
        return (f"ERROR: {e}", [])

# Display paginated and scrollable text
def scrollable_text(text_lines, links):
    page = 0
    scroll_x = 0
    lines_per_page = 12
    total_pages = (len(text_lines) + lines_per_page - 1) // lines_per_page

    while True:
        card.clear()
        card.setfont('6x8')
        for i in range(lines_per_page):
            idx = page * lines_per_page + i
            if idx >= len(text_lines):
                break
            line = text_lines[idx]
            line_part = line[scroll_x:scroll_x + 40]
            card.prinS(line_part, [0, i * 10], [255, 255, 255])

        card.prinS(f"Page {page+1}/{total_pages}", [0, 120], [150, 150, 150])
        card.prinS("A: URL  B: Exit  C: Link#", [100, 120], [100, 100, 100])

        while True:
            action = card.dpad()
            if action or card.pressing(['any']):
                break
            time.sleep(0.05)

        if action == "DOWN" and page < total_pages - 1:
            page += 1
        elif action == "UP" and page > 0:
            page -= 1
        elif action == "LEFT" and scroll_x > 0:
            scroll_x -= 5
        elif action == "RIGHT":
            scroll_x += 5
        elif card.pressing(['a']):
            return "again", None
        elif card.pressing(['b']):
            return "exit", None
        elif card.pressing(['c']):
            link_num_str = card.imput("Link #: ", [0, 110], [255, 255, 0])
            try:
                link_num = int(link_num_str)
                if 0 <= link_num < len(links):
                    return "follow", links[link_num]
                else:
                    card.prinS("Invalid link!", [0, 100], [255, 0, 0])
                    time.sleep(1)
            except:
                card.prinS("Invalid input!", [0, 100], [255, 0, 0])
                time.sleep(1)

# Main app
def cardbrowser():
    if not connect_wifi():
        return

    url = None

    while True:
        card.clear()
        card.setfont('8x8')
        card.prinS("CardBrowse", [20, 10], [0, 255, 255])
        if not url:
            url = card.imput("Enter URL: ", [0, 60], [255, 255, 255])

        card.clear()
        card.prinS("Fetching...", [0, 30], [0, 255, 0])
        content, links = fetch_page(url)
        lines = content.split('\n')

        result, link_url = scrollable_text(lines, links)

        if result == "exit":
            break
        elif result == "again":
            url = None
        elif result == "follow":
            url = link_url

    card.clear()
    card.prinS("Goodbye!", [30, 60], [255, 0, 0])
    time.sleep(1)
    card.clear()

# Run browser
cardbrowser()

