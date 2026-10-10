(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const memory = new Map();
  const storage = {
    get(key) {
      try { return localStorage.getItem(key); }
      catch { return memory.get(key) || null; }
    },
    set(key, value) {
      memory.set(key, value);
      try { localStorage.setItem(key, value); } catch { /* Session-only fallback. */ }
    }
  };
  const lessons = window.CODEX_COURSE?.lessons || $$('.course-card').map(card => ({
    id: card.dataset.lesson, slug: card.getAttribute('href').replace(/\.html$/, ''),
    title: $('h3', card)?.textContent, minutes: 120
  }));
  const lesson = document.body.dataset.lesson;
  const seconds = id => {
    const value = Number(storage.get('codex-time-' + id) || 0);
    return Number.isFinite(value) && value >= 0 ? Math.floor(value) : 0;
  };
  function refresh() {
    const complete = lessons.filter(item => storage.get('codex-done-' + item.id) === '1').length;
    $$('.course-card[data-lesson]').forEach(card => {
      card.classList.toggle('is-done', storage.get('codex-done-' + card.dataset.lesson) === '1');
    });
    const progress = $('#course-progress');
    if (progress) progress.textContent = `完成 ${complete} / ${lessons.length} 單元`;
    const bar = $('#course-progress-bar');
    if (bar) bar.style.width = (lessons.length ? complete / lessons.length * 100 : 0) + '%';
    const total = lessons.reduce((sum, item) => sum + seconds(item.id), 0);
    const hours = $('#course-hours');
    if (hours) hours.textContent = `累計學習 ${Math.floor(total / 3600)} 小時 ${Math.floor(total % 3600 / 60)} 分`;
    const resume = $('#resume-learning');
    if (resume) {
      const next = lessons.find(item => storage.get('codex-done-' + item.id) !== '1');
      resume.href = next ? next.slug + '.html' : lessons.at(-1).slug + '.html';
      resume.textContent = next ? '繼續學習：' + next.title : '已完成課程，重訪最終整合實作';
    }
  }

  const theme = $('#theme-select');
  if (theme) {
    theme.value = window.codexTheme?.get() || 'system';
    theme.addEventListener('change', () => window.codexTheme?.set(theme.value));
  }

  $$('.tabs').forEach((group, groupIndex) => {
    group.setAttribute('role', 'tablist');
    const container = group.closest('.section') || group.parentElement;
    const buttons = $$('.tab', group);
    const panels = $$('[data-panel]', container).filter(panel => buttons.some(button => button.dataset.show === panel.dataset.panel));
    const activate = button => {
      buttons.forEach(item => {
        const active = item === button;
        item.classList.toggle('active', active);
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
      });
      panels.forEach(panel => panel.classList.toggle('hidden', panel.dataset.panel !== button.dataset.show));
    };
    buttons.forEach((button, index) => {
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-selected', String(button.classList.contains('active')));
      button.tabIndex = button.classList.contains('active') ? 0 : -1;
      const panel = panels.find(item => item.dataset.panel === button.dataset.show);
      if (panel) {
        panel.id ||= `panel-${groupIndex}-${button.dataset.show}`;
        button.id ||= `tab-${groupIndex}-${button.dataset.show}`;
        button.setAttribute('aria-controls', panel.id);
        panel.setAttribute('role', 'tabpanel');
        panel.setAttribute('aria-labelledby', button.id);
      }
      button.addEventListener('click', () => activate(button));
      button.addEventListener('keydown', event => {
        if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
          : (index + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
        buttons[next].focus();
        activate(buttons[next]);
      });
    });
  });

  $$('[data-copy-target]').forEach(button => button.addEventListener('click', async () => {
    const element = document.getElementById(button.dataset.copyTarget);
    if (!element) return;
    const original = button.innerHTML;
    try {
      await navigator.clipboard.writeText(element.value ?? element.innerText ?? '');
      button.textContent = '已複製 ✓';
    } catch {
      if (element.select) element.select();
      button.textContent = '請手動複製選取內容';
    }
    setTimeout(() => { button.innerHTML = original; }, 1800);
  }));

  $$('.feedback').forEach(element => element.setAttribute('aria-live', 'polite'));
  $$('.quiz button[data-correct]').forEach(button => button.addEventListener('click', () => {
    const feedback = $('.feedback', button.closest('.quiz'));
    const correct = button.dataset.correct === 'true';
    feedback.textContent = button.dataset.explain || (correct ? '答對了，請回想判斷依據。' : '回到情境找需求、限制與證據，再試一次。');
    feedback.style.color = correct ? 'var(--lime)' : 'var(--orange)';
  }));

  $$('.checklist input[type=checkbox]').forEach(input => input.addEventListener('change', () => {
    const list = input.closest('.checklist');
    const progress = $('[data-check-progress]', list.parentElement);
    if (progress) progress.textContent = `完成 ${$$('input:checked', list).length} / ${$$('input', list).length}`;
  }));
  const done = $('#lesson-done');
  if (done && lesson) {
    done.checked = storage.get('codex-done-' + lesson) === '1';
    done.addEventListener('change', () => {
      storage.set('codex-done-' + lesson, done.checked ? '1' : '0');
      refresh();
    });
  }

  const timer = $('.timerbox');
  if (timer && lesson) {
    let elapsed = seconds(lesson);
    let interval = null;
    const paint = () => {
      $('#timer-value').textContent = [Math.floor(elapsed / 3600), Math.floor(elapsed % 3600 / 60), elapsed % 60]
        .map(value => String(value).padStart(2, '0')).join(':');
    };
    const pause = () => { clearInterval(interval); interval = null; };
    paint();
    $('#timer-start')?.addEventListener('click', () => {
      if (interval !== null) return;
      interval = setInterval(() => {
        if (document.visibilityState === 'visible') {
          elapsed++;
          storage.set('codex-time-' + lesson, String(elapsed));
          paint(); refresh();
        }
      }, 1000);
    });
    $('#timer-pause')?.addEventListener('click', pause);
    $('#timer-reset')?.addEventListener('click', () => {
      pause(); elapsed = 0;
      storage.set('codex-time-' + lesson, '0');
      paint(); refresh();
    });
    window.addEventListener('pagehide', pause);
  }

  const search = $('#course-search');
  if (search) search.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    $$('.course-card').forEach(card => card.classList.toggle('hidden', !!query && !card.innerText.toLowerCase().includes(query)));
    const count = $$('.course-card:not(.hidden)').length;
    const status = $('#search-status');
    if (status) status.textContent = query ? `找到 ${count} 個單元` : '';
  });
  document.addEventListener('keydown', event => {
    if (search && (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault(); search.focus();
    }
    if (event.key === 'Escape' && search) {
      search.value = ''; search.dispatchEvent(new Event('input')); search.blur();
    }
  });

  const path = $('#learning-path');
  const routes = {
    start: ['01', '02', '05'], build: ['03', '04', '05', '07', '12'], scale: ['06', '08', '09', '10'],
    automation: ['11', '13', '14', '15', '19', '20'], creative: ['16', '17', '18'], all: []
  };
  const descriptions = {
    start: '推薦 01 → 02 → 05：交辦、脈絡與驗收。',
    build: '推薦 03 → 04 → 05 → 07 → 12：除錯、開發、驗收、介面與案例。',
    scale: '推薦 06 → 08 → 09 → 10：隔離、遠端、客製化與第一階段整合。',
    automation: '推薦 11 → 13 → 14 → 15 → 19 → 20：應用、Hooks、SDK、擴充、郵件與資料整合。',
    creative: '推薦 16 → 17 → 18：生圖素材、影片剪輯與動畫製作。',
    all: '依 01–20 完成四個階段，每階段 10 小時；也可依需求先選主題。'
  };
  if (path) path.addEventListener('change', () => {
    $$('.course-card').forEach(card => card.classList.toggle('recommended', (routes[path.value] || []).includes(card.dataset.lesson)));
    $('#path-description').textContent = descriptions[path.value] || descriptions.all;
  });

  const main = $('main');
  if (main && (lesson || document.body.dataset.guide)) {
    const details = document.createElement('details');
    details.className = 'contents';
    const summary = document.createElement('summary'); summary.textContent = '本頁目錄';
    const nav = document.createElement('nav'); nav.setAttribute('aria-label', '本頁章節');
    $$('.section h2', main).forEach((heading, index) => {
      heading.id ||= 'section-' + (index + 1);
      const link = document.createElement('a');
      link.href = '#' + heading.id; link.textContent = heading.textContent; nav.append(link);
    });
    details.append(summary, nav); $('.hero', main)?.after(details);
  }
  window.addEventListener('storage', refresh);
  refresh();
})();
