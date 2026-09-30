/* Store comparison panel, shared by index.html (PC builder) and gear.html (gaming gear).
   Any element with data-stores="<product id>" opens it. Stores don't publish prices we can read,
   so each card links to that store's search for the item, and the viewer can note the price they
   see; notes stay in this browser (localStorage) and the cheapest noted store is highlighted. */
(function(){
  const STORES=[
    {k:'jib',n:'JIB',tag:'IT store',c:'#E4002B',u:q=>`https://www.jib.co.th/web/product/product_search/0?str_search=${q}`},
    {k:'ihavecpu',n:'iHAVECPU',tag:'IT store',c:'#F47B20',u:q=>`https://ihavecpu.com/product/search/${q}`},
    {k:'advice',n:'Advice',tag:'IT store',c:'#0054A6',u:q=>`https://www.advice.co.th/product/search?keyword=${q}`},
    {k:'bnn',n:'Banana IT',tag:'IT store',c:'#F5C400',u:q=>`https://www.bnn.in.th/th/p?q=${q}`},
    {k:'shopee',n:'Shopee',tag:'Marketplace',c:'#EE4D2D',u:q=>`https://shopee.co.th/search?keyword=${q}`},
    {k:'lazada',n:'Lazada',tag:'Marketplace',c:'#0F146D',u:q=>`https://www.lazada.co.th/catalog/?q=${q}`}
  ];
  const KEY='rg-store-prices';
  const load=()=>{try{return JSON.parse(localStorage.getItem(KEY))||{}}catch(e){return{}}};
  const save=v=>{try{localStorage.setItem(KEY,JSON.stringify(v))}catch(e){}};
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const baht=n=>'฿'+Math.round(n).toLocaleString('en-US');
  const item=id=>{try{return BYID[id]}catch(e){return null}};
  const photoOf=id=>((window.IMG||window.PIMG||{})[id]||[])[0];

  const css=`
.st-scrim{position:fixed;inset:0;background:var(--scrim,rgba(0,0,0,.55));z-index:90;display:grid;place-items:center;padding:16px;backdrop-filter:blur(4px)}
.st-box{width:min(760px,100%);max-height:calc(100vh - 32px);overflow:auto;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:20px;box-shadow:var(--neon,var(--shadow));padding:20px}
.st-head{display:flex;gap:14px;align-items:center}
.st-head img{width:72px;height:72px;object-fit:contain;background:#fff;border-radius:12px;padding:4px;flex:none}
.st-head h2{margin:2px 0 0;font-size:19px;line-height:1.2}
.st-head .x{margin-left:auto;align-self:flex-start}
.st-sub{font-size:13px;color:var(--muted);margin:12px 0 14px}
.st-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.st-card{display:flex;flex-direction:column;gap:10px;border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--surface-2);position:relative}
.st-card.best{border-color:var(--ok);box-shadow:0 0 0 1px var(--ok) inset}
.st-top{display:flex;align-items:center;gap:10px}
.st-logo{width:34px;height:34px;border-radius:9px;display:grid;place-items:center;color:#fff;font-weight:700;font-size:13px;flex:none}
.st-name{font-weight:600}.st-tag{font-size:11.5px;color:var(--muted)}
.st-best{position:absolute;top:10px;right:10px;font-size:11px;font-weight:600;color:var(--ok);background:var(--ok-soft);padding:2px 8px;border-radius:99px}
.st-row{display:flex;gap:8px;align-items:center}
.st-row a{flex:1;text-align:center;text-decoration:none}
.st-price{width:108px;padding:7px 9px;border-radius:9px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:inherit;font-size:13px}
.st-diff{font-size:12px;color:var(--muted);min-height:16px}
.st-diff.lo{color:var(--ok)}.st-diff.hi{color:var(--err)}
.st-foot{display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between;align-items:center;margin-top:14px;font-size:12.5px;color:var(--muted)}
@media (max-width:560px){.st-box{padding:16px}.st-head img{width:56px;height:56px}}`;
  const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

  let open=null,lastFocus=null;
  function render(){
    const p=open;if(!p)return;
    const q=encodeURIComponent(p.brand+' '+p.name.replace(/\s*\(.*?\)\s*/g,' ').replace(/\s+/g,' ').trim());
    const notes=(load()[p.id])||{};
    const vals=STORES.map(s=>+notes[s.k]||0).filter(Boolean),min=vals.length?Math.min(...vals):0;
    const img=photoOf(p.id);
    const box=document.querySelector('.st-box');
    box.innerHTML=`<div class="st-head">${img?`<img src="${esc(img)}" alt="" referrerpolicy="no-referrer" onerror="this.remove()">`:''}
        <div style="min-width:0"><div class="pbrand">${esc(p.brand)}</div><h2 id="stTitle">${esc(p.name)}</h2><div class="st-tag">Our reference price ${p.price?baht(p.price):'n/a'}</div></div>
        <button class="btn sm ghost x" data-st-close aria-label="Close">✕</button></div>
      <p class="st-sub">Open two or more stores to compare. Type the price you see into each card and we'll mark the cheapest. Your notes stay in this browser.</p>
      <div class="st-grid">${STORES.map(s=>{const v=+notes[s.k]||0,best=v&&v===min&&vals.length>1,d=v&&p.price?(v-p.price)/p.price*100:null;
        return `<div class="st-card ${best?'best':''}">${best?'<span class="st-best">Cheapest</span>':''}
          <div class="st-top"><span class="st-logo" style="background:${s.c}">${esc(s.n.slice(0,2))}</span><div><div class="st-name">${esc(s.n)}</div><div class="st-tag">${esc(s.tag)}</div></div></div>
          <div class="st-row"><a class="btn sm primary" href="${s.u(q)}" target="_blank" rel="noopener">Search ↗</a>
            <input class="st-price num" type="number" inputmode="numeric" min="0" step="1" placeholder="฿ price" value="${v||''}" data-st-k="${s.k}" aria-label="Price at ${esc(s.n)}"></div>
          <div class="st-diff ${d===null?'':d<0?'lo':d>0?'hi':''}">${d===null?'':d===0?'Same as our price':`${Math.abs(d).toFixed(0)}% ${d<0?'below':'above'} our price`}</div></div>`}).join('')}</div>
      <div class="st-foot"><span>${vals.length>1?`Best noted: ${baht(min)} · spread ${baht(Math.max(...vals)-min)}`:'Note at least two prices to compare.'}</span>
        <span style="display:flex;gap:8px"><a class="btn sm ghost" href="https://www.google.com/search?tbm=shop&q=${q}" target="_blank" rel="noopener">Google Shopping ↗</a>${vals.length?'<button class="btn sm ghost" data-st-clear>Clear notes</button>':''}</span></div>`;
  }
  function show(id){
    const p=item(id);if(!p||p.none)return;
    open=p;lastFocus=document.activeElement;
    let sc=document.querySelector('.st-scrim');
    if(!sc){sc=document.createElement('div');sc.className='st-scrim';sc.innerHTML='<div class="st-box" role="dialog" aria-modal="true" aria-labelledby="stTitle"></div>';document.body.appendChild(sc)}
    sc.hidden=false;render();sc.querySelector('[data-st-close]').focus();
  }
  function hide(){const sc=document.querySelector('.st-scrim');if(sc)sc.hidden=true;open=null;lastFocus?.focus?.()}

  document.addEventListener('click',e=>{
    const b=e.target.closest('[data-stores]');if(b){e.preventDefault();e.stopPropagation();show(b.dataset.stores);return}
    if(!open)return;
    if(e.target.classList.contains('st-scrim')||e.target.closest('[data-st-close]')){hide();return}
    if(e.target.closest('[data-st-clear]')){const all=load();delete all[open.id];save(all);render()}
  },true);
  document.addEventListener('change',e=>{const i=e.target.closest('[data-st-k]');if(!i||!open)return;
    const all=load(),n=all[open.id]||{},v=Math.max(0,Math.round(+i.value||0));if(v)n[i.dataset.stK]=v;else delete n[i.dataset.stK];
    if(Object.keys(n).length)all[open.id]=n;else delete all[open.id];save(all);render();
    document.querySelector(`[data-st-k="${i.dataset.stK}"]`)?.focus()});
  document.addEventListener('keydown',e=>{if(open&&e.key==='Escape')hide()});
  window.openStores=show;
})();
