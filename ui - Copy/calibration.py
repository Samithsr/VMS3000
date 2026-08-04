import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time
import threading
from datetime import datetime

class CalibrationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calibration")
        self.root.geometry("1320x900")
        self.root.resizable(False, False)
        
        self.ser = None
        self.is_connected = False
        self.current_slave_id = 15
        self.current_baud = 115200
        
        self.setup_ui()
        self.load_com_ports()

    def setup_ui(self):
        # ==================== CONNECTION FRAME ====================
        conn_frame = tk.LabelFrame(self.root, text="Connection", font=("MS Sans Serif", 10, "bold"))
        conn_frame.place(x=1040, y=570, width=210, height=250)

        tk.Label(conn_frame, text="Slave Id", font=("MS Sans Serif", 8, "bold")).place(x=10, y=30)
        self.module_Address_Cmbox = ttk.Combobox(conn_frame, values=[str(i) for i in range(1, 32)], width=8)
        self.module_Address_Cmbox.set("15")
        self.module_Address_Cmbox.place(x=100, y=30)

        tk.Label(conn_frame, text="Com Port", font=("MS Sans Serif", 8, "bold")).place(x=10, y=70)
        self.COM_Port_Cmbox = ttk.Combobox(conn_frame, width=8)
        self.COM_Port_Cmbox.place(x=100, y=70)

        tk.Label(conn_frame, text="Baud Rate", font=("MS Sans Serif", 8, "bold")).place(x=10, y=110)
        self.Baud_Rate_Cmbox = ttk.Combobox(conn_frame, values=["9600", "19200", "38400", "57600", "115200"], width=8)
        self.Baud_Rate_Cmbox.set("115200")
        self.Baud_Rate_Cmbox.place(x=100, y=110)

        self.connect_btn = tk.Button(conn_frame, text="Connect", font=("MS Sans Serif", 9, "bold"), 
                                   bg="#421F00", fg="white", command=self.connect_device)
        self.connect_btn.place(x=45, y=150, width=120, height=35)

        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect", font=("MS Sans Serif", 9, "bold"), 
                                      bg="#421F00", fg="white", command=self.disconnect_device, state="disabled")
        self.disconnect_btn.place(x=45, y=195, width=120, height=35)

        # ==================== DATE TIME FRAME ====================
        dt_frame = tk.Frame(self.root)
        dt_frame.place(x=670, y=760, width=370, height=70)

        tk.Button(dt_frame, text="SET DATE-TIME", font=("MS Sans Serif", 9, "bold"), 
                 bg="#421F00", fg="white", command=self.set_date_time).pack(pady=15, padx=10, side="left")
        
        tk.Button(dt_frame, text="Exit", font=("MS Sans Serif", 9, "bold"), 
                 bg="#421F00", fg="white", command=self.root.quit).pack(pady=15, padx=10, side="left")

        # ==================== GAIN SECTIONS ====================
        self.gain_var = tk.IntVar(value=1)
        
        # Gain -1
        self.create_gain_section(1, "Gain -1", 10, 10)
        # Gain -2
        self.create_gain_section(2, "Gain -2", 10, 290)
        # Gain (CH Gain)
        self.create_gain_section(3, "Gain", 10, 570)

    def create_gain_section(self, gain_num, title, x, y):
        frame = tk.LabelFrame(self.root, text=title, font=("MS Sans Serif", 13), 
                            height=260, width=1230)
        frame.place(x=x, y=y)

        # Present Gain
        present_frame = tk.LabelFrame(frame, text="Present Gain", font=("MS Sans Serif", 10, "bold"))
        present_frame.place(x=20, y=30, width=280, height=160)
        
        self.present_gains = []
        for i in range(4):
            tk.Label(present_frame, text=f"CH{i+1} GAIN{gain_num}", 
                    font=("MS Sans Serif", 8, "bold")).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(present_frame, width=12, justify="center", font=("MS Sans Serif", 9, "bold"))
            entry.insert(0, "0.0")
            entry.config(state="readonly")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.present_gains.append(entry)

        # Calculated Gain
        calc_frame = tk.LabelFrame(frame, text="Calculated Gain", font=("MS Sans Serif", 10, "bold"))
        calc_frame.place(x=320, y=30, width=300, height=160)
        
        self.calc_gains = []
        self.check_vars = []
        for i in range(4):
            tk.Label(calc_frame, text=f"CH{i+1} GAIN{gain_num}", 
                    font=("MS Sans Serif", 8, "bold")).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(calc_frame, width=12, justify="center", font=("MS Sans Serif", 9, "bold"))
            entry.insert(0, "0.0")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.calc_gains.append(entry)
            
            var = tk.BooleanVar()
            chk = tk.Checkbutton(calc_frame, variable=var)
            chk.grid(row=i, column=2)
            self.check_vars.append(var)

        # Read Value
        read_frame = tk.LabelFrame(frame, text="Read Value", font=("MS Sans Serif", 10, "bold"))
        read_frame.place(x=640, y=30, width=150, height=170)
        
        self.read_values = []
        for i in range(4):
            entry = tk.Entry(read_frame, width=10, justify="center", font=("MS Sans Serif", 9, "bold"))
            entry.insert(0, "0.0")
            entry.config(state="readonly")
            entry.grid(row=i, column=0, padx=10, pady=8)
            self.read_values.append(entry)
        
        tk.Label(read_frame, text="Mills", font=("MS Sans Serif", 8, "bold")).grid(row=4, column=0, pady=5)

        # Actual Values
        actual_frame = tk.LabelFrame(frame, text="Actual Values", font=("MS Sans Serif", 10, "bold"))
        actual_frame.place(x=810, y=30, width=390, height=170)
        
        # Vrms and Mills columns
        tk.Label(actual_frame, text="In Mills", font=("MS Sans Serif", 8, "bold")).grid(row=0, column=0, columnspan=2)
        tk.Label(actual_frame, text="Vrms In Volts", font=("MS Sans Serif", 8, "bold")).grid(row=0, column=2, columnspan=2)
        
        self.actual_mills = []
        self.actual_vrms = []
        
        for i in range(4):
            # Mills
            entry_m = tk.Entry(actual_frame, width=12, justify="center", font=("MS Sans Serif", 9, "bold"))
            entry_m.insert(0, "0.0")
            entry_m.grid(row=i+1, column=0, padx=5, pady=3)
            self.actual_mills.append(entry_m)
            
            # Vrms
            entry_v = tk.Entry(actual_frame, width=12, justify="center", font=("MS Sans Serif", 9, "bold"))
            entry_v.insert(0, "0.0")
            entry_v.grid(row=i+1, column=2, padx=5, pady=3)
            self.actual_vrms.append(entry_v)

        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.place(x=320, y=200)

        tk.Button(btn_frame, text="Calculate", font=("MS Sans Serif", 9, "bold"), 
                 bg="#421F00", fg="white", width=12, command=lambda g=gain_num: self.calculate_gain(g)).pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="Write", font=("MS Sans Serif", 9, "bold"), 
                 bg="#421F00", fg="white", width=12, command=lambda g=gain_num: self.write_gain(g)).pack(side="left", padx=10)

    def load_com_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.COM_Port_Cmbox['values'] = ports
        if ports:
            self.COM_Port_Cmbox.set(ports[0])

    def connect_device(self):
        if self.is_connected:
            return
            
        try:
            port = self.COM_Port_Cmbox.get()
            baud = int(self.Baud_Rate_Cmbox.get())
            slave = int(self.module_Address_Cmbox.get())
            
            self.ser = serial.Serial(port, baud, timeout=1)
            self.current_slave_id = slave
            self.is_connected = True
            
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            messagebox.showinfo("Success", f"Connected to {port} at {baud} baud")
            
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def disconnect_device(self):
        if self.ser:
            self.ser.close()
        self.is_connected = False
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")

    def set_date_time(self):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect first")
            return
        # Send date time command (placeholder)
        dt = datetime.now()
        messagebox.showinfo("Date Time", f"Set to: {dt.strftime('%Y-%m-%d %H:%M:%S')}")

    def calculate_gain(self, gain_num):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect device first")
            return
            
        try:
            # Read values from actual mills
            for i in range(4):
                mills = float(self.actual_mills[i].get() or 0)
                vrms = float(self.actual_vrms[i].get() or 0)
                
                if vrms != 0:
                    gain = mills / vrms
                    self.calc_gains[i*3 + (gain_num-1)].delete(0, tk.END)  # Simplified indexing
                    self.calc_gains[i*3 + (gain_num-1)].insert(0, f"{gain:.4f}")
        except Exception as e:
            messagebox.showerror("Calculate Error", str(e))

    def write_gain(self, gain_num):
        if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect device first")
            return
            
        try:
            for i in range(4):
                if self.check_vars[i].get():
                    gain_val = float(self.calc_gains[i*3 + (gain_num-1)].get() or 0)
                    # TODO: Send Modbus/Protocol command to write gain
                    print(f"Writing CH{i+1} Gain{gain_num}: {gain_val}")
            
            messagebox.showinfo("Success", f"Gain {gain_num} values written successfully")
        except Exception as e:
            messagebox.showerror("Write Error", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CalibrationApp()
    app.run()