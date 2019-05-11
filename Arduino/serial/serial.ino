void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {}
  Serial.println("Serial Connected");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Serial Connected 2");

}
