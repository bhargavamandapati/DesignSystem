(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const kebab=s=>s.replace(/[A-Z]/g,m=>'-'+m.toLowerCase());
const store={get(k,d){try{return localStorage.getItem(k)||d}catch(e){return d}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};

/* ---------- icons (Aurora set, generated from tools/icons_src.py) ---------- */
const ICONS=ICONLIB.icons;const byName={};ICONS.forEach(i=>byName[i.n]=i);
const pathsSvg=i=>i.p.map(([d,f])=>`<path d="${d}"${f?' fill="currentColor"':''}/>`).join('');
document.body.insertAdjacentHTML('afterbegin','<svg width="0" height="0" style="position:absolute" aria-hidden="true">'+ICONS.map(i=>`<symbol id="i-${i.n}" viewBox="0 0 24 24">${pathsSvg(i)}</symbol>`).join('')+'</svg>');
const icon=n=>{if(!byName[n])console.warn('missing icon',n);return `<svg class="i" aria-hidden="true"><use href="#i-${n}"/></svg>`};
function expandIcons(root=document){$$('ic',root).forEach(e=>{const t=document.createElement('span');t.style.display='contents';t.innerHTML=icon(e.getAttribute('n'));e.replaceWith(t.firstChild)})}
expandIcons();

/* ---------- theme / driving ---------- */
const root=document.documentElement;
function setTheme(t){root.dataset.theme=t;store.set('aurora-theme',t);
 $('#themeBtn').innerHTML=(t==='night'?icon('moon'):icon('bright'))+' '+(t==='night'?'Night':'Day');
 $('#themeBtn').setAttribute('aria-pressed',t==='night');
 ['roleTheme','a11yTheme'].forEach(i=>{const e=$('#'+i);if(e)e.textContent=t==='night'?'Night':'Day'});
 renderRoles();renderContrast();renderExport();renderSpecs();}
function setDriving(d){document.body.dataset.driving=d;store.set('aurora-drv',d);
 $('#drvBtn').innerHTML=icon('car')+' '+(d?'Driving':'Parked');$('#drvBtn').setAttribute('aria-pressed',d);
 $$('.drvlabel').forEach(e=>e.textContent=d?'Driving':'Parked');}
$('#themeBtn').onclick=()=>setTheme(root.dataset.theme==='night'?'day':'night');
$('#drvBtn').onclick=()=>setDriving(document.body.dataset.driving!=='true');
$('#menuBtn').onclick=()=>document.body.classList.toggle('nav-open');

/* ---------- helpers ---------- */
function lum(h){const c=[1,3,5].map(i=>parseInt(h.substr(i,2),16)/255).map(v=>v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4));return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function ratio(a,b){const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
const T=()=>TOKENS[root.dataset.theme];
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');clearTimeout(toast.i);toast.i=setTimeout(()=>t.classList.remove('show'),1500)}
async function copy(txt){try{await navigator.clipboard.writeText(txt)}catch(e){const a=document.createElement('textarea');a.value=txt;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(_){}a.remove()}toast('Copied')}

/* ---------- spec chips ---------- */
$$('[data-spec]').forEach(e=>{e.classList.add('spec');e.innerHTML=e.dataset.spec.split(';').map(p=>{const [k,v]=p.split('|');return `<span><b>${k}</b>${v||''}</span>`}).join('')});

/* ---------- color ---------- */
(function(){const w=$('#tonalpal');let h='';
 for(const [name,steps] of Object.entries(TOKENS.tonal)){h+=`<div class="tonalrow"><div class="n">${name}</div>`+Object.entries(steps).map(([k,v])=>`<div class="sw" style="background:${v};color:${+k>=60?'#000':'#fff'}" title="${name} ${k} ${v}">${k}</div>`).join('')+'</div>'}
 w.innerHTML=h;})();
const ROLE_GROUPS={'roles-accent':['primary','onPrimary','primaryContainer','onPrimaryContainer','secondary','onSecondary','secondaryContainer','onSecondaryContainer','tertiary','onTertiary','tertiaryContainer','onTertiaryContainer'],
'roles-status':['error','onError','errorContainer','onErrorContainer','success','onSuccess','successContainer','onSuccessContainer','warning','onWarning','warningContainer','onWarningContainer'],
'roles-surface':['background','onBackground','surface','onSurface','surfaceVariant','onSurfaceVariant','surfaceContainerLowest','surfaceContainerLow','surfaceContainer','surfaceContainerHigh','surfaceContainerHighest','outline','outlineVariant','inverseSurface','inverseOnSurface','inversePrimary']};
function renderRoles(){const t=T();for(const [id,list] of Object.entries(ROLE_GROUPS)){
 $('#'+id).innerHTML=list.map(r=>{const bg=t[r];const isOn=r.startsWith('on')&&r!=='onSurface'&&false;
  // pick readable label color
  const fg=ratio(bg,'#000000')>ratio(bg,'#FFFFFF')?'#000000':'#FFFFFF';
  return `<button class="role" style="background:${bg};color:${fg};cursor:pointer;text-align:left;font:inherit" data-copy-text="${bg}"><b>${r}</b><small>${bg.toUpperCase()}<br>${fg==='#000000'?'':''}${Math.round(ratio(bg,fg)*10)/10}:1 label</small></button>`}).join('')}
 $$('.role').forEach(b=>b.onclick=()=>copy(b.dataset.copyText))}

/* ---------- typography ---------- */
const TYPE=[['Display','t-display',56,64,400,'-0.25','Headline of the screen'],['Headline Large','t-headline-l',40,48,400,'0','Sunday route to the lake'],['Headline Medium','t-headline-m',36,44,400,'0','Midnight Violet Drive'],['Headline Small','t-headline-s',32,40,400,'0','Navigate to Home'],
['Title Large','t-title-l',32,40,500,'0','Bluetooth devices'],['Title Medium','t-title-m',28,36,500,'0.15','Turn right onto Violet Ave'],['Title Small','t-title-s',24,32,500,'0.1','Recently played'],
['Body Large','t-body-l',28,36,400,'0.3','Neon Orchid — Amethyst Roads'],['Body Medium','t-body-m',24,32,400,'0.25','12.4 km · Light traffic'],['Body Small','t-body-s',20,28,400,'0.4','Updated 2 min ago (non-critical)'],
['Label Large','t-label-l',28,36,500,'0.1','Navigate'],['Label Medium','t-label-m',24,32,500,'0.5','NOW PLAYING'],['Label Small','t-label-s',20,28,500,'0.5','DAY · 21°C']];
$('#typescale').innerHTML=TYPE.map(t=>`<div class="ty"><div><div class="nm">${t[0]}</div><small>${t[1].replace('t-','.t-')}</small></div><div class="${t[1]}">${t[6]}</div><small>${t[2]}sp / ${t[3]}sp<br>w${t[4]} · ls ${t[5]}</small></div>`).join('');

/* ---------- spacing / shape / elevation ---------- */
const SP=[['space.2xs',4],['space.xs',8],['space.sm',12],['space.md',16],['space.lg',24],['space.xl',32],['space.2xl',40],['space.3xl',48],['space.4xl',64],['space.5xl',96]];
$('#spacescale').innerHTML=SP.map(s=>`<div class="sp-row"><code>${s[0]}</code><span>${s[1]} dp</span><div class="bar" style="width:${s[1]*3}px"></div></div>`).join('');
const SH=[['none',0],['xs',8],['sm',12],['md',16],['lg',24],['xl',28],['2xl',40],['full',999]];
$('#shapescale').innerHTML=SH.map(s=>`<div style="text-align:center"><div class="sh" style="border-radius:${s[1]}px"></div><small><code>shape.${s[0]}</code><br>${s[1]===999?'50%':s[1]+' dp'}</small></div>`).join('');
const EL=[['level0','surface','none'],['level1','surfaceContainerLow','0 1px 3px rgba(0,0,0,.4)'],['level2','surfaceContainer','0 2px 6px rgba(0,0,0,.4)'],['level3','surfaceContainerHigh','0 4px 12px rgba(0,0,0,.45)'],['level4','surfaceContainerHigh','0 6px 16px rgba(0,0,0,.5)'],['level5','surfaceContainerHighest','0 10px 28px rgba(0,0,0,.55)']];
$('#elev').innerHTML=EL.map((e,i)=>`<div style="text-align:center"><div class="el" style="background:var(--c-${kebab(e[1])});box-shadow:${e[2]}">${e[1]}</div><small><code>elevation.${e[0]}</code></small></div>`).join('');

/* ---------- driving demo list ---------- */
const songs=['Midnight Violet Drive','Lavender Haze','Indigo Skyline','Plum Highway','Orchid Hours','Twilight Lane','Amethyst Roads','Velvet Static'];
$('#drvlist').innerHTML=Array.from({length:24},(_,i)=>{const n=songs[i%8]+(i>7?' '+(Math.floor(i/8)+1):'');return `<div class="a-li click"><div class="lead-i">${icon('music')}</div><div class="tx"><div class="p">${n}</div></div><div class="tr">${i+1} / 24</div></div>`}).join('');
$('#drvlist').style.maxHeight='480px';$('#drvlist').style.overflow='auto';

/* ---------- contrast ---------- */
const PAIRS=[['onSurface','surface'],['onSurfaceVariant','surface'],['primary','surface'],['onPrimary','primary'],['onPrimaryContainer','primaryContainer'],['onSecondaryContainer','secondaryContainer'],['onTertiaryContainer','tertiaryContainer'],['onError','error'],['onErrorContainer','errorContainer'],['onSuccessContainer','successContainer'],['onWarningContainer','warningContainer'],['onSurface','surfaceContainerHigh'],['inverseOnSurface','inverseSurface'],['tertiary','surface'],['outline','surface']];
function renderContrast(){const t=T();$('#contrastTbl tbody').innerHTML=PAIRS.map(([f,b])=>{const r=ratio(t[f],t[b]);const ui=f==='outline'||f==='tertiary';
 return `<tr><td><code>${f}</code> ${t[f]}</td><td><code>${b}</code> ${t[b]}</td><td><span style="background:${t[b]};color:${t[f]};padding:4px 12px;border-radius:8px;font-weight:600;font-size:18px">Aa 24</span></td><td><b>${r.toFixed(2)}</b>:1</td><td><span class="pill ${r>=(ui?3:4.5)?'ok':'no'}">${r>=(ui?3:4.5)?'Pass':'Fail'}</span> <small>${ui?'3:1 UI':'4.5:1'}</small></td><td><span class="pill ${r>=7?'ok':''}">${r>=7?'Pass':'—'}</span></td></tr>`}).join('')}
function customPair(){const f=$('#cfg').value,b=$('#cbg').value,r=ratio(f,b);const o=$('#cout');o.style.color=f;o.style.background=b;$('#cr').textContent=r.toFixed(2)+':1 '+(r>=7?'AAA':r>=4.5?'AA':r>=3?'AA large/UI only':'Fail')}
$('#cfg').oninput=$('#cbg').oninput=customPair;customPair();

/* ---------- export ---------- */
let exp='xml';
const hexA=h=>'#FF'+h.slice(1).toUpperCase();
const EX={
 xml:()=>['night','day'].map(m=>`<!-- res/values${m==='night'?'-night':''}/colors.xml -->\n<resources>\n`+Object.entries(TOKENS[m]).map(([k,v])=>`  <color name="aurora_${kebab(k).replace(/-/g,'_')}">${hexA(v)}</color>`).join('\n')+'\n</resources>').join('\n\n'),
 theme:()=>`<!-- res/values/themes.xml -->\n<style name="Theme.Aurora" parent="Theme.Material3.DayNight.NoActionBar">\n`+['primary','onPrimary','primaryContainer','onPrimaryContainer','secondary','onSecondary','secondaryContainer','onSecondaryContainer','tertiary','onTertiary','error','onError','background','onBackground','surface','onSurface','surfaceVariant','onSurfaceVariant','outline','outlineVariant'].map(k=>`  <item name="${k==='primary'||k==='background'||k==='surface'||k==='outline'||k==='outlineVariant'||k==='error'?'color'+k[0].toUpperCase()+k.slice(1):'color'+k[0].toUpperCase()+k.slice(1)}">@color/aurora_${kebab(k).replace(/-/g,'_')}</item>`).join('\n')+`\n  <item name="shapeAppearanceMediumComponent">@style/ShapeAppearance.Aurora.Medium</item>\n  <item name="android:fontFamily">sans-serif</item>\n</style>\n\n<!-- Car UI Library RRO (res/values/car_ui_overlays.xml) -->\n<resources>\n  <dimen name="car_ui_touch_target_size">76dp</dimen>\n  <dimen name="car_ui_toolbar_height">96dp</dimen>\n  <dimen name="car_ui_list_item_height">96dp</dimen>\n  <dimen name="car_ui_primary_icon_size">40dp</dimen>\n  <bool name="car_ui_scrollbar_enable">true</bool>\n</resources>`,
 css:()=>['night','day'].map(m=>`:root[data-theme="${m}"]{\n`+Object.entries(TOKENS[m]).map(([k,v])=>`  --aurora-${kebab(k)}: ${v};`).join('\n')+'\n}').join('\n\n'),
 json:()=>JSON.stringify({$schema:'design-tokens',color:TOKENS,type:Object.fromEntries(TYPE.map(t=>[t[0],{size:t[2]+'sp',lineHeight:t[3]+'sp',weight:t[4],letterSpacing:t[5]}])),space:Object.fromEntries(SP.map(s=>[s[0],s[1]+'dp'])),shape:Object.fromEntries(SH.map(s=>[s[0],s[1]+'dp'])),touch:{min:'76dp',primary:'96dp'}},null,2),
 kt:()=>`// Aurora AAOS Compose theme\nval AuroraNight = darkColorScheme(\n`+['primary','onPrimary','primaryContainer','onPrimaryContainer','secondary','onSecondary','secondaryContainer','onSecondaryContainer','tertiary','onTertiary','tertiaryContainer','onTertiaryContainer','error','onError','errorContainer','onErrorContainer','background','onBackground','surface','onSurface','surfaceVariant','onSurfaceVariant','outline','outlineVariant','inverseSurface','inverseOnSurface','inversePrimary','scrim'].map(k=>`    ${k} = Color(${hexA(TOKENS.night[k]).replace('#','0x')}),`).join('\n')+`\n)\n\nval AuroraTypography = Typography(\n`+TYPE.filter(t=>t[0]!=='Display').map(t=>{const n=t[0].replace(/ (\w)/g,(m,c)=>c.toUpperCase());return `    ${n[0].toLowerCase()+n.slice(1)} = TextStyle(fontSize = ${t[2]}.sp, lineHeight = ${t[3]}.sp, fontWeight = FontWeight.W${t[4]}),`}).join('\n')+`\n)\n\n// Minimum touch size\nCompositionLocalProvider(LocalMinimumInteractiveComponentSize provides 76.dp) { content() }`
};
const EXN={xml:['Android colors.xml','xml'],theme:['themes.xml + RRO','xml'],css:['CSS variables','css'],json:['JSON tokens','json'],kt:['Compose','kt']};
function renderExport(){$('#exportTabs').innerHTML=Object.entries(EXN).map(([k,v])=>`<button aria-selected="${k===exp}" data-k="${k}">${v[0]}</button>`).join('');
 $$('#exportTabs button').forEach(b=>b.onclick=()=>{exp=b.dataset.k;renderExport()});
 $('#exportOut code').textContent=EX[exp]()}
$('#dlExport').onclick=()=>dl('aurora-tokens.'+EXN[exp][1],EX[exp](),'text/plain');
$$('.cp[data-copy]').forEach(b=>b.onclick=()=>copy($(b.dataset.copy).textContent));

/* ---------- checklist ---------- */
const CHK=['Every task completable in ≤ 12 s eyes-off / ≤ 2 s glances','Driving variant defined (≤ 6 visible items, no keyboard, ≤ 120 chars)','Touch targets ≥ 76 dp with ≥ 16 dp spacing','Text ≥ 24 sp for driver-critical content; contrast ≥ 4.5:1 (7:1 for alerts)','Meaning never conveyed by color alone','Rotary: all controls focusable with visible 6 dp ring; no focus traps','Voice equivalent for each primary action','Day and Night themes verified, roles used instead of hex','Animations ≤ 300 ms, honor reduced motion, none decorative while driving','Content depth ≤ 3; Back is consistent and always available','Tested on 1280×720, 1920×720 and portrait; insets respected','RTL, +40% text expansion and font scale 130% verified','TalkBack/Voice Access labels and roles set on all controls'];
$('#chk').innerHTML=CHK.map((c,i)=>`<div class="a-li click" tabindex="0" data-i="${i}" style="min-height:84px"><button class="a-check" role="checkbox" aria-checked="false" aria-label="${c}"><svg class="i"><use href="#i-check"/></svg></button><div class="tx"><div class="p" style="font-size:24px;white-space:normal">${c}</div></div></div>`).join('')+'<div class="a-li hdr" id="chkp"></div>';
function chkProg(){const n=$$('#chk .a-check[aria-checked=true]').length;$('#chkp').textContent=n+' / '+CHK.length+' complete'}chkProg();
$$('#chk .a-li[data-i]').forEach(r=>{const cb=$('.a-check',r);const tg=()=>{cb.setAttribute('aria-checked',cb.getAttribute('aria-checked')!=='true');chkProg()};r.onclick=e=>{if(e.target.closest('.a-check'))return;tg()};cb.onclick=tg;r.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();tg()}}});

/* ---------- interactive components ---------- */
$$('.a-sw').forEach(s=>s.onclick=()=>s.setAttribute('aria-checked',s.getAttribute('aria-checked')!=='true'));
$$('.a-check').forEach(c=>{if(c.closest('#chk'))return;c.onclick=()=>c.setAttribute('aria-checked',c.getAttribute('aria-checked')!=='true')});
$$('.a-radio').forEach(r=>r.onclick=()=>{$$(`.a-radio[data-g="${r.dataset.g}"]`).forEach(o=>o.setAttribute('aria-checked',o===r))});
$$('.a-chip').forEach(c=>c.onclick=()=>c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')!=='true'));
$$('.a-seg').forEach(g=>$$('button',g).forEach(b=>b.onclick=()=>$$('button',g).forEach(o=>o.setAttribute('aria-pressed',o===b))));
$$('.a-tgl').forEach(b=>b.onclick=()=>b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true'));
$$('.a-tabs').forEach(g=>$$('.a-tab',g).forEach(b=>b.onclick=()=>$$('.a-tab',g).forEach(o=>o.setAttribute('aria-selected',o===b))));
$$('.a-slider input').forEach(i=>{const u=()=>{i.style.setProperty('--v',((i.value-i.min)/(i.max-i.min)*100)+'%');i.nextElementSibling.textContent=i.value};i.oninput=u;u()});
$$('.a-nav').forEach(n=>$$('a',n).forEach(a=>a.onclick=e=>{e.preventDefault();$$('a',n).forEach(o=>o.removeAttribute('aria-current'));a.setAttribute('aria-current','page')}));
$$('.a-dock a,.frame a').forEach(a=>a.addEventListener('click',e=>e.preventDefault()));
$$('.a-menu li').forEach(l=>l.onclick=()=>$$('.a-menu li').forEach(o=>o.classList.toggle('sel',o===l)));
$$('.a-list .a-li.click').forEach(l=>{if(l.closest('#chk')||l.closest('.frame'))return;l.addEventListener('click',()=>{$$('.a-li.click',l.parentNode).forEach(o=>o.classList.remove('sel'));l.classList.add('sel')})});
$('#snackBtn').onclick=()=>{let s=$('#liveSnack');if(!s){s=document.createElement('div');s.id='liveSnack';s.className='a-snack a-root';s.style.cssText='position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:90;font-size:26px';s.innerHTML='<span>Snackbar shown for 5 s</span><button class="a-btn text">OK</button>';s.lastChild.onclick=()=>s.remove();document.body.appendChild(s);setTimeout(()=>s.remove(),5000)}};
/* hvac */
let temp=21,fan=3;const fb=()=>{$('#fanbars').innerHTML=[0,1,2,3,4].map(i=>`<i style="width:14px;height:${12+i*8}px;border-radius:4px;background:${i<fan?'var(--c-primary)':'var(--c-secondary-container)'}"></i>`).join('')};fb();
$$('#hvacCtl [data-t]').forEach(b=>b.onclick=()=>{temp=Math.min(28,Math.max(16,temp+(b.dataset.t==='+'?.5:-.5)));$('#tv').textContent=temp.toFixed(1)});
$$('#hvacCtl [data-f]').forEach(b=>b.onclick=()=>{fan=Math.min(5,Math.max(0,fan+(b.dataset.f==='+'?1:-1)));fb()});
/* play */
$('#playBtn').onclick=e=>{const b=e.currentTarget;const p=b.dataset.playing!=='true';b.dataset.playing=p;b.innerHTML=icon(p?'pause':'play')};
/* motion */
$('#motionBtn').onclick=()=>{const d=$('#motionDot');d.style.transition='none';d.style.left='8px';void d.offsetWidth;d.style.transition='left 300ms cubic-bezier(.05,.7,.1,1)';d.style.left='288px'};
/* rotary */
const rg=$('#rotgrid');const rl=['Navigate','Call','Media','Climate','Vehicle','Settings','Voice','Apps','Home'];
rg.innerHTML=rl.map((l,i)=>`<div class="a-rot" tabindex="${i?-1:0}" role="button">${l}</div>`).join('');
const rc=$$('.a-rot',rg);let ri=0;const rf=n=>{ri=(n+rc.length)%rc.length;rc.forEach((c,i)=>{c.tabIndex=i===ri?0:-1;c.classList.toggle('focus',i===ri)});rc[ri].focus({preventScroll:true});$('#rotout').textContent='Focus: '+rl[ri]};
rg.addEventListener('keydown',e=>{const m={ArrowRight:1,ArrowLeft:-1,ArrowDown:3,ArrowUp:-3}[e.key];if(m){e.preventDefault();rf(ri+m)}else if(e.key==='Enter'||e.key===' '){e.preventDefault();$('#rotout').textContent='Activated: '+rl[ri];toast(rl[ri]+' activated')}});
rc.forEach((c,i)=>c.addEventListener('focus',()=>{ri=i;rc.forEach((x,j)=>x.classList.toggle('focus',j===i));$('#rotout').textContent='Focus: '+rl[i]}));

/*SCREENS*/
/*ICONS_UI*/
/*SPECS*/

/* ---------- nav ---------- */
const secs=$$('section.sec[data-title]');const groups=[];secs.forEach(s=>{if(!groups.includes(s.dataset.group))groups.push(s.dataset.group)});
const side=$('#sidenav');
side.innerHTML='<input id="navq" type="search" placeholder="Search sections ( / )" aria-label="Search sections">'+groups.map(g=>`<h6>${g}</h6>`+secs.filter(s=>s.dataset.group===g).map(s=>`<a href="#${s.id}" data-t="${s.dataset.title.toLowerCase()}">${s.dataset.title}</a>`).join('')).join('');
$('#navq').oninput=e=>{const q=e.target.value.toLowerCase();$$('a',side).forEach(a=>a.style.display=a.dataset.t.includes(q)?'':'none')};
addEventListener('keydown',e=>{if(e.key==='/'&&!/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault();$('#navq').focus()}});
$$('a',side).forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('nav-open')));
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){$$('a',side).forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))}})},{rootMargin:'-20% 0px -70% 0px'});
secs.forEach(s=>io.observe(s));

/* ---------- init ---------- */
setTheme(store.get('aurora-theme','night'));
setDriving(store.get('aurora-drv','false')==='true');
showScreen();
requestAnimationFrame(fit);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
if('serviceWorker' in navigator&&/^https?:/.test(location.protocol)){navigator.serviceWorker.register('sw.js').catch(()=>{})}
})();
