StormLogger
===========

A simple class that implements logging.Handler to send to Splunk Storm in Python 3

Resources
=========

I initially tried to use https://github.com/andresriancho/splunk-logger which resulted in a number of Python 3 specific issues related to cStringIO.  Rather than troubleshoot, I trimmed it down to the bare essentials, modified it with the information provided by http://docs.splunk.com/Documentation/Storm/latest/User/Stormdatainputendpointexamples#Example:_Input_data_with_Python, and even then it didn't work...

So then I replaced all of the urllib and urllib2 calls with the appropriate calls to urllib.request and urllib.parse.

Usage
=====

It's dead simple to use. Below demonstrates how to attach it.  Be sure to replace *** with your own codes that can be found in the data section of your project's console in Splunk Storm.

::


    import logging
    from storm_logger import StormLogger

    ACCES_TOKEN = '***'
    PROJECT_ID = '***'
    
    # Also called the API Hostname in the Storm GUI, api-*****.data.splunkstorm.com
    API_FQDN = '***'

    storm_handler = StormLogger(access_token=ACCESS_TOKEN,
                               project_id=PROJECT_ID,
                               api_fqdn=API_FQDN)
    
    logging.basicConfig(level.logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    logging.getLogger('').addHandler(storm_handler)

    logging.debug('Test Message')
