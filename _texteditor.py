import time
import sys
import os
from cardputerlib import prinS, clear, waitfor, imput, button, pressing
from cardkey import KeyBoard
try:
    import sdcard
    import machine
    import uos

    # Configure SPI and CS pin to match your hardware setup
    spi = machine.SPI(1, baudrate=1000000, sck=machine.Pin(40), mosi=machine.Pin(14), miso=machine.Pin(39))
    cs = machine.Pin(12, machine.Pin.OUT)

    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    SDCARD_MOUNTED = True
except Exception as e:
    print("SD card mount failed:", e)
    SDCARD_MOUNTED = False
def is_dir(path):
    try:
        mode = os.stat(path)[0]
        return mode & 0x4000 == 0x4000  # 0x4000 = stat.S_IFDIR
    except:
        return False

def syntax_check(source, filename="<string>"):
    try:
        compile(source, filename, "exec")
        return True, None
    except Exception as e:
        return False, str(e)

class TextEditor:
    def __init__(self, filename="untitled.txt"):
        self.keyboard = KeyBoard()
        self.filename = filename
        self.text = self.load_file()
        self.cursor_pos = len(self.text)
        self.last_text = ""
        self.overide = False
        self.last_cursor_pos = -1
        self.scroll_offset = 0
        self.horiz_scroll_offset = 0

    def load_file(self):
        try:
            with open(self.filename, "r") as file:
                return file.read()
        except OSError:
            return ""

    def save_file(self):
        with open(self.filename, "w") as file:
            file.write(self.text)

    def insert_char(self, char):
        if char == "\\":
            self.pending_backslash = True
            return

        if hasattr(self, "pending_backslash") and self.pending_backslash:
            if char == "n":
                self.text = self.text[:self.cursor_pos] + "\n" + self.text[self.cursor_pos:]
                self.cursor_pos += 1
                del self.pending_backslash
                time.sleep(0.05)
            else:
                self.pending_backslash = False
        else:
            self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
            self.cursor_pos += 1

    def backspace(self):
        if self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1

    def move_cursor_left(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def move_cursor_right(self):
        if self.cursor_pos < len(self.text):
            self.cursor_pos += 1

    def scroll_up(self):
        lines = self.text.split("\n")
        cursor_line = self.text.count("\n", 0, self.cursor_pos)
        
        if cursor_line > 0:
            # Get the start of the previous line
            prev_line_start = self.text.rfind("\n", 0, self.text.rfind("\n", 0, self.cursor_pos))
            prev_line_start = prev_line_start + 1 if prev_line_start != -1 else 0
            
            # Calculate the column in the previous line
            cursor_column = self.cursor_pos - self.text.rfind("\n", 0, self.cursor_pos) - 1
            
            # Ensure the cursor stays within bounds of the new line
            if cursor_column < len(lines[cursor_line - 1]):
                self.cursor_pos = prev_line_start + cursor_column
            else:
                self.cursor_pos = prev_line_start + len(lines[cursor_line - 1])
        
        self.update_screen()

    def scroll_down(self):
        lines = self.text.split("\n")
        cursor_line = self.text.count("\n", 0, self.cursor_pos)
        
        if cursor_line < len(lines) - 1:
            # Get the start of the next line
            next_line_start = self.text.find("\n", self.cursor_pos) + 1
            next_line_start = next_line_start if next_line_start != -1 else len(self.text)
            
            # Calculate the column in the next line
            cursor_column = self.cursor_pos - self.text.rfind("\n", 0, self.cursor_pos) - 1
            
            # Ensure the cursor stays within bounds of the new line
            if cursor_column < len(lines[cursor_line + 1]):
                self.cursor_pos = next_line_start + cursor_column
            else:
                self.cursor_pos = next_line_start + len(lines[cursor_line + 1])
        
        self.update_screen()
    def move_by(self):
        clear()
        time.sleep(0.1)
        num_str = imput('+ or - height: ', [0, 0], [255, 255, 255])
        try:
            num = int(num_str)
        except ValueError:
            return  # Exit if input isn't a number

        lines = self.text.split("\n")
        current_line = self.text.count("\n", 0, self.cursor_pos)
        target_line = current_line + num

        # Clamp the target line
        target_line = max(0, min(len(lines) - 1, target_line))

        # Compute current column
        try:
            line_start = self.text.rfind("\n", 0, self.cursor_pos)
            if line_start == -1:
                column = self.cursor_pos
            else:
                column = self.cursor_pos - line_start - 1
        except:
            column = 0

        # Compute new cursor position at target line and column
        new_pos = 0
        for i in range(target_line):
            new_pos += len(lines[i]) + 1  # +1 for newline
        new_pos += min(column, len(lines[target_line]))

        self.cursor_pos = new_pos
        self.update_screen()

    def update_screen(self):
        if self.text != self.last_text or self.cursor_pos != self.last_cursor_pos or self.overide:
            self.overide = False
            clear()

            screen_width = 230
            screen_height = 135
            line_height = 8
            max_chars_per_line = screen_width // 8
            max_lines = screen_height // line_height

            lines = self.text.split("\n")
            total_lines = len(lines)

            cursor_line = self.text.count("\n", 0, self.cursor_pos)
            cursor_column = self.cursor_pos - self.text.rfind("\n", 0, self.cursor_pos) - 1

            if cursor_line < self.scroll_offset:
                self.scroll_offset = cursor_line
            elif cursor_line >= self.scroll_offset + max_lines:
                self.scroll_offset = cursor_line - max_lines + 1

            if cursor_column < self.horiz_scroll_offset:
                self.horiz_scroll_offset = cursor_column
            elif cursor_column >= self.horiz_scroll_offset + max_chars_per_line:
                self.horiz_scroll_offset = cursor_column - max_chars_per_line + 1

            if self.scroll_offset > total_lines - max_lines:
                self.scroll_offset = max(0, total_lines - max_lines)

            for i in range(min(max_lines, total_lines - self.scroll_offset)):
                line = lines[self.scroll_offset + i]
                prinS(line[self.horiz_scroll_offset:self.horiz_scroll_offset + max_chars_per_line], [0, i * line_height], [255, 255, 255])

            cursor_x = (cursor_column - self.horiz_scroll_offset) * 8
            cursor_y = (cursor_line - self.scroll_offset) * line_height
            prinS("_", [cursor_x, cursor_y], [255, 255, 255])

            self.last_text = self.text
            self.last_cursor_pos = self.cursor_pos

    def run(self):
        clear()
        prinS(f"Editing: {self.filename}", [0, 0], [0, 255, 0])
        self.overide = True
        time.sleep(1)
        clear()
        self.update_screen()

        while not pressing(['ESC']):
            if button():
                self.text = self.text[:self.cursor_pos] + "\n" + self.text[self.cursor_pos:]
                self.cursor_pos += 1
                self.update_screen()
                time.sleep(0.09)

            keys = self.keyboard.get_pressed_keys()
            if keys:
                for key in keys:
                    if key == 'ENT':
                        if self.filename.endswith(".py"):
                            ok, err = syntax_check(self.text, self.filename)
                            if not ok:
                                clear()
                                prinS("Syntax Error!", [0, 0], [255, 0, 0])
                                prinS(err[:100], [0, 8], [255, 0, 0])
                                time.sleep(2)
                                prinS('save?(y)', [0,20], [0,255,0])
                                while True:
                                    if pressing(['any']):
                                        break
                                    time.sleep(0.05)
                                if pressing(['any']) and not pressing(['y']):
                                    time.sleep(0.1)
                                    continue
                                self.update_screen()
                        self.save_file()
                        clear()
                        prinS(f"\nSaved: {self.filename}!", [0, 0], [0, 255, 0])
                        self.overide = True
                        time.sleep(1)
                        clear()
                        self.update_screen()
                    elif key == 'BSPC':
                        self.backspace()
                    elif key == 'LEFT':
                        self.move_cursor_left()
                    elif key == 'RIGHT':
                        self.move_cursor_right()
                    elif key == 'UP':
                        self.scroll_up()
                    elif key == 'DOWN':
                        self.scroll_down()
                    elif key == 'ESC':
                        break
                    elif key == 'TAB':
                        [self.insert_char(' ') for z in range(4)]
                    elif key == 'OPT':
                        self.move_by()
                    elif key and len(key) == 1:
                        self.insert_char(key)
                    self.update_screen()
            time.sleep(0.1)
def delete_folder_recursive(path):
    """Recursively delete all files and subfolders in a directory."""
    for item in os.listdir(path):
        full_item = path + item
        if is_dir(full_item):
            delete_folder_recursive(full_item + '/')
        else:
            os.remove(full_item)
    os.rmdir(path.rstrip('/'))
# Add the duplicate_to_file_path function
def duplicate_to_file_path(src, dst):
    """Duplicates a file from the source path to the destination path."""
    try:
        with open(src, 'r') as src_file:
            content = src_file.read()
        with open(dst, 'w') as dst_file:
            dst_file.write(content)
        clear()
        prinS(f"File duplicated: {src} -> {dst}", [0, 0], [0, 255, 0])
        time.sleep(1)
    except Exception as e:
        clear()
        prinS(f"Error duplicating file: {e}", [0, 0], [255, 0, 0])
        time.sleep(1)

# Add the move_to_file_path function
def move_to_file_path(src, dst):
    """Moves a file from the source path to the destination path."""
    try:
        os.rename(src, dst)
        clear()
        prinS(f"File moved: {src} -> {dst}", [0, 0], [0, 255, 0])
        time.sleep(1)
    except Exception as e:
        clear()
        prinS(f"Error moving file: {e}", [0, 0], [255, 0, 0])
        time.sleep(1)

def list_files2(directory, dev=False):
    """Returns a list of files and directories from the given directory."""
    files = []
    for file in os.listdir(directory):
        full_path = directory.rstrip("/") + "/" + file
        if (not file.endswith(".py") or file.endswith('py.py')) or dev:
            if is_dir(full_path):
                files.append(file + '/')
            else:
                files.append(file)
    return files


def delete_file(directory):
    """Handles deletion of files and folders (only if 'd foldername' is typed)."""
    devses=False
    while True:
        clear()
        prinS(f"Available ({directory}):", [0, 0], [255, 255, 255])
        lists = list_files2(directory, dev=devses)
        prinS(', '.join(lists), [0, 8], [255, 255, 255])
        user_input = imput("File or 'd folder' or '!esc': ", [0, 112], [255, 255, 255])
        clear()

        if user_input == '!esc' or user_input == '':
            break
        if user_input == 'dev':
            devses=True
        elif user_input.startswith('d '):
            folder = user_input[2:].strip()
            full_path = directory + folder + '/'
            if is_dir(full_path):
                confirm = imput(f"Delete folder '{folder}' recursively? (y/n):", [0, 0], [255, 0, 0])
                if confirm == 'y':
                    try:
                        delete_folder_recursive(full_path)
                    except Exception as e:
                        prinS(f"Err: {str(e)}", [0, 0], [255, 0, 0])
                        time.sleep(1)
            else:
                prinS(f"No such folder: {folder}", [0, 0], [255, 0, 0])
                time.sleep(1)
        else:
            file_path = directory + user_input
            confirm = imput(f"Delete file {user_input}? (y/n):", [0, 0], [255, 0, 0])
            if confirm == 'y' and (not user_input.endswith('.py') or user_input.endswith('py.py') or devses):
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    prinS(f"Not found: {file_path}", [0, 0], [255, 0, 0])
                    time.sleep(1)


def handle_directory_navigation(dis, filename):
    """Handles directory navigation based on user input."""
    if filename.startswith('c '):
        newname = filename[2:]
        if newname.endswith('/'):
            try:
                os.mkdir(dis + newname.rstrip('/'))
            except Exception as e:
                prinS(str(e), [0, 120], [255, 0, 0])
                time.sleep(1)
    elif filename.endswith('/'):
        dis += filename
    elif filename == '..':
        # Go back one directory
        if dis != '/':
            dis = '/'.join(dis.strip('/').split('/')[:-1])
            dis = '/' + dis + '/' if dis else '/'
    return dis

def edit_file(dis, filename, dev):
    """Edits a file using TextEditor."""
    if (not filename.endswith('.py') or filename.endswith('py.py') or dev) and not filename.endswith('/') and filename != '..' and not filename.startswith('c '):
        editor = TextEditor(dis + filename.rstrip("/"))
        editor.run()

def main():
    dev = False
    dis = '/'
    deks = '/'
    
    while True:
        if not dev:
            clear()
            prinS(f"Available ({dis}):", [0, 0], [255, 255, 255])
            lists = list_files2(dis.rstrip("/"))
            prinS(', '.join(lists), [0, 8], [255, 255, 255])
            filename = imput('Enter filename, del,move,dup,..: ', [0, 112], [255, 255, 255])
        
        if filename == 'del':
            delete_file(deks)
        # Inside your existing main loop where the user chooses filename
        elif filename == 'dup':
            clear()
            source = imput("Enter source file to duplicate: ", [0, 0], [255, 0, 0])
            destination = imput("Enter destination file path: ", [0, 20], [255, 0, 0])
            if source != '' and destination != '':
                duplicate_to_file_path(source, destination)

        elif filename == 'move':
            clear()
            source = imput("Enter source file to move: ", [0, 0], [255, 0, 0])
            destination = imput("Enter destination file path: ", [0, 20], [255, 0, 0])
            if source != '' and destination != '':
                move_to_file_path(source, destination)

        elif filename == 'dev' or dev:
            dev = True
            clear()
            prinS(f"Available ({dis}):", [0, 0], [255, 255, 255])
            lists = list_files2(dis.rstrip("/"), dev=True)
            prinS(', '.join(lists), [0, 8], [255, 255, 255])
            filename = imput('Enter filename to edit or "del": ', [0, 112], [255, 255, 255])
            
        if pressing(['ESC']):
            break
            
        if filename != 'del' and filename != 'dev' and filename != 'dup' and filename != 'move':
            dis = handle_directory_navigation(dis, filename)
            print(dis,filename)
            edit_file(dis, filename, dev)


main()



