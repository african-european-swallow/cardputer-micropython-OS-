from cardputershell import ShellPrinter
import time
shell = ShellPrinter()

# Print multiple lines
#shell.set_font('16x16')
shell.print("Hello, welcome to the shell!")
shell.print("This line is long enough to demonstrate wrapping within the screen.")
shell.print("Another log entry!")
# Clear the display
#shell.clear()

# Change text color
shell.set_color((0, 255, 0))
shell.print("Green text!")
# Change font dynamically
#shell.set_font('16x16')
'''shell.print("Using a larger font now!")
for i in range(100):
    shell.print(str(i))'''
shell.print("o")
shell.print("p")
shell.print("p")
shell.print(str(shell.input('Test: ')))
time.sleep(2)