import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.patches as patches

#system parameters

#masses in Kg
m1 = 1
m2 = 2
m3 = 1.5

#Natural lengths in metres
L1 = 15
L2 = 20
L3 = 25


#Spring constants in N/m
k01 = 10
k12 = 15
k23 = 10

#User data sample
A = 50 #Initial displacement of m3 at t0s to start the oscillation


#FPS and step-size

fps_var = 20 #fps
simulation_end_time = 20 #seconds
h = 0.0005 #Step size

n_skip = int(1/(fps_var*h))

#Numerical Integration variables

time = np.arange(0,simulation_end_time,h)
x1 = np.zeros(len(time))
x2 = np.zeros(len(time))
x3 = np.zeros(len(time))

v1 = np.zeros(len(time))
v2 = np.zeros(len(time))
v3 = np.zeros(len(time))

a1 = np.zeros(len(time))
a2 = np.zeros(len(time))
a3 = np.zeros(len(time))

#Intial value problem

x1[0] = L1
x2[0] = L1 + L2
x3[0] = L1 + L2 + L3 + A

v1[0] = 0
v2[0] = 0
v3[0] = 0

#Kinetic energies

KE1 = np.zeros(len(time))
KE2 = np.zeros(len(time))
KE3 = np.zeros(len(time))

#Potential energies

U1 = np.zeros(len(time))
U2 = np.zeros(len(time))
U3 = np.zeros(len(time))

#Total Energy

TE = np.zeros(len(time))


#initial energy

KE1[0] = 0
KE2[0] = 0
KE3[0] = 0

U1[0] = 0
U2[0] = 0
U3[0] = 0.5*k23*(A**2)

TE[0] = U3[0]


#Visualisation
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Coupled spring mass', artist='Saif',
                comment='Coupled mass simulation')
writer = FFMpegWriter(fps=fps_var, metadata=metadata)

fig, ax = plt.subplots(figsize=(15, 4))
ax.set_xlim(0,100)
ax.set_ylim(0,5)
ax.set_aspect('equal')

s = 2 #Masses size 
y = s/2 #nela meeda unnam. y maaradu. half of box size at centre

mass1 = patches.Rectangle((0,0), s, s, color = 'red')
mass2 = patches.Rectangle((0,0), s, s, color = 'blue')
mass3 = patches.Rectangle((0,0), s, s, color = 'green')

ax.add_patch(mass1)
ax.add_patch(mass2)
ax.add_patch(mass3)

spring1, = ax.plot([], [], lw=2)
spring2, = ax.plot([], [], lw=2)
spring3, = ax.plot([], [], lw=2)


#Euler method

for i in range (len(time)-1):

    #Equations of motion for accelerations
    a1[i] = (-(k01 + k12)*x1[i] + k12*x2[i] + (-k12*L2 + k01*L1))/m1
    a2[i] = (k12*x1[i] + k23*x3[i] - (k12 + k23)*x2[i] - (k23*L3 - k12*L2))/m2
    a3[i] = (-k23*x3[i] + k23*x2[i] + k23*L3)/m3

    #Iterations
    v1[i+1] = v1[i] + h*a1[i]
    v2[i+1] = v2[i] + h*a2[i]
    v3[i+1] = v3[i] + h*a3[i]

    x1[i+1] = x1[i] + h*v1[i+1]
    x2[i+1] = x2[i] + h*v2[i+1]
    x3[i+1] = x3[i] + h*v3[i+1]




    #When masses collide with each other or the walls
    if (x2[i+1] - x1[i+1]) <= s and v1[i+1] - v2[i+1] > 0: 
        v1_old = v1[i+1]
        v2_old = v2[i+1]
        v1[i+1] = ((2*m2*v2_old) + v1_old*(m1-m2))/(m1+m2)
        v2[i+1] = ((2*m1*v1_old) + v2_old*(m2-m1))/(m1+m2)
        midpoint1 = (x2[i+1] + x1[i+1])/2 
        x1[i+1] = midpoint1 - s/2 + 0.001 #to avoid sticking due to numerical errors
        x2[i+1] = midpoint1 + s/2 + 0.001 #to avoid sticking due to numerical errors
    
    if (x3[i+1] - x2[i+1]) <= s and v2[i+1] - v3[i+1] > 0:
        v2_old = v2[i+1]
        v3_old = v3[i+1]
        v2[i+1] = ((2*m3*v3_old) + v2_old*(m2-m3))/(m2+m3)
        v3[i+1] = ((2*m2*v2_old) + v3_old*(m3-m2))/(m2+m3)
        midpoint2 = (x3[i+1] + x2[i+1])/2
        x2[i+1] = midpoint2 - s/2 + 0.001 #to avoid sticking due to numerical errors
        x3[i+1] = midpoint2 + s/2 + 0.001 #to avoid sticking due to numerical errors


    #Elastic collision with rigid wall. reverse velocity
    if x1[i+1] < s/2:
        v1[i+1] = -v1[i+1]
        x1[i+1] = s/2 + (s/2 - x1[i+1]) #reflect position

    KE1[i+1] = 0.5*m1*(v1[i+1]**2)
    KE2[i+1] = 0.5*m2*(v2[i+1]**2)
    KE3[i+1] = 0.5*m3*(v3[i+1]**2)

    U1[i+1] = 0.5*k01*((L1 - x1[i+1])**2)
    U2[i+1] = 0.5*k12*((x2[i+1] - x1[i+1] - L2)**2)
    U3[i+1] = 0.5*k23*((x3[i+1] - x2[i+1] - L3)**2)

    TE[i+1] = KE1[i+1] + KE2[i+1] + KE3[i+1] + U1[i+1] + U2[i+1] + U3[i+1]


# Energy plots

plt.figure(figsize=(12, 6))


plt.plot(time, TE, 'k-', lw=3, label='Total Energy')


plt.plot(time, KE1, 'r-o', markevery=100, label='m1 KE (Red)')
plt.plot(time, KE2, 'b-s', markevery=100, label='m2 KE (Blue)')
plt.plot(time, KE3, 'g-^', markevery=100, label='m3 KE (Green)')


plt.plot(time, U1, 'r--', alpha=0.6, label='Spring1 PE')
plt.plot(time, U2, 'b--', alpha=0.6, label='Spring2 PE')
plt.plot(time, U3, 'g--', alpha=0.6, label='Spring3 PE')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

plt.title("System Energy Analysis")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


#Animation
with writer.saving(fig, "Coupled_spring_mass.mp4", 100):
    for i in range(0, len(time), n_skip):
        x10 = x1[i]
        x20 = x2[i]
        x30 = x3[i]
        mass1.set_xy((x10 - (s/2) , 0))
        mass2.set_xy((x20 - (s/2) , 0))
        mass3.set_xy((x30 - (s/2) , 0))
        spring1.set_data([0, x10-(s/2)],[s/2,s/2])
        spring2.set_data([x10+(s/2), x20-(s/2)],[s/2,s/2])
        spring3.set_data([x20+(s/2), x30-(s/2)],[s/2,s/2])
        writer.grab_frame()