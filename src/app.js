(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const kebab=s=>s.replace(/[A-Z]/g,m=>'-'+m.toLowerCase());
const store={get(k,d){try{return localStorage.getItem(k)||d}catch(e){return d}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};

/* ---------- icons ---------- */
const ICONS={
home:'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z',menu:'M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z',
play:'M8 5v14l11-7z',pause:'M6 19h4V5H6v14zm8-14v14h4V5h-4z',next:'M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z',prev:'M6 6h2v12H6zm3.5 6l8.5 6V6z',
search:'M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z',
phone:'M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z',
nav:'M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z',
mic:'M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z',
vol:'M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 7.97v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z',
close:'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z',
check:'M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z',chev:'M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z',
back:'M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z',add:'M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z',minus:'M19 13H5v-2h14z',
bt:'M17.71 7.71L12 2h-1v7.59L6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 11 14.41V22h1l5.71-5.71-4.3-4.29 4.3-4.29zM13 5.83l1.88 1.88L13 9.59V5.83zm1.88 10.46L13 18.17v-3.76l1.88 1.88z',
wifi:'M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9zm8 8l3 3 3-3a4.24 4.24 0 0 0-6 0zm-4-4l2 2a7.07 7.07 0 0 1 10 0l2-2C15.14 9.14 8.87 9.14 5 13z',
music:'M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z',
bell:'M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z',
settings:'M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.49.49 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.48.48 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z',
car:'M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z',
snow:'M22 11h-4.17l3.24-3.24-1.41-1.42L15 11h-2V9l4.66-4.66-1.42-1.41L13 6.17V2h-2v4.17L7.76 2.93 6.34 4.34 11 9v2H9L4.34 6.34 2.93 7.76 6.17 11H2v2h4.17l-3.24 3.24 1.41 1.42L9 13h2v2l-4.66 4.66 1.42 1.41L11 17.83V22h2v-4.17l3.24 3.24 1.42-1.41L13 15v-2h2l4.66 4.66 1.41-1.42L17.83 13H22z',
fav:'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z',
more:'M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z',
warn:'M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z',
info:'M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z',
shuffle:'M10.59 9.17L5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41l-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z',
bright:'M20 8.69V4h-4.69L12 .69 8.69 4H4v4.69L.69 12 4 15.31V20h4.69L12 23.31 15.31 20H20v-4.69L23.31 12 20 8.69zM12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm0-10c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4z',
moon:'M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.39 5.39 0 0 1-4.4 2.26 5.4 5.4 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z',
seat:'M4 18v3h3v-3h10v3h3v-6H4zm15-8h3v3h-3zM2 10h3v3H2zm13-8H9C7.9 2 7 2.9 7 4v7c0 1.1.9 2 2 2h6c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z',
signal:'M2 22h20V2z',
apps:'M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z',
fan:'M12 11a1 1 0 100 2 1 1 0 000-2zM12 2c3 0 4.5 2 4.5 4.5S13.5 10.5 12 11c-1-3-2-6 0-9zM22 12c0 3-2 4.5-4.5 4.5S13.5 13.5 13 12c3-1 6-2 9 0zM12 22c-3 0-4.5-2-4.5-4.5S10.5 13.5 12 13c1 3 2 6 0 9zM2 12c0-3 2-4.5 4.5-4.5S10.5 10.5 11 12c-3 1-6 2-9 0z',
defrost:'M5 6h14l2 9v2H3v-2l2-9zm1.600 2L5.200 14h13.600L17.400 8H6.600zM8 19h2v2H8zm3 0h2v2h-2zm3 0h2v2h-2z'
};
const sprite='<svg width="0" height="0" style="position:absolute" aria-hidden="true">'+Object.entries(ICONS).map(([k,d])=>`<symbol id="i-${k}" viewBox="0 0 24 24"><path d="${d}"/></symbol>`).join('')+'</svg>';
document.body.insertAdjacentHTML('afterbegin',sprite);
const icon=n=>`<svg class="i" aria-hidden="true"><use href="#i-${n}"/></svg>`;
function expandIcons(root=document){$$('ic',root).forEach(e=>{const t=document.createElement('span');t.style.display='contents';t.innerHTML=icon(e.getAttribute('n'));e.replaceWith(t.firstChild)})}
expandIcons();

/* ---------- theme / driving ---------- */
const root=document.documentElement;
function setTheme(t){root.dataset.theme=t;store.set('aurora-theme',t);
 $('#themeBtn').innerHTML=(t==='night'?icon('moon'):icon('bright'))+' '+(t==='night'?'Night':'Day');
 $('#themeBtn').setAttribute('aria-pressed',t==='night');
 ['roleTheme','a11yTheme'].forEach(i=>{const e=$('#'+i);if(e)e.textContent=t==='night'?'Night':'Day'});
 renderRoles();renderContrast();renderExport();}
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

/* ---------- icon grid ---------- */
$('#iconGrid').innerHTML=Object.keys(ICONS).map(k=>`<button data-n="${k}" title="Copy name">${icon(k)}<span>${k}</span></button>`).join('');
$$('#iconGrid button').forEach(b=>b.onclick=()=>copy('ic_'+b.dataset.n));

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
$('#dlExport').onclick=()=>{const b=new Blob([EX[exp]()],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='aurora-tokens.'+EXN[exp][1];a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)};
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

/* ---------- screens ---------- */
const screens=$$('.frame-wrap[data-screen]');
$('#screenTabs').innerHTML=screens.map((s,i)=>`<button role="tab" aria-selected="${i===0}" data-i="${i}">${s.dataset.screen}</button>`).join('');
function showScreen(i){screens.forEach((s,j)=>s.style.display=j===i?'block':'none');$$('#screenTabs button').forEach((b,j)=>b.setAttribute('aria-selected',j===i));fit()}
$$('#screenTabs button').forEach(b=>b.onclick=()=>showScreen(+b.dataset.i));
function fit(){$$('.frame-wrap').forEach(w=>{const f=$('.frame',w);const wd=w.clientWidth;if(!wd)return;const s=wd/1280;f.style.transform=`scale(${s})`;w.style.height=(720*s)+'px'})}
addEventListener('resize',fit);
/* disable dock links in frames */

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
showScreen(0);
$$('.frame-wrap.anat').forEach(w=>w.style.display='block');
requestAnimationFrame(fit);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
if('serviceWorker' in navigator&&/^https?:/.test(location.protocol)){navigator.serviceWorker.register('sw.js').catch(()=>{})}
})();
