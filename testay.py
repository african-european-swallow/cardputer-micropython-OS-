import uasyncio as asyncio
import cardputerlib as card
import sys

card.clear()

# Define screen colors
ON_COLOR = [0, 128, 255]
OFF_COLOR = [0, 0, 0]

blinking = True
running = True  # Global control flag

# Utility: Update screen
def update_screen(color, message):
    card.rect(0, 0, 30, 30, color, fill=True)
    card.prinS(message, [100, 50], [255, 255, 255])

# Task: Blink screen color
async def blink_screen():
    on = True
    while running:
        if blinking:
            update_screen(ON_COLOR if on else OFF_COLOR,
                          "Blinking ON (` to quit)" if on else "")
            on = not on
        else:
            update_screen(OFF_COLOR, "Blinking OFF (` to quit)")
        await asyncio.sleep(0.5)

# Task: Handle button toggle and exit key
async def check_inputs():
    global blinking, running
    while running:
        if card.button():  # Your button logic
            blinking = not blinking
            print("Blinking toggled:", blinking)
            await asyncio.sleep(0.3)  # Debounce

        # Exit if ` key is being held
        if card.pressing(['`']):
            print("Detected ` key hold — exiting")
            running = False
            break

        await asyncio.sleep(0.05)

# Main runner
async def main():
    task1 = asyncio.create_task(blink_screen())
    task2 = asyncio.create_task(check_inputs())
    while running:
        await asyncio.sleep(0.1)
    task1.cancel()
    task2.cancel()
    card.prinS("Exiting...", [100, 100], [255, 0, 0])
    await asyncio.sleep(1)
    raise SystemExit  # Or sys.exit()

# Run the program
asyncio.run(main())
