#!/usr/bin/env python3

from datetime import datetime
from poordub import PcmAudio, ratio_to_db
from snips_skill import *
from spoken_time import *
from spoken_time import _ # Kludge to avoid a message catalog for 2 strings
import json, re, threading, time


class Clock( Skill):
    
    'An interactive audible clock'
    
    repetitions = 0
    presence = { 'play' : True }


    def add_arguments( self):
        super().add_arguments()
        self.parser.add_argument( '--site',
            help='Site ID for a single time announcement')
        self.parser.add_argument( '--chime',  help='Name of chime in config.ini')
        self.parser.add_argument( 'text', nargs='*', default='',
            help='Additional text to speak after the time announcement')


    @intent( 'dnknth:currentTime', silent=True)
    def current_time( self, userdata, msg):
        if not self.options.site:
            return _('It is {time}.').format( time=spoken_time())


    @intent( 'dnknth:currentDate', silent=True)
    def current_date( self, userdata, msg):
        if not self.options.site:
            return _('Today is {date}.').format( date=absolute_spoken_date())
        
    
    @on_play_finished()
    def play_finished( self, userdata, msg):
        if self.options.site == msg.payload['siteId']:
            self.disconnect()
            

    def on_connect( self, client, userdata, flags, rc):
        'Setup presence handler'        
        super().on_connect( client, userdata, flags, rc)
        
        if not self.options.site: return
        site = self.get_config( self.options.site)
        topic = site.get( 'presence_topic')
        if not topic: return

        self.presence.clear()
        self.pattern = re.compile( site.get( 'presence_pattern', '.*'))
        self.subscribe( topic, qos=1)
        self.message_callback_add( topic, self.presence_handler)
        time.sleep( 0.05) # Collect presence probes

    
    @staticmethod
    def presence_handler( self, userdata, msg):
        'Collect presence probes'
        if self.pattern.match( msg.topic):
            value = json.loads( msg.payload)
            self.log.debug( 'Received message: %s -> %s', msg.topic, value)
            self.presence[msg.topic] = value


    def chime( self):
        'Play the chimes(s)'
        chime = self.get_config( self.options.chime)
        site = self.get_config( self.options.site)
        wav_path = chime.get( 'chime', 'sounds/clock-chime.wav')
        volume = chime.getint( 'volume', 0) or site.getint( 'volume', 100)

        # Get audio and adjust volume
        sound = PcmAudio.from_file( wav_path).to_mono().normalize() \
            + ratio_to_db( volume / 100.0)

        if chime.getboolean( 'hours'): # Ring the hour
            repetitions = (datetime.now().hour + 11) % 12 + 1
            if repetitions:
                spacing = max( 0, chime.getfloat( 'spacing', 0))
                gap = PcmAudio.silence( spacing * 1000)
                sound = gap.join( [sound] * repetitions)
                
        time.sleep( chime.getfloat( 'delay', 0))
        return self.play_sound( self.options.site, sound.to_buffer())
        
    
    def run( self):
        with self.connect():
            
            mqtt_thread = threading.Thread( target=self.loop_forever, name='MQTT')
            mqtt_thread.start()

            if self.options.site:
                if not any( self.presence.values()):
                    self.log.debug( 'Nobody home, exiting...')
                    return
            
                if self.options.chime:
                    self.chime()

                else:
                    text = _('It is {time}.').format( time=spoken_time( am_pm=False))
                    self.speak( self.options.site, text + ' ' + ' '.join(self.options.text))
                    return
                
            mqtt_thread.join()

   
if __name__ == '__main__': # Let's go!
    
    Clock().run()