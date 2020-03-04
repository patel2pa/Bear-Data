
#include "Wire.h" 
#define Xbee Serial

const int MPU_ADDR = 0x68; 

int16_t accelerometer_x, accelerometer_y, accelerometer_z; 
int16_t gyro_x, gyro_y, gyro_z; 
int16_t temperature; 

char tmp_str[7]; 
char* convert_int16_to_str(int16_t i) { 
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}

void setup() {
  Xbee.begin(9600);
  Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR); 
  Wire.write(0x6B); 
  Wire.write(0); 
  Wire.endTransmission(true);
}
void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); 
  Wire.endTransmission(false); 
  Wire.requestFrom(MPU_ADDR, 7*2, true); 
  
  accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  //temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
  //gyro_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  //gyro_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  //gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
  
  Serial.print(convert_int16_to_str(accelerometer_x));
  Serial.print(","); 
  Serial.print(convert_int16_to_str(accelerometer_y));
  Serial.print(","); 
  Serial.println(convert_int16_to_str(accelerometer_z));
  String str = (convert_int16_to_str(accelerometer_x))+"//"+(convert_int16_to_str(accelerometer_x))+"//"+(convert_int16_to_str(accelerometer_x));

  Xbee.println(str);
  
  delay(100);
}
