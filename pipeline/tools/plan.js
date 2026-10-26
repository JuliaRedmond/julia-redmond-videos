// Turns a script (beats without timings) into a timed config for template/page.html.
// Ported from the original batch1-v2 planner; adds `checks` beats and a 20-27 s window.
const HOOKD=4.4,END=2.6,HOLD=1.5,TARGET=24.0,MIN=20.0,MAXD=27.0;
const TAG='Less Reminding. More Ownership.';
function lastEvent(b){
 if(b.type==='statement')return Math.max(...b.lines.map((l,i)=>{l=typeof l==='string'?{t:l}:l;return .1+i*1.2+(l.strike?1.4:(l.hl?1.05:0))}));
 if(b.type==='try')return (!b.label?.length?.7:(b.pre?.length?.95:.3))+.7;
 if(b.type==='cover')return 1.2+((b.lines||[]).length?(b.lines.length-1)*.6+.6:0);
 if(b.type==='chips')return .2+5*.35+.45;
 if(b.type==='checks'){const first=(b.header||[]).length?.75:.35;return first+(b.items.length-1)*1.4+.75}
 throw new Error('no timing for beat type '+b.type);
}
function plan(sp){
 const mids=sp.beats.slice(1);const fixed=HOOKD+END+HOLD*mids.length;const E=mids.reduce((a,b)=>a+lastEvent(b),0);
 const s=Math.max(1.07,Math.min(2.0,(TARGET-fixed)/E));let total=fixed+s*E;
 const w_h=1,w_m=2,w_e=.5,extra=Math.max(0,MIN-total),W=w_h+w_m*mids.length+w_e;
 const ph=extra*w_h/W,pm=extra*w_m/W,pe=extra*w_e/W;let t=0;const out=[];
 sp.beats.forEach((b0,k)=>{const b={...b0};let d;
  if(k===0)d=HOOKD+ph;else{b.sc=Math.round(s*1000)/1000;d=lastEvent(b)*s+HOLD+pm}
  b.start=Math.round(t*1000)/1000;b.end=Math.round((t+d)*1000)/1000;t+=d;out.push(b)});
 out.push({type:'end',start:Math.round(t*1000)/1000,end:Math.round((t+END+pe)*1000)/1000,tagline:sp.tagline||TAG,cta:sp.cta});t+=END+pe;
 return {id:sp.id,skills:sp.skills,duration:Math.round(t*100)/100,focus:sp.focus??.42,beats:out};
}
module.exports={plan,MIN,MAXD};
