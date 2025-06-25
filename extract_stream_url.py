import requests
import sys

def extract_stream_url(channel, logo_url, stream_type):
    response = requests.get("https://embed.zattoo.com/token.json")
    response.raise_for_status()

    session_token = response.json()["session_token"]
    if not session_token:
        raise  "session_token invalid"

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
        raise "invalid stream url"

    print("#EXTM3U")
    print(f"#EXTINF:-1 tvg-name=\"{channel}\" tvg-id=\"{channel}\" tvg-logo=\"{logo_url}\",{channel}")
    print(url)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python extract_stream_url.py channel logo_url (hls|dash)")
    else:
        extract_stream_url(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else "hls")
