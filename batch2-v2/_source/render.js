const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const {spawn,execFileSync}=require('child_process');const fs=require('fs');const path=require('path');
const [,, cfgPath, outMp4, audioWav, ...rest]=process.argv;
const stills=(rest.find(a=>a.startsWith('--stills='))||'').split('=')[1];
const noText=rest.includes('--notext');
(async()=>{
 const cfg=JSON.parse(fs.readFileSync(cfgPath));const B=__dirname;
 const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+B+'/page.html');await pg.evaluate(c=>build(c),cfg);
 await pg.evaluate(()=>{document.getElementById('bg').style.left='0'});
 if(stills){for(const s of stills.split(',')){await pg.evaluate(t=>setT(t),+s);await pg.screenshot({path:`${path.dirname(outMp4)}/${path.basename(outMp4,'.mp4')}_t${s}.png`})}await br.close();return}
 const N=Math.round(cfg.duration*30);
 const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',audioWav,
  '-t',String(cfg.duration),'-filter_complex',`[1:a]atrim=0:${cfg.duration},afade=t=in:d=0.3,afade=t=out:st=${cfg.duration-1.5}:d=1.5[a]`,'-map','0:v','-map','[a]',
  '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high','-r','30','-c:a','aac','-b:a','192k','-movflags','+faststart',outMp4],{stdio:['pipe','inherit','inherit']});
 for(let f=0;f<N;f++){await pg.evaluate(t=>setT(t),f/30);const buf=await pg.screenshot({type:'jpeg',quality:95});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await br.close();console.log('done',N);
})();
