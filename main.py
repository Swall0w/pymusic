import feedparser
import vlc
import argparse
import sys
import time

def arg():
    parser = argparse.ArgumentParser(description='Simple Podcast Streamer.')
    parser.add_argument('--add','-a',type=str,help='Podcast URL')
    parser.add_argument('--list','-l',action='store_true',help='Podcast list')
    parser.add_argument('--delete','-d',type=int,help='delete podcast channel.')
    parser.add_argument('--detail',type=int,default=-1,help='podcast channel detail.')
    parser.add_argument('--play','-p',action='store_true',help='Podcast URL')
    parser.add_argument('--download',action='store_true',help='Podcast Download')
    parser.add_argument('--channel','-c',type=int,help='Podcast Channel that you want to listen.')
    parser.add_argument('--track','-t',type=int,help='Podcast tracl that you want to listen.')
    return parser.parse_args()

def converttime(time):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    return int(hours), int(minutes), int(seconds)

def stream(rss_url, track):
    rssdata = feedparser.parse(rss_url).entries[track]
    print(rssdata.summary)
    mp3_url = rssdata.media_content[0]['url']
    player = vlc.MediaPlayer(mp3_url)
    player.play()
    while True:
        hours, minutes, seconds = converttime(player.get_time()/1000)
        m_hours, m_minutes, m_seconds = converttime(player.get_length()/1000)
        comment = '\r{0}  time: {1}:{2}:{3} / {4}:{5}:{6}'.format('playing...', hours, minutes, seconds, m_hours, m_minutes, m_seconds)
        sys.stdout.write(comment)
        sys.stdout.flush()
        time.sleep(0.1)

#    RSS_URL = 'http://feeds.feedburner.com/tabitabi-podcast/artlife'
#    news_dic = feedparser.parse(RSS_URL)
#    print(news_dic.feed.title)
#    print(news_dic.key)
#
#    for index, entry in enumerate(news_dic.entries):
#        title = entry.title
#        link  = entry.link
#        media = entry.media_content
#        if index == 0:
#            mp3_url = media[0]['url']
#            player = vlc.MediaPlayer(mp3_url)
#            player.play()
#            while True:
#                print('playing')
#                pass
##        filename = wget.download(mp3_url)

def detail(channel_url):
    rssdata = feedparser.parse(channel_url)
    for index, entry in enumerate(rssdata.entries):
        print(index, entry.title)

def main():
    args = arg()

# Load Channels
    with open('.channels','r') as f:
        channels = [item.strip() for item in f.readlines()]
    
    if args.list:
        for index, channel in enumerate(channels):
            print(index, channel)

    if args.detail >= 0:
        detail(channels[args.detail])

    if args.play:
        stream(channels[args.channel], args.track)




if __name__ == '__main__':
    main()
