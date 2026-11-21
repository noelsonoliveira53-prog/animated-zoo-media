"""Rebuild a thumbnail from the finished repo MP4 with new 3-word text (same style as finish.py)."""
import json, subprocess, sys, os
sys.path.insert(0, '/root/zoo/blender/zoo3d'); import finish as F
REPO = '/home/claude/animated-zoo-media'
def rethumb(sid, words, folder):
    job = json.load(open(f'/root/zoo/blender/zoo3d/jobs/{sid}.json')) if os.path.exists(f'/root/zoo/blender/zoo3d/jobs/{sid}.json') else {}
    tf = job.get('thumb_frame', 120) / 24
    mp4 = os.path.join(REPO, folder if folder != '.' else '', f'{sid}.mp4')
    ch = job.get('channel', 'zoo')
    tsub = f'/tmp/{sid}_thumb.ass'
    open(tsub, 'w').write(f"""[Script Info]
PlayResX: 1280
PlayResY: 720
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Baloo 2 ExtraBold,150,{F.HILITE.get(ch, '&H0000D7FF&')},&H00FFFFFF&,&H00301808&,&H96000000&,-1,0,0,0,100,100,2,-4,1,10,6,7,40,40,26,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:10.00,T,,0,0,0,,{words}
""")
    dst = os.path.join(REPO, 'brand', folder if folder != '.' else 'zoo', f'thumb_{sid}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{tf:.2f}', '-i', mp4, '-frames:v', '1',
                    '-vf', f'crop=iw*0.82:ih*0.82:(iw-ow)/2:ih*0.02,scale=1280:720,eq=saturation=1.15:contrast=1.05,subtitles={tsub}:fontsdir={F.FONT_DIR}', dst], check=True)
    return dst
if __name__ == '__main__':
    for sid, words, folder in json.load(open(sys.argv[1])):
        print(rethumb(sid, words, folder))
