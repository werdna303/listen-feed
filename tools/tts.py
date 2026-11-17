import sys, re, subprocess, numpy as np, soundfile as sf, time
from kokoro_onnx import Kokoro
import os
V=os.environ.get('KOKORO_DIR', os.path.expanduser('~/kokoro/'))
k = Kokoro(V+'kokoro-v1.0.int8.onnx', V+'voices-v1.0.bin')
src, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv)>3 else 'am_michael'
text = open(src).read()
paras = [p.strip() for p in re.split(r'\n\s*\n|\n', text) if p.strip()]
chunks=[]
for p in paras:
    sents = re.split(r'(?<=[.!?])\s+', p); cur=''
    for s in sents:
        if len(cur)+len(s) > 400 and cur: chunks.append(cur); cur=s
        else: cur = (cur+' '+s).strip()
    if cur: chunks.append(cur)
    chunks.append(None)  # paragraph pause
audio=[]; sr=24000; t=time.time()
for c in chunks:
    if c is None: audio.append(np.zeros(int(sr*0.6),dtype=np.float32)); continue
    a, sr = k.create(c, voice=voice, speed=1.0, lang='en-us'); audio.append(a.astype(np.float32))
wav = out[:-4]+'.wav'; sf.write(wav, np.concatenate(audio), sr)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',wav,'-ac','1','-b:a','64k',out],check=True)
import os; os.remove(wav); print(out, round(time.time()-t), 's')
