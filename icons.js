/* Inline icon treatment based on Lucide (ISC License): https://lucide.dev/license */
(()=>{
const NS='http://www.w3.org/2000/svg';
const paths={
sparkles:'<path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-2-5.8L4 11l6-2.2L12 3Z"/><path d="m19 14 1 2.5 2.5 1-2.5 1L19 21l-1-2.5-2.5-1 2.5-1L19 14ZM5 2l.8 2.2L8 5l-2.2.8L5 8l-.8-2.2L2 5l2.2-.8L5 2Z"/>',
book:'<path d="M12 7v14"/><path d="M3 18V5a2 2 0 0 1 2-2h3a4 4 0 0 1 4 4 4 4 0 0 1 4-4h3a2 2 0 0 1 2 2v13a2 2 0 0 1-2 2h-4a3 3 0 0 0-3 3 3 3 0 0 0-3-3H5a2 2 0 0 1-2-2Z"/>',
compass:'<circle cx="12" cy="12" r="10"/><path d="m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3 6.3-2.1Z"/>',
bug:'<path d="m8 2 1.9 2h4.2L16 2M9 14h6M10 10h4M4 13H2m20 0h-2M5 7 3 5m16 2 2-2M5 19l-2 2m16-2 2 2"/><rect x="5" y="6" width="14" height="16" rx="7"/><path d="M12 6v16"/>',
workflow:'<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h6m0 0-3-3m3 3-3 3"/>',
check:'<path d="m9 12 2 2 4-4"/><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11Z"/>',
git:'<circle cx="6" cy="3" r="2"/><circle cx="6" cy="21" r="2"/><circle cx="18" cy="18" r="2"/><path d="M6 5v14m12-3V9a4 4 0 0 0-4-4h-2m0 0 3-3m-3 3 3 3"/>',
monitor:'<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>',
cloud:'<path d="M20 16.2A4.5 4.5 0 0 0 18 7.5a6 6 0 0 0-11.6 1.8A4 4 0 0 0 7 17h11"/>',
puzzle:'<path d="M19.4 13a1.7 1.7 0 0 0 1.6-1.7V6a2 2 0 0 0-2-2h-5.3a1.7 1.7 0 1 0-3.4 0H5a2 2 0 0 0-2 2v5.3a1.7 1.7 0 1 1 0 3.4V20a2 2 0 0 0 2 2h5.3a1.7 1.7 0 1 1 3.4 0H19a2 2 0 0 0 2-2v-5.3a1.7 1.7 0 0 0-1.6-1.7Z"/>',
gauge:'<path d="m12 14 4-4"/><path d="M3.3 17a9 9 0 1 1 17.4 0"/><path d="M5 17h14"/>',
plane:'<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
folder:'<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-8l-2-3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/><path d="M8 13h8m-8 4h5"/>',
learn:'<path d="M22 10v6M2 10l10-5 10 5-10 5-10-5Z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
list:'<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>',
clock:'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
copy:'<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
play:'<path d="m7 4 14 8-14 8V4Z"/>',
pause:'<path d="M8 5h3v14H8zm5 0h3v14h-3z"/>',
reset:'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
search:'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
idea:'<path d="M9 18h6m-5 4h4"/><path d="M8 14a7 7 0 1 1 8 0c-.8.6-1 1.3-1 2H9c0-.7-.2-1.4-1-2Z"/>',
arrow:'<path d="M5 12h14m-7-7 7 7-7 7"/>',
checkCircle:'<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'
};
const names=['compass','book','bug','workflow','check','git','monitor','cloud','puzzle','gauge','sparkles'];
function make(name,cls='icon'){const svg=document.createElementNS(NS,'svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('width','18');svg.setAttribute('height','18');svg.setAttribute('fill','none');svg.setAttribute('stroke','currentColor');svg.setAttribute('stroke-width','1.7');svg.setAttribute('stroke-linecap','round');svg.setAttribute('stroke-linejoin','round');svg.setAttribute('aria-hidden','true');svg.setAttribute('focusable','false');svg.setAttribute('class',cls);svg.innerHTML=paths[name]||paths.sparkles;return svg}
document.querySelectorAll('.course-card[data-lesson]').forEach(card=>{const i=Math.max(0,Number(card.dataset.lesson)-1);const tag=card.querySelector('.tag');if(tag){const mark=document.createElement('span');mark.className='card-glyph';mark.append(make(names[i]||'sparkles','icon icon-card'));tag.append(mark)}});
document.querySelectorAll('.timerbox').forEach(box=>{const label=box.querySelector('span');if(label)label.prepend(make('clock','icon icon-small'));[['timer-start','play'],['timer-pause','pause'],['timer-reset','reset']].forEach(([id,name])=>{const b=box.querySelector('#'+id);if(b)b.prepend(make(name,'icon icon-small'))})});
document.querySelectorAll('[data-copy-target]').forEach(b=>b.prepend(make('copy','icon icon-small')));
const homeProgress=document.querySelector('#course-progress')?.closest('.box');if(homeProgress){const t=homeProgress.querySelector('.tag');if(t)t.prepend(make('checkCircle','icon icon-small'))}
const homeTimer=document.querySelector('.tag')?.closest('.grid')?.querySelectorAll('.box')?.[1];if(homeTimer){const t=homeTimer.querySelector('.tag');if(t)t.prepend(make('clock','icon icon-small'))}
const hero=document.querySelector('.hero');if(hero){const h=hero.querySelector('h1');if(h){const badge=document.createElement('span');badge.className='hero-spark';badge.append(make(document.body.dataset.lesson?names[Math.max(0,Number(document.body.dataset.lesson)-1)]:'sparkles','icon'));h.append(badge)}}
document.querySelectorAll('.source-links').forEach(row=>row.setAttribute('aria-label','官方參考連結'));
})();
