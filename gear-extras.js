/* gear.html extras: a fuller "in short" summary, a "who it's for" guide built from each product's specs,
   and colourway pickers (data in gear-colors.js). Loaded before the page script; everything here runs at render time. */
(function(){
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const sv=(p,l)=>((p.spec||[]).find(s=>s[0]===l)||[])[1]||'';
  const all=p=>(p.spec||[]).map(s=>s[1]).join(' ')+' '+p.name+' '+(p.desc||'');
  const num=s=>{const m=String(s).replace(/,/g,'').match(/\d+(\.\d+)?/);return m?+m[0]:0};
  const baht=n=>'฿'+Math.round(n).toLocaleString('en-US');
  const GAMES={fps:'Valorant · CS2 · Apex Legends',moba:'League of Legends · Dota 2 · WoW',story:'Elden Ring · Cyberpunk 2077 · Baldur’s Gate 3',race:'Forza · F1 · Gran Turismo',all:'Fortnite · Minecraft · GTA V',fight:'Street Fighter 6 · Tekken 8'};

  function tier(p){
    const same=P.filter(x=>x.cat===p.cat).map(x=>x.price).sort((a,b)=>a-b);
    const r=same.findIndex(v=>v>=p.price)/Math.max(1,same.length-1);
    return r<0.3?'budget':r<0.7?'mid-range':'premium';
  }
  function who(p){
    const W=[],t=all(p),price=p.price;
    const add=(t,d,g)=>W.push({t,d,g});
    if(p.cat==='keyboard'){
      const he=/hall|magnetic|analog|omnipoint|hfx|lekker/i.test(t)||!!sv(p,'Actuation');
      if(he)add('Competitive FPS players','Rapid Trigger resets a key the instant you lift it, so counter-strafing and peeking feel sharper.','fps');
      if(/60%|65%/.test(p.sub))add('Low-sensitivity aimers & small desks','A compact board leaves room for big mouse swipes.', he?null:'fps');
      if(p.sub==='75%')add('All-rounders','Keeps the function row and arrows while staying compact.','all');
      if(p.sub==='TKL')add('Balanced gamers','Full-size keys without the number pad, for more mouse room.','all');
      if(/Full size|96/.test(p.sub))add('Gamers who also work','The number pad helps with spreadsheets, accounting and MMO hotkeys.','moba');
      if(/low.profile|scissor/i.test(t))add('Fast typists','Low-profile keys feel close to a laptop and are easy on the wrists.',null);
      if(p.wl)add('Clean-desk & multi-device users','Wireless lets one keyboard hop between PC, laptop and tablet.',null);
      if(price<2000)add('Students & first setups','A solid first gaming keyboard without a big spend.',null);
      if(price>6500)add('Enthusiasts','Premium build, better stabilisers and finishes that last.',null);
    }else if(p.cat==='mouse'){
      const w=num(sv(p,'Weight')),poll=sv(p,'Polling rate');
      if(w&&w<=62)add('Fast-flick FPS aimers',`At about ${w} g it starts and stops quickly for flicks and tracking.`,'fps');
      if(p.sub==='Ergonomic')add('Palm-grip players','A right-handed hump fills the palm, comfortable for long sessions.','all');
      if(p.sub==='Ultralight')add('Claw & fingertip grip','A symmetrical, low-weight shell suits claw and fingertip grips.','fps');
      if(p.sub==='Multi-button')add('MMO, MOBA & productivity','Extra side buttons hold abilities, macros and shortcuts.','moba');
      if(/8,000|4,000/.test(poll))add('High-refresh monitor owners','High polling rates pay off most on 240 Hz and faster screens.','fps');
      if(price<1500)add('Students & first setups','Gets the essentials right for a small budget.',null);
      if(p.wl)add('Cable-free desks','No cable drag, and it travels easily with a laptop.',null);
    }else if(p.cat==='headset'){
      const anc=/noise cancel|anc/i.test(t);
      if(p.sub==='Wireless')add('PC & console switchers','Wireless freedom for the desk or the couch.','all');
      if(anc)add('Noisy rooms & commuters','Active noise cancelling shuts out fans, traffic and family.',null);
      if(p.sub==='Studio')add('Music listeners & creators','Accurate sound for music and editing; add a separate mic for chat.','story');
      if(p.sub==='Earbuds / IEM')add('Footstep hunters & mobile gamers','In-ear sound is precise and light, great for competitive and mobile play.','fps');
      if(p.sub==='Wired')add('Never-charge gamers','Plug in and play with zero battery worries or latency.','fps');
      if(price>8000)add('Audiophile gamers','Premium drivers for cinematic single-player worlds.','story');
      if(price<2000)add('Budget setups','Clear chat and decent sound for a small spend.',null);
    }else if(p.cat==='monitor'){
      const hz=num(sv(p,'Refresh rate')),panel=sv(p,'Panel');
      if(hz>=240)add('Esports players',`${hz} Hz keeps motion crisp and inputs feeling instant.`,'fps');
      if(/OLED/i.test(panel))add('Immersive single-player fans','OLED gives perfect blacks, vivid HDR and near-instant response.','story');
      if(p.sub==='1440p')add('All-round gamers','The sweet spot of sharpness and frame rate for most graphics cards.','all');
      if(p.sub==='4K')add('Creators & console players','Very sharp for editing, and a great match for PS5 and Xbox Series X.','story');
      if(p.sub==='Ultrawide')add('Sim racers & multitaskers','Extra width wraps around racing and flight sims, and fits two windows side by side.','race');
      if(p.sub==='1080p'&&price<6000)add('Budget builds','High frame rates without needing an expensive graphics card.','all');
    }else{
      const s=p.sub,surf=sv(p,'Surface');
      if(s==='Mouse pad'){
        if(/control|rubber/i.test(surf))add('Tactical FPS players','A controlled glide makes micro-adjustments and stopping easier.','fps');
        else add('Tracking-heavy games','A faster glide helps smooth tracking and big flicks.','fps');
        add('Anyone with a new mouse','A good pad is the cheapest aim upgrade you can make.',null);
      }
      if(s==='Controller'){add('Action, racing & sports players','Analog sticks and triggers suit driving, fighting and third-person games.','race');add('Couch & PC gamers','Works across PC and consoles for relaxed play.','fight')}
      if(s==='Microphone'){add('Streamers & content creators','A dedicated mic sounds far clearer than a headset boom.',null);add('Discord & online classes','Clear voice for chat, study calls and meetings.',null)}
      if(s==='Webcam')add('Streamers & remote workers','A sharper, better-lit picture for streams and calls.',null);
      if(s==='Stream control')add('Streamers','One-tap scene switching, audio control and shortcuts while live.',null);
      if(s==='Chair')add('Long gaming & study sessions','Support for your back through marathon sessions.',null);
    }
    return W.slice(0,4);
  }
  function summary(p){
    const c=(window.CATS||[]).find?CATS.find(x=>x.key===p.cat):null,one=c?c.one:p.cat;
    const tr=tier(p),bits=[];
    bits.push(`${p.brand} ${p.name} is a ${tr} ${p.cat==='accessory'?p.sub.toLowerCase():one} at about ${baht(p.price)}.`);
    const hl=(p.spec||[]).slice(0,3).map(([k,v])=>`${k}: ${v}`).join(' · ');
    if(hl)bits.push(`Key specs — ${hl}.`);
    bits.push(p.wl?'It connects wirelessly, so there is no cable on your desk.':p.cat==='monitor'?'':'It is wired, so there is nothing to charge and no wireless lag.');
    const cw=(window.COLORS||{})[p.id];
    if(cw)bits.push(`Available in ${cw.c.length} colourways, including ${cw.c.slice(0,3).map(x=>x.n).join(', ')}.`);
    return bits.filter(Boolean).join(' ');
  }
  window.gearProfile=function(p){
    const W=who(p),games=[...new Set(W.map(w=>w.g).filter(Boolean))].slice(0,2);
    return `<div class="gx"><div class="sec-h"><h2>In short</h2><span class="muted">${esc(tier(p))} ${esc(p.cat==='accessory'?p.sub.toLowerCase():'pick')}</span></div>
      <p class="gx-sum">${esc(summary(p))}</p>
      ${W.length?`<div class="sec-h" style="margin-top:14px"><h2>Who it’s for</h2><span class="muted">Guide based on specs</span></div>
      <div class="gx-who">${W.map(w=>`<div class="gx-p"><b>${esc(w.t)}</b><span>${esc(w.d)}</span></div>`).join('')}</div>`:''}
      ${games.length?`<div class="gx-games"><span class="eyebrow">Great in</span>${games.map(g=>`<span class="tag">${esc(GAMES[g])}</span>`).join('')}</div>`:''}</div>`;
  };
  window.gearWho=p=>who(p).map(w=>w.t);

  /* ---------- colourways ---------- */
  const sel={};
  window.cwCard=function(p){
    const cw=(window.COLORS||{})[p.id];if(!cw)return'';
    return `<div class="cw-row" aria-label="Colourways">${cw.c.slice(0,6).map((c,i)=>`<button class="cw-dot ${ (sel[p.id]||0)===i?'on':''}" data-cw="${esc(p.id)}" data-i="${i}" title="${esc(c.n)}" aria-label="${esc(c.n)}"><img src="${esc(c.img)}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>`).join('')}${cw.c.length>6?`<span class="cw-more">+${cw.c.length-6}</span>`:''}<span class="cw-name">${esc(cw.c[sel[p.id]||0].n)}</span></div>`;
  };
  window.cwDetail=function(p){
    const cw=(window.COLORS||{})[p.id];if(!cw)return'';
    return `<div class="cw-detail"><div class="sec-h"><h2>Colourways</h2><span class="muted">${cw.c.length} options · from ${cw.src==='store'?'the official store':'Amazon listings'}</span></div>
      <div class="cw-grid">${cw.c.map((c,i)=>`<button class="cw-opt ${(sel[p.id]||0)===i?'on':''}" data-cw="${esc(p.id)}" data-i="${i}" aria-pressed="${(sel[p.id]||0)===i}"><img src="${esc(c.img)}" alt="" loading="lazy" referrerpolicy="no-referrer"><span>${esc(c.n)}</span></button>`).join('')}</div></div>`;
  };
  window.cwImage=id=>{const cw=(window.COLORS||{})[id];return cw&&sel[id]!==undefined?cw.c[sel[id]].img:null};
  document.addEventListener('click',e=>{
    const b=e.target.closest('[data-cw]');if(!b)return;e.preventDefault();e.stopPropagation();
    const id=b.dataset.cw,i=+b.dataset.i,cw=(window.COLORS||{})[id];if(!cw)return;sel[id]=i;const c=cw.c[i];
    document.querySelectorAll(`[data-cw="${CSS.escape(id)}"]`).forEach(x=>{const on=+x.dataset.i===i;x.classList.toggle('on',on);if(x.hasAttribute('aria-pressed'))x.setAttribute('aria-pressed',on)});
    document.querySelectorAll('.cw-row').forEach(r=>{if(r.querySelector(`[data-cw="${CSS.escape(id)}"]`)){const n=r.querySelector('.cw-name');if(n)n.textContent=c.n}});
    document.querySelectorAll(`[data-photo="${CSS.escape(id)}"] img`).forEach(img=>{img.dataset.alt='';img.src=c.img});
  },true);
})();
