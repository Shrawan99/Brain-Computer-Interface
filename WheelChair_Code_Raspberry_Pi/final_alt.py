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
blink1=GPIO.PWM(12,50)
blink2=GPIO.PWM(13,50)
blink1.start(0)
blink2.start(0)



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
headset.blinked=0

def single_blink(headset):
  print "Single blink"
  GPIO.output(7,0)
  GPIO.output(8,1)
  headset.single_blink=False

def double_blink(headset):
  print "Double blink"
  GPIO.output(7,1)
  GPIO.output(8,0)
  headset.double_blink=False
def on_blink(headset):
  print"Blinked."
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

headset.single_blink=False
headset.double_blink=False
def checkblink(headset):
  while True:
    if headset.blinked==1 and not headset.single_blink:
      headset.single_blink=True
      mindwave.threading.Thread(target=single_blink,args=(headset,)).start()
    elif headset.blinked==2 and not headset.double_blink:
      headset.double_blink=True
      mindwave.threading.Thread(target=double_blink,args=(headset,)).start()
    headset.blinked=0    
    time.sleep(1)

blnk = mindwave.threading.Thread(target=checkblink,args=(headset,))
blnk.daemon = True
blnk.start()
    
def on_raw(headset,raw):
    if headset.poor_signal==0:
        if raw>400 and headset.listener.initial==0:
            headset.listener.initial=mindwave.datetime.datetime.now()
        elif raw<-90 and headset.listener.timer()>20 and headset.listener.timer()<300:
            print "got it"
            headset.blinked+=1
            print headset.blinked
            #mindwave.threading.Thread(target=on_blink,args=(headset,)).start()
            headset.listener.initial=0
        elif headset.listener.timer()>500:
            headset.listener.initial=0
headset.raw_value_handlers.append(on_raw)



while True:
  #print headset.raw_value
  try:
    if headset.poor_signal:
      print headset.poor_signal
    '''
    if headset.poor_signal == 0:
      GPIO.output(3,1)
      GPIO.output(10,0)
    else:
      GPIO.output(3,0)
      GPIO.output(10,1)
      
    '''      
    #print 'raw '+str(headset.raw_value)
    #print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
    '''
    if headset.attention >= 90 or headset.meditation >= 90:
      #GPIO.output(7,1)
      #GPIO.output(8,1)
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
          #GPIO.output(7,1)
          #GPIO.output(8,1)
          GPIO.output(11,0)
          p.ChangeDutyCycle(55)
          print "car is moving 60 miles/sec...."
        else:
          if headset.attention >=45 or headset.meditation >= 65:
           # GPIO.output(7,1)
            #GPIO.output(8,0)
            GPIO.output(11,0)
            p.ChangeDutyCycle(35)
            print "car is going to start...."
          else:
            #GPIO.output(7,0)
            #GPIO.output(8,0)
            GPIO.output(11,0)
            p.ChangeDutyCycle(0)
            print "Sorry Your concentration level is low...."
                  
            
    '''
              
    time.sleep(0.5)
  except KeyboardInterrupt:
    headset.disconnect()
    #GPIO.cleanup()
    #p.stop()
    break  
  
