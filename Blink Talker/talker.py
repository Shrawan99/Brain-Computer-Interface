import mindwave, keyboard, time

def on_blink(headset):
    keyboard.Keyboard.blink_counter+=1

def send_poor(headset,raw_value):
    keyboard.Keyboard.poor_signal=headset.poor_signal

def on_raw(headset,raw):
    if headset.poor_signal==0:
        if raw>400 and headset.listener.initial==0:
            headset.listener.initial=mindwave.datetime.datetime.now()
        elif raw<-90 and headset.listener.timer()>20 and headset.listener.timer()<300:
            on_blink(headset)
            headset.listener.initial=0
        elif headset.listener.timer()>500:
            headset.listener.initial=0

if __name__ == '__main__':
    headset = mindwave.Headset('/dev/ttyUSB0')
    time.sleep(2)

    headset.connect()
    print "Connecting"

    while headset.status != 'connected':
        time.sleep(0.5)
        if headset.status == 'standby':
            headset.connect()
            print "Retrying"
    try:
        print "connected"
        headset.blink_handlers.append(on_blink)
        headset.raw_value_handlers.append(on_raw)
        headset.raw_value_handlers.append(send_poor)
        keyboard.start()

    except KeyboardInterrupt:
        headset.disconnect()
    except:
        headset.disconnect()
        print "Unknown Error"
        raise
