import urllib2,time,os
import xbmcaddon,xbmcgui,xbmc

## MXQ OpeneElec URL Library
#url = 'https://github.com/kszaq/OpenELEC.tv/releases/download/5.0.8p1/OpenELEC-Amlogic.MXQ.arm-5.0.8-20150409.tar'
url = 'https://github.com/kszaq/OpenELEC.tv/releases/download/5.0.8p8/OpenELEC-Amlogic.MXQ.arm-5.0.8-20150511.tar'

addon_id = 'script.mxqboxupdater'
__addon__ = xbmcaddon.Addon(addon_id)
AddName = __addon__.getAddonInfo('name') 

dpath = '/storage/.update'

CHUNKsize = 1024
cvMpsBps = 1048576

class Main():
          
    def go(self):
        
        req = xbmcgui.Dialog().yesno(AddName,'Start the update','[COLOR red]If your Box is not a BEELINK MXQ, you risk to brik it !!!!![/COLOR]')
        
        if not req :
            xbmcgui.Dialog().ok(AddName,'Check your Box model before you proceed !!')
            exit()
        
        mxq = xbmcgui.Dialog().yesno(AddName,'This will take some time to be executed','[COLOR red]Do you want to proceed ???[/COLOR]')
        
        if mxq :
            pDialog = xbmcgui.DialogProgress()
            pDialog.create(AddName, 'Downloading ... Please wait !!')
            
            localFilename = url.split('/')[-1]
            with open(dpath + '/' + localFilename, 'wb') as f:
                start = time.clock()
                r = urllib2.urlopen(url)
                total_length = r.headers.get('content-length')
                print total_length
                dl = 0
                if total_length is None:
                    f.write(r.content)
                else:
                    while True:
                        if pDialog.iscanceled():
                            f.close()
                            pDialog.close()
                            os.remove(dpath + '/' + localFilename)
                            exit()
                        chunk = r.read(CHUNKsize)
                        if len(chunk) == 0: 
                            if int(dl) != int(total_length):
                                line = '[Downloaded %s from %s]' % (dl,total_length)
                                xbmcgui.Dialog().ok(AddName, 'Error is occured',line,'[COLOR red]Try to download again !![/COLOR]')
                                f.close()
                                pDialog.close()
                                os.remove(dpath + '/' + localFilename)
                                exit()
                            break
                        dl += len(chunk)
                        f.write(chunk)
                        done = int(100 * dl / int(total_length))
                        
                        line1 = 'Downloading ... Please wait !! '
                        line2 = 'Filename:[COLOR red] %s[/COLOR]' % localFilename
                        line3 = '\r[%s from %s] @ %s Mb/sec' % (dl,total_length,float("{0:.2f}".format(dl//(time.clock() - start)/cvMpsBps)))
                        pDialog.update(done,line1,line2,line3)
            
            f.close()            
            pDialog.close()
            
            req = xbmcgui.Dialog().yesno(AddName,'Reboot now ??')
        
            if req :
                xbmc.executebuiltin('Reboot')
        else:
            xbmcgui.Dialog().ok(AddName,'Very Well, Safe is Safe')
            

if ( __name__ == "__main__" ):
    Main().go()
