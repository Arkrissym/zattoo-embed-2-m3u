#### A little script to extract stream urls from tv channels using embedded zattoo players.

To find the required "channel name" open your browsers developer tools and search for a similiar link: https://embed.zattoo.com/zapi/watch/live/{channel}

#### Example docker-compose.yml
``` yml
services:
  systa-rest:
    image: ghcr.io/arkrissym/zattoo-embed-2-m3u:main
    restart: always
    environment:
      - CHANNEL={channel}
      - LOGO_URL={logo_url}
      - STREAM_TYPE=dash
      - INTERVAL=86400
    volumes:
      - ./out:/out
```
