import ssl, os, requests
from threading import active_count, Thread
from random import randint, choice
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from UserAgent import UserAgent

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
DeviceTypes                       = ["SM-G9900", "sm-g950f", "SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR", "SM-M326B", "SM-A528B", "SM-F711B", "SM-F926B", "SM-A037G", "SM-A225F", "SM-M325FV", "SM-A226B", "SM-M426B", "SM-A525F"]
Platforms                         = ["android", "windows", "ios", "iphone"]
Channel                           = ["tiktok_web", "googleplay", "App%20Store"]
ApiDomain                         = ["api19.tiktokv.com", "api.toutiao50.com", "api19.toutiao50.com"]
r                                 = requests.Session()
ThreadCount                       = 0
TotalSendedView                   = 0
TotalFailedReq                    = 0
ShareChoice                       = True
ViewChoice                        = True
DebugMode                         = False

r.cookies.set_policy(BlockCookies())

def Clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        pass

def Title(Content):
    global DebugMode
    if os.name == 'posix':
        return True
    elif os.name in ('ce', 'nt', 'dos'):
        os.system(f"title {Content}")
        return False
    else:
        pass

def ReadFile(filename,method):
    with open(filename,method,encoding='utf8') as f:
        content = [line.strip('\n') for line in f]
        return content

def SendView(item_id, proxy, timeout, proxytype):
    global TotalSendedView, TotalFailedReq, ShareChoice, ViewChoice, DebugMode
    proxy         = {f'{proxytype}': f'{proxytype}://{proxy}'}
    platform      = choice(Platforms)
    osVersion     = randint(1, 12)
    DeviceType    = choice(DeviceTypes)
    headers       = {
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "user-agent": choice(UserAgent)
                    }
    appName       = choice(["tiktok_web", "musically_go"])
    Device_ID     = randint(1000000000000000000, 9999999999999999999)
    apiDomain     = choice(ApiDomain)
    channelLol    = choice(Channel)
    URI           = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    Data          = f"item_id={item_id}"

    if ShareChoice == True:
        Data += "&share_delta=1"
    else:
        pass
    
    if ViewChoice == True:
        Data += "&play_delta=1"

    try:
        req = r.post(URI, headers=headers, data=Data, proxies=proxy,timeout=timeout, stream=True, verify=False)
        try:
            if (req.json()["status_code"] == 0):
                TotalFailedReq += 1
                if DebugMode == True:
                    print( f"Fail : {TotalFailedReq}")
                else:
                    Title(f"Thread :{str(active_count()-1)} / Hit :{TotalSendedView} / Fail :{TotalFailedReq}")
            else:
                pass
        except:
            TotalSendedView += 1
            print( f"Sended View/Share: {TotalSendedView}")
            Title(f"Thread :{str(active_count()-1)} / Hit :{TotalSendedView} / Fail :{TotalFailedReq}")
    except:
        pass

def ClearURI(link):
    if ("vm.tiktok.com" in itemID or "vt.tiktok.com" in itemID):
        return r.head(itemID, stream=True, verify=False, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
    else:
        return itemID.split("/")[5].split("?", 1)[0]

if (__name__ == "__main__"):
    Clear()
   
    proxy        = ReadFile("Proxies.txt", 'r')
    itemID       = input("Video Link > ", )
    amount       = input("Amount (0=inf) > ", )
    Proxytype    = input("Proxy Type > ", )
    Timeout      = input("Proxy Timeout > ", )
    NThread      = input("Thread Amount > ", )
    ShareChoice  = input("Want Share [y/n] > ", )
    ViewChoice   = input("Want View [y/n] > ", )
    
    if Title("a") == True:
        Debug = input("Debug Fails [y/n] ? > ", )
        if Debug.lower().startswith("y"):
            DebugMode = True
        else:
            DebugMode = False

    if ShareChoice.lower().startswith("y"):
        ShareChoice = True
    elif ShareChoice.lower().startswith("n"):
        ShareChoice = False

    if ViewChoice.lower().startswith("y"):
        ViewChoice = True
    elif ViewChoice.lower().startswith("n"):
        ViewChoice = False

    itemID = ClearURI(itemID)

    ProxyChoose = True
    while ProxyChoose:
        if Proxytype.lower().startswith("h"):
            Proxytype = "http"
            ProxyChoose = False
            print("le proxy choisis est http")
        elif Proxytype.lower().endswith("4"):
            Proxytype = "socks4"
            ProxyChoose = False
        elif Proxytype.lower().endswith("5"):
            Proxytype = "socks5"
            ProxyChoose = False
            print("le proxy est socks5")
        else:
            ProxyChoose = True
            print("Invalid Proxy Type | Choose : Http, Socks4, Socks5")
            Proxytype = input("Proxy Type > ")

    if (int(amount) == 0):
        while True:
            Run = True
            while Run:
                if (active_count() <= int(NThread)):
                    Thread(target=(SendView), args=(itemID,choice(proxy),int(Timeout),Proxytype,)).start()
    else:
       for _ in range(int(amount)):
            Run = True
            while Run:
                if (active_count() <= int(NThread)):
                    Thread(target=(SendView), args=(itemID,choice(proxy),Timeout,Proxytype,)).start()   
    