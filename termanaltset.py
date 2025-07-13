from cardputershell import ShellPrinter
import time, random
shell = ShellPrinter()
def reverse_string(s):
  """Reverses a string manually using a loop."""
  reversed_s = ""
  for i in range(len(s) - 1, -1, -1):
    reversed_s += s[i]
  return reversed_s
def revv():
    name = shell.input('Name: ')
    shell.print(reverse_string(name))
    time.sleep(3)
shell.print('hello!, WELCOME')
ables = ['Reverse', 'Random']
def rando():
    shell.print(str(random.randint(0, int(shell.input('Printing a random number between 0 and: ')))))
    time.sleep(1.5)
while True:
    shell.print('What do you want to do? (you can use "exit")')
    for e in range(len(ables)):
        shell.print(f'{str(e + 1)}: {ables[e]}')
    num = shell.input('')
    if num == 'exit':
        break
    if num == '1':
        shell.clear()
        revv()
        shell.clear()
    elif num == '2':
        shell.clear()
        rando()
        shell.clear()