#### A little script to extract stream urls from tv channels using embedded zattoo players.

To find the required "channel" open your browsers developer tools and search for a similiar link: https://embed.zattoo.com/zapi/watch/live/{channel}

#### Example in.m3u
``` m3u
#EXTM3U
#EXTINF:-1 tvg-name="channel name" tvg-id="channel id" tvg-logo="logo_url",channel_name
{channel}.dash

```
If yout prefer HLS over DASH replace .dash with .hls


#### Example docker-compose.yml
``` yml
services:
  app:
    image: ghcr.io/arkrissym/zattoo-embed-2-m3u:main
    restart: always
    ports:
      - 5000:5000
    environment:
      - HOST_IP=your_host:5000
    volumes:
      - ./in.m3u:/in.m3u
```
