# this file makes use of code presented in this resources
# https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
import logging
import serial
import tkinter as tk
from serial.tools import list_ports


# connection parameters
ARDUINO_NAME = "seeduino"
BAUD_RATE = 9600
TIME_OUT = 10
NUM_BYTES = 2


# set up log messages for connect
msg_arduino_adapter_connect_start = "Adapter started searching for connected arduino"
msg_arduino_adapter_no_device_found = "Adapter has not found any connected devices"
msg_arduino_adapter_device_found = "Adapter found {name} connected to {port}"
msg_arduino_adapter_connect_failed = "No arduino is found"
msg_arduino_adapter_connect_successful = "Adapter connected to an arduino device on port {port}"


# this class handles connection with arduino:
class ArduinoAdapter(object):
    def __init__(self):
        self.serial = None
        self.port_name = None
        self.baud_rate = BAUD_RATE
        self.time_out = TIME_OUT
        self.num_bytes = NUM_BYTES

    # establishes connection with arduino
    def connect(self):
        # start logging
        logging.info(msg_arduino_adapter_connect_start)
        # get the list of all connected devices
        devices = list_ports.comports()
        # if no device is found raise the warning
        if len(devices) == 0:
            logging.warning(msg_arduino_adapter_no_device_found)
            raise IOError(msg_arduino_adapter_no_device_found)
        # if there are some connected devices
        else:
            for i in range(len(devices)):
                # log the device name
                logging.info(msg_arduino_adapter_device_found.format(name=devices[i][1].lower(), port=devices[i][0]))
                # check if this device is an arduino
                if ARDUINO_NAME in devices[i][1].lower():
                    # if it is, establish connection with it
                    self.serial = serial.Serial(devices[i][0], self.baud_rate, timeout=self.time_out)
                    # report successful connection
                    logging.info(msg_arduino_adapter_connect_successful.format(port=devices[i][0]))
                    # exit function
                    return
            # if no arduino was found among devices
            logging.warning(msg_arduino_adapter_connect_failed)
            raise IOError(msg_arduino_adapter_connect_failed)

    # read a symbol from COM port
    def read(self):
        return self.serial.read(self.num_bytes).decode("utf-8")


class KeyBoardAdapter(object):
    def read(self):
        return


def predict():
    pass


# an interactive entry that allows to display suggestions
class AutocompleteEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        # set internal parameters
        # current length of listbox
        self.listboxLength = 0
        # parent (root)
        self.parent = args[0]
        # whether list of choices is currently displayed
        # Custom matches function
        self.matchesFunction = kwargs['matchesFunction']
        del kwargs['matchesFunction']
        # init exactly as parent class
        tk.Entry.__init__(self, *args, **kwargs)
        # direct user input to the entry
        self.focus()
        # get a variable to track
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        # bind change of the text in textbox to  the corresponding function
        self.var.trace('w', self.changed)

        self.bind("<Right>", self.selection)
        self.bind("<Enter>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.bind("<Return>", self.delentry)
        self.bind("<Escape>", self.deleteListbox)

        self.listboxUp = False

    def deleteListbox(self, event=None):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxUp = False

    def select(self, event=None):
        if self.listboxUp:
            index = self.listbox.curselection()[0]
            value = self.listbox.get(tk.ACTIVE)
            self.listbox.destroy()
            self.listboxUp = False
            self.delete(0, tk.END)
            self.insert(tk.END, value)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.deleteListbox()
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listboxLength = len(words)
                    self.listbox = tk.Listbox(self.parent,
                        width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(
                        x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                else:
                    self.listboxLength = len(words)
                    self.listbox.config(height=self.listboxLength)

                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END, w)
            else:
                self.deleteListbox()

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)

    def delentry(self,event):
        T.insert(tk.INSERT, self.get())
        T.insert(tk.INSERT, " ")
        self.delete(0, 'end')

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            self.listbox.selection_clear(first=index)
            index = str(int(index) - 1)
            if int(index) == -1:
                index = str(self.listboxLength-1)

            self.listbox.see(index)  # Scroll!
            self.listbox.selection_set(first=index)
            self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
            else:
                index = self.listbox.curselection()[0]

            if index != tk.END:
                self.listbox.selection_clear(first=index)
                if int(index) == self.listboxLength-1:
                    index = "0"
                else:
                    index = str(int(index)+1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        print(self.var.get())
        text = "recommendation"
        return [text]


if __name__ == '__main__':
    # setup logging
    logging.basicConfig(filename='logs/main_execution.log', filemode='w', level=logging.DEBUG)
    # init Arduino adapter
#    my_adapter = ArduinoAdapter()
    # connect adapter and arduino
#    my_adapter.connect()


    # init tkinter main window
    root = tk.Tk()
    # init a text enty to store already typed text
    T = tk.Text(root, height=10, width=50)
    # init interactive entry
    entry = AutocompleteEntry(root, matchesFunction=predict, width=32)
    entry.grid(row=0, column=0)
    T.grid(column=0)
    root.mainloop()



