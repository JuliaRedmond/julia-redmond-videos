// Usage: node render.js <script.json> <out.mp4> [--stills=0.1,3,9] [--check]
// Renders template/page.html frame-by-frame with headless Chromium, encodes silent 1080x1920 30fps MP4 with ffmpeg,
// and writes <out>_copy.md (caption, hashtags, YouTube Shorts title, Pinterest title + description).
const {chromium}=require('playwright');
const {spawn}=require('child_process');const fs=require('fs');const path=require('path');
const [,, scriptPath, outMp4, ...rest]=process.argv;
const stills=(rest.find(a=>a.startsWith('--stills='))||'').split('=')[1];
const check=rest.includes('--check');
const FPS=30;
// Safe zone (TikTok/Reels/Shorts UI overlays): keep text out of top 250 px, bottom 380 px, sides 60 px.
const SAFE={l:60,r:1020,t:250,b:1540};
(async()=>{
 const cfg=JSON.parse(fs.readFileSync(scriptPath));
 const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1920}});
 await pg.goto('file://'+path.resolve(__dirname,'../template/page.html'));
 await pg.evaluate(()=>document.fonts.ready);
 const total=await pg.evaluate(c=>build(c),cfg);
 await pg.evaluate(()=>document.fonts.ready);
 if(total<20||total>40)console.warn(`WARNING: duration ${total}s is outside the 20-40 s target`);
 if(check){let bad=0;
  const times=[];let t0=0;for(const s of cfg.scenes){times.push(t0+s.dur-.4);t0+=s.dur}times.push(t0+4);
  for(const t of times){await pg.evaluate(t=>setT(t),t);
   const r=await pg.evaluate(S=>[...document.querySelectorAll('.scene .it, #end img, #tag, #cta')].filter(e=>{const o=+getComputedStyle(e).opacity;let p=e.parentElement,q=o;while(p&&p.id!=='stage'){q*=+getComputedStyle(p).opacity;p=p.parentElement}return q>.9}).map(e=>{const rg=document.createRange();rg.selectNodeContents(e);const rr=[...rg.getClientRects()];const b=e.getBoundingClientRect();const L=Math.min(b.left,...rr.map(x=>x.left)),R=Math.max(b.right,...rr.map(x=>x.right));return {c:e.className||e.id,l:L,r:R,t:b.top,b:b.bottom,sw:false};}),SAFE);
   for(const e of r){if(e.sw||e.l<SAFE.l||e.r>SAFE.r||e.t<SAFE.t||e.b>SAFE.b){bad++;console.log(`t=${t.toFixed(1)} OUTSIDE SAFE ZONE / OVERFLOW: ${e.c} [${e.l|0},${e.t|0}]-[${e.r|0},${e.b|0}]`)}}}
  console.log(bad?`${bad} safe-zone problem(s)`:`safe-zone check OK (${total}s)`);await br.close();process.exit(bad?1:0)}
 if(stills){for(const s of stills.split(',')){await pg.evaluate(t=>setT(t),+s);await pg.screenshot({path:`${outMp4.replace(/\.mp4$/,'')}_t${s}.png`})}await br.close();return}
 const N=Math.round(total*FPS);
 const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-',
  '-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-t',String(total),
  '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high','-r',String(FPS),
  '-c:a','aac','-b:a','96k','-movflags','+faststart',outMp4],{stdio:['pipe','inherit','inherit']});
 for(let f=0;f<N;f++){await pg.evaluate(t=>setT(t),f/FPS);const buf=await pg.screenshot({type:'jpeg',quality:95});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await br.close();
 const c=cfg.copy||{};
 fs.writeFileSync(outMp4.replace(/\.mp4$/,'_copy.md'),
`# ${cfg.id} - ${cfg.title}\n\n- Audience: ${cfg.audience}\n- Theme: ${cfg.theme}\n- Length: ${total.toFixed(1)} s, 1080x1920, silent (add trending audio in-app)\n- On-screen CTA: ${cfg.end.cta} (${cfg.end.cta2||'Link in bio'}). No URL on screen; add the landing-page link only once approved.\n\n## Caption (TikTok / Instagram / Facebook)\n\n${c.caption}\n\n${(c.hashtags||[]).join(' ')}\n\n## YouTube Shorts title\n\n${c.yt_title}\n\n## Pinterest\n\n**Pin title:** ${c.pin_title}\n\n**Pin description:** ${c.pin_desc}\n`);
 console.log('rendered',N,'frames,',total,'s ->',outMp4);
})();
