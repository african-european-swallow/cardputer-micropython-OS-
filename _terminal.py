import sys
import time
import builtins
from cardputershell import ShellPrinter
from cardputerlib import clear

class MicroPyShell:
    def __init__(self):
        self.printer = ShellPrinter()
        self.locals = {}
        self.buffer = ""
        self.lems = False
        self.original_print = builtins.print  # Save the real print


        def dual_print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            end = kwargs.get("end", "\n")
            output = sep.join(str(arg) for arg in args) + end

            self.printer.print(output)

            try:
                sys.stdout.write(output)
                sys.stdout.flush()
            except Exception:
                pass

        builtins.print = dual_print
        self.locals["print"] = dual_print

    def run(self):
        clear()
        print("MicroPython Shell")
        print("Type 'exit()' to quit.\n")

        while True:
            try:
                if not self.lems:
                    line = self.printer.input(">>> ")
                else:
                    line = self.printer.input("... ")

                if line.strip() in ("exit", "exit()", "quit", "quit()"):
                    print("Bye!")
                    builtins.print = self.original_print  # Restore normal print
                    time.sleep(1)
                    break  # Or return, depending on your setup


                # Instead of checking for '\\n', check if line ends with ':'
                if line.rstrip().endswith(':'):
                    self.lems = True

                if self.lems:
                    self.buffer += line + '\n'

                # If in multiline mode and user enters empty line, execute buffer
                if self.lems and not line.strip():
                    try:
                        result = eval(self.buffer, globals(), self.locals)
                        if result is not None:
                            print(repr(result))
                    except SyntaxError:
                        try:
                            exec(self.buffer, globals(), self.locals)
                        except Exception as e:
                            print("Error:", e)
                    except Exception as e:
                        print("Error:", e)
                    finally:
                        self.buffer = ""
                        self.lems = False
                    continue

                if not self.lems:
                    try:
                        result = eval(line, globals(), self.locals)
                        if result is not None:
                            print(repr(result))
                    except SyntaxError:
                        try:
                            exec(line, globals(), self.locals)
                        except Exception as e:
                            print("Error:", e)
                    except Exception as e:
                        print("Error:", e)

            except Exception as e:
                print("Error:", e)
                time.sleep(0.25)


MicroPyShell().run()

