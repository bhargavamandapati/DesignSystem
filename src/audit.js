/* ---- live compliance audit: automotive rules + theme consistency ---- */
const TOUCH_SEL='.a-btn,.a-ib,.a-chip,.a-sw,.a-check,.a-radio,.a-tab,.a-seg button,.a-nav a,.a-menu li,.a-fab,.a-rail a,.a-kb button,.a-tgl,.a-li.click,.a-app,.a-slider input,.a-lvl,.dialpad button';
const HIT_EXP={'a-chip':[0,12],'a-sw':[4,12],'a-check':[32,32],'a-radio':[32,32]}; // ::before expansions (w,h)
const lumH=h=>{const c=[1,3,5].map(i=>parseInt(h.substr(i,2),16)/255).map(v=>v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4));return .2126*c[0]+.7152*c[1]+.0722*c[2]};
const crH=(a,b)=>{const x=lumH(a),y=lumH(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const rgbOf=c=>{const m=c&&c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[ ,\/]+/).map(Number);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}};
function hueOf(c){const mx=Math.max(c.r,c.g,c.b),mn=Math.min(c.r,c.g,c.b),d=mx-mn;if(d<14)return null;let h;if(mx===c.r)h=((c.g-c.b)/d+6)%6;else if(mx===c.g)h=(c.b-c.r)/d+2;else h=(c.r-c.g)/d+4;return h*60}
const hueDist=(a,b)=>{const d=Math.abs(a-b)%360;return d>180?360-d:d};
const hexRgb=h=>({r:parseInt(h.substr(1,2),16),g:parseInt(h.substr(3,2),16),b:parseInt(h.substr(5,2),16)});
function auditTheme(id){setTheme(id);const t=T(),res={id,name:THEMES[id].name};
 /* 1. contrast of every spec pair (non-disabled) */
 const cf=[];let cn=0;
 for(const [sec,list] of Object.entries(SPECS))list.forEach(c=>c.st.forEach(r=>{if(/disabled|driving|scrim|track|skeleton|divider/i.test(r[0])||!r[2]||r[2]==='—')return;const fg=resolveHex(r[2]);if(!fg)return;const bg=resolveHex(r[1])||t.surface;cn++;const k=crH(fg,bg);const need=r[2]==='outline'?3:4.5;if(k<need)cf.push(`${c.n} · ${r[0]}: ${r[2]} on ${r[1]==='—'?'surface':r[1]} = ${k.toFixed(2)}:1`)}));
 [['outline','surface'],['outline','surfaceContainer'],['outline','surfaceContainerHigh'],['onPrimaryContainer','surface'],['onPrimaryContainer','surfaceContainerHigh'],['primary','surface']].forEach(([a,b])=>{cn++;const k=crH(t[a],t[b]);if(k<3)cf.push(`${a} on ${b} = ${k.toFixed(2)}:1 (UI needs 3:1)`)});
 res.contrast={checked:cn,fail:cf};
 /* 2. touch targets */
 const tf=[];let tn=0;
 $$(TOUCH_SEL,$('main')).forEach(e=>{if(e.closest('.a-nav-hidden')||!e.offsetParent&&getComputedStyle(e).position!=='fixed')return;const w=e.offsetWidth,h=e.offsetHeight;if(!w||!h)return;tn++;let ex=[0,0];for(const k in HIT_EXP)if(e.classList.contains(k))ex=HIT_EXP[k];
  const hw=w+ex[0],hh=h+ex[1];if(e.matches('.a-slider input')){if(hh<76)tf.push(`${e.className||e.tagName}: ${hw}×${hh}`);return}
  if(Math.min(hw,hh)<76)tf.push(`${(e.className||e.tagName).toString().split(' ').slice(0,2).join('.')}: ${hw}×${hh} dp`)});
 res.touch={checked:tn,fail:[...new Set(tf)]};
 /* 3. text size */
 const small=[],mid={};let fn=0;
 const isComp=e=>{for(let n=e;n&&n.id!=='main';n=n.parentElement){if([...n.classList].some(c=>/^a-(?!root$)/.test(c)))return true}return false};
 $$('main .a-root *').forEach(e=>{if(e.closest('svg')||e.closest('.frame-wrap.anat')||e.closest('.cap,small,code,pre,.spec,.specblock,.tw,.viewbar,.icons,.codewrap,.ty,.fcmp,.card-d,.themecards,.stage>.cap')||!isComp(e))return;const own=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length);if(!own)return;fn++;const fs=parseFloat(getComputedStyle(e).fontSize);if(fs<20)small.push(`${e.tagName.toLowerCase()}.${(e.className||'').toString().split(' ')[0]} "${e.textContent.trim().slice(0,18)}" ${fs}px`);else if(fs<24)mid[fs]=(mid[fs]||0)+1});
 res.fonts={checked:fn,fail:[...new Set(small)],mid:Object.entries(mid).map(([k,v])=>`${v}× ${k}sp`).join(', ')||'none'};
 /* 4. borders match theme hue */
 const ph=hueOf(hexRgb(t.primary)),sem=[t.error,t.success,t.warning,t.errorContainer,t.onErrorContainer,t.warningContainer,t.successContainer].map(h=>h.toLowerCase());
 const bf=[];let bn=0;const seen=new Set();
 $$('main .a-root *, main .stage, main .card-d, main .tw, main .frame-wrap, main .themecard').forEach(e=>{if(e.closest('.themecards')||e.closest('#icDetail')||e.id==='cfg'||e.id==='cbg')return;const s=getComputedStyle(e);
  const sources=[['border',s.borderTopWidth!=='0px'&&s.borderTopStyle!=='none'?s.borderTopColor:null],['outline',s.outlineStyle!=='none'&&s.outlineWidth!=='0px'?s.outlineColor:null]];
  (s.boxShadow||'').split(/,(?![^(]*\))/).forEach(p=>{if(/inset/.test(p)&&/0px 0px 0px/.test(p)){const m=p.match(/rgba?\([^)]+\)/);if(m)sources.push(['inset-ring',m[0]])}});
  sources.forEach(([k,col])=>{const c=rgbOf(col);if(!c||c.a<.05)return;const key=k+col+e.className;if(seen.has(key))return;seen.add(key);bn++;
   const hex='#'+[c.r,c.g,c.b].map(v=>Math.round(v).toString(16).padStart(2,'0')).join('');if(sem.includes(hex)||[t.surface,t.background,t.surfaceContainerLowest,t.surfaceContainerLow,t.surfaceContainer,t.surfaceContainerHigh,t.surfaceContainerHighest].some(x=>x.toLowerCase()===hex))return;
   const h=hueOf(c);if(h===null){bf.push(`${k} neutral gray ${hex} on .${(e.className||e.tagName).toString().split(' ')[0]}`);return}
   if(hueDist(h,ph)>22)bf.push(`${k} hue ${Math.round(h)}° (theme ${Math.round(ph)}°) on .${(e.className||e.tagName).toString().split(' ')[0]}`)})});
 res.borders={checked:bn,fail:[...new Set(bf)]};
 return res}
