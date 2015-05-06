import urllib2
import xbmcaddon,xbmcgui


url_fr = 'https://github.com/pampereo/AS0x16-Repository/raw/master/Misc/initiator_script/initial_fr.tar'
url_de = 'https://github.com/pampereo/AS0x16-Repository/raw/master/Misc/initiator_script/initial_de.tar'
url_en = 'https://github.com/pampereo/AS0x16-Repository/raw/master/Misc/initiator_script/initial_en.tar'

addon_id = 'script.arabicIPTVinitiator'
dpath = '/storage/backup/'
dfile = 'restore.tar'
__addon__ = xbmcaddon.Addon(addon_id)
AddName = __addon__.getAddonInfo('name') 

CHUNKsize = 16 * 1024

class Main():
          
    def go(self):
        
        req = xbmcgui.Dialog().select('Which language you want to download ?', ['EN','DE','FR'], 0)
        
        if req == 0:
            url = url_en
        elif req == 1:
            url = url_de
        elif req == 2:
            url = url_fr
        else:
            exit()
        
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
        xbmcgui.Dialog().ok(AddName,'Downlaod finished', 'restore the settings via OpenElec Tool !!!')
        
if ( __name__ == "__main__" ):
    Main().go()
