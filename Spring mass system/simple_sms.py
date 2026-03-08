import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patches as patches

L = 6 #natural legnth of the spring in metres
A = 3 #amplitude of vibration in metres
k = 20 #spring constant in N/m
s = 2 #size of the block


h = 0.02 #time step
time_array = np.arange(0,10,h) #10s simulation time
x = np.zeros(len(time_array))
v = np.zeros(len(time_array))
y = s/2
m = 1 #mass in kg

x[0] = A + L
v[0] = 0

for i in range (len(time_array)-1):
    v[i+1] = v[i] + (k*h/m)*(L-x[i])
    x[i+1] = x[i] + h*v[i+1]

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Simple spring mass', artist='Saif',
                comment='Spring mass simulation')
writer = FFMpegWriter(fps=50, metadata=metadata)

fig,ax = plt.subplots()
ax.set_xlim(0,12)
ax.set_ylim(0,8)
ax.set_aspect('equal')

red_box = patches.Rectangle((0,0), s, s, color = 'red')
ax.add_patch(red_box)
blue_line, = ax.plot([], [], lw=2)

with writer.saving(fig, "Simple_spring_mass.mp4", 50):
    for i in range(len(time_array)):
        x0 = x[i]
        red_box.set_xy((x0 - (s/2) , 0))
        blue_line.set_data([0, x0-(s/2)],[s/2,s/2])
        writer.grab_frame()


