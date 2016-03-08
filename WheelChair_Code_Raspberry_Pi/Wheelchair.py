import mindwave, time, os ,subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT) #green signal ok
GPIO.setup(5,GPIO.OUT) #poor signal
GPIO.setup(7,GPIO.OUT) #first two are led for array
GPIO.setup(8,GPIO.OUT) #second two led for array
GPIO.setup(10,GPIO.OUT) #last two led for array
GPIO.setup(11,GPIO.OUT) #Base motor
GPIO.setup(12,GPIO.OUT) #Base motor 
GPIO.setup(13,GPIO.OUT) #Base motor
GPIO.setup(15,GPIO.OUT) #base motor 
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP) #switch input
GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(22,GPIO.OUT) #Movable part
GPIO.setup(23,GPIO.OUT) #Movabel part
GPIO.setup(24,GPIO.OUT) #Gripper
GPIO.setup(26,GPIO.OUT)  #Gripper
GPIO.output(22,0)
GPIO.output(23,0)
GPIO.output(24,0)
GPIO.output(26,0)
a=GPIO.PWM(12, 100) 
b=GPIO.PWM(15, 100) 
a.start(0)
b.start(0)
switch = GPIO.input(18)

headset = mindwave.Headset('/dev/ttyUSB0')
time.sleep(0.5)
def say(something):
  os.system('espeak -ven+m4 -s150 2</dev/null "{0}"'.format(something))

headset.connect()
print "Connecting"
say('connecting')

while headset.status != 'connected':
  time.sleep(0.5)
  if headset.status == 'standby':
    headset.connect()
    print "Retrying"
    say('retrying')
print "connected"

if not switch == GPIO.HIGH: #external switch is connected to pin 18
  headset.blinked=False
  print "Robot mode"
  say('robot mode')
  def on_blink(headset): 
    if headset.attention>=70 or headset.meditation>=65:
      print"Blinked."
      #say('blinked')
      GPIO.output(21,1)#griper open for 0.5 s
      GPIO.output(22,0)
      #GPIO.output(24,0)
      #GPIO.output(26,1)
      print"Gripper moved"
      #say('gripper moved')
      time.sleep(0.2)
      GPIO.output(21,0)#griper close for 
      GPIO.output(22,1)
      #GPIO.output(24,1)
      #GPIO.output(26,0)
      time.sleep(0.4)
      GPIO.output(22,0)
      GPIO.output(21,0)
      #GPIO.output(24,0)
      #GPIO.output(26,0)
      time.sleep(1)
      #GPIO.output(22,1)#movable part turn 360
      #GPIO.output(23,0) 
      #print "movable part moved"
      #time.sleep(2)
      #GPIO.output(22,0)
      #GPIO.output(24,1)#again gripper open 
      #GPIO.output(26,0)
      #time.sleep(0.3)
      #GPIO.output(24,0)
      #GPIO.output(26,1)#Again gripper CLOSE 
      #time.sleep(0.1)
      #GPIO.output(26,0)	
      #GPIO.output(22,0)
      #GPIO.output(23,1)#movable part turn 360
      #time.sleep(1)
      #GPIO.output(23,0)
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
	  headset.listener.initial=0
      elif headset.listener.timer()>500:
        headset.listener.initial=0
  headset.raw_value_handlers.append(on_raw)

	
	
  while True:
    try:
      headset.blinked=False	
      print headset.poor_signal
      if headset.poor_signal == 0:
        GPIO.output(3,1)
	GPIO.output(5,0)
        GPIO.output(10,0)
      else:
        GPIO.output(3,0)
	GPIO.output(5,1)
        GPIO.output(10,0)
      print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
      if headset.attention >= 100 or headset.meditation >= 90:
        GPIO.output(7,1)
	GPIO.output(8,1)
	GPIO.output(10,1)
	GPIO.output(11,0)
	GPIO.output(13,0)
	a.ChangeDutyCycle(100) 
	b.ChangeDutyCycle(100)
	print "maximum speed...."
	#say('maximum speed')
      else:
        if headset.attention >=90 or headset.meditation >= 80:
	  GPIO.output(7,1)
	  GPIO.output(8,1)
	  GPIO.output(10,1)
	  GPIO.output(11,0)
	  GPIO.output(13,0)
	  a.ChangeDutyCycle(80)
	  b.ChangeDutyCycle(80)
	  print "car is moving 70 miles/hour...."
	  #say('70 miles per second')
	else:
	  if headset.attention >=80 or headset.meditation >= 70:
	    GPIO.output(7,1)
	    GPIO.output(8,1)
	    GPIO.output(10,0)
            GPIO.output(11,0)
            GPIO.output(13,0)
	    a.ChangeDutyCycle(55)
	    b.ChangeDutyCycle(55)
            print "car is moving 60 miles/hour...."
	    #say('60 miles per second')
	  else:
	    if headset.attention >=70 or headset.meditation >= 65:
	      GPIO.output(7,1)
	      GPIO.output(8,0)
              GPIO.output(10,0)
	      GPIO.output(11,0)
	      GPIO.output(13,0)
	      a.ChangeDutyCycle(35)
	      b.ChangeDutyCycle(35)
	      print "car is going to start...."
	      #say('car is going to start  Please Concerntrate')
	    else:
              GPIO.output(7,0)
	      GPIO.output(8,0)
	      GPIO.output(10,0)
	      GPIO.output(11,0)
	      GPIO.output(13,0)
	      a.ChangeDutyCycle(0)
	      b.ChangeDutyCycle(0)
	      print "Sorry Your concentration level is low...."
	      #say('sorry your concentration level is low')					
      time.sleep(1)
    except KeyboardInterrupt:
      headset.disconnect()
      GPIO.output(21,0)
      GPIO.output(22,0)
      GPIO.output(23,0)
      GPIO.output(24,0)
      GPIO.cleanup()
      a.stop()
      b.stop()
      break  

