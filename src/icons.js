/* ---- icon library UI ---- */
let icSel=null;
const svgStr=(i,size=24)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${pathsSvg(i)}</svg>`;
const vdStr=i=>`<vector xmlns:android="http://schemas.android.com/apk/res/android"\n    android:width="24dp" android:height="24dp"\n    android:viewportWidth="24" android:viewportHeight="24"\n    android:tint="?attr/colorControlNormal">`+i.p.map(([d,f])=>`\n    <path android:pathData="${d}" android:strokeWidth="2" android:strokeLineCap="round" android:strokeLineJoin="round" android:strokeColor="#FF000000" android:fillColor="${f?'#FF000000':'#00000000'}"/>`).join('')+`\n</vector>\n`;
const DL_OK=/\.(svg|zip|json|txt|md|csv|html|png)$/i;
async function dl(name,data,type){
 try{if(window.claude&&claude.use){const d=await claude.use('downloads');if(d){await d.save({filename:DL_OK.test(name)?name:name+'.txt',data});return}}}catch(e){if(e&&e.code==='declined')return}
 const b=data instanceof Blob?data:new Blob([data],{type:type||'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),800)}
function crc32(buf){let t=crc32.t;if(!t){t=crc32.t=[];for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0}}let r=-1;for(let i=0;i<buf.length;i++)r=(r>>>8)^t[(r^buf[i])&255];return(r^-1)>>>0}
function makeZip(files){const enc=new TextEncoder(),chunks=[],cen=[];let off=0;const u16=v=>[v&255,v>>8&255],u32=v=>[v&255,v>>8&255,v>>16&255,v>>>24&255];
 files.forEach(f=>{const nm=enc.encode(f.name),d=enc.encode(f.data),crc=crc32(d);const h=[0x50,0x4b,3,4,...u16(20),...u16(0x0800),...u16(0),...u16(0),...u16(0x21),...u32(crc),...u32(d.length),...u32(d.length),...u16(nm.length),...u16(0)];chunks.push(new Uint8Array(h),nm,d);cen.push({nm,crc,len:d.length,off});off+=h.length+nm.length+d.length});
 let cs=0;const cp=[];cen.forEach(c=>{const h=[0x50,0x4b,1,2,...u16(20),...u16(20),...u16(0x0800),...u16(0),...u16(0),...u16(0x21),...u32(c.crc),...u32(c.len),...u32(c.len),...u16(c.nm.length),...u16(0),...u16(0),...u16(0),...u16(0),...u32(0),...u32(c.off)];cp.push(new Uint8Array(h),c.nm);cs+=h.length+c.nm.length});
 return new Blob([...chunks,...cp,new Uint8Array([0x50,0x4b,5,6,0,0,0,0,...u16(cen.length),...u16(cen.length),...u32(cs),...u32(off),0,0])],{type:'application/zip'})}
function renderIcons(){const q=($('#icq').value||'').toLowerCase(),cat=$('#iccat').value;
 let h='',n=0;ICONLIB.order.forEach(c=>{if(cat&&cat!==c)return;const list=ICONS.filter(i=>i.c===c&&(i.n.includes(q)||c.toLowerCase().includes(q)));if(!list.length)return;n+=list.length;
  h+=`<div class="iccat">${c} · ${list.length}</div><div class="icons">`+list.map(i=>`<button data-n="${i.n}" aria-pressed="${icSel===i.n}" title="${i.n}">${icon(i.n)}<span>${i.n}</span></button>`).join('')+'</div>'});
 $('#iconGrid').innerHTML=h||'<p>No icons match.</p>';
 $$('#iconGrid button').forEach(b=>b.onclick=()=>selIcon(b.dataset.n))}
function selIcon(n){icSel=n;const i=byName[n];$$('#iconGrid button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.n===n));
 $('#icDetail').classList.add('on');$('#icBig').innerHTML=icon(n);$('#icName').textContent='ic_'+n.replace(/-/g,'_');
 $('#icMeta').textContent=i.c+' · 24×24 dp grid · 2 dp stroke · '+i.p.length+' path'+(i.p.length>1?'s':'')+(i.p.some(p=>p[1])?' · filled parts':'')}
$('#icq').oninput=renderIcons;$('#iccat').onchange=renderIcons;
$('#iccat').innerHTML='<option value="">All families</option>'+ICONLIB.order.map(c=>`<option>${c}</option>`).join('');
$('#icsize').onchange=e=>$('#iconGrid').style.setProperty('--ics',e.target.value+'px');
$('#icCount').textContent=ICONS.length;
$('#icDl').onclick=()=>icSel&&dl(icSel+'.svg',svgStr(byName[icSel]),'image/svg+xml');
$('#icCp').onclick=()=>icSel&&copy(svgStr(byName[icSel]));
$('#icAn').onclick=()=>icSel&&copy(vdStr(byName[icSel]));
$('#icZip').onclick=()=>dl('aurora-icons-svg.zip',makeZip(ICONS.map(i=>({name:i.n+'.svg',data:svgStr(i)+'\n'}))));
$('#icZipA').onclick=()=>dl('aurora-icons-android.zip',makeZip(ICONS.map(i=>({name:'ic_'+i.n.replace(/-/g,'_')+'.xml',data:vdStr(i)}))));
renderIcons();
