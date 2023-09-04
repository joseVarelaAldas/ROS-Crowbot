import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
import matplotlib.pyplot as plt
import time

distancia=10
luz=[0,0]
def Distancia(mensaje):
 global distancia
 distancia=int(mensaje.data)
 #print(distancia)

def Luz(mensaje):
 global luz
 luz[0]=int(mensaje.data[0])
 luz[1]=int(mensaje.data[1])
 print(luz)

rospy.init_node("CONTROLADOR",disable_signals=True, anonymous=True)
rospy.Subscriber('Distance',Int32,Distancia)
rospy.Subscriber('Light',Int32MultiArray,Luz)
rate = rospy.Rate(10)
d1=[]
d2=[]
t=[]
tini=time.time()
i=-1
while (distancia>4):
 
 if (distancia<300):
    t.append(time.time()-tini)
    d1.append(luz[0])
    d2.append(luz[1])
    i=i+1
 rate.sleep()
 pass
rospy.signal_shutdown('Fin')
fig, ax = plt.subplots(figsize=(12, 6))
plt.plot(t,d1,c='b', label='L1',linewidth=2)
plt.plot(t,d2,c='r', label='L2',linewidth=2)
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('Light Data', fontsize=12)
plt.legend()
plt.grid()
plt.xlim([t[0], t[i]])
#plt.ylim([0, max(d)])
#plt.show()
import os
os.remove("FigLight.png")
plt.savefig('FigLight.png',dpi=200)