function auditHtml(rs){const ok=a=>a.length===0?'<span class="pill ok">Pass</span>':`<span class="pill no">${a.length} issue${a.length>1?'s':''}</span>`;
 return `<div class="tw"><table class="tbl"><thead><tr><th>Theme</th><th>Contrast (text 4.5:1 · UI 3:1)</th><th>Touch targets ≥ 76 dp</th><th>Text ≥ 20 sp</th><th>Borders in theme hue</th></tr></thead><tbody>`+rs.map(r=>`<tr><td><b>${r.name}</b></td><td>${ok(r.contrast.fail)} <small>${r.contrast.checked} pairs</small></td><td>${ok(r.touch.fail)} <small>${r.touch.checked} controls</small></td><td>${ok(r.fonts.fail)} <small>${r.fonts.checked} text nodes · 20–23sp: ${r.fonts.mid}</small></td><td>${ok(r.borders.fail)} <small>${r.borders.checked} borders/outlines</small></td></tr>`).join('')+'</tbody></table></div>'+
 rs.filter(r=>r.contrast.fail.length+r.touch.fail.length+r.fonts.fail.length+r.borders.fail.length).map(r=>`<h4>${r.name} — details</h4><pre><code>${[...r.contrast.fail.map(x=>'contrast  '+x),...r.touch.fail.map(x=>'touch     '+x),...r.fonts.fail.map(x=>'font      '+x),...r.borders.fail.map(x=>'border    '+x)].join('\n').replace(/</g,'&lt;')}</code></pre>`).join('')}
function runAudit(all){const cur=root.dataset.theme,ids=all?TORDER:[cur];const rs=ids.map(auditTheme);setTheme(cur);$('#auditOut').innerHTML=auditHtml(rs);window.__auditResult=rs;return rs}
$('#auditOne').onclick=()=>runAudit(false);$('#auditAll').onclick=()=>runAudit(true);
window.runAudit=runAudit;
