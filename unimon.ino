
#include <UTFT.h>
#include <ITDB02_Touch.h>

// Declare which fonts we will be using
extern uint8_t SmallFont[];
extern uint8_t BigFont[];
extern uint8_t SevenSegNumFont[];


UTFT lcd(ILI9325D_8,A5,A4,A3,A2);  
ITDB02_Touch  touch(A1,A2,A0,8,9);

//Operations
#define PRINT 1
#define CLEAR 0
#define SETFG 2
#define SETBG 3
#define FILLSCR 4
void setup(){
  // Initialize GLCD
  lcd.InitLCD(LANDSCAPE);
  lcd.setColor(0xFF,0xff,0xff);
  lcd.setBackColor(0x40, 0x3F, 0x42);
  //lcd.clrScr(); 
  lcd.fillScr(0x40, 0x3F, 0x42); // Fill bgcolor
  
  // Initialize Touch  
  touch.InitTouch();
  touch.setPrecision(PREC_MEDIUM);  
  
  
  lcd.setFont(BigFont);
  lcd.print("UniMon v0.0.1",CENTER,0);
  lcd.print("NOT CONNECTED",CENTER,100);
  pinMode(13,OUTPUT);
  
  // Initialize Serial
  Serial.begin(9600);
  while(!Serial) ;
  lcd.fillScr(0x40, 0x3F, 0x42);
  lcd.setFont(SmallFont);
}

void loop(){
  while (touch.dataAvailable() == true){
    digitalWrite(13,HIGH);
    touch.read();
    Serial.print(touch.getX());
    Serial.print(":");
    Serial.println(touch.getY());
    digitalWrite(13,LOW);
  }
  
  while(Serial.available() > 0 ){
    digitalWrite(13,HIGH);
    
    if(Serial.read() != 0xff){
      break;
    }
    
    int code = Serial.read();
    int x,y;  
    switch(code){
      case PRINT:
        x = Serial.read();
        y = Serial.read();
        if(Serial.read() == 'b')
          lcd.setFont(BigFont);
        else
          lcd.setFont(SmallFont);
        
        char msg[64];
        for(int i=0;i<64;i++)
          msg[i]=0;
        Serial.readBytesUntil(0x00,msg,64);
        lcd.print(msg,x,y);
        break;
      case CLEAR:
        lcd.clrScr();
        break;
      case SETFG:
        lcd.setColor(Serial.read(),Serial.read(),Serial.read());
        break;
      case SETBG:
        lcd.setBackColor(Serial.read(),Serial.read(),Serial.read());
        break;
      case FILLSCR:
        lcd.fillScr(Serial.read(),Serial.read(),Serial.read());
    }
    Serial.println("SCRDONE");
  }
  digitalWrite(13,LOW);
}

void cryError(){
  
  //lcd.print("Something went wrong",CENTER,CENTER);
}
