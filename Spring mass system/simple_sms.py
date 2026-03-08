import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Simulation Constants

g = 9.8
h = 0.01



# dict to store postion and velocity    


system_params = {
    "l":1, "k":1, "m":1, "x":1, "v":0
}


#Visu constants

block_size = 0.1*system_params["l"]

#Fields dict for entry boxes

fields = [
    ("l", "Natural length of Spring (m)", 1,0),
    ("k", "Spring constant (N/m)", 1,1),
    ("m", "mass of body (m)", 3,0),
    ("x", "Initial position (m)", 3,1),
    ("v", "Initial velocity (m/s)", 5,0)
]


#Defining frame


root = tk.Tk()
root.title("Spring Mass system")
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
canvas_widget.grid(row=0, column=2, rowspan = 10, columnspan=10, sticky="nsew")
frame.columnconfigure(1, weight=1)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 0.5)
ax.set_aspect('equal')


#Methods

def submit_values():
    try:
        for field_name, entry_box in entry_boxes.items():
            val = float(entry_box.get())
            system_params[field_name] = val
                
    except Exception:
        print("Please enter valid numerical values.")
        return False
    
    if system_params["m"] <= 0:
        print("Mass must be positive.")
        return False
    
    if system_params["k"] <= 0:
        print("Spring constant must be positive.")
        return False
    
    if system_params["l"] <= 0:
        print("Natural length must be positive.")
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

    system_params["v"] = system_params["v"] + (system_params["k"]*h/system_params["m"])*(system_params["l"]-system_params["x"])
    system_params["x"] = system_params["x"] + h*system_params["v"]

def update(frame):

    evaluate()
    body.center = (system_params["x"], 0)
    line.set_data([0, system_params["x"]], [0, 0])
    return body, line

def start_simulation():    

    if submit_values():
        body.center = (system_params["x"], 0)
        line.set_data([0, system_params["x"]], [0, 0])

        max_reach = max(system_params["l"], system_params["x"])
        amplitude = abs(system_params["x"] - system_params["l"])
        limit_max = max_reach + amplitude + (block_size * 2)
        
        ax.set_xlim(-limit_max, limit_max)
        ax.set_ylim(-limit_max/2, limit_max/2)
        body.set_radius(0.15*limit_max)

def run_animation():
    global anim
    if 'anim' in globals() and anim is not None:
        anim.event_source.stop()  # Stop the previous animation if it exists
    anim = manimation.FuncAnimation(fig, update, frames=None, interval = 10, blit=True, cache_frame_data=False)
    canvas.draw()




body = patches.Circle((system_params["x"], 0), 0, color='blue')
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