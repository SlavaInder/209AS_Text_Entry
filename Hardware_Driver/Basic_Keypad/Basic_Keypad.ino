// What: Supplying T9 keypad values to serial
// Where: https://learn.adafruit.com/matrix-keypad/arduino
// Why: The code is used to read rows and columns of T9
// keypad and send the value to serial 
// Reusing existing code saves time for 
// developing the major components of the system

#include "Adafruit_Keypad.h"

#define KEYPAD_PID3845

#define R1    2
#define R2    3
#define R3    4
#define R4    5
#define C1    8
#define C2    9
#define C3    10
#define C4    11

#include "keypad_config.h"

Adafruit_Keypad customKeypad = Adafruit_Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
  customKeypad.begin();
}

void loop() {
  customKeypad.tick();

  while(customKeypad.available()){
    keypadEvent e = customKeypad.read();
    /* 
     key map
     1 (backspace) 2 (ABC) 3 (DEF) 
     4 (JHI) 5 (JKL) 6 (MNO)
     7 (PQRS) 8 (TUV) 9 (WXYZ)
     * (F1) 0 (Space) # (F2)   
     */
    if(e.bit.EVENT == KEY_JUST_PRESSED) Serial.println((char)e.bit.KEY);
  }

  delay(10);
}
