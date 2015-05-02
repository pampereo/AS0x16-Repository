import xbmcgui, xbmcaddon
import urllib2,urllib
import cookielib
import os

## Variables ##
url = 'http://www.teledunet.com/boutique/connexion.php'
down_url2 = 'http://www.teledunet.com/download.php?name=TeledunetAmerica&america'
down_url1 = 'http://www.teledunet.com/download.php?name=TeledunetEurope&europe'

addon_id = 'script.teledunetListUpdater'
__addon__ = xbmcaddon.Addon(id=addon_id)
df =  __addon__.getSetting("folder")
AddName = __addon__.getAddonInfo('name') 

values = {'login_user' : __addon__.getSetting("username"),
          'pass_user' : __addon__.getSetting("password")}

strKodi = ' live=true'
label1 = ' [COLOR red](Europe)[/COLOR]'
label2 = ' [COLOR green](America)[/COLOR]'
Oname = df+"teledunetKodi.m3u"

## Functions ##
class Main():
    
    def verifyFile(self,infile):
        a = os.path.getsize(infile)
        if a <= 0 :
            return False
        else:
            return True
            
    #todo
    def cleanLogin(self):
        return
    
    def saveData(self,name,data):
        f = open(name,"w")
        f.write(data)
        f.close()
        
    def processFile(self,infile,out,wlabel,ahead):
        if  ahead:
            infile.readline() 
        
        for line in infile:
            x = ''.join(line).rstrip()
            if "#EXTM3U" in x:
                out.write(x+"\n")
                continue
            elif "#EXTINF" in x:
                x = x + wlabel
            else :
                x = x + strKodi
                
            out.write(x+"\n")
    
    def go(self):   
        data = urllib.urlencode(values)
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(
                      urllib2.HTTPRedirectHandler(),
                      urllib2.HTTPHandler(debuglevel=0),
                      urllib2.HTTPSHandler(debuglevel=0),
                      urllib2.HTTPCookieProcessor(cookies))
        
        response = opener.open(url, data)
        the_page = response.read()
        http_headers = response.info()
         
        try:
                data1 = opener.open(down_url1).read()
                data2 = opener.open(down_url2).read()
                
                self.saveData(df+"f1.tmp", data1)
                self.saveData(df+"f2.tmp", data2)
                
                if self.verifyFile(df+"f1.tmp") or self.verifyFile(df+"f2.tmp"):
                    
                    if self.verifyFile(df+"f1.tmp"):
                        ahead = False
                    else:
                        ahead = True
                    
                    out = open(Oname,"w")                
                    f1 = open(df+"f1.tmp","r")
                    f2 = open(df+"f2.tmp","r")
            
                    self.processFile(f1, out, label1, ahead) 
                    self.processFile(f2, out, label2, not ahead)
                   
                    out.close()
                    f1.close()
                    f2.close()
                    xbmcgui.Dialog().ok(AddName,"SUCCESS","File saved under :",Oname)
                    
                else:
                    xbmcgui.Dialog().ok(AddName,"Verify your Username/password")
        except:
                xbmcgui.Dialog().ok(AddName,"Verify your Login/network Settings")
                
        # cleaning part
        try:
                os.remove(df+"f1.tmp")
                os.remove(df+"f2.tmp")
        except:
                xbmcgui.Dialog().ok(AddName,"TMP Files not available")
        
                    
if ( __name__ == "__main__" ):
    Main().go()