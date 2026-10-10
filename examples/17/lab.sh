#!/usr/bin/env bash
set -euo pipefail
mkdir -p output
ffmpeg -hide_banner -loglevel error -n -f lavfi -i 'testsrc2=size=1280x720:rate=30' -f lavfi -i 'sine=frequency=440:sample_rate=48000' -t 8 -c:v libx264 -pix_fmt yuv420p -c:a aac output/source.mp4
ffmpeg -hide_banner -loglevel error -n -ss 2 -i output/source.mp4 -t 4 -map 0:v:0 -map 0:a:0 -c:v libx264 -pix_fmt yuv420p -c:a aac output/clip.mp4
ffmpeg -hide_banner -loglevel error -n -i output/clip.mp4 -vf 'crop=720:720:280:0,scale=360:360' -c:v libx264 -pix_fmt yuv420p -c:a copy output/square.mp4
ffprobe -v error -show_streams -show_format -of json output/square.mp4 > output/report.json
python3 - <<'CHECK'
import json
from pathlib import Path
r=json.loads(Path('output/report.json').read_text())
v=next(s for s in r['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(360,360)
assert abs(float(r['format']['duration'])-4)<0.15
assert any(s['codec_type']=='audio' for s in r['streams'])
print('PASS: 360x360, approximately 4 seconds, audio present')
CHECK
