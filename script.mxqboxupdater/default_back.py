import urllib2
import xbmcaddon,xbmcgui,xbmc

url = 'https://github.com/kszaq/OpenELEC.tv/releases/download/5.0.8p7/OpenELEC-Amlogic.MXQ.arm-5.0.8-20150501.tar'

addon_id = 'script.mxqboxupdater'
dpath = '/storage/.update/'
dfile = 'update.tar'

CHUNKsize = 16 * 1024

__addon__ = xbmcaddon.Addon(addon_id)
AddName = __addon__.getAddonInfo('name') 

class Main():
          
    def go(self):
        
        req = xbmcgui.Dialog().yesno(AddName,'Start the update','[COLOR red]If your Box is not a BEELINK MXQ, you risk to brik it !!!!![/COLOR]')
        
        if not req :
            xbmcgui.Dialog().ok(AddName,'Check your Box model before you proceed !!')
            exit()
        
        mxq = xbmcgui.Dialog().yesno(AddName,'This will take some time to be executed','[COLOR red]Do you want to proceed ???[/COLOR]')
        
        if mxq :
            pDialog = xbmcgui.DialogProgress()
            pDialog.create(AddName, 'Downloading process','Please wait !!')
            tarfile = urllib2.urlopen(url)
           
            with open(dpath+dfile, 'wb') as fp:
                i = 1
                while True:
                    if pDialog.iscanceled():
                        exit()
                    chunk = tarfile.read(CHUNKsize)
                    if len(chunk) == 0: break
                    fp.write(chunk)
                    pDialog.update(10*i, 'Downloading process','Please wait !!')
                    i = i + 1
            
            fp.close()            
            pDialog.close()
            
            req = xbmcgui.Dialog().yesno(AddName,'Reboot now ??')
        
            if req :
                xbmc.executebuiltin('Reboot')
        else:
            xbmcgui.Dialog().ok(AddName,'Very Well, Safe is Safe')
            

if ( __name__ == "__main__" ):
    Main().go()
