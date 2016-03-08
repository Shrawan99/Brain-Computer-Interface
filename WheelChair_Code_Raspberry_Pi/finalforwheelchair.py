import mindwave, time, subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
p=GPIO.PWM(12,50)
p.start(0)


headset = mindwave.Headset('/dev/ttyUSB0')
time.sleep(0.5)
def say(something):
  subprocess.call('espeak', something)

headset.connect()
print "Connecting"

while headset.status != 'connected':
  time.sleep(0.5)
  if headset.status == 'standby':
    headset.connect()
    print "Retrying"

print "connected"
headset.blinked=False
headset.blinked_counter=0
def on_blink(headset):
  print"Blinked."
  headset.blinked_counter+=1
  if headset.blinked_counter==1:
    GPIO.output(12,0)
    GPIO.output(26,1)
    GPIO.output(24,0)
    time.sleep(0.5)
    GPIO.output(26,0)
    time.sleep(0.1)
    GPIO.output(23,1)
    time.sleep(2)
    GPIO.output(23,0)
    time.sleep(0.1)
    GPIO.output(24,1)
    time.sleep(0.5)
    GPIO.output(24,0)
    GPIO.output(23,1)
    time.sleep(1)
    GPIO.output(23,0)
    time.sleep(2)
    GPIO.output(12,1)
  else:
    if headset.blinked_counter==2:
    {



    }
    else:
         
      headset.blinked=False
    
def on_raw(headset,raw):
    if headset.poor_signal==0:
        if raw>400 and headset.listener.initial==0:
            headset.listener.initial=mindwave.datetime.datetime.now()
        elif raw<-90 and headset.listener.timer()>20 and headset.listener.timer()<300:
            print "got it"
            if not headset.blinked:
	        headset.blinked=True
                mindwave.threading.Thread(target=on_blink,args=(headset,)).start()
``            headset.listener.initial=0
        elif headset.listener.timer()>500:
            headset.listener.initial=0
headset.raw_value_handlers.append(on_raw)



while True:
  #print headset.raw_value
  try:
    print headset.poor_signal
    if headset.poor_signal == 0:
      GPIO.output(3,1)
      GPIO.output(10,0)
    else:
      GPIO.output(3,0)
      GPIO.output(10,1)
      
      
    print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
    if headset.attention >= 90 or headset.meditation >= 90:
      GPIO.output(7,1)
      GPIO.output(8,1)
      #GPIO.output(10,1)
      GPIO.output(11,1)
      p.ChangeDutyCycle(100)
      print "car is moving in maximum speed...."
    else:
      if headset.attention >=70 or headset.meditation >= 80:
        GPIO.output(7,1)
        GPIO.output(8,1)
        GPIO.output(11,0)
        p.ChangeDutyCycle(80)
        print "car is moving 70 miles/sec...."
      else:
        if headset.attention >=60 or headset.meditation >= 70:
          GPIO.output(7,1)
          GPIO.output(8,1)
          GPIO.output(11,0)
          p.ChangeDutyCycle(55)
          print "car is moving 60 miles/sec...."
        else:
          if headset.attention >=45 or headset.meditation >= 65:
            GPIO.output(7,1)
            GPIO.output(8,0)
            GPIO.output(11,0)
            p.ChangeDutyCycle(35)
            print "car is going to start...."
          else:
            GPIO.output(7,0)
            GPIO.output(8,0)
            GPIO.output(11,0)
            p.ChangeDutyCycle(0)
            print "Sorry Your concentration level is low...."
                  
            
              
              
    time.sleep(1)
  except KeyboardInterrupt:
    headset.disconnect()
    GPIO.cleanup()
    p.stop()
    break  
  
