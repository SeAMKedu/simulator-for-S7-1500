import os
import pathlib
import time
from threading import Thread

import customtkinter as ctk
import snap7
import snap7.util
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Window resolution.
RESX = 500
RESY = 640
# Colors.
COLOR_FG = "white"
# Widths and heights of the frames.
WIDTH_CYL = RESX * 0.7 - 10
WIDTH_MOT = RESX * 0.3 - 10
HEIGHT_NAME = 28
HEIGHT_IMAGE = 50
HEIGHT_IO = (RESY - 4 * (HEIGHT_NAME + HEIGHT_IMAGE)) / 4
# Images.
PATH = pathlib.Path(__file__).parent
IMAGE_CYL = Image.open(os.path.join(PATH, "images", "cylinder.png"))
IMAGE_MT0 = Image.open(os.path.join(PATH, "images", "motor_red.png"))
IMAGE_MTT = Image.open(os.path.join(PATH, "images", "motor_yellow.png"))
IMAGE_MT1 = Image.open(os.path.join(PATH, "images", "motor_green.png"))
# Minimum and maximum X position of the cylinder.
CYL_XMIN = 0
CYL_XMAX = 180
# Delay when the motor starts or stops.
MOTOR_TRANSITION_DELAY = 2


class NameFrame(ctk.CTkFrame):
    """Frame that contains the name of the cylinder or motor."""
    def __init__(self, master, name: int, width: int, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2CC985", width=width, height=HEIGHT_NAME)
        self.font = ctk.CTkFont(weight="bold")
        self.label = ctk.CTkLabel(self, width=width, text=name, font=self.font)
        self.label.grid(row=0, column=0)


class IOFrame(ctk.CTkFrame):
    """Frame that contains the values of the inputs and outputs."""
    def __init__(self, master, width: int, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=COLOR_FG, width=width, height=HEIGHT_IO)

        self.label1 = ctk.CTkLabel(self, width=width, anchor="w")
        self.label1.grid(row=0, column=0)
        self.label2 = ctk.CTkLabel(self, width=width, anchor="w")
        self.label2.grid(row=1, column=0)


class CylinderImageFrame(ctk.CTkFrame):
    """Frame that contains the movable image of the cylinder."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=COLOR_FG, width=WIDTH_CYL, height=HEIGHT_IMAGE)

        self.xpos = CYL_XMIN
        self.img_cyl = ctk.CTkImage(light_image=IMAGE_CYL, size=(150, 50))
        self.image = ctk.CTkLabel(self, image=self.img_cyl, text="")
        self.image.grid(row=0, column=0)
        self.image.place(x=CYL_XMIN)
    
    def _move2plus(self):
        for x in range(CYL_XMIN, CYL_XMAX + 1):
            self.xpos = x
            self.image.place(x=self.xpos)
            time.sleep(0.01)

    def _move2minus(self):
        for x in range(CYL_XMIN, CYL_XMAX + 1):
            self.xpos = CYL_XMAX - x
            self.image.place(x=self.xpos)
            time.sleep(0.01)

    def move_to_plus(self):
        """Start a thread that moves the image to the right."""
        Thread(target=self._move2plus).start()

    def move_to_minus(self):
        """Start a thread that moves the image to the left."""
        Thread(target=self._move2minus).start()


class MotorImageFrame(ctk.CTkFrame):
    """Frame that contains the image of the motor."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=COLOR_FG, width=WIDTH_MOT, height=HEIGHT_IMAGE)

        self.state = 0
        self.img0 = ctk.CTkImage(light_image=IMAGE_MT0, size=(80, 50))
        self.imgt = ctk.CTkImage(light_image=IMAGE_MTT, size=(80, 50))
        self.img1 = ctk.CTkImage(light_image=IMAGE_MT1, size=(80, 50))
        self.image0 = ctk.CTkLabel(self, image=self.img0, text="") # motor OFF
        self.image0.grid(row=0, column=0)
        self.imaget = ctk.CTkLabel(self, image=self.imgt, text="") # transition
        self.imaget.grid(row=0, column=0)
        self.image1 = ctk.CTkLabel(self, image=self.img1, text="") # motor ON
        self.image1.grid(row=0, column=0)
        self.image0.lift()

    def _start_motor(self):
        self.imaget.lift()  # show yellow motor
        time.sleep(MOTOR_TRANSITION_DELAY)
        self.image1.lift()  # show green motor
        self.state = 1
    
    def _stop_motor(self):
        self.imaget.lift()  # show yellow motor
        time.sleep(MOTOR_TRANSITION_DELAY)
        self.image0.lift()  # show red motor
        self.state = 0

    def turn_on(self):
        """Show the image of the green motor."""
        Thread(target=self._start_motor).start()
        
    def turn_off(self):
        """Show the image of the red motor."""
        Thread(target=self._stop_motor).start()


class CylinderFrame(ctk.CTkFrame):
    """Frame that contains the name, image, and IO variables of the cylinder."""
    def __init__(self, master, num: int, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=COLOR_FG, width=WIDTH_CYL)

        self.name = NameFrame(self, name=f"Cylinder {num}", width=WIDTH_CYL)
        self.name.grid(row=0, column=0, columnspan=2)

        self.image = CylinderImageFrame(self)
        self.image.grid(row=1, column=0, columnspan=2)

        self.io1 = IOFrame(self, width=WIDTH_CYL/2)
        self.io1.grid(row=2, column=0)

        self.io2 = IOFrame(self, width=WIDTH_CYL/2)
        self.io2.grid(row=2, column=1)


class MotorFrame(ctk.CTkFrame):
    """Frame that contains the name, image, and IO variables of the motor."""
    def __init__(self, master, num: int, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color=COLOR_FG, width=WIDTH_MOT)

        self.name = NameFrame(self, name=f"Motor {num}", width=WIDTH_MOT)
        self.name.grid(row=0, column=0)

        self.image = MotorImageFrame(self)
        self.image.grid(row=1, column=0)

        self.io = IOFrame(self, width=WIDTH_MOT)
        self.io.grid(row=2, column=0)


class ConfigFrame(ctk.CTkFrame):
    """Frame that contains the configuration for the PLC connection."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=RESX, height=RESY)

        self.client = snap7.client.Client()

        self.addr = ctk.StringVar(master=self, value="192.168.0.1")
        self.rack = ctk.IntVar(master=self, value=0)
        self.slot = ctk.IntVar(master=self, value=1)
        self.dbi = ctk.IntVar(master=self, value=2) # data block for inputs
        self.dbq = ctk.IntVar(master=self, value=3) # data block for outputs

        self.label1 = ctk.CTkLabel(self, width=200, text="PLC Address")
        self.label1.grid(row=0, column=0, pady=5)
        self.entry1 = ctk.CTkEntry(self, textvariable=self.addr)
        self.entry1.grid(row=0, column=1, pady=5)

        self.label2 = ctk.CTkLabel(self, width=200, text="Rack number")
        self.label2.grid(row=1, column=0, pady=5)
        self.entry2 = ctk.CTkEntry(self, textvariable=self.rack)
        self.entry2.grid(row=1, column=1, pady=5)

        self.label3 = ctk.CTkLabel(self, width=200, text="Slot number")
        self.label3.grid(row=2, column=0, pady=5)
        self.entry3 = ctk.CTkEntry(self, textvariable=self.slot)
        self.entry3.grid(row=2, column=1, pady=5)

        self.label4 = ctk.CTkLabel(self, width=200, text="DB number for inputs")
        self.label4.grid(row=3, column=0, pady=5)
        self.entry4 = ctk.CTkEntry(self, textvariable=self.dbi)
        self.entry4.grid(row=3, column=1, pady=5)

        self.label5 = ctk.CTkLabel(self, width=200, text="DB number for outputs")
        self.label5.grid(row=4, column=0, pady=5)
        self.entry5 = ctk.CTkEntry(self, textvariable=self.dbq)
        self.entry5.grid(row=4, column=1, pady=5)

        self.button = ctk.CTkButton(self, text="Connect", command=self._connect)
        self.button.grid(row=5, column=0, pady=(20, 0))
        self.connstatus = ctk.CTkLabel(self, text="Not connected")
        self.connstatus.grid(row=5, column=1, pady=(20, 0))

        self._connect()

    def _connect(self):
        """Connect to the PLC."""
        try:
            addr = self.addr.get()
            rack = self.rack.get()
            slot = self.slot.get()
            self.client.connect(addr, rack, slot)
            self.connstatus.configure(text="Connected")
        except RuntimeError as error:
            self.connstatus.configure(text=error.args[0])



class SimulationFrame(ctk.CTkFrame):
    """Frame that contains the cylinders and motors."""
    def __init__(self, master, plc: ConfigFrame, **kwargs):
        super().__init__(master, **kwargs)

        self.plc = plc
        # Input variables.
        self.iCyl1minus = False
        self.iCyl1plus = False
        self.iCyl2minus = False
        self.iCyl2plus = False
        self.iCyl3minus = False
        self.iCyl3plus = False
        self.iCyl4minus = False
        self.iCyl4plus = False
        self.iMot1running = False
        self.iMot2running = False
        self.iMot3running = False
        self.iMot4running = False
        # Output variables.
        self.qCyl1toMinus = False
        self.qCyl1toPlus = False
        self.qCyl2toMinus = False
        self.qCyl2toPlus = False
        self.qCyl3toMinus = False
        self.qCyl3toPlus = False
        self.qCyl4toMinus = False
        self.qCyl4toPlus = False
        self.qMot1start = False
        self.qMot2start = False
        self.qMot3start = False
        self.qMot4start = False
        # Cylinders.
        self.cyl1 = CylinderFrame(self, num=1)
        self.cyl1.grid(row=0, column=0)
        self.cyl2 = CylinderFrame(self, num=2)
        self.cyl2.grid(row=1, column=0)
        self.cyl3 = CylinderFrame(self, num=3)
        self.cyl3.grid(row=2, column=0)
        self.cyl4 = CylinderFrame(self, num=4)
        self.cyl4.grid(row=3, column=0)
        # Motors.
        self.mot1 = MotorFrame(self, num=1)
        self.mot1.grid(row=0, column=1)
        self.mot2 = MotorFrame(self, num=2)
        self.mot2.grid(row=1, column=1)
        self.mot3 = MotorFrame(self, num=3)
        self.mot3.grid(row=2, column=1)
        self.mot4 = MotorFrame(self, num=4)
        self.mot4.grid(row=3, column=1)

    def dbread(self):
        """Read outputs from the PLC and control cylinders and motors."""
        # Read outputs from the data block on the PLC.
        if self.plc.client.get_connected():
            db_number = self.plc.dbq.get()
            buffer = self.plc.client.db_read(db_number, 0, 2)
            self.qCyl1toMinus = snap7.util.get_bool(buffer, 0, 0)
            self.qCyl1toPlus = snap7.util.get_bool(buffer, 0, 1)
            self.qMot1start = snap7.util.get_bool(buffer, 0, 2)
            self.qCyl2toMinus = snap7.util.get_bool(buffer, 0, 3)
            self.qCyl2toPlus = snap7.util.get_bool(buffer, 0, 4)
            self.qMot2start = snap7.util.get_bool(buffer, 0, 5)
            self.qCyl3toMinus = snap7.util.get_bool(buffer, 0, 6)
            self.qCyl3toPlus = snap7.util.get_bool(buffer, 0, 7)
            self.qMot3start = snap7.util.get_bool(buffer, 1, 0)
            self.qCyl4toMinus = snap7.util.get_bool(buffer, 1, 1)
            self.qCyl4toPlus = snap7.util.get_bool(buffer, 1, 2)
            self.qMot4start = snap7.util.get_bool(buffer, 1, 3)
        # Move cylinder to the plus position.
        if self.iCyl1minus and self.qCyl1toPlus:
            self.iCyl1minus = False
            self.cyl1.image.move_to_plus()
        if self.iCyl2minus and self.qCyl2toPlus:
            self.iCyl2minus = False
            self.cyl2.image.move_to_plus()
        if self.iCyl3minus and self.qCyl3toPlus:
            self.iCyl3minus = False
            self.cyl3.image.move_to_plus()
        if self.iCyl4minus and self.qCyl4toPlus:
            self.iCyl4minus = False
            self.cyl4.image.move_to_plus()
        # Move cylinder to the minus position.
        if self.iCyl1plus and self.qCyl1toMinus:
            self.iCyl1plus = False
            self.cyl1.image.move_to_minus()
        if self.iCyl2plus and self.qCyl2toMinus:
            self.iCyl2plus = False
            self.cyl2.image.move_to_minus()
        if self.iCyl3plus and self.qCyl3toMinus:
            self.iCyl3plus = False
            self.cyl3.image.move_to_minus()
        if self.iCyl4plus and self.qCyl4toMinus:
            self.iCyl4plus = False
            self.cyl4.image.move_to_minus()
        # Start motor.
        if self.mot1.image.state == 0 and self.qMot1start:
            self.mot1.image.state = -1
            self.mot1.image.turn_on()
        if self.mot2.image.state == 0 and self.qMot2start:
            self.mot2.image.state = -1
            self.mot2.image.turn_on()
        if self.mot3.image.state == 0 and self.qMot3start:
            self.mot3.image.state = -1
            self.mot3.image.turn_on()
        if self.mot4.image.state == 0 and self.qMot4start:
            self.mot4.image.state = -1
            self.mot4.image.turn_on()
        # Stop motor.
        if self.mot1.image.state == 1 and self.qMot1start == False:
            self.mot1.image.state = -1
            self.mot1.image.turn_off()
        if self.mot2.image.state == 1 and self.qMot2start == False:
            self.mot2.image.state = -1
            self.mot2.image.turn_off()
        if self.mot3.image.state == 1 and self.qMot3start == False:
            self.mot3.image.state = -1
            self.mot3.image.turn_off()
        if self.mot4.image.state == 1 and self.qMot4start == False:
            self.mot4.image.state = -1
            self.mot4.image.turn_off()

        self.after(10, self.dbread)

    def dbwrite(self):
        """Update sim inputs and write them to the data block on the PLC."""
        # Set the inputs of the cylinders.
        self.iCyl1minus = True if self.cyl1.image.xpos == CYL_XMIN else False
        self.iCyl2minus = True if self.cyl2.image.xpos == CYL_XMIN else False
        self.iCyl3minus = True if self.cyl3.image.xpos == CYL_XMIN else False
        self.iCyl4minus = True if self.cyl4.image.xpos == CYL_XMIN else False
        self.iCyl1plus = True if self.cyl1.image.xpos == CYL_XMAX else False
        self.iCyl2plus = True if self.cyl2.image.xpos == CYL_XMAX else False
        self.iCyl3plus = True if self.cyl3.image.xpos == CYL_XMAX else False
        self.iCyl4plus = True if self.cyl4.image.xpos == CYL_XMAX else False
        # Set the inputs of the motors.
        if self.mot1.image.state == 1:
            self.iMot1running = True
        elif self.mot1.image.state == 0:
            self.iMot1running = False
        if self.mot2.image.state == 1:
            self.iMot2running = True
        elif self.mot2.image.state == 0:
            self.iMot2running = False
        if self.mot3.image.state == 1:
            self.iMot3running = True
        elif self.mot3.image.state == 0:
            self.iMot3running = False
        if self.mot4.image.state == 1:
            self.iMot4running = True
        elif self.mot4.image.state == 0:
            self.iMot4running = False
        # Set the label texts.
        self.cyl1.io1.label1.configure(text=f" iCyl1minus = {self.iCyl1minus}")
        self.cyl2.io1.label1.configure(text=f" iCyl2minus = {self.iCyl2minus}")
        self.cyl3.io1.label1.configure(text=f" iCyl3minus = {self.iCyl3minus}")
        self.cyl4.io1.label1.configure(text=f" iCyl4minus = {self.iCyl4minus}")
        self.cyl1.io2.label1.configure(text=f" iCyl1plus = {self.iCyl1plus}")
        self.cyl2.io2.label1.configure(text=f" iCyl2plus = {self.iCyl2plus}")
        self.cyl3.io2.label1.configure(text=f" iCyl3plus = {self.iCyl3plus}")
        self.cyl4.io2.label1.configure(text=f" iCyl4plus = {self.iCyl4plus}")
        self.mot1.io.label1.configure(text=f" iMot1running = {self.iMot1running}")
        self.mot2.io.label1.configure(text=f" iMot2running = {self.iMot2running}")
        self.mot3.io.label1.configure(text=f" iMot3running = {self.iMot3running}")
        self.mot4.io.label1.configure(text=f" iMot4running = {self.iMot4running}")
        self.cyl1.io1.label2.configure(text=f" qCyl1toMinus = {self.qCyl1toMinus}")
        self.cyl2.io1.label2.configure(text=f" qCyl2toMinus = {self.qCyl2toMinus}")
        self.cyl3.io1.label2.configure(text=f" qCyl3toMinus = {self.qCyl3toMinus}")
        self.cyl4.io1.label2.configure(text=f" qCyl4toMinus = {self.qCyl4toMinus}")
        self.cyl1.io2.label2.configure(text=f" qCyl1toPlus = {self.qCyl1toPlus}")
        self.cyl2.io2.label2.configure(text=f" qCyl2toPlus = {self.qCyl2toPlus}")
        self.cyl3.io2.label2.configure(text=f" qCyl3toPlus = {self.qCyl3toPlus}")
        self.cyl4.io2.label2.configure(text=f" qCyl4toPlus = {self.qCyl4toPlus}")
        self.mot1.io.label2.configure(text=f" qMot1start = {self.qMot1start}")
        self.mot2.io.label2.configure(text=f" qMot2start = {self.qMot2start}")
        self.mot3.io.label2.configure(text=f" qMot3start = {self.qMot3start}")
        self.mot4.io.label2.configure(text=f" qMot4start = {self.qMot4start}")

        # Write inputs to the data block on the PLC.
        if self.plc.client.get_connected():
            data = bytearray([0b00000000, 0b00000000]) # 1 byte = 8 bits
            snap7.util.set_bool(data, 0, 0, self.iCyl1minus)
            snap7.util.set_bool(data, 0, 1, self.iCyl1plus)
            snap7.util.set_bool(data, 0, 2, self.iMot1running)
            snap7.util.set_bool(data, 0, 3, self.iCyl2minus)
            snap7.util.set_bool(data, 0, 4, self.iCyl2plus)
            snap7.util.set_bool(data, 0, 5, self.iMot2running)
            snap7.util.set_bool(data, 0, 6, self.iCyl3minus)
            snap7.util.set_bool(data, 0, 7, self.iCyl3plus)
            snap7.util.set_bool(data, 1, 0, self.iMot3running)
            snap7.util.set_bool(data, 1, 1, self.iCyl4minus)
            snap7.util.set_bool(data, 1, 2, self.iCyl4plus)
            snap7.util.set_bool(data, 1, 3, self.iMot4running)
            db_number = self.plc.dbi.get()
            self.plc.client.db_write(db_number, 0, data)

        self.after(20, self.dbwrite)


class Tabview(ctk.CTkTabview):
    """Tabs of the application."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=RESX, height=RESY)
        self.tab1 = self.add(name="PLC Config")
        self.tab2 = self.add(name="Simulation")
        self.set("Simulation")  # set visible tab


class App(ctk.CTk):
    """Main application."""
    def __init__(self):
        super().__init__()

        self.title("Simulator for Siemens Simatic S7-1500 PLCs")
        self.geometry(f"{RESX}x{RESY}")
        self.resizable(width=False, height=False)
        self.wm_iconbitmap(bitmap="seamk.ico")

        self.tabview = Tabview(self)
        self.tabview.grid(row=0, column=0)

        self.cfgtab = ConfigFrame(self.tabview.tab1)
        self.cfgtab.grid(row=0, column=0)

        self.simtab = SimulationFrame(self.tabview.tab2, self.cfgtab)
        self.simtab.grid(row=0, column=0)

        Thread(target=self.simtab.dbread).start()
        Thread(target=self.simtab.dbwrite).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
