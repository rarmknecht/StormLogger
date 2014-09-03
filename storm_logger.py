import urllib.parse
import urllib.request
import socket
import logging

class StormLogger(logging.Handler):
    
    INPUT_URL_FMT = 'https://%s/1/inputs/http'

    def __init__(self, access_token=None, project_id=None, api_fqdn=None):
        logging.Handler.__init__(self)
        self.project_id = project_id
        self.access_token = access_token
        self.api_fqdn = api_fqdn

        self.url = self.INPUT_URL_FMT % self.api_fqdn
        self.pass_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        self.pass_manager.add_password(None, self.url, 'x', access_token)
        self.auth_handler = urllib.request.HTTPBasicAuthHandler(self.pass_manager)
        self.opener = urllib.request.build_opener(self.auth_handler)
        urllib.request.install_opener(self.opener)
                
    def usesTime(self):
        return False

    def emit(self, record):
        
        try:
            response = self._send_to_splunk(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            # All errors end here.
            self.handleError(record)

    def _send_to_splunk(self, record):
        sourcetype = 'syslog'
        host = socket.gethostname()
        
        event_text = {'level' : record.levelname, 
                      'module' : record.module,
                      'line' : record.lineno,
                      'data' : self.format(record)
                    }
        params = {'project': self.project_id,
                  'sourcetype': sourcetype,
                  'host': host}

        url = '%s?%s' % (self.url, urllib.parse.urlencode(params))
        try:
            data = urllib.parse.urlencode(event_text)
            data = data.encode('utf-8')
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            return response.read()
        except (IOError, OSError):
            raise
