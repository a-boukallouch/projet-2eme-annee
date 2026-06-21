# projet-2eme-annee
Code source des projets :  bras robot - turboréateur - voiture_tel

<img width="248" height="239" alt="image" src="https://github.com/user-attachments/assets/62a81360-74f1-4572-83e2-05342b23978a" />


# 🦾 Bras Robotique à Contrôle Gestuel (Projet MIC2)

## 📝 Description
Conception et réalisation de A à Z d'un prototype de bras robotique imprimé en 3D, capable de reproduire en temps réel les mouvements de la main de l'utilisateur grâce à la vision par ordinateur. Ce projet pluridisciplinaire mêle conception mécanique (CAO), électronique embarquée et intelligence artificielle.

---

## 🚀 Fonctionnalités
* **Détection en temps réel :** Suivi de l'état de la main (ouverte/fermée) via le flux d'une webcam standard.
* **Contrôle synchronisé :** Pilotage fluide et temporisé de 3 servomoteurs simultanément.
* **Design sur mesure :** Modélisation 3D complète avec une approche *Top-Down*, optimisée pour une impression 3D rapide et sans supports.
* **Communication bidirectionnelle :** Interface entre l'ordinateur et le microcontrôleur via le port Série (USB).

---

## 🛠️ Technologies & Matériel

### Logiciels
* **Python :** Script de vision par ordinateur (détection de la main) et communication série.
* **C++ / Arduino IDE :** Logique embarquée et contrôle matériel.
* **Autodesk Fusion 360 :** Modélisation 3D (CAO) de toutes les pièces mécaniques.
* **Bambu Studio :** Tranchage (Slicing) pour l'impression 3D.

### Matériel Utilisé
* 1x Carte microcontrôleur Arduino
* 3x Servomoteurs SG90
* 1x Webcam
* 1x Imprimante 3D (Bambu Lab P1S)
* Plaque d'essai (Breadboard), câblage et alimentation.

---

## ⚙️ Architecture du Système (Comment ça marche ?)
1. **La Vision (Python) :** La webcam capture l'utilisateur. Le script Python analyse l'image, détecte si la main est ouverte ou fermée, et envoie un caractère simple (`O` ou `F`) sur le port série.
2. **Le Cerveau (Arduino) :** L'Arduino écoute le port USB à 9600 bauds. À la réception d'une instruction, la carte valide l'état et déclenche la séquence mécanique.
3. **Les Muscles (Servomoteurs) :** L'Arduino génère des signaux PWM progressifs vers les 3 moteurs SG90 pour exécuter une transition fluide (ex: ouverture complète en 3 secondes).

---

## 📥 Installation & Utilisation

### 1. Mécanique
* Imprimer les pièces 3D (Les fichiers `.stl` et `.step` se trouvent dans le dossier `/3D_Models`).
* Assembler le bras et câbler les servomoteurs sur les broches numériques `9`, `10` et `11`.

### 2. Côté Arduino (C++)
* Ouvrir le fichier `.ino` avec l'IDE Arduino.
* Téléverser le code sur la carte.
* ⚠️ **Important :** Fermer le moniteur série de l'IDE après le téléversement pour libérer le port USB.

