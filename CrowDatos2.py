import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import Bool
import matplotlib.pyplot as plt
import time

distancia=10
boton=0
def Distancia(mensaje):
 global distancia
 distancia=int(mensaje.data)
 #print(distancia)

def Boton(mensaje):
 global boton
 boton=int(mensaje.data)
 print(boton)

rospy.init_node("CONTROLADOR",disable_signals=True, anonymous=True)
rospy.Subscriber('Distance',Int32,Distancia)
rospy.Subscriber('Button',Bool,Boton)
rate = rospy.Rate(10)
d=[]
t=[]
tini=time.time()
i=-1
while (distancia>4):
 
 if (distancia<300):
    t.append(time.time()-tini)
    d.append(boton)
    i=i+1
 rate.sleep()
 pass

rospy.signal_shutdown('Fin')

fig, ax = plt.subplots(figsize=(12, 6))
plt.plot(t,d,c='b', label='y1',linewidth=2)
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 
plt.xlabel('Time [sec.]', fontsize=12)
plt.ylabel('State Button', fontsize=12)
#plt.legend()
plt.grid()
plt.xlim([t[0], t[i]])
plt.ylim([0, max(d)])
#plt.show()
import os
os.remove("FigButton.png")
plt.savefig('FigButton.png',dpi=200)
