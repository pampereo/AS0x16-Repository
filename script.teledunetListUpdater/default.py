import xbmc,xbmcgui,xbmcaddon
import urllib2,urllib
import cookielib
import re
import random

addon_id = 'script.teledunetListUpdater'
url = 'http://www.teledunet.com/boutique/connexion.php'
urllist = (['http://www.teledunet.com/download.php?name=TeledunetGermany&germany',
           'http://www.teledunet.com/download.php?name=TeledunetEurope&europe',
           'http://www.teledunet.com/download.php?name=TeledunetAmerica&america'])

colorlist = (['red','green','blue','yellow'])

__addon__ = xbmcaddon.Addon(addon_id)
df =  __addon__.getSetting("folder")
clr = __addon__.getSetting("dellogin") == 'true'
cln = __addon__.getSetting("delsetting") == 'true'
AddName = __addon__.getAddonInfo('name') 

values = {'login_user' : __addon__.getSetting("username"),
          'pass_user' : __addon__.getSetting("password")}

paramKodi = __addon__.getSetting("paramKodi")
Oname = df + __addon__.getSetting("oname")

pEXTM3U = True

class Main():
          
    def clearLogin(self):
        __addon__.setSetting('username','')
        __addon__.setSetting('password','')
        __addon__.setSetting('folder','')
        __addon__.setSetting('dellogin','false')
        
    def cleanSetting(self):
        __addon__.setSetting('paramKodi',' live=true')
        __addon__.setSetting('oname','teledunetKodi.m3u')
        __addon__.setSetting('delsetting','false')
     
    def processFile(self,inData,outData,wlabel,gr):
        
        global pEXTM3U
        
        for line in inData:
            x = ''.join(line).rstrip()
            if "#EXTM3U" in x :
                if pEXTM3U :
                    pEXTM3U = False
                    outData.write(x+"\n")
                    continue 
                else :
                    continue
            elif "#EXTINF" in x:
                me = re.search("(.*),(.*)", x)
                x = me.group(1)+gr+","+me.group(2)+wlabel
                outData.write(x+"\n")  
            else :
                x = x + paramKodi
                outData.write(x+"\n") 
    
    def go(self):
               
        if clr and cln :
            self.clearLogin()
            self.cleanSetting()
            xbmcgui.Dialog().ok(AddName,"Login and Settings deleted !!")
            exit()
        elif not clr and cln :
            self.cleanSetting()
            xbmcgui.Dialog().ok(AddName,"Settings deleted !!")
            exit()
        elif clr and not cln:
            self.clearLogin()
            xbmcgui.Dialog().ok(AddName,"Login deleted !!")
            exit()
            
        if len(colorlist) < len(urllist):
            xbmcgui.Dialog().ok(AddName,"not enough colors !!","Add some colors to list !!")
            exit()
          
        data = urllib.urlencode(values)
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(
                      urllib2.HTTPRedirectHandler(),
                      urllib2.HTTPHandler(debuglevel=0),
                      urllib2.HTTPSHandler(debuglevel=0),
                      urllib2.HTTPCookieProcessor(cookies))
        
        opener.open(url, data)
         
        try:
            out = open(Oname,"w")
            usedColor = ([])
            for i in range(len(urllist)) :
                dataurl = opener.open(urllist[i]).readlines()
                if dataurl is None:
                    continue
                
                srvname = 'Srv%s' % str(i+1)
                srvcolor = random.choice(colorlist)
                while srvcolor in usedColor :
                    srvcolor = random.choice(colorlist)
                    print 'color in'
                usedColor.append(srvcolor)
                
                srvlabel = ' [COLOR %s](%s)[/COLOR]' % (srvcolor,srvname)
                srvgrp = ' group-title="%s"' % srvname
                
                self.processFile(dataurl, out, srvlabel, srvgrp)
                
            
            ## Cleaning  
            out.close() 
            opener.close()
            cookies.clear_expired_cookies()
            cookies.clear_session_cookies()
            
            xbmc.executebuiltin('Notification(%s, %s)'%("File saved under: ", Oname))
            
            ret = xbmcgui.Dialog().yesno(AddName,'Restart Now?','[COLOR red]The entire System will reboot !!![/COLOR]')
            if ret :
                xbmc.executebuiltin('Reboot')
                    
        except:
        
            opener.close()
            cookies.clear_expired_cookies()
            cookies.clear_session_cookies()
            
            ret = xbmcgui.Dialog().yesno(AddName,"Verify your Login/network Settings","Do you want to open the Settings Window ?")
            
            if ret :
                __addon__.openSettings()

if ( __name__ == "__main__" ):
    Main().go()
