import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import matplotlib.pyplot as plt
import time

distancia=10
def Distancia(mensaje):
 global distancia
 distancia=int(mensaje.data)
 print(distancia)

vel = Twist()
pubControl=rospy.Publisher('Control',Twist,queue_size=10)
rospy.init_node("CONTROLADOR",disable_signals=True, anonymous=True)
rospy.Subscriber('Distance',Int32,Distancia)
rate = rospy.Rate(10)
e=[0.1]
ref=0.2
Kp=0.4
Ki=0.4
Kd=0.4
t=[0]
tini=time.time()
i=-1
ts=0.05
u=[0]
while (distancia>4):
 dis=distancia
 if (dis<300):
  i=i+1
  error=dis/100-ref
  e.append(error)
  t.append(time.time()-tini)
  uc=Kp*error+Ki*sum(e)*ts+Kd*(error-e[i])
  u.append(uc)
  vel.linear.x=uc
  vel.angular.z=0
  pubControl.publish(vel)
  rate.sleep()
 pass
vel.linear.x=0
vel.angular.z=0
pubControl.publish(vel)

rospy.signal_shutdown('Fin')

fig1, ax2 = plt.subplots(figsize=(12, 6))
plt.plot(t,e,c='b', label='y1',linewidth=2)
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Error [m]', fontsize=12)
#plt.legend()
plt.grid()
plt.xlim([t[0], t[i]])
plt.ylim([min(e), max(e)])
#plt.show()
import os
os.remove("FigError1.png")
plt.savefig('FigError1.png',dpi=200)

fig2, ax2 = plt.subplots(figsize=(12, 6))
plt.plot(t,u,c='g', label='y2',linewidth=2)
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Velocity [m/s]', fontsize=12)
#plt.legend()
plt.grid()
plt.xlim([t[0], t[i]])
plt.ylim([min(u), max(u)])
#plt.show()
os.remove("Figu1.png")
plt.savefig('Figu1.png',dpi=200)