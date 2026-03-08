import tkinter as tk
from simpleeval import simple_eval
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#Creating the frame
root = tk.Tk()
root.title("Two body simualation")
root.geometry("800x1000")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

def submit_values():
    try:
        for field_name, entry_box in entry_boxes.items():
            val = float(simple_eval(entry_box.get()))
            current_state[field_name] = val
    except Exception:
        print("Please enter valid numerical values.")
        return False
    
    if current_state["m1"] <= 0 or current_state["m2"] <= 0:
        print("Masses must be positive.")
        return False
    elif current_state["simspeed"] <= 0:
        print("Simulation speed must be positive.")
        return False
    elif current_state["xpos1"] == current_state["xpos2"] and current_state["ypos1"] == current_state["ypos2"]:
        print("Initial positions cannot be the same.")
        return False
    else:
        return True
    


def on_entry_click(event,entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.insert(0, '')
        entry.config(fg='black') # Change text to black when typing

def on_focusout(event, entry, placeholder):
    """Function that restores placeholder if box is left empty"""
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')


fields = [
    ("m1", "Mass of body 1 (kg)", 0, 0),
    ("m2", "Mass of body 2 (kg)", 0, 1),
    ("xvel1", "Initial x-velocity of body 1 (m/s)", 1, 0),
    ("yvel1", "Initial y-velocity of body 1 (m/s)", 2, 0),
    ("xvel2", "Initial x-velocity of body 2 (m/s)", 1, 1),
    ("yvel2", "Initial y-velocity of body 2 (m/s)", 2, 1),
    ("xpos1", "Initial x-position of body 1 (m)", 3, 0),
    ("ypos1", "Initial y-position of body 1 (m)", 4, 0),
    ("xpos2", "Initial x-position of body 2 (m)", 3, 1),
    ("ypos2", "Initial y-position of body 2 (m)", 4, 1),
    ("simspeed", "Simulation speed (real seconds per simulation second)", 5, 0) 
]

entry_boxes = {}
for field_name, placeholder, row, col in fields:
    entry_box = tk.Entry(frame, fg='grey')
    entry_box.insert(0, placeholder)
    entry_box.grid(row=row, column=col, padx=10, pady=10)
    entry_box.bind('<FocusIn>', lambda event, ent = entry_box, ph=placeholder: on_entry_click(event, ent, ph))
    entry_box.bind('<FocusOut>', lambda event, ent = entry_box, ph=placeholder: on_focusout(event, ent, ph))

    entry_boxes[field_name] = entry_box



fig, ax = plt.subplots(figsize=(5, 5))
ax.set_facecolor('black')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=2, rowspan = 10, columnspan=10, sticky="nsew")


G = 6.67430e-11
h = 10 #Euler-Cromer time step in seconds

current_state = {
    "m1" : 0, "m2" : 0, "xvel1" : 0, "yvel1" : 0, "xvel2" : 0, "yvel2" : 0,
    "xpos1" : 0, "ypos1" : 0, "xpos2" : 0, "ypos2" : 0
} 

def Euler_Cromer():
    acc1_x = G*current_state["m2"]*(current_state["xpos2"] - current_state["xpos1"])/((current_state["xpos2"] - current_state["xpos1"])**2 + (current_state["ypos2"] - current_state["ypos1"])**2)**(3/2)
    acc1_y = G*current_state["m2"]*(current_state["ypos2"] - current_state["ypos1"])/((current_state["xpos2"] - current_state["xpos1"])**2 + (current_state["ypos2"] - current_state["ypos1"])**2)**(3/2)
    acc2_x = G*current_state["m1"]*(current_state["xpos1"] - current_state["xpos2"])/((current_state["xpos2"] - current_state["xpos1"])**2 + (current_state["ypos2"] - current_state["ypos1"])**2)**(3/2)
    acc2_y = G*current_state["m1"]*(current_state["ypos1"] - current_state["ypos2"])/((current_state["xpos2"] - current_state["xpos1"])**2 + (current_state["ypos2"] - current_state["ypos1"])**2)**(3/2)

    current_state["xvel1"] += acc1_x*h
    current_state["yvel1"] += acc1_y*h
    current_state["xvel2"] += acc2_x*h
    current_state["yvel2"] += acc2_y*h

    current_state["xpos1"] += current_state["xvel1"]*h
    current_state["ypos1"] += current_state["yvel1"]*h
    current_state["xpos2"] += current_state["xvel2"]*h
    current_state["ypos2"] += current_state["yvel2"]*h


