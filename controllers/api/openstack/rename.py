import cherrypy
from datetime import datetime
from time import mktime
from getFunctions import getNovaInstance
from novaclient.exceptions import ClientException, NotFound

class Rename(object):
    exposed = True

    '''
        Rename VM
        id          : id of VM
        name        : name for the new VM
    '''
    @cherrypy.tools.isAuthorised()
    @cherrypy.tools.json_in()
    def PUT(self):
        json = cherrypy.request.json
        username = cherrypy.request.cookie.get('fedid').value
        novaClient = getNovaInstance()

        try:
            print("id = " + str(json['id']))
            x = novaClient.servers.find(id=json['id']);
            x.update(json['name']);
            cherrypy.log("- Renamed VM(" + json['id'] + ") to '" + json['name'], username)
        except (ClientException, KeyError) as e:
            cherrypy.log('- ' + str(e), username)
            raise cherrypy.HTTPError('500 There has been a problem with renaming the VM, try again later.')

