// Usage: node render.js <script.json> <out.mp4> [--stills=0.3,5,12] [--check] [--silent] [--copy-only]
// Plans timings from the script, renders template/page.html frame-by-frame with headless Chromium, and encodes a
// 1080x1920 30 fps MP4 with ffmpeg. Audio is assets/ragtime-loop.m4a (the original synthesized ragtime) unless --silent.
// Also writes <out>_copy.md (caption, hashtags, YouTube Shorts title, Pinterest title + description).
const {chromium}=require('playwright');
const {spawn}=require('child_process');const {plan,MIN,MAXD}=require('./plan.js');const fs=require('fs');const path=require('path');
const [,, scriptPath, outMp4, ...rest]=process.argv;
const stills=(rest.find(a=>a.startsWith('--stills='))||'').split('=')[1];
const check=rest.includes('--check'), silent=rest.includes('--silent'), notext=rest.includes('--notext'), copyOnly=rest.includes('--copy-only');
const FPS=30;
const LINKS=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../links.json')));
// which links belong to a video follows from its CTA (on-screen CTA stays "link in bio"; URLs only go in copy files)
function linksFor(cta){
 if(/Start Kit/.test(cta))return ['kit'];
 if(/Parent Script/.test(cta))return ['cards'];
 if(/Workbook for Teens/.test(cta))return ['teen-workbook','teen-amazon'];
 if(/Executive Function for Kids/.test(cta))return ['kids-book'];
 throw new Error('no link mapping for CTA: '+cta);
}
function writeCopy(script,total,outMp4){
 const c=script.copy||{};const L=linksFor(script.cta).map(k=>LINKS[k]);const main=L[0];
 const urls=L.map(l=>`- ${l.label}: ${l.url}`).join('\n');
 fs.writeFileSync(outMp4.replace(/\.mp4$/,'_copy.md'),
`# ${script.id} - ${script.title}

- Audience: ${script.audience}
- Theme: ${script.theme}
- Length: ${total.toFixed(1)} s, 1080x1920, original synthesized ragtime track (swap for a trending sound in-app if you like)
- On-screen CTA: ${script.cta} (no URL on screen)

## Links for this video

${urls}

## Caption (TikTok / Instagram / Facebook)

${c.caption}

${main.label}: ${main.url}

${(c.hashtags||[]).join(' ')}

_TikTok and Instagram captions don't make links clickable, so keep "link in bio" there and put ${main.url} in the bio link. Facebook can keep the URL line._

## YouTube Shorts

**Title:** ${c.yt_title}

**Description:**

${(c.caption||'').replace(/:? ?link in bio\.?/i,'.').replace(/\.\./g,'.')}

${urls}

${(c.hashtags||[]).join(' ')} #Shorts

## Pinterest

**Pin title:** ${c.pin_title}

**Pin description:** ${c.pin_desc} Learn more: ${main.url}

**Destination link:** ${main.url}
`);
}

