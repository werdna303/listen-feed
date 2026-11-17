"""Build feed.xml for the Listen podcast from episodes/*.mp3 (+ matching .txt for descriptions).
Usage: python3 build_feed.py BASE_URL   e.g. https://werdna303.github.io/listen-feed/"""
import sys, os, re, subprocess, email.utils, html, json
base = sys.argv[1].rstrip('/') + '/'
here = os.path.dirname(os.path.abspath(__file__))
ep_dir = os.path.join(here, 'episodes')
meta_path = os.path.join(here, 'published.json')   # slug -> first-published timestamp, keeps order stable
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
items = []
import time
for f in sorted(os.listdir(ep_dir)):
    if not f.endswith('.mp3'): continue
    slug = f[:-4]; p = os.path.join(ep_dir, f)
    txt = os.path.join(ep_dir, slug + '.txt')
    lines = open(txt).read().split('\n') if os.path.exists(txt) else [slug]
    title = re.sub(r'^Listen\.\s*', '', lines[0]).strip().rstrip('.')
    body = ' '.join(l for l in lines[2:] if l.strip())
    desc = body[:600].rsplit(' ', 1)[0] + '...'
    dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
    if slug not in meta: meta[slug] = time.time() + len(meta)  # stable order for a batch
    items.append((meta[slug], slug, title, desc, os.path.getsize(p), int(dur)))
json.dump(meta, open(meta_path,'w'), indent=1)
items.sort(reverse=True)
e = html.escape
out = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
 '<channel>', '<title>Listen</title>', f'<link>{base}</link>', '<language>en-ca</language>',
 '<description>Half-hour teaching episodes for morning runs.</description>',
 '<itunes:author>Listen</itunes:author>', '<itunes:explicit>false</itunes:explicit>',
 '<itunes:block>Yes</itunes:block>',
 f'<itunes:image href="{base}cover.jpg"/>', f'<image><url>{base}cover.jpg</url><title>Listen</title><link>{base}</link></image>',
 '<itunes:category text="Education"/>']
for ts, slug, title, desc, size, dur in items:
    url = base + 'episodes/' + slug + '.mp3'
    out += ['<item>', f'<title>{e(title)}</title>', f'<description>{e(desc)}</description>',
            f'<enclosure url="{url}" length="{size}" type="audio/mpeg"/>',
            f'<guid isPermaLink="false">listen-{slug}</guid>',
            f'<pubDate>{email.utils.formatdate(ts)}</pubDate>',
            f'<itunes:duration>{dur}</itunes:duration>', '</item>']
out += ['</channel>', '</rss>']
open(os.path.join(here, 'feed.xml'), 'w').write('\n'.join(out) + '\n')
print(len(items), 'episodes ->', base + 'feed.xml')
