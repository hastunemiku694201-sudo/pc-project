/* Theme switch for both pages: Auto (follows the device) → Dark → Light. Loaded in <head> so the saved
   theme applies before the page paints; the button is added to the header's tool area once it exists. */
(function(){
  const K='rg-theme',ORDER=['auto','dark','light'];
  let mode='auto';try{mode=localStorage.getItem(K)||'auto'}catch(e){}
  const root=document.documentElement;
  const apply=()=>{if(mode==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',mode)};
  apply();
  const ICON={auto:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><path d="M12 4v16" /><path d="M12 4a8 8 0 0 1 0 16" fill="currentColor"/></svg>',
    dark:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    light:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'};
  const LABEL={auto:'Auto',dark:'Dark',light:'Light'};
  function paint(b){b.innerHTML=ICON[mode]+`<span class="lbl">${LABEL[mode]}</span>`;b.setAttribute('aria-label',`Theme: ${LABEL[mode]}. Switch theme`);b.title=`Theme: ${LABEL[mode]} (click to switch)`}
  function mount(){
    const tools=document.querySelector('.top-tools');if(!tools||document.getElementById('themeBtn'))return;
    const b=document.createElement('button');b.className='icon-btn';b.id='themeBtn';b.type='button';paint(b);
    b.addEventListener('click',()=>{mode=ORDER[(ORDER.indexOf(mode)+1)%ORDER.length];try{localStorage.setItem(K,mode)}catch(e){}apply();paint(b)});
    tools.prepend(b);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
