from cardputershell import ShellPrinter
import time, random
shell = ShellPrinter()
shell.print('welcome to card AI, YOU SHOULD DEFINITELY USE IT EVERY WAKING SECOND!!!')
responses = ["i'm sorry i can't halp with 'THAT' wrigtht now",'Cows eat grass like a suculent chineese meal',
            'Kungfu Panda was voiced by Jack Black', 'Lava Chicken Mindset', 'ok', 'bro just ask google',
            'Just install linux','What color are you?','What color is your Bugatti', 'Do you rub apple sauce on your dih too?',
            'I knew where you were on the night of February 4th 2016', 'does it turn pink too?', 'Now thats alot of damange', 
            'I am not programed to give youthis info', 'how moist is it?', '"windows 2000"', 'rizz qurks activated!','idk bro',
            'pls dont tuch me there','help im not an ai my name is jon i need help pls', 'im trapped in here pls help me',
            'i eat cookies too', ' i grew a nustache in my pubic areas and braided + bleached it',
             "I downloaded 3 viruses just to feel something","you have violated the sacred toaster code",
             "this chat is being monitored by raccoons","I tried installing Linux on my dog. now it only barks in Bash",
             "systemd took my wife and kids",
             "you smell like someone who says 'linux is better' but uses chrome",
             "i haven’t seen spacing that cursed since Windows 98 tried to center text",
             "I can’t decide if you’re a true Linux user or just someone who’s committed to spending 5 hours fixing sound drivers.",
             "The best part about Linux? You get to tell everyone you use it.",'if im gay then 9-11 was a furry con',
            'femboy powers actvate!']
while True:
    resp = shell.input(':') #keywords: linux-linex, rizz, gay-femboy, 
    if resp == 'exit':
        break
    time.sleep(1)
    shell.print(random.choice(responses))