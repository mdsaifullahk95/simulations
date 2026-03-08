import tkinter as tk
import math
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#Simulation Constants

g=9.8
h = 0.01


#Current state dict to store positions

current_state = {
    "l":1, "Q":0, "w": 0
}


#Defining frame


root = tk.Tk()
root.title("Simple Pendulum")
root.geometry("800x1000")

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight =1)

frame = tk. Frame(root)
frame.grid(row=0, column=0, sticky = "nsew")

#Livesim widget

fig, ax = plt.subplots(figsize=(5, 5))
ax.set_facecolor('black')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=1, rowspan = 10, columnspan=10, sticky="nsew")
frame.columnconfigure(1, weight=1)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 0.5)
ax.set_aspect('equal')





#methods

def submit_values():
    try:
        for field_name, entry_box in entry_boxes.items():
            val = float(entry_box.get())
            current_state[field_name] = val
    except Exception:
        print("Please enter valid numerical values.")
        return False
    
    if current_state["l"] <= 0:
        print("Length must be positive.")
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

def evaluate():

    l = current_state["l"]

    current_state["Q"] = current_state["Q"] + (h*current_state["w"])
    current_state["w"] = current_state["w"] - (g*h/l)*math.sin(current_state["Q"])



def update(frame):

    l = current_state["l"]

    evaluate()
    body.center = (l*np.sin(current_state["Q"]), -l*np.cos(current_state["Q"]))
    line.set_data([0, l*np.sin(current_state["Q"])], [0, -l*np.cos(current_state["Q"])])
    return body, line

def start_simulation():

    

    if submit_values():
        l = current_state["l"]
        body.center = (l*np.sin(current_state["Q"]), -l*np.cos(current_state["Q"]))
        line.set_data([0, l*np.sin(current_state["Q"])], [0, -l*np.cos(current_state["Q"])])
        limits = l*1.2
        body.set_radius(0.15*limits)
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)


def run_animation():
    global anim
    if 'anim' in globals() and anim is not None:
        anim.event_source.stop()  # Stop the previous animation if it exists
    anim = manimation.FuncAnimation(fig, update, frames=None, interval = 10, blit=True, cache_frame_data=False)
    canvas.draw()


#Creating boxes and labels

fields = [
    ("l", "length of pendulum (m)", 1,0),
    ("Q", "Angle with vertical (rad)", 3,0),
    ("w", "Initial velocity (rad/s)", 5,0),
]

body = patches.Circle((current_state["l"]*np.sin(current_state["Q"]), -current_state["l"]*np.cos(current_state["Q"])), 0, color='blue')
ax.add_patch(body)

line, = ax.plot([], [], lw=2)

entry_boxes = {}
for field_name, placeholder, row, col in fields:

    label = tk.Label(frame, text=f"{placeholder}:")
    label.grid(row = row -1, column = col, padx = 1, pady = 10)



    entry_box = tk.Entry(frame, fg='grey')
    entry_box.insert(0, placeholder)
    entry_box.grid(row=row, column=col, padx=10, pady=10)
    entry_box.bind('<FocusIn>', lambda event, ent = entry_box, ph=placeholder: on_entry_click(event, ent, ph))
    entry_box.bind('<FocusOut>', lambda event, ent = entry_box, ph=placeholder: on_focusout(event, ent, ph))

    entry_boxes[field_name] = entry_box


submit = tk.Button(frame, text="Start Simulation", command=lambda: [start_simulation(), run_animation()])
submit.grid(row=6, column=0, pady=20)



root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy(), exit()))

root.mainloop()