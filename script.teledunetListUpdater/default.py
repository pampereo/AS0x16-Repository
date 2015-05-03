import xbmcgui, xbmcaddon
import urllib2,urllib
import cookielib
import re

## Variables ##
url = 'http://www.teledunet.com/boutique/connexion.php'
down_url2 = 'http://www.teledunet.com/download.php?name=TeledunetAmerica&america'
down_url1 = 'http://www.teledunet.com/download.php?name=TeledunetEurope&europe'
addon_id = 'script.teledunetListUpdater'

__addon__ = xbmcaddon.Addon(id=addon_id)
df =  __addon__.getSetting("folder")
clr = __addon__.getSetting("delsetting") == 'true'
AddName = __addon__.getAddonInfo('name') 

values = {'login_user' : __addon__.getSetting("username"),
          'pass_user' : __addon__.getSetting("password")}

paramKodi = ' live=true'
name1 ='Server 1'
label1 = ' [COLOR red](%s)[/COLOR]' % name1
groupe1 = ' group-title="%s"' % name1

name2 = 'Server 2'
label2 = ' [COLOR green](%s)[/COLOR]' % name2
groupe2 = ' group-title="%s"' % name2

Oname = df+"teledunetKodi.m3u"
pEXTM3U = True

## Functions ##
class Main():
          
    def cleanLogin(self):
        __addon__.setSetting('username','')
        __addon__.setSetting('password','')
        __addon__.setSetting('folder','')
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
        
        if clr :
            self.cleanLogin()
            xbmcgui.Dialog().ok(AddName,"Setting deleted !!")
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
                    
                out.close()
                
                xbmcgui.Dialog().ok(AddName,"SUCCESS","File saved under :",Oname)
                
        except:
                xbmcgui.Dialog().ok(AddName,"Verify your Login/network Settings")

                    
if ( __name__ == "__main__" ):
    Main().go()