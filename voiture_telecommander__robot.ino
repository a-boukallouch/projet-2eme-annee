

#include <WiFi.h>
#include <WebServer.h>


// --- Configuration des Pins ---
const int motorPinA = 18; const int motorPinB = 19;
const int motorPinC = 22; const int motorPinD = 23;


WebServer server(80);


// --- LA PAGE WEB (Le Joystick) ---
const char* html_page = R"=====(
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Robot Control</title>
  <style>
    body { background-color: #2c3e50; color: white; text-align: center; font-family: Arial, sans-serif; touch-action: none; margin: 0; padding-top: 50px; }
    #zone { width: 300px; height: 300px; background-color: #ecf0f1; border-radius: 20px; margin: 0 auto; position: relative; box-shadow: 0px 0px 20px rgba(0,0,0,0.5); }
    #stick { width: 80px; height: 80px; background-color: #e74c3c; border-radius: 50%; position: absolute; top: 110px; left: 110px; box-shadow: 0px 5px 10px rgba(0,0,0,0.3); }
    h1 { margin-bottom: 30px; }
  </style>
</head>
<body>
  <h1>Pilote ton Robot</h1>
  <div id="zone"><div id="stick"></div></div>


  <script>
    var zone = document.getElementById('zone');
    var stick = document.getElementById('stick');
    var isDragging = false;
    var lastSend = 0;


    function bouger(e) {
      if(!isDragging) return;
      e.preventDefault(); // Empêche l'écran de scroller sur téléphone
     
      var rect = zone.getBoundingClientRect();
      var clientX = e.touches ? e.touches[0].clientX : e.clientX;
      var clientY = e.touches ? e.touches[0].clientY : e.clientY;


      var x = clientX - rect.left;
      var y = clientY - rect.top;


      // Garder le joystick dans le carré
      x = Math.max(40, Math.min(x, 260));
      y = Math.max(40, Math.min(y, 260));


      stick.style.left = (x - 40) + 'px';
      stick.style.top = (y - 40) + 'px';


      // Ne pas saturer le robot : on envoie l'ordre toutes les 50ms
      var now = Date.now();
      if (now - lastSend > 50) {
        // Les mêmes calculs que dans App Inventor !
        var valX = Math.round((x - 150) * 1.7);
        var valY = Math.round((150 - y  ) * 1.7);
        fetch('/drive?x=' + valX + '&y=' + valY);
        lastSend = now;
      }
    }


    // Commandes Souris (PC)
    zone.addEventListener('mousedown', function(e){ isDragging = true; bouger(e); });
    window.addEventListener('mousemove', bouger);
    window.addEventListener('mouseup', arret);


    // Commandes Tactiles (Téléphone)
    zone.addEventListener('touchstart', function(e){ isDragging = true; bouger(e); }, {passive: false});
    window.addEventListener('touchmove', bouger, {passive: false});
    window.addEventListener('touchend', arret);


    function arret() {
      if(!isDragging) return;
      isDragging = false;
      stick.style.left = '110px';
      stick.style.top = '110px';
      fetch('/drive?x=0&y=0'); // Stoppe les moteurs
    }
  </script>
</body>
</html>
)=====";


void setup() {
  Serial.begin(115200);
 
  ledcAttach(motorPinA, 5000, 8); ledcAttach(motorPinB, 5000, 8);
  ledcAttach(motorPinC, 5000, 8); ledcAttach(motorPinD, 5000, 8);


  // Démarrage du WiFi
  WiFi.softAP("RobotJoystick", "12345678");
  Serial.println("Robot Pret ! IP: 192.168.4.1");


  // Envoi de la page Web (le joystick)
  server.on("/", []() {
    server.send(200, "text/html", html_page);
  });


  // Réception des ordres
  server.on("/drive", []() {
    int x = server.arg("x").toInt();
    int y = server.arg("y").toInt();


    piloter(y + x, y - x);
    server.send(200, "text/plain", "OK");
  });


  server.begin();
}


void loop() {
  server.handleClient();
}










// Fonction des moteurs (CORRIGÉE POUR INVERSER LE SENS)
void piloter(int g, int d) {
  g = constrain(g, -255, 255);
  d = constrain(d, -255, 255);


  // Moteur Gauche (Inversé)
  if (g > 0) {
    ledcWrite(motorPinA, abs(g)); ledcWrite(motorPinB, 0);
  } else if (g < 0) {
    ledcWrite(motorPinA, 0); ledcWrite(motorPinB, abs(g));
  } else {
    ledcWrite(motorPinA, 0); ledcWrite(motorPinB, 0);
  }


  // Moteur Droit (Inversé)
  if (d > 0) {
    ledcWrite(motorPinC, 0); ledcWrite(motorPinD, abs(d));
  } else if (d < 0) {
    ledcWrite(motorPinC, abs(d)); ledcWrite(motorPinD, 0);
  } else {
    ledcWrite(motorPinC, 0); ledcWrite(motorPinD, 0);
  }
}