### 3. Côté Python
* Installer les dépendances requises : 
  ```bash
  pip install pyserial
  # Ajouter ici les autres bibliothèques utilisées par votre script IA (ex: opencv-python, mediapipe...)




<img width="236" height="295" alt="image" src="https://github.com/user-attachments/assets/4ba06788-f657-4c3c-8df3-a8e2d4105abf" />






# 🏎️ Rover IoT Télécommandé par Wi-Fi (ESP32)

## 📝 Description
Conception et fabrication d'un mini-véhicule robotique contrôlable depuis n'importe quel smartphone ou ordinateur, sans application tierce. Le cœur du robot (un ESP32) génère son propre réseau Wi-Fi et héberge une interface Web tactile. Ce projet combine mécanique (découpe laser et impression 3D), électronique et développement web embarqué.

📸 **[Insérer ici une photo de la voiture découpée au laser]**

---

## 🚀 Fonctionnalités
* **Zéro Application :** Le pilotage se fait entièrement via le navigateur Web (Chrome, Safari, etc.).
* **Réseau Autonome :** Le robot crée son propre Point d'Accès Wi-Fi (SoftAP).
* **Joystick Tactile Interactif :** Interface fluide développée en JavaScript avec gestion du "Touch" pour mobile et du clic pour PC.
* **Pilotage Différentiel :** Algorithme mathématique convertissant les coordonnées X/Y du joystick en vitesse indépendante pour les moteurs gauches et droits.
* **Design Hybride :** Châssis conçu sur mesure, mixant des pièces découpées au laser et des éléments imprimés en 3D.

---

## 🛠️ Technologies & Matériel

### Logiciels & Langages
* **C++ (Arduino IDE) :** Logique matérielle, gestion du réseau Wi-Fi et serveur Web (`WiFi.h`, `WebServer.h`).
* **HTML / CSS / JavaScript :** Front-end de l'interface de contrôle (Joystick virtuel).
* **CAO 3D & 2D :** Modélisation des pièces pour l'impression 3D et tracés vectoriels pour la découpe laser.

### Matériel Utilisé
* 1x Microcontrôleur ESP32 (avec puce Wi-Fi intégrée).
* 4x Moteurs motoréducteurs CC ("moteurs jaunes" TT).
* 1x Driver moteur (Pont en H - ex: L298N).
* Châssis en bois/acrylique (Découpe Laser) et supports imprimés en 3D.

---

## ⚙️ Architecture du Code (Comment ça marche ?)
1. **Initialisation (C++) :** Au démarrage, l'ESP32 configure ses broches PWM (via `ledcAttach`) et lance un réseau Wi-Fi nommé `RobotJoystick`.
2. **Le Serveur Web :** L'ESP32 écoute sur le port 80. Lorsqu'un utilisateur se connecte, il lui envoie le code de la page Web (stocké dans la variable `html_page`).
3. **Le Client (JavaScript) :** Le script du joystick capture les mouvements du doigt sur l'écran et calcule l'angle et la force. Toutes les 50ms, il envoie une requête HTTP (`/drive?x=...&y=...`) au robot.
4. **L'Actionneur :** Le serveur reçoit les coordonnées, la fonction `piloter()` calcule la distribution de puissance (mixage différentiel) et ajuste le signal PWM des moteurs pour faire tourner, avancer ou reculer le robot.

<img width="224" height="266" alt="image" src="https://github.com/user-attachments/assets/2e2d7d88-ea7e-4f62-a2da-0ca1e4955e70" />



# INSA AeroDesign Lab — Sizing Turboréacteur & Aero-Strike 2026

## Description
Ce projet d'avant-projet aéronautique combine la rigueur scientifique de la thermodynamique et de la mécanique du vol avec une approche interactive double : un tableau de bord web de dimensionnement en temps réel et un jeu vidéo d'arcade type *Shoot 'em up* (SHMUP). 

Le cœur de l'application résout la dépendance circulaire classique en conception d'aéronefs : la masse de carburant dépend de la masse totale au décollage (MTOW), qui dépend elle-même du carburant requis et de la masse des réacteurs. Le programme modélise cette physique par une méthode itérative de point fixe s'appuyant sur les données d'avions industriels réels (Airbus A320neo, A350, Boeing 787).

* **L'interface Web** permet de configurer graphiquement une mission et d'analyser en temps réel la télémétrie de l'appareil avec un rendu de particules p5.js et un graphique d'itérations dynamiques.
* **Le Jeu Vidéo** convertit les résultats de ce simulateur thermodynamique directement en variables de gameplay, où l'inertie de pilotage et les types d'armes dépendent du moteur installé et de la masse calculée.

---

## Technologies utilisées
* **Langages :** Python, HTML5, CSS3, JavaScript.
* **Moteurs Graphiques & Analytics :**
  * Pygame (Moteur du jeu vidéo).
  * p5.js (Rendu des flux aérodynamiques et particules de poussée).
  * Chart.js (Graphique de convergence de la boucle de point fixe).

---

## Ce que j'ai codé

### ⚙️ Modélisation Thermodynamique & Algorithme de Point Fixe
* Implémentation du solveur de masse itératif (`solver_avion` / `runPhysics`) qui effectue automatiquement 15 itérations pour stabiliser la balance des masses (cellule, charge utile, moteurs et kérosène).
* Intégration du cycle thermodynamique de Brayton-Joule calculant le besoin en énergie selon la traînée aérodynamique en palier, l'énergie potentielle d'altitude (10 000 m) et le Pouvoir Calorifique Inférieur (PCI) du carburant.
* Modélisation du ratio statistique industriel de masse moteur fixé à 20 kg/kN pour ajuster le poids du réacteur selon la poussée maximale requise au décollage.

### ✈️ Physique de Vol Réelle (Inertie de Masse)
* Traduction du Principe Fondamental de la Dynamique (F = m * a) dans le code de pilotage : la vitesse maximale de déplacement de l'avion est inversement proportionnelle à sa masse totale au décollage (MTOW). Un avion lourdement chargé en passagers ou en carburant est physiquement plus lourd et "pataud" à manoeuvrer qu'un jet régional léger.

### 🎯 Armement & Pouvoirs de Moteurs Indexés
* Programmation d'un système d'attaque adaptatif lié au réacteur sélectionné par le solveur :
  * **CFM56 :** Mode "RAPID" à cadence de tir élevée.
  * **LEAP-1A :** Mode "SPREAD" avec un tir en éventail couvrant une zone plus large.
  * **GEnx / GE9X :** Mode "BEAM" / "MEGA_BEAM" générant de longs lasers plasma perforants, illustrant la puissance brute en mégawatts (MW) des gros-porteurs.

### 🖥️ Expérience Utilisateur & Systèmes de Jeu
* Développement du menu de configuration de l'appareil (sélection des passagers, de la distance de vol, de la finesse et activation optionnelle du mode "matériaux avancés" en composites carbonés).
* Conception d'un système d'objectifs de vol et de scénarios de mission (Défi Transatlantique, Jumbo Challenge, Green Pioneer).
* Codage des comportements de vagues d'ennemis oscillantes ("Créatures de traînée") et d'un affrontement final contre un Boss doté d'une barre de vie et d'une IA de riposte à tir périodique.



  
