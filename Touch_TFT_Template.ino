/* Arduino Leonardo sample application for
   ITDB02 2.8" TouchScreen Module
   Using UTFT library https://github.com/telamon/utft
*/

#include <UTFT.h>
#include <ITDB02_Touch.h>

// Declare which fonts we will be using
extern uint8_t SmallFont[];
//extern uint8_t BigFont[];
//extern uint8_t SevenSegNumFont[];


UTFT lcd(ILI9325D_8,A5,A4,A3,A2);  
ITDB02_Touch  touch(A1,A2,A0,8,9);

void setup(){
  // Initialize GLCD
  lcd.InitLCD(PORTRAIT);
  lcd.setColor(0, 255, 0);
  lcd.setBackColor(32, 32, 32);
  //lcd.clrScr(); 
  lcd.fillScr(32,32,32); // Fill bgcolor
  
  // Initialize Touch  
  touch.InitTouch();
  touch.setPrecision(PREC_MEDIUM);
  
  // Initialize Serial
  //Serial.begin(9600);
  
  lcd.setFont(SmallFont);
  lcd.print("X:",LEFT,20);
  lcd.print("Y:",LEFT,40);
  Mouse.begin();
}

void loop(){
  while (touch.dataAvailable() == true){
    touch.read();
    lcd.printNumI(touch.getX(),CENTER,20,3,'0');
    lcd.printNumI(touch.getY(),CENTER,40,3,'0');
    Mouse.move(touch.getX()-128, touch.getY()-128, 0);
    //lcd.drawPixel (touch.getX(), touch.getY());
  }
}

