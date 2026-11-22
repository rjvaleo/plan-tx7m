// Trust center prototype. Everything here is local to the page: nothing is stored or sent.
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var DOCS = 'https://developers.deepgram.com/';

  // What a reviewer has to collect. gated = needs the NDA.
  var ITEMS = [
    { id: 'soc2', name: 'SOC 2 Type II report', what: 'The auditor’s full report.', gated: true },
    { id: 'pen', name: 'Penetration-test summary', what: 'Scope, date and outcome of the latest third-party test.', gated: true },
    { id: 'baa', name: 'Healthcare agreement', what: 'The business associate agreement, signed online.', act: 'Sign and add' },
    { id: 'dpa', name: 'Data processing agreement', what: 'Standard terms, with the transfer clauses.' },
    { id: 'idp', name: 'Sign-on and access summary', what: 'Single sign-on, multi-factor login, roles and the audit log on one page.' },
    { id: 'answers', name: 'Questionnaire answers', what: '', inList: false },
    { id: 'sbom', name: 'Bill of materials', what: '', inList: false },
    { id: 'subs', name: 'Subprocessor list', what: '', inList: false }
  ];

  // t: 'now' = stated on Deepgram's public pages today, 'plan' = proposed in the plan.
  var QA = [
    { q: 'Is customer data encrypted in transit and at rest?', a: 'Yes. TLS 1.3 in transit and AES-256 at rest.', t: 'now', s: DOCS + 'trust-security/your-data' },
    { q: 'Can we stop our audio from being kept?', a: 'Yes. A request sent with the opt-out flag is not retained.', t: 'now', s: DOCS + 'trust-security/your-data' },
    { q: 'Can one setting turn retention off for our whole account?', a: 'An admin sets it once in the Console.', t: 'plan' },
    { q: 'Is our audio used to train models?', a: 'Not when the opt-out is set. Requests take part by default.', t: 'now', s: DOCS + 'trust-security/your-data' },
    { q: 'Where is data processed? Which regions?', a: 'A global endpoint, plus endpoints in the EU, Australia and India.', t: 'now', s: DOCS + 'reference/regional-endpoints' },
    { q: 'Do you support single sign-on?', a: 'Yes. Your admin connects your identity provider in the Console.', t: 'plan' },
    { q: 'Can we require multi-factor login?', a: 'Yes, for every member of your organization.', t: 'plan' },
    { q: 'Is there an audit log of admin actions?', a: 'Yes. Role changes, key events and sign-ins, in the Console and by API.', t: 'plan' },
    { q: 'What roles exist?', a: 'Owner, admin and member, each with a published list of permissions.', t: 'now', s: DOCS + 'guides/deep-dives/working-with-roles' },
    { q: 'Do keys survive when a team member leaves?', a: 'Yes. Service accounts hold keys for the project, not a person.', t: 'plan' },
    { q: 'Do you hold a SOC 2 report?', a: 'Yes, Type 1 and Type 2.', t: 'now', s: DOCS + 'trust-security/data-privacy-compliance' },
    { q: 'Will you sign a HIPAA business associate agreement?', a: 'Yes, for Enterprise customers.', t: 'now', s: 'https://deepgram.com/pricing' },
    { q: 'Are you FedRAMP authorized?', a: 'No. Not today.', t: 'now', s: 'https://deepgram.com/blog/best-voice-ai-platforms-enterprise-comparison' },
    { q: 'Do you offer FIPS-validated cryptography?', a: 'Yes, in the self-hosted images, validated to FIPS 140-3.', t: 'now', s: DOCS + 'docs/fips-compliant-deployment' },
    { q: 'Can we run it ourselves, or air-gapped?', a: 'Yes. Self-hosted on your own infrastructure, including offline.', t: 'now', s: DOCS + 'docs/self-hosted-introduction' },
    { q: 'Is there an uptime commitment?', a: 'Yes, 99.9% for the single-tenant service.', t: 'now', s: 'https://deepgram.com/dedicated' },
    { q: 'Who are your subprocessors?', a: 'A public list names each one and what it handles.', t: 'now', s: 'https://deepgram.com/privacy/subprocessors' },
    { q: 'Do you provide a software bill of materials?', a: 'Yes, with every self-hosted release.', t: 'plan' }
  ];

  var state = { nda: false, got: {} };
  var start = Date.now();

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function renderDocs() {
    $('docs').innerHTML = ITEMS.filter(function (i) { return i.inList !== false; }).map(function (i) {
      var has = state.got[i.id], locked = i.gated && !state.nda;
      var mark = has ? '<span class="st ok">In your packet</span>' : locked ? '<span class="st gate">NDA needed</span>' : '<span class="st ok">' + (i.gated ? 'Unlocked' : 'Open') + '</span>';
      var btn = has ? '' : locked ? '<button class="btn sm ghost" type="button" data-nda>Accept the NDA to unlock</button>'
        : '<button class="btn sm" type="button" data-add="' + i.id + '">' + (i.act || 'Add to my packet') + '</button>';
      return '<div class="doc' + (has ? ' has' : '') + '"><div><b>' + esc(i.name) + '</b><span>' + esc(i.what) + '</span></div><div class="dact">' + mark + btn + '</div></div>';
    }).join('');
  }

  function renderPacket() {
    var n = ITEMS.filter(function (i) { return state.got[i.id]; }).length;
    $('got').textContent = n; $('need').textContent = ITEMS.length;
    $('meter').style.width = (100 * n / ITEMS.length) + '%';
    $('plist').innerHTML = ITEMS.map(function (i) { return '<li class="' + (state.got[i.id] ? 'y' : '') + '">' + esc(i.name) + '</li>'; }).join('');
    var all = n === ITEMS.length;
    $('export').disabled = !all;
    $('phint').textContent = all ? 'Everything a review needs, and nobody was emailed.' : 'Collect all ' + ITEMS.length + ' to export. ' + (ITEMS.length - n) + ' to go.';
    document.querySelectorAll('[data-add]').forEach(function (b) {
      var id = b.getAttribute('data-add');
      if (state.got[id] && !b.closest('.docs')) { b.disabled = true; b.textContent = 'In your packet'; }
    });
  }

  function renderQA() {
    var term = $('q').value.trim().toLowerCase();
    var hits = QA.filter(function (x) { return !term || (x.q + ' ' + x.a).toLowerCase().indexOf(term) > -1; });
    $('qa').innerHTML = hits.length ? hits.map(function (x) {
      var tag = x.t === 'now' ? '<span class="st ok">True today</span>' + (x.s ? ' <a class="src" href="' + x.s + '">source</a>' : '') : '<span class="st move">Proposed in the plan</span>';
      return '<div class="qrow"><b>' + esc(x.q) + '</b><p>' + esc(x.a) + '</p><div>' + tag + '</div></div>';
    }).join('') : '<p class="note">No answer matches “' + esc(term) + '”. In the real page, this search would be logged so the missing answer gets written.</p>';
  }

  function renderSbom() {
    var r = $('rel').value, cdx = $('fmt').value === 'cdx';
    $('sbomOut').textContent = cdx
      ? '{\n  "bomFormat": "CycloneDX",\n  "specVersion": "1.6",\n  "metadata": { "component": { "name": "self-hosted-engine", "version": "release-' + r + '" } },\n  "components": [\n    { "type": "library", "name": "<component>", "version": "<version>", "purl": "<package address>" }\n  ]\n}'
      : 'SPDXVersion: SPDX-2.3\nDocumentName: self-hosted-engine-release-' + r + '\nPackageName: <component>\nPackageVersion: <version>\nExternalRef: PACKAGE-MANAGER purl <package address>';
  }

  function add(id) { state.got[id] = true; renderDocs(); renderPacket(); }

  function openNda() { $('nda').showModal(); }
  function acceptNda() {
    state.nda = true; $('nda').close();
    $('who').innerHTML = '<div><b>Viewing as Dana Okafor, Northwind Health</b><span>NDA accepted. Confidential reports are unlocked for this visit.</span></div><span class="st ok">NDA on file</span>';
    renderDocs();
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t) return;
    if (t.hasAttribute('data-nda') || t.id === 'ndaOpen') return openNda();
    if (t.id === 'ndaYes') return acceptNda();
    if (t.id === 'ndaNo') return $('nda').close();
    if (t.id === 'doneX') return $('done').close();
    if (t.hasAttribute('data-add')) return add(t.getAttribute('data-add'));
    if (t.id === 'export') {
      $('doneP').textContent = ITEMS.length + ' items collected in ' + $('clock').textContent + ', with 0 emails to Deepgram.';
      $('doneL').innerHTML = ITEMS.map(function (i) { return '<li><b>' + esc(i.name) + '</b></li>'; }).join('');
      $('done').showModal();
    }
  });
  $('q').addEventListener('input', renderQA);
  $('rel').addEventListener('change', renderSbom);
  $('fmt').addEventListener('change', renderSbom);
  setInterval(function () {
    var s = Math.floor((Date.now() - start) / 1000);
    $('clock').textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2);
  }, 1000);

  renderDocs(); renderQA(); renderSbom(); renderPacket();
})();