// Text/box elements that must never overlap each other. Text-only ones use tight glyph rects, boxed ones use their box.
const TEXT_SEL='.hline,.sline,.chead,.trylabel,.ctext,#end .tag';
const BOX_SEL='.label,.card,.sticky,.bigchip,.bookimg,#end .cta,#end img';
(async()=>{
 const script=JSON.parse(fs.readFileSync(scriptPath));const cfg=plan(script);const MUSIC=path.resolve(__dirname,'../assets/ragtime-loop.m4a');
 if(copyOnly){writeCopy(script,cfg.duration,outMp4);console.log('copy written',outMp4.replace(/\.mp4$/,'_copy.md'));return}
 const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1920}});
 pg.on('pageerror',e=>{console.log('PAGE ERROR',e.message);process.exitCode=1});
 await pg.goto('file://'+path.resolve(__dirname,'../template/page.html'));
 await pg.evaluate(c=>build(c),cfg);await pg.evaluate(()=>{document.getElementById('bg').style.left='0'});
 const total=cfg.duration;
 if(total<MIN||total>MAXD)console.warn(`WARNING: duration ${total}s is outside the ${MIN}-${MAXD} s target`);
 if(check){let bad=0;
  // CTA rule: parent resources (Start Kit, Parent Script Cards) are never the CTA on teen-facing videos, and vice versa
  if(script.audience==='teen'&&!/Workbook for Teens/.test(script.cta)){bad++;console.log('CTA RULE: teen video must end on the Teens workbook, got:',script.cta)}
  if(script.audience==='parent'&&/Teens/.test(script.cta)){bad++;console.log('CTA RULE: parent video must not end on the teen workbook, got:',script.cta)}
  const bounds=await pg.evaluate(()=>H.bounds);
  for(const b of bounds){bad++;console.log('OUTSIDE SAFE ZONE (top 250 / bottom 350 / sides 60):',b)}
  // text must never overlap, including mid-transition: sample every 1/20 s and test every visible pair
  const hits=new Map();
  for(let t=0;t<=total;t+=.05){
   await pg.evaluate(t=>setT(t),t);
   const items=await pg.evaluate(([TS,BS])=>{
    const eff=e=>{let o=1;for(let p=e;p&&p.id!=='stage';p=p.parentElement)o*=+getComputedStyle(p).opacity;return o};
    const out=[];
    for(const [sel,isText] of [[TS,true],[BS,false]])for(const e of document.querySelectorAll(sel)){
     const o=eff(e);if(o<.12)continue;let rects;
     if(isText){const r=document.createRange();r.selectNodeContents(e);rects=[...r.getClientRects()].filter(q=>q.width>2).map(q=>({l:q.left,r:q.right,t:q.top+q.height*.22,b:q.bottom-q.height*.22}))}
     else{const q=e.getBoundingClientRect();rects=[{l:q.left,r:q.right,t:q.top,b:q.bottom}]}
     out.push({n:(e.textContent||e.tagName).trim().slice(0,24),rects})}
    return out},[TEXT_SEL,BOX_SEL]);
   for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
    const A=items[i],B=items[j];if(A.n===B.n)continue;
    for(const a of A.rects)for(const b of B.rects){
     const w=Math.min(a.r,b.r)-Math.max(a.l,b.l),h=Math.min(a.b,b.b)-Math.max(a.t,b.t);
     if(w>4&&h>4){const k=A.n+' x '+B.n;if(!hits.has(k))hits.set(k,t)}}}}
  for(const [k,t] of hits){bad++;console.log(`TEXT OVERLAP at t=${t.toFixed(2)}s: ${k}`)}
  console.log(bad?`${bad} problem(s)`:`checks OK: safe zone + no overlapping text (${total}s)`);await br.close();process.exit(bad?1:0)}
 if(notext)await pg.evaluate(()=>document.body.classList.add('notext'));
 if(stills){for(const s of stills.split(',')){await pg.evaluate(t=>setT(t),+s);await pg.screenshot({path:`${outMp4.replace(/\.mp4$/,'')}_t${s}.png`})}await br.close();return}
 const N=Math.round(total*FPS);
 const audio=silent?['-f','lavfi','-i','anullsrc=r=44100:cl=stereo','-t',String(total),'-filter_complex','[1:a]anull[a]']
  :['-i',MUSIC,'-t',String(total),'-filter_complex',`[1:a]atrim=0:${total},afade=t=in:d=0.3,afade=t=out:st=${(total-1.5).toFixed(2)}:d=1.5[a]`];
 const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-',...audio,'-map','0:v','-map','[a]',
  '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high','-r',String(FPS),
  '-c:a','aac','-b:a','192k','-movflags','+faststart',outMp4],{stdio:['pipe','inherit','inherit']});
 for(let f=0;f<N;f++){await pg.evaluate(t=>setT(t),f/FPS);const buf=await pg.screenshot({type:'jpeg',quality:95});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await br.close();
 writeCopy(script,total,outMp4);
 console.log('rendered',N,'frames,',total,'s ->',outMp4);
})();
