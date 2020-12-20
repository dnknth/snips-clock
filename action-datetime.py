#!/usr/bin/env python3

import locale
from snips_skill import end_session, on_intent, Skill
from spoken_time import *
from spoken_time import _


class Clock( Skill):
    
    "An interactive audible clock"

    def add_arguments( self):
        self.parser.add_argument( 'site', nargs='?',
            help="Site ID for a single time announcement")        

    @on_intent( "dnknth:currentTime")
    @end_session
    def currentTime( self, userdata, msg):
        return _("It is {time}").format( time=spoken_time())

    @on_intent( "dnknth:currentDate")
    @end_session
    def currentDate( self, userdata, msg):
        return _("Today is {date}").format( date=absolute_spoken_date())

   
if __name__ == '__main__': # Let's go!
    
    with Clock().connect() as clock:

        if clock.options.site:
            clock.speak( clock.options.site,
                _("It is {time}").format( time=spoken_time( am_pm=False)))
        else:
            clock.loop_forever()
