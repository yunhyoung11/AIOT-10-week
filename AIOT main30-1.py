import paho.mqtt.client as mqtt     #mqtt 통신 모듈을 불러옴  
import time             #시간관련 기능을 사용하기 위해 불러옴 
from gpiozero import LED    #GPIO 핀 제어를 하기 위해 불러옴 
import threading        #두 작업을 동시에 처리하기 위해 불러옴 

greenLed = LED(16)     #16번 핀에 연결된 초록 LED 설정 
blueLed = LED(20)      #20번 핀에 연결된 파랑 LED 설정 
redLed = LED(21)       #21번 핀에 연결된 빨강 LED 설정 

def on_message(client, userdata, msg):  #MQTT 메세지를 받으면 자동 실행되는 함수 
    print(msg.topic+" "+str(msg.payload))  #받은 토픽과 메세지를 출력 
    message = msg.payload.decode()          #MQTT메세지를 문자열로 전환 
    print(message)          #문자열 메세지 출력 
    if message == "green_on":   #메세지가 green on 이면 초록 LED 켬 
        greenLed.on()
    elif message == "green_off":   #메세지가 green off 이면 초록 LED 끔 
        greenLed.off()
    elif message == "blue_on":  #메세지가 blue on 이면 파랑 LED 켬
        blueLed.on()
    elif message == "blue_off":  #메세지가 blue off 이면 파랑 LED 끔 
        blueLed.off()
    elif message == "red_on":  #메세지가 red on 이면 빨강 LED 켬
        redLed.on()
    elif message == "red_off":  #메세지가 red off 이면 빨강 LED 끔 
        redLed.off()

client = mqtt.Client()      #MQTT 클라이언트 객체 생성 
client.on_message = on_message      #메세지를 받으면 함수를 실행 

broker_address="192.168.137.230"    #MQTT 브로커 주소 저장 
client.connect(broker_address)      #브로커에 접속 
client.subscribe("led",1)           #led토픽을 구독 

count = 0    #숫자 변수 생성 
def send_thread():  #메세지를 계속 보내는 함수 
    global count   #함수 밖에서 선언된 변수 count를 전역에서 사용  
    while 1:  #프로그램 종료까지 반복 
        count = count + 1    #count를 1씩 증가 
        client.publish("hello", str(count))     #hello 토픽으로 count 값을 문자열로 변환 
        time.sleep(1.0)  #1초 대기 

task = threading.Thread(target = send_thread)     #send_thread 함수를 별도 스레드로 실행 
task.start()  #스레드 시작 

client.loop_forever()   #메세지를 기다리는 무한반복  
