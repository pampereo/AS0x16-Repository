import xbmc,xbmcgui,xbmcaddon
import urllib2,urllib
import cookielib
import re

url = 'http://www.teledunet.com/boutique/connexion.php'
down_url2 = 'http://www.teledunet.com/download.php?name=TeledunetAmerica&america'
down_url1 = 'http://www.teledunet.com/download.php?name=TeledunetEurope&europe'
addon_id = 'script.teledunetListUpdater'

__addon__ = xbmcaddon.Addon(addon_id)
df =  __addon__.getSetting("folder")
clr = __addon__.getSetting("dellogin") == 'true'
cln = __addon__.getSetting("delsetting") == 'true'
AddName = __addon__.getAddonInfo('name') 

values = {'login_user' : __addon__.getSetting("username"),
          'pass_user' : __addon__.getSetting("password")}

paramKodi = __addon__.getSetting("paramKodi")
Oname = df + __addon__.getSetting("oname")
name1 = __addon__.getSetting("srv1Name")
name2 = __addon__.getSetting("srv2Name")
colSrv1 = __addon__.getSetting("colSrv1")
colSrv2 = __addon__.getSetting("colSrv2")

label1 = ' [COLOR %s](%s)[/COLOR]' % (colSrv1,name1)
groupe1 = ' group-title="%s"' % name1
label2 = ' [COLOR %s](%s)[/COLOR]' % (colSrv2,name2)
groupe2 = ' group-title="%s"' % name2

pEXTM3U = True

class Main():
          
    def clearLogin(self):
        __addon__.setSetting('username','')
        __addon__.setSetting('password','')
        __addon__.setSetting('folder','')
        __addon__.setSetting('dellogin','false')
        
    def cleanSetting(self):
        __addon__.setSetting('colSrv1','yellow')
        __addon__.setSetting('colSrv2','blue')
        __addon__.setSetting('srv1Name','Srv1')
        __addon__.setSetting('srv2Name','Srv2')
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
            
        data = urllib.urlencode(values)
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(
                      urllib2.HTTPRedirectHandler(),
                      urllib2.HTTPHandler(debuglevel=0),
                      urllib2.HTTPSHandler(debuglevel=0),
                      urllib2.HTTPCookieProcessor(cookies))
        
        response = opener.open(url, data)
        #the_page = response.read()
        #http_headers = response.info()
         
        try:
            data1 = opener.open(down_url1).readlines()
            data2 = opener.open(down_url2).readlines() 
            out = open(Oname,"w")                
            
            self.processFile(data1, out, label1, groupe1) 
            self.processFile(data2, out, label2, groupe2)
            
            ## Cleaning  
            out.close() 
            opener.close()
            cookies.clear_expired_cookies()
            cookies.clear_session_cookies()
            
            xbmc.executebuiltin('Notification(%s, %s)'%("File saved under: ", Oname))
            
            ret = xbmcgui.Dialog().yesno(AddName,'Restart Now?','[COLOR red]The entire System will reboot !!![COLOR]')
            if ret :
                xbmc.executebuiltin('Reboot')
                    
        except:
        
            opener.close()
            cookies.clear_expired_cookies()
            cookies.clear_session_cookies()
            
            ret = xbmcgui.Dialog().yesno(AddName,"Verify your Login/network Settings","Do you want to open the Settings Window ?")
            
            if ret :
                xbmc.executebuiltin('xbmc.ReplaceWindow(addonsettings)')

                    
if ( __name__ == "__main__" ):
    Main().go()
