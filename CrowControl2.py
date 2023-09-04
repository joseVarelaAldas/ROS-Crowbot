import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool
import matplotlib.pyplot as plt
import time

boton=0
luz=[1000,1000]
def Luz(mensaje):
 global luz
 luz[0]=int(mensaje.data[0])
 luz[1]=int(mensaje.data[1])
 #print(luz)
def Boton(mensaje):
 global boton
 boton=int(mensaje.data)
 #print(boton)

vel = Twist()
pubControl=rospy.Publisher('Control',Twist,queue_size=10)
rospy.init_node("CONTROLADOR",disable_signals=True, anonymous=True)
rospy.Subscriber('Light',Int32MultiArray,Luz)
rospy.Subscriber('Button',Bool,Boton)
rate = rospy.Rate(10)
ey=[0.05]
Ey=[50]
Yref=0
Kw=2
t=[0]
tini=time.time()
i=-1
ts=0.05
Dt=[0]
w=[0]
print(luz)
while (boton==0):
 L=luz
 L[0]=(4095-L[0])/4095
 L[1]=(4095-L[1])/4095
 print(L)
 if (L[1]<4096):
  i=i+1
  Y=(L[0]-L[1])

  errorY=Yref-Y

  ey.append(errorY)
  Ey.append(errorY*100)
  t.append(time.time()-tini)
  dt=t[i]-t[i-1]
  Dt.append(dt)
  wc=Kw*errorY
  w.append(wc)
  vel.linear.x=0
  vel.angular.z=wc
  pubControl.publish(vel)
  rate.sleep()
 pass

vel.linear.x=0
vel.angular.z=0
pubControl.publish(vel)

rospy.signal_shutdown('Fin')

fig1, ax1 = plt.subplots(figsize=(12, 6))
plt.plot(t,Ey,c='r', label='e_y',linewidth=2)
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Error [%]', fontsize=12)
plt.grid()
plt.xlim([t[0], t[i]])
#plt.show()
import os
os.remove("FigError2.png")
plt.savefig('FigError2.png',dpi=200)

fig2, ax2 = plt.subplots(figsize=(12, 6))
plt.plot(t,w,c='g', label='w',linewidth=2)
plt.rc('xtick', labelsize=12) 
plt.rc('ytick', labelsize=12) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Angular Velocity [rad/s]', fontsize=12)
plt.grid()
plt.xlim([t[0], t[i]])
plt.ylim([min(w), max(w)])

os.remove("Figu2.png")
plt.savefig('Figu2.png',dpi=200)

fig3, ax3 = plt.subplots(figsize=(12, 6))
plt.plot(t,Dt,c='g', label='w',linewidth=2)
plt.rc('xtick', labelsize=12) 
plt.rc('ytick', labelsize=12) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Latency [sec.]', fontsize=12)
plt.grid()
plt.xlim([t[0], t[i]])
plt.ylim([min(Dt), max(Dt)])

os.remove("FigT.png")
plt.savefig('FigT.png',dpi=200)