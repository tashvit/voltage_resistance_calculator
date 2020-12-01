# Program to determine closest resistor values


# Import tkinter module
import tkinter as tk
from tkinter import ttk

# Creating main tkinter window/top level
master = tk.Tk()

# Creating label widgets
label_1 = tk.Label(master, text="Calculate Resistor Value Combinations (R2 and R1)")
label_2 = ttk.Label(master, text="Voltage In (V):")
label_3 = ttk.Label(master, text="Expected Voltage Out (V):")
label_4 = ttk.Label(master, text="Threshold (V): ")

# Grid method to arrange labels in respective rows and columns
label_1.grid(row=0, column=0, pady=5, columnspan=4)
label_2.grid(row=1, column=0, pady=2)
label_3.grid(row=2, column=0, pady=2)
label_4.grid(row=3, column=0, pady=2)

# Creating entry widgets
entry_1 = ttk.Entry(master)
entry_2 = ttk.Entry(master)
entry_3 = ttk.Entry(master)

# Arranging entry widgets
entry_1.grid(row=1, column=1, pady=2)
entry_2.grid(row=2, column=1, pady=2)
entry_3.grid(row=3, column=1, pady=2)

# Adding image
img = tk.PhotoImage(file="new_voltage_image.png")
img1 = img.subsample(1, 1)

# Using label to set image
tk.Label(master, image=img1).grid(row=5, column=0, columnspan=4, rowspan=4, padx=5, pady=5)

# Label widget
label_5 = ttk.Label(master, text="R2 : Possible value for Resistor 2 (Ohms)\n"
                                 "R1 : Possible value for Resistor 1 (Ohms)\n"
                                 "V Out : Actual voltage output (Volts)\n"
                                 "Difference : Difference between expected voltage output and V Out (Volts)")
label_5.grid(row=11, column=0, pady=2, columnspan=4, rowspan=4)

# Creating frame and canvas for table
scroll_canvas = tk.Canvas(master, borderwidth=0, background="#ffffff")
scroll_frame = tk.Frame(scroll_canvas, background="#ffffff")
vertical_scroll_bar = tk.Scrollbar(master, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=vertical_scroll_bar.set)

vertical_scroll_bar.grid(row=16, column=5, sticky="nse")
scroll_canvas.grid(row=16, column=0, columnspan=4)
scroll_canvas.create_window((5, 5), window=scroll_frame, anchor="nw")

scroll_frame.bind("<Configure>", lambda event, canvas=scroll_canvas: on_frame_configure(canvas))

# Adding calculate button widget
button = ttk.Button(master, text="Calculate", command=lambda: populate(scroll_frame))
button.grid(row=4, column=2)


# Functions
def calculate_voltage(r2, r1, v_in):
    """Function to calculate voltage"""
    v_out = (r2 / (r1 + r2)) * v_in
    return v_out


def calculate_resistors(expected_voltage, voltage_in, threshold=0.01):
    """Calculate closest resistor1 and resistor2 values"""
    r2_r1_values = []
    for r2 in range(100, 10001, 100):
        for r1 in range(100, 10001, 100):
            voltage_out = calculate_voltage(r2, r1, voltage_in)
            if abs(voltage_out - expected_voltage) <= threshold:
                r2_r1_values.append((str(r2), str(r1), str(round(voltage_out, 10)),
                                     str(round(abs(voltage_out - expected_voltage), 10))))
    # Sorting list of tuples by voltage difference
    r2_r1_values.sort(key=lambda tup: tup[3])
    return r2_r1_values


def create_table_list():
    """Create list to be added to table"""
    resistors_list = calculate_resistors(float(entry_2.get()),
                                         float(entry_1.get()), float(entry_3.get()))
    table_list = [("R2", "R1", "V Out", "Difference")] + resistors_list
    return table_list


def populate(my_frame):
    """Create frame embedded in canvas to hold table"""
    table_list = create_table_list()
    for row in range(len(table_list)):
        for column in range(len(table_list[0])):
            tk.Label(my_frame, text=table_list[row][column], width=13, borderwidth="1",
                     relief="solid").grid(row=row, column=column)


def on_frame_configure(my_canvas):
    """Reset scroll region to encompass inner frame"""
    my_canvas.configure(scrollregion=scroll_canvas.bbox("all"))


def load_sample():
    """Showcase example table"""
    entry_1.insert(0, "9")
    entry_2.insert(0, "5")
    entry_3.insert(0, "0.01")
    populate(scroll_frame)


if __name__ == "__main__":
    load_sample()
    tk.mainloop()
