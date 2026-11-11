"""Two-pass loudness normalization to a new MP3; retains source. Requires ffmpeg."""
import argparse,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('output',type=Path); a=p.parse_args()
assert not a.output.exists(), 'Refusing overwrite'
base=['ffmpeg','-hide_banner','-nostdin','-i',str(a.input)]
r=subprocess.run(base+['-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(re.findall(r'\{[^{}]*\}',r.stderr,re.S)[-1])
f='loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:print_format=json:'+':'.join(f'{k}={m[v]}' for k,v in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
a.output.parent.mkdir(parents=True,exist_ok=True)
r=subprocess.run(base+['-af',f,'-ar','44100','-c:a','libmp3lame','-b:a','128k','-n',str(a.output)],capture_output=True,text=True,check=True)
a.output.with_suffix('.loudness.json').write_text(json.dumps({'input':str(a.input),'first_pass':m,'second_pass':json.loads(re.findall(r'\{[^{}]*\}',r.stderr,re.S)[-1])},indent=2),encoding='utf-8')
print(a.output)
