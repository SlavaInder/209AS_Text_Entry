# this file makes use of code presented in this resources
# https://stackoverflow.com/questions/24214643/python-to-automatically-select-serial-ports-for-arduino
import logging
import serial
import tkinter as tk
from serial.tools import list_ports
import predictors_lib as pred
import autocomplete as ac


# predictor parameters
MEMORY_LEN = 5
NUM_PREDICTIONS = 5

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
        self.is_connected = False

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
        if self.is_connected:
            return self.serial.read(self.num_bytes).decode("utf-8")
        else:
            return ""


# an interactive entry that allows to display suggestions
class AutocompleteEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        # set internal parameters
        # current length of listbox
        self.listboxLength = 0
        # memory remembering last typed words
        self.memory = [""]
        # parent (root)
        self.parent = args[0]
        # init memory for a decoder
        self.recordings = []
        # arduino adapter to read from com port
        self.arduino_adapter = kwargs['arduino_adapter']
        del kwargs['arduino_adapter']
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
        self.bind("<Escape>", self.delete_listbox)

        self.listboxUp = False

        self.after(50, self.arduino_read)

    def arduino_read(self):
        if self.arduino_adapter.read() != "":
            complete_history = disp_string(self.recordings, self.arduino_adapter.read())
            self.var.set(complete_history)
            self.after(50, self.arduino_read)


    def delete_listbox(self, event=None):
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
            self.delete_listbox()
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
                self.delete_listbox()

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)

    def delentry(self,event):
        T.insert(tk.INSERT, self.get())
        self.memory.pop(0)
        self.memory.append(self.get())
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
        current_text = self.var.get()
        options = self.matchesFunction(self.memory, current_text)
        return options


def autocomplete_predictor_wrapper(memory, seq):
    last_word = memory[-1]
    predictions_raw = ac.predict(last_word, seq, NUM_PREDICTIONS)
    predictions_clear = []
    for i in range(len(predictions_raw)):
        predictions_clear.append(predictions_raw[i][0])
    return predictions_clear


def disp_string(rec_list, ch):
    s = b''.join(rec_list).decode("ascii")
    l1 = [i for i, letter in enumerate(s) if letter == ch]
    l2 = [i-1 for i, letter in enumerate(s) if letter == ch]
    l1.extend(l2)
    idx = list(range(len(rec_list)))
    cov_idx = list(set(idx)^set(l1))
    disp_list = [rec_list[i] for i in cov_idx]
    disp_str = b''.join(disp_list).decode("ascii")
    return disp_str

if __name__ == '__main__':
    # setup logging
    logging.basicConfig(filename='logs/main_execution.log', filemode='w', level=logging.DEBUG)
    # init Arduino adapter
    my_adapter = ArduinoAdapter()
    # connect adapter and arduino
    # my_adapter.connect()

    # init trie
    t9 = pred.Trie()
    # train trie
    training_set_location = "./training_sets/smsCorpus_en_2015.03.09_all.json"
    t9.json_train_adapter(training_set_location)

    # train swapnil model
    ac.load()

    # init tkinter main window
    root = tk.Tk()
    # init a text entry to store already typed text
    T = tk.Text(root, height=10, width=50)
    # init interactive entry
    entry = AutocompleteEntry(root,
#                              matchesFunction=t9.predict,
                              matchesFunction=autocomplete_predictor_wrapper,
                              arduino_adapter=my_adapter,
                              width=32)
    entry.grid(row=0, column=0)
    T.grid(column=0)
    root.mainloop()



