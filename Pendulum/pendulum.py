import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

g=9.8
l=1
theta_0 = math.pi/4
omega_0 = 0
h = 0.02

time = np.arange(0,30,h)

theta = np.zeros(len(time))
omega = np.zeros(len(time))
theta[0] = theta_0
omega[0] = omega_0

for i in range (len(time)-1):
    theta[i+1] = theta[i] + (h*omega[i])
    omega[i+1] = omega[i] - (g*h/l)*math.sin(theta[i+1])

x = l*np.sin(theta)
y = -l*np.cos(theta)

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Simple Pendulum', artist='Saif',
                comment='Pendulum simulation')
writer = FFMpegWriter(fps=50, metadata=metadata)

fig,ax = plt.subplots()
ax.set_xlim(-1.2,1.2)
ax.set_ylim(-1.2,1.2)
ax.grid(True)
ax.set_aspect('equal')


red_circle, = ax.plot([], [], 'ro', markersize = 20)
blue_line, = ax.plot([], [], lw=2)

with writer.saving(fig, "Simple_Pendulum.mp4", 100):
    for i in range(len(time)):
        x0 = x[i]
        y0 = y[i]
        red_circle.set_data([x0], [y0])
        blue_line.set_data([0,x0],[0,y0])
        writer.grab_frame()