def start_simulation():
    if submit_values():
        body1.center = (current_state["xpos1"], current_state["ypos1"])
        body2.center = (current_state["xpos2"], current_state["ypos2"])
        dist = np.sqrt((current_state["xpos2"] - current_state["xpos1"])**2 + (current_state["ypos2"] - current_state["ypos1"])**2)
        global limits
        limits = dist*1.5
        body1.set_radius(0.03*limits)
        body2.set_radius(0.03*limits)
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)



body1 = patches.Circle((current_state["xpos1"], current_state["ypos1"]), 0, color='blue')
body2 = patches.Circle((current_state["xpos2"], current_state["ypos2"]), 0, color='red')
ax.add_patch(body1)
ax.add_patch(body2)

def update(frame):

    for _ in range(int(current_state["simspeed"])):
        Euler_Cromer()
    body1.center = (current_state["xpos1"], current_state["ypos1"])
    body2.center = (current_state["xpos2"], current_state["ypos2"])
    return body1, body2

def run_animation():
    global anim
    if 'anim' in globals() and anim is not None:
        anim.event_source.stop()  # Stop the previous animation if it exists
    anim = manimation.FuncAnimation(fig, update, frames=None, interval = 20, blit=True, cache_frame_data=False)
    canvas.draw()


submit = tk.Button(frame, text="Start Simulation", command=lambda: [start_simulation(), run_animation()])
submit.grid(row=6, column=0, columnspan=2, pady=20)

sun_earth_template_button = tk.Button(frame, text="Sun-Earth Template", command=lambda: [entry_boxes["m1"].delete(0, tk.END), entry_boxes["m1"].insert(0, "1.989e30"), entry_boxes["m2"].delete(0, tk.END), entry_boxes["m2"].insert(0, "5.972e24"), entry_boxes["xvel1"].delete(0, tk.END), entry_boxes["xvel1"].insert(0, "0"), entry_boxes["yvel1"].delete(0, tk.END), entry_boxes["yvel1"].insert(0, "0"), entry_boxes["xvel2"].delete(0, tk.END), entry_boxes["xvel2"].insert(0, "0"), entry_boxes["yvel2"].delete(0, tk.END), entry_boxes["yvel2"].insert(0, "29780"), entry_boxes["xpos1"].delete(0, tk.END), entry_boxes["xpos1"].insert(0, "0"), entry_boxes["ypos1"].delete(0, tk.END), entry_boxes["ypos1"].insert(0, "0"), entry_boxes["xpos2"].delete(0, tk.END), entry_boxes["xpos2"].insert(0, "149600000000"), entry_boxes["ypos2"].delete(0, tk.END), entry_boxes["ypos2"].insert(0, "0")])
sun_earth_template_button.grid(row=7, column=0, columnspan=2, pady=10)

earth_moon_template_button = tk.Button(frame, text="Earth-Moon Template", command=lambda: [entry_boxes["m1"].delete(0, tk.END), entry_boxes["m1"].insert(0, "5.972e24"), entry_boxes["m2"].delete(0, tk.END), entry_boxes["m2"].insert(0, "7.348e22"), entry_boxes["xvel1"].delete(0, tk.END), entry_boxes["xvel1"].insert(0, "0"), entry_boxes["yvel1"].delete(0, tk.END), entry_boxes["yvel1"].insert(0, "0"), entry_boxes["xvel2"].delete(0, tk.END), entry_boxes["xvel2"].insert(0, "0"), entry_boxes["yvel2"].delete(0, tk.END), entry_boxes["yvel2"].insert(0, "1022"), entry_boxes["xpos1"].delete(0, tk.END), entry_boxes["xpos1"].insert(0, "0"), entry_boxes["ypos1"].delete(0, tk.END), entry_boxes["ypos1"].insert(0, "0"), entry_boxes["xpos2"].delete(0, tk.END), entry_boxes["xpos2"].insert(0, "384400000"), entry_boxes["ypos2"].delete(0, tk.END), entry_boxes["ypos2"].insert(0, "0")])
earth_moon_template_button.grid(row=8, column=0, columnspan=2, pady=10)


root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy(), exit()))

root.mainloop()