else: #switch else
  headset.blinked=False
  print "Wheelchair mode"
  say('wheelchair mode')
  def single_blink(headset):
    print "Single blink"
    print 'left'
    say('left')
    GPIO.output(21,1)
    GPIO.output(22,0)
    GPIO.output(23,0)
    GPIO.output(24,0)
    time.sleep(5)
    GPIO.output(21,0)
    GPIO.output(22,0)
    GPIO.output(23,0)
    GPIO.output(24,0)
    #GPIO.output(7,0)
    #GPIO.output(8,1)
    headset.single_blink=False

  def double_blink(headset):
    print "Double blink"
    print 'right'
    say('right')
    GPIO.output(21,0)
    GPIO.output(22,0)
    GPIO.output(23,1)
    GPIO.output(24,0)
    time.sleep(5)
    GPIO.output(21,0)
    GPIO.output(22,0)
    GPIO.output(23,0)
    GPIO.output(24,0)
    #GPIO.output(7,1)
    #GPIO.output(8,0)
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
    print headset.raw_value
    try:
      if headset.poor_signal:
        print headset.poor_signal
   
      if headset.poor_signal == 0:
        GPIO.output(3,1)
        GPIO.output(5,0)
      else:
        GPIO.output(3,0)
        GPIO.output(5,1)
      
          
      #print 'raw '+str(headset.raw_value)
      print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
    
      if headset.attention >= 90 or headset.meditation >= 90:
        GPIO.output(7,1)
        GPIO.output(8,1)
        GPIO.output(10,1)
        GPIO.output(11,0)
        GPIO.output(13,0)
        GPIO.output(21,1)
        GPIO.output(22,0)
        GPIO.output(23,1)
        GPIO.output(24,0)
   
     #p.ChangeDutyCycle(100)
        print "car is moving in maximum speed...."
      else:
        if headset.attention >=80 or headset.meditation >= 80:
          GPIO.output(7,1)
          GPIO.output(8,1)
          GPIO.output(10,1)
          GPIO.output(11,0)
          GPIO.output(13,0)
          #GPIO.output(21,1)
          #GPIO.output(22,0)
          #GPIO.output(23,1)
          #GPIO.output(24,0)
       
	   #p.ChangeDutyCycle(80)
          print "car is moving 70 miles/sec...."
        else:
          if headset.attention >=75 or headset.meditation >= 70:
            GPIO.output(7,1)
            GPIO.output(8,1)
            GPIO.output(10,0)
            GPIO.output(11,0)
            GPIO.output(13,0)
	    #GPIO.output(21,0)
            #GPIO.output(22,0)
            #GPIO.output(23,0)
            #GPIO.output(24,0)

            #p.ChangeDutyCycle(55)
            print "car is moving 60 miles/sec...."
          else:
            if headset.attention >=70 or headset.meditation >= 65:
              GPIO.output(7,1)
              GPIO.output(8,0)
              GPIO.output(10,0)
              GPIO.output(11,0)
              GPIO.output(13,0)
	      #GPIO.output(21,0)
	      #GPIO.output(22,0)
	      #GPIO.output(23,0)
	      #GPIO.output(24,0)
              #p.ChangeDutyCycle(35)
              say('wheelchair is moving')
	      print "car is going to start...."
            else:
              GPIO.output(7,0)
              GPIO.output(8,0)
              GPIO.output(10,0)
              GPIO.output(11,0)
              GPIO.output(13,0)
	      GPIO.output(21,0)
	      GPIO.output(22,0)
	      GPIO.output(23,0)
	      GPIO.output(24,0)
              #GPIO.output(11,0)
              #p.ChangeDutyCycle(0)
              print "Sorry Your concentration level is low...."
                  
              
      time.sleep(0.5)
    except KeyboardInterrupt:
      GPIO.output(21,0)
      GPIO.output(22,0)
      GPIO.output(23,0)
      GPIO.output(24,0)
      headset.disconnect()
      GPIO.cleanup()
      #p.stop()
      break  
  
  
