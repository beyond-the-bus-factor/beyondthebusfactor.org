---
---
/* Scenario card tool.
   Data comes from _data/scenarios.json, which is generated in the
   resilience-resources repo by tools/build-deck.py. */
(function () {
  var DATA = {{ site.data.scenarios | jsonify }};
  var mount = document.getElementById('tool');
  var tpl = document.getElementById('tool-tpl');
  if (!mount || !tpl) return;

  /* Check the data before clearing the mount point. The no-JavaScript
     fallback lives inside it, and wiping that first would turn a bad data
     file into a blank page with nothing to click. */
  function usable(d) {
    return d && d.sectors && d.categories && d.difficulty &&
      Array.isArray(d.scenarios) && d.scenarios.length > 0;
  }
  if (!usable(DATA)) {
    var warn = document.createElement('p');
    warn.className = 'tool-fallback';
    warn.innerHTML = 'The card data could not be loaded. All the scenarios are readable in ' +
      '<a href="{{ site.repo_resources }}/blob/main/resources/scenario-cards.md">the scenario cards document</a>, ' +
      'and the <a href="{{ site.repo_resources }}/raw/main/deck/scenario-deck.pdf">printable deck</a> is a PDF.';
    mount.textContent = '';
    mount.appendChild(warn);
    return;
  }

  mount.textContent = '';
  mount.appendChild(tpl.content.cloneNode(true));

  /* Live controls rather than a form: nothing is submitted, so a form
     element here only promises a submit button that does not exist. */
  var form = mount.querySelector('.tool-filters');
  var stage = mount.querySelector('.tool-stage');
  var count = mount.querySelector('.tool-count');

  var groups = {
    sectors: DATA.sectors,
    categories: DATA.categories,
    difficulty: DATA.difficulty
  };
  var picked = { sectors: [], categories: [], difficulty: [] };
  var drawn = [];

  function chip(group, value, label) {
    var id = 'f-' + group + '-' + value;
    var wrap = document.createElement('span');
    wrap.className = 'chip';
    var input = document.createElement('input');
    input.type = 'checkbox';
    input.id = id;
    input.value = value;
    input.dataset.group = group;
    var lab = document.createElement('label');
    lab.setAttribute('for', id);
    lab.textContent = label;
    wrap.appendChild(input);
    wrap.appendChild(lab);
    return wrap;
  }

  Object.keys(groups).forEach(function (group) {
    var box = form.querySelector('[data-group="' + group + '"]');
    Object.keys(groups[group]).forEach(function (value) {
      box.appendChild(chip(group, value, groups[group][value]));
    });
  });

  function matches(s) {
    if (picked.sectors.length && !picked.sectors.some(function (x) { return s.sectors.indexOf(x) > -1; })) return false;
    if (picked.categories.length && picked.categories.indexOf(s.category) < 0) return false;
    if (picked.difficulty.length && picked.difficulty.indexOf(String(s.difficulty)) < 0) return false;
    return true;
  }

  function pool() { return DATA.scenarios.filter(matches); }

  function updateCount() {
    var n = pool().length;
    count.textContent = n === DATA.scenarios.length
      ? 'All ' + n + ' scenarios'
      : n + (n === 1 ? ' scenario matches' : ' scenarios match');
    form.querySelector('[data-act="draw"]').disabled = n === 0;
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function list(items, cls) {
    var ul = el('ul', cls);
    items.forEach(function (i) { ul.appendChild(el('li', null, i)); });
    return ul;
  }

  function render(s) {
    var card = el('article', 'scard');

    var top = el('p', 'scard-top');
    top.appendChild(el('span', 'scard-cat', DATA.categories[s.category]));
    top.appendChild(el('span', 'scard-fits', s.sectors.map(function (x) { return DATA.sectors[x]; }).join(', ')));
    card.appendChild(top);

    card.appendChild(el('h2', null, s.title));
    card.appendChild(el('p', 'scard-lede', s.summary));

    var body = el('div', 'scard-body');

    var a = el('div', 'scard-col');
    a.appendChild(el('h3', null, 'The situation'));
    s.situation.forEach(function (p) { a.appendChild(el('p', null, p)); });
    body.appendChild(a);

    var b = el('div', 'scard-col');
    b.appendChild(el('h3', null, 'Questions to work through'));
    b.appendChild(list(s.questions));

    var det = el('details', 'scard-think');
    var sum = el('summary', null, 'Think about (for the facilitator)');
    det.appendChild(sum);
    det.appendChild(list(s.think_about));
    b.appendChild(det);
    body.appendChild(b);

    card.appendChild(body);

    var foot = el('p', 'scard-foot');
    foot.appendChild(el('span', 'scard-level', DATA.difficulty[String(s.difficulty)]));
    foot.appendChild(el('span', null, s.minutes + ' minutes'));
    card.appendChild(foot);

    return card;
  }

  function notes(s) {
    var box = el('section', 'scard-notes');
    box.appendChild(el('h3', null, 'What we could not answer'));
    box.appendChild(el('p', 'scard-hint',
      'The gaps are the output of the session, not the answers. This box saves in this browser only, and never leaves your device.'));

    var ta = document.createElement('textarea');
    ta.rows = 5;
    ta.setAttribute('aria-label', 'Notes for ' + s.title);
    var key = 'bbf-notes-' + s.slug;
    try { ta.value = localStorage.getItem(key) || ''; } catch (e) {}
    var saved = el('span', 'scard-saved', '');
    ta.addEventListener('input', function () {
      try {
        localStorage.setItem(key, ta.value);
        saved.textContent = 'Saved in this browser';
        saved.removeAttribute('data-state');
      } catch (e) {
        saved.textContent = 'Not saved, this browser is blocking storage. Copy your notes before leaving.';
        saved.setAttribute('data-state', 'error');
      }
    });
    box.appendChild(ta);

    var actions = el('p', 'scard-actions');
    var copy = el('button', 'btn btn-ghost btn-sm', 'Copy scenario and notes');
    copy.type = 'button';

    function assemble() {
      return s.title + '\n' + s.summary + '\n\n' +
        s.situation.join('\n\n') + '\n\nQuestions to work through\n' +
        s.questions.map(function (q) { return '- ' + q; }).join('\n') +
        '\n\nWhat we could not answer\n' + (ta.value || '(nothing written down yet)') +
        '\n\nFrom beyondthebusfactor.org, released under CC0.';
    }

    function done() {
      saved.removeAttribute('data-state');
      copy.textContent = 'Copied';
      setTimeout(function () { copy.textContent = 'Copy scenario and notes'; }, 2000);
    }

    /* The clipboard API is absent over plain http and can reject on a
       permission prompt or inside an embedded context. Rather than failing
       with no feedback, put the text in a box and select it so the reader
       can copy it themselves. */
    function fallback() {
      saved.textContent = 'Could not copy for you. The text is selected below, press the copy key.';
      saved.setAttribute('data-state', 'error');
      var out = box.querySelector('.scard-copy-fallback');
      if (!out) {
        out = document.createElement('textarea');
        out.className = 'scard-copy-fallback';
        out.rows = 6;
        out.setAttribute('aria-label', 'Scenario and notes, ready to copy');
        box.appendChild(out);
      }
      out.value = assemble();
      out.focus();
      out.select();
    }

    copy.addEventListener('click', function () {
      var text = assemble();
      if (!navigator.clipboard || !navigator.clipboard.writeText) { fallback(); return; }
      try {
        navigator.clipboard.writeText(text).then(done, fallback);
      } catch (e) {
        fallback();
      }
    });
    actions.appendChild(copy);
    actions.appendChild(saved);
    box.appendChild(actions);
    return box;
  }

  function draw() {
    var p = pool();
    if (!p.length) return;
    var fresh = p.filter(function (s) { return drawn.indexOf(s.slug) < 0; });
    if (!fresh.length) { drawn = []; fresh = p; }
    var s = fresh[Math.floor(Math.random() * fresh.length)];
    drawn.push(s.slug);

    stage.textContent = '';
    stage.appendChild(render(s));
    stage.appendChild(notes(s));

    var again = el('p', 'scard-again');
    var btn = el('button', 'btn btn-primary', 'Draw another');
    btn.type = 'button';
    btn.addEventListener('click', function () { draw(); });
    again.appendChild(btn);
    again.appendChild(el('span', 'scard-progress',
      drawn.length + ' of ' + p.length + ' drawn'));
    stage.appendChild(again);

    stage.querySelector('h2').setAttribute('tabindex', '-1');
    stage.querySelector('h2').focus();
  }

  form.addEventListener('change', function (e) {
    var g = e.target.dataset.group;
    if (!g) return;
    picked[g] = Array.prototype.slice
      .call(form.querySelectorAll('[data-group="' + g + '"] input:checked'))
      .map(function (i) { return i.value; });
    drawn = [];
    updateCount();
  });

  form.addEventListener('click', function (e) {
    var act = e.target.dataset.act;
    if (act === 'draw') draw();
    if (act === 'reset') {
      form.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = false; });
      picked = { sectors: [], categories: [], difficulty: [] };
      drawn = [];
      updateCount();
    }
  });

  updateCount();
})();
