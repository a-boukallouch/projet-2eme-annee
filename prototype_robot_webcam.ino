
#include <Servo.h>


Servo moteur1;
Servo moteur2;
Servo moteur3;


int angle1 = 90;
int angle2 = 90;
int angle3 = 90;


void setup() {
  Serial.begin(9600);


  moteur1.attach(9);
  moteur2.attach(10);
  moteur3.attach(11);


  moteur1.write(angle1);
  moteur2.write(angle2);
  moteur3.write(angle3);


  delay(1000);
}


void loop() {
  if (Serial.available() > 0) {
    String commande = Serial.readStringUntil('\n');
    commande.trim();


    int virgule1 = commande.indexOf(',');
    int virgule2 = commande.indexOf(',', virgule1 + 1);


    if (virgule1 > 0 && virgule2 > virgule1) {
      int nouvelAngle1 = commande.substring(0, virgule1).toInt();
      int nouvelAngle2 = commande.substring(virgule1 + 1, virgule2).toInt();
      int nouvelAngle3 = commande.substring(virgule2 + 1).toInt();


      nouvelAngle1 = constrain(nouvelAngle1, 0, 180);
      nouvelAngle2 = constrain(nouvelAngle2, 0, 180);
      nouvelAngle3 = constrain(nouvelAngle3, 0, 180);


      angle1 = nouvelAngle1;
      angle2 = nouvelAngle2;
      angle3 = nouvelAngle3;


      moteur1.write(angle1);
      moteur2.write(angle2);
      moteur3.write(angle3);


      Serial.print("OK ");
      Serial.print(angle1);
      Serial.print(",");
      Serial.print(angle2);
      Serial.print(",");
      Serial.println(angle3);
    }
  }
}



