#include <ToneESP32.h>
#include <WiFi.h>
#include <FastLED.h>
#include <ros.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int32MultiArray.h>

const char* ssid     = "docentes";
const char* password = "do2022asd*";
// Set the rosserial socket server IP address
IPAddress server(172,18,16,19);
// Set the rosserial socket server port
const uint16_t serverPort = 11411;

ros::NodeHandle nh;
std_msgs::Int32 distance_msg;
std_msgs::Bool button_msg;
std_msgs::Int32MultiArray light_msg;
std_msgs::Int32MultiArray line_msg;

ros::Publisher chatter1("Distance", &distance_msg);
ros::Publisher chatter2("Button", &button_msg);
ros::Publisher chatter3("Light", &light_msg);
ros::Publisher chatter4("Line", &line_msg);

int distance = 0, stateButton,Ultrasonic_Pin = 27, Button_pin = 18, Light_pin1=34, Light_pin2=35, Buzzer_pin = 33;
int Line_pin1=36,Line_pin2=39;
int light[2],line[2];

CRGB leds[4];     
CRGB myRGBcolor(0, 0, 0);

ToneESP32 buzzer(Buzzer_pin, 0);

void messageControl(const geometry_msgs::Twist& control_msg){
  float u = control_msg.linear.x; 
  float w = control_msg.angular.z;
  Serial.println("u="+String(u)+' '+"w="+String(w)); 
  robot(u,w);
}
void messageLeds( const std_msgs::Int32MultiArray& leds_msg){
  myRGBcolor.r = leds_msg.data[0];
  myRGBcolor.g = leds_msg.data[1];
  myRGBcolor.b = leds_msg.data[2];
  for (int i = 0; i <= 3; i++) 
    leds[i] = myRGBcolor;
  FastLED.show();  
}
void messageBuzzer(const std_msgs::Bool& buzzer_msg){
  if (buzzer_msg.data) 
    buzzer.tone(NOTE_B4, 1000);
}
ros::Subscriber<geometry_msgs::Twist> subControl("Control", &messageControl );
ros::Subscriber<std_msgs::Int32MultiArray> subLeds("Leds", &messageLeds );
ros::Subscriber<std_msgs::Bool> subBuzzer("Buzzer", &messageBuzzer );

void Get_Distance() {
  pinMode(Ultrasonic_Pin, OUTPUT);
  digitalWrite(Ultrasonic_Pin, HIGH);
  delayMicroseconds(20);
  digitalWrite(Ultrasonic_Pin, LOW);
  pinMode(Ultrasonic_Pin, INPUT);
  int Time_Echo_us = pulseIn(Ultrasonic_Pin, HIGH);
  distance = Time_Echo_us / 58;
}

void Get_Button() {
  stateButton=not(digitalRead(Button_pin));
}

void Get_Light() {
  light[0]=analogRead(Light_pin1);
  light[1]=analogRead(Light_pin2);
}
void Get_Line() {
  line[0]=analogRead(Line_pin1);
  line[1]=analogRead(Line_pin2);
}

void robot(float u, float w) {
  float r=0.02, d=0.08,K=40;
  float wd = u/r+w*d/(2*r);
  float wi = u/r-w*d/(2*r);
  int L,R,L1=0,L2=0,R1=0,R2=0;
  L=int(K*wi);
  R=int(K*wd);
  if (L>0)
    L1=L;
  else
    L2=abs(L);
  if (R>0)
    R1=R;
  else
    R2=abs(R);
  Serial.println("Motores:"+String(L1)+' '+String(L2)+' '+String(R1)+' '+String(R2));
  ledcWrite(12, L2);
  ledcWrite(13, L1);
  ledcWrite(14, R2);
  ledcWrite(15, R1);
}

void setup()
{
 pinMode(Button_pin,INPUT);
 FastLED.addLeds<WS2812, 25, GRB>(leds, 4); //RGB light pin 25, the number of lights is 4
 FastLED.setBrightness(100);                //RGB light brightness range 0-255

 for (int i = 12; i <= 15; i++) {  
    ledcSetup(i, 255, 8);           
    ledcAttachPin(i, i);           
  }
  // Use ESP8266 serial to monitor the process
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect the ESP8266 the the wifi AP
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Set the connection to rosserial socket server
  nh.getHardware()->setConnection(server, serverPort);
  nh.initNode();
  delay(1000);
  // Another way to get IP
  Serial.print("IP = ");
  Serial.println(nh.getHardware()->getLocalIP());
  // Start to be polite
  nh.advertise(chatter1);
  nh.advertise(chatter2);
  nh.advertise(chatter3);
  nh.advertise(chatter4);
  nh.subscribe(subControl);
  nh.subscribe(subLeds);
  nh.subscribe(subBuzzer);
  delay(1000);
}

void loop()
{
  Get_Distance();
  Get_Button();
  Get_Light();
  Get_Line();
  if (nh.connected()) {
    Serial.print("Connected ");
    distance_msg.data = distance;
    chatter1.publish( &distance_msg );
    Serial.print("Distance:"+String(distance)+"cm ");
    button_msg.data = stateButton;
    chatter2.publish( &button_msg );
    Serial.print("Button State:"+String(stateButton)+" ");
    light_msg.data_length=2;
    light_msg.data = light;
    chatter3.publish(&light_msg );
    Serial.print("Light array:"+String(light[0])+" "+String(light[1])+" ");
    line_msg.data_length=2;
    line_msg.data = line;
    chatter4.publish(&line_msg );
    Serial.println("Line array:"+String(line[0])+" "+String(line[1])+" ");
  } else {
    Serial.println("Not Connected");
  }
  nh.spinOnce();
  delay(1);
}
