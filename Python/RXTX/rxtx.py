#!/usr/bin/env python
import serial
import time
import thread
from ublox_lara_r2 import *


class RXTX(object):
    '''
    Listens to text on serial, sends it via UMTS to ThingSpeak.
    Start like this:
        from RXTX import *
        r = RXTX(debug=True)
        r.connect()
    '''

    def __init__(self, debug=False):
        '''
        debug: boolean
            Whether to print debug info or not
        '''
        self.debug = debug
        self.port = 80

        # https://thingspeak.com/channels/778930
        # self.url = 'api.thingspeak.com'
        # self.api_key = 'XLQ16T0SUPGXSNMV'

        # http://dweet.io/follow/scary-weather
        self.url = 'dweet.io'
        self.api_key = 'scary-weather'
        


    def init_lara(self):
        '''
        Initializes the ublox lara r2 UMTS module, returns initialised object
        '''
        u = Ublox_lara_r2()
        u.initialize()
        u.reset_power()
        time.sleep(20.)
        u.debug = self.debug
        if self.debug:
            u.sendAT("AT+CMEE=2\r\n") # set verbose error codes

         # select carrier
        u.sendAT("AT+COPS?\r\n") # show connected carrier
        u.sendAT("AT+URAT?\r\n") # shows radio access technology, see chapter 7.7.3 in Commands manual
        #u.sendAT('AT+UPSD=0,0,0\r\n') # sets IPv4
        #u.sendAT('AT+UPSD=0,1,"internet"\r\n') # sets APN
        u.sendAT('AT+UPSDA=0,3\r\n') # activates packet switched data
        u.sendAT('AT+UHTTP=0\r\n') # reset the HTTP profile #0

        return u


    def connect(self):
        '''
        Connect to the serial, send to ThingSpeak
        '''
        u = self.init_lara()

        # Initiate a serial connection
        ser = serial.Serial('/dev/ttyACM0', 115200)

        # set lara r2 to self.url
        u.sendAT('AT+UHTTP=0,1,"{}"\r\n'.format(self.url)) # set domain
        u.sendAT('AT+UHTTP=0,5,{}\r\n'.format(self.port)) # set port
        u.sendAT('AT+UDNSRN=0,"{}"\r\n'.format(self.url))
        
        while True:
            try:
                time.sleep(0.01) # TODO check if necesssary
                # read message from the serial connection
                str_message = str(ser.readline())
                message = str_message.rstrip()

                if self.debug:
                    print('Message received: ', message)

                if '' != message and None != message:
                    try:
                        #prepare request
                        # url = '/update?api_key={}&field1={}'.format(self.api_key, message)
                        url = '/dweet/for/{}'.format(self.api_key)
                        if self.debug:
                            print(url)
                        # send GET request
                        # u.sendAT('AT+UHTTPC=0,1,"{}","get.ffs"\r\n'.format(url))
                        # send POST request with data in application/json form
                        if u.sendAT('AT+UHTTPC=0,1,"{}?{}","post.ffs"\r\n'.format(url, message), "OK\r\n"):
                            # TODO quit while loop after n attempts
                            while not "UUHTTPCR" in u.response:
                                time.sleep(0.5)
                            if "0,1,1" in u.response.split("UUHTTPCR")[1]:
                                if u.sendAT('AT+URDFILE="post.ffs"\r\n', "OK\r\n"): # get response from FS
                                    ser.write(b'{}\r\n'.format(u.response))
                            else:
                                ser.write(b'Error occured while sending\r\n')
                        else:
                            ser.write(b'Error occured while trying to send\r\n')
                    except ValueError:
                        print(message)
            except Exception, e:
                if self.debug:
                    print('An exception ocurred', str(e))
                pass