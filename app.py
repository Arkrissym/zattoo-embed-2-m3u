import sys
import requests
from cachetools import cached, TTLCache
from threading import Lock
from flask import Flask, redirect, abort
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

out_m3u = ""
channels = {}

cache_lock = Lock()

@cached(cache=TTLCache(maxsize=32, ttl=3600), lock=cache_lock)
def get_stream_url(channel, stream_type):
    response = requests.get("https://embed.zattoo.com/token.json")
    response.raise_for_status()

    session_token = response.json()["session_token"]
    if not session_token:
        raise Exception("session_token invalid")

    data = {    "https_watch_urls": True,
                "partner_site": channel,
                "session_token": session_token,
                "stream_type": stream_type,
                "uuid": session_token
            }
    response = requests.post(f"https://embed.zattoo.com/zapi/watch/live/{channel}",
                                data=data,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
    response.raise_for_status()

    url = response.json()["stream"]["url"]
    if not url:
        raise Exception("invalid stream url")

    print(f"Resolved url for {channel}:{stream_type} : {url}")

    return url

@app.get("/m3u")
def get_m3u():
    return out_m3u

@app.get("/<channel>")
def get_stream(channel):
    if not channel in channels.keys():
        abort(404)

    url = get_stream_url(channel, channels[channel])
    return redirect(url)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python proxy.py /path/to/in.m3u host_or_ip")
    else:
        in_file=sys.argv[1]
        with open(in_file, "r") as file:
            for line in file.readlines():
                if line.startswith("#"):
                    out_m3u += line
                else:
                    parts = line.split('.')
                    if len(parts) != 2:
                        raise Exception("Invalid input: " + line)

                    t = parts[1]
                    if t.startswith("hls"):
                        t = "hls"
                    elif t.startswith("dash"):
                        t = "dash"
                    else:
                        raise Exception("Invalid stream type: " + t)
                    channels[parts[0]] = t

                    out_m3u += f"http://{sys.argv[2]}/{parts[0]}\n"

            file.close()

        app.run(host="0.0.0.0", port=5000, debug=False)
c
