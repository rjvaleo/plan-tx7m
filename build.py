# Builds the five pages of the Deepgram pitch site into this folder.
# Run: python build.py
import html, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
READ = 'November 22, 2026'

NAV = [('index.html', 'The plan'), ('evidence.html', 'The evidence'), ('prototype.html', 'The prototype'), ('how.html', 'How I built it'), ('why.html', 'Why me')]

def page(fn, title, desc, body, script=''):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == fn else '', t) for h, t in NAV)
    out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<meta name="robots" content="noindex,nofollow"><title>%s</title><meta name="description" content="%s">'
           '<link rel="stylesheet" href="assets/site.css"></head><body><a class="skip" href="#main">Skip to content</a>'
           '<div class="flag"><div class="w"><b>Unofficial.</b> A job application for Deepgram&rsquo;s Senior Product Manager, Enterprise role, built from public pages. Not affiliated with Deepgram.</div></div>'
           '<header class="w nav"><a class="me" href="index.html"><i></i>Richard J. Valeo</a><nav aria-label="Pages">%s</nav></header>'
           '<main id="main">%s</main>'
           '<footer class="w foot"><span>Richard J. Valeo &middot; Georgetown, Colorado &middot; <a href="https://rjvaleo.github.io/">rjvaleo.github.io</a> &middot; <a href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></span>'
           '<span>Public pages read on %s. Nothing here comes from inside Deepgram.</span></footer>%s</body></html>') % (E(title), E(desc), nav, body, READ, script)
    open(os.path.join(HERE, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn, len(out))

ST = {'ok': 'Shown', 'gate': 'Request-only', 'none': 'Not found', 'move': 'In motion', 'self': 'Self-serve'}
def st(kind, label=None):
    cls = 'ok' if kind == 'self' else kind
    return '<span class="st %s">%s</span>' % (cls, E(label or ST[kind]))

# ---------------------------------------------------------------- the plan
# (name, state today, note today, state after, note after, week it changes or None)
BOARD = [
 ('Identity', 'Who can get in, and how the buyer controls it.', [
   ('Roles and permissions', 'ok', 'Three fixed roles with a published list of what each can do.', 'ok', 'Unchanged. An auditor role is the first I would add later.', None),
   ('Single sign-on', 'none', 'No documentation, changelog entry or pricing line.', 'self', 'Documented, priced, and set up by the customer&rsquo;s own admin.', 4),
   ('Multi-factor login', 'none', 'A staff reply in July 2025 said there were no plans.', 'ok', 'Enforceable for a whole organization.', 8),
   ('Service accounts', 'none', 'Keys belong to a person. The docs suggest a shared mailbox.', 'ok', 'Keys that belong to the project and survive staff changes.', 9),
   ('Admin audit log', 'none', 'Only request logs, kept 90 days.', 'ok', 'Role changes, key events and sign-ins, exportable.', 10),
   ('Automated provisioning', 'none', 'Not documented.', 'none', 'Cut from these twelve weeks. It follows single sign-on.', None)]),
 ('Security', 'How the service protects what it is sent.', [
   ('Encryption', 'ok', 'TLS 1.3 in transit, AES-256 at rest.', 'ok', 'Unchanged.', None),
   ('Zero retention', 'ok', 'Available as a flag on each request.', 'self', 'One account-level switch an admin sets.', 7),
   ('Penetration-test summary', 'none', 'A yearly third-party assessment is mentioned. No summary or way to ask.', 'gate', 'In the trust center, behind a click-through NDA.', 5),
   ('Software bill of materials', 'none', 'Not in the docs, changelog or self-hosted repository.', 'self', 'Published with every self-hosted release.', 11)]),
 ('Compliance', 'The proof a procurement team files.', [
   ('SOC 2 report', 'gate', 'Claimed for Type 1 and 2. Three pages give three ways to ask.', 'self', 'One route: the trust center, behind a click-through NDA.', 4),
   ('Healthcare agreement', 'gate', 'By contact form, Enterprise plan only.', 'self', 'Requested and signed in the trust center.', 5),
   ('GDPR, CCPA, PCI', 'ok', 'Stated on the docs and pricing pages.', 'ok', 'Unchanged.', None),
   ('FIPS 140-3', 'ok', 'Validated images for self-hosted since July 2026.', 'ok', 'Plus a plain statement of what holds for the hosted API.', 12),
   ('FedRAMP', 'none', 'Deepgram&rsquo;s own blog lists it as a limitation.', 'move', 'A decision memo: tier, route and budget.', 12)]),
 ('Experience', 'What the reviewer&rsquo;s afternoon feels like.', [
   ('Trust center', 'none', 'No portal. Four static docs pages and one marketing page.', 'self', 'Live, with documents, answers and status in one place.', 5),
   ('Answered questionnaire', 'none', 'Not found.', 'self', 'The standard cloud questionnaire, pre-filled and searchable.', 6),
   ('Enterprise features on the pricing page', 'none', 'The plan table compares rates only.', 'ok', 'Listed by plan.', 4),
   ('Public pages agree with each other', 'none', 'They disagree in eight places.', 'ok', 'Fixed, with an owner for each page.', 2),
   ('Status page', 'ok', 'Public, with 90-day uptime and alerts.', 'ok', 'Unchanged.', None)]),
]
cols = ''
count = {'today': {}, 'after': {}}
for name, sub, items in BOARD:
    rows = ''
    for n, a, an, b, bn, wk in items:
        count['today'][a] = count['today'].get(a, 0) + 1
        count['after'][b] = count['after'].get(b, 0) + 1
        badge = '<span class="wk">week %d</span>' % wk if wk else ''
        rows += ('<div class="item%s"><b>%s</b><div class="today">%s<small>%s</small></div><div class="after">%s%s<small>%s</small></div></div>'
                 % (' moved' if wk else '', n, st(a), an, st(b), badge, bn))
    cols += '<div class="col"><h3>%s</h3><p>%s</p>%s</div>' % (name, sub, rows)
total = sum(count['today'].values())
def tally(view, parts):
    return '<div class="tally %s">%s</div>' % (view, ''.join('<span><b>%d</b>%s</span>' % (sum(count[view].get(k, 0) for k in ks), label) for ks, label in parts))
TALLY = (tally('today', [(['ok'], 'shown'), (['gate'], 'request-only'), (['none'], 'not found')])
         + tally('after', [(['ok', 'self'], 'shown or self-serve'), (['gate'], 'behind an NDA'), (['move'], 'in motion'), (['none'], 'not yet')]))

def lane(label, cls, start, end, text):
    return '<div class="lane"><b>%s</b><div class="bar %s" style="grid-column:%d/%d">%s</div></div>' % (label, cls, start + 1, end + 2, text)
GANTT = ('<div class="gantt" role="img" aria-label="Twelve-week timeline in four overlapping phases: weeks 1 to 2, 3 to 6, 5 to 10 and 8 to 12."><div class="gin">'
         '<div class="wkrow"><span>Week</span>' + ''.join('<span>%d</span>' % i for i in range(1, 13)) + '</div>'
         + lane('Listen, rank, fix', 'a', 1, 2, 'Rank, fix')
         + lane('Make it visible', 'b', 3, 6, 'Trust center, sign-on launch, questionnaire')
         + lane('Close the access gaps', 'c', 5, 10, 'Multi-factor login, service accounts, audit log')
         + lane('Start the slow work', 'e', 8, 12, 'Bill of materials, FedRAMP memo')
         + '<div class="gates"><b>Gates</b><span style="grid-column:3/7">End of week 2: ranking agreed with sales</span><span style="grid-column:7/11">End of week 6: a reviewer can self-serve</span><span style="grid-column:11/14">End of week 12: review, then replan</span></div>'
         '</div></div>')

def phase(when, title, why, items, know):
    lis = ''
    for t, d, tags in items:
        lis += '<li><b>%s</b><span>%s</span>%s</li>' % (t, d, ''.join('<span class="tag">%s</span>' % x for x in tags))
    return '<div class="phase"><span class="when">%s</span><h3>%s</h3><p class="note" style="margin-top:8px">%s</p><ul>%s</ul><p class="know"><b>How I will know.</b> %s</p></div>' % (when, title, why, lis, know)

PHASES = '<div class="phases">' + phase('Weeks 1 to 2', 'Listen, rank, fix',
    'The ranking on this page is an outsider&rsquo;s. Two weeks with sales and security make it Deepgram&rsquo;s.', [
    ('Read the stalled deals with sales, and the last ten security questionnaires.', 'Which missing piece stopped which deal, and what it was worth.', ['Sales', 'Security']),
    ('Fix every place where public pages disagree.', 'Eight today. Each is a page edit with a named owner. No engineering.', ['Docs and site']),
    ('Pick one route for compliance documents.', 'Three pages give three routes today. One route goes on all of them now, before any portal exists.', ['Docs and site', 'Security'])],
    'A ranked list of blockers with deal value beside each, agreed with the head of sales.') + phase('Weeks 3 to 6', 'Make it visible',
    'Deepgram holds reports and agreements that buyers must ask a person for. Every rival I read runs a trust center.', [
    ('A trust center, live.', 'SOC 2 report and penetration-test summary behind a click-through NDA. Healthcare agreement, data processing agreement and subprocessor list self-serve.', ['Docs and site', 'Legal', 'Security']),
    ('Single sign-on, launched properly.', 'Documented, on the pricing page, and set up by the customer&rsquo;s own admin.', ['Console', 'Docs and site']),
    ('An answered security questionnaire.', 'The standard cloud questionnaire, pre-filled and searchable. ElevenLabs and OpenAI already publish theirs.', ['Security', 'Docs and site']),
    ('Enterprise features on the pricing page.', 'The plan table compares rates only. A buyer cannot tell which plan carries what.', ['Docs and site'])],
    'Document requests handled by a person fall toward zero, and time in security review is measured for the first time.') + phase('Weeks 5 to 10', 'Close the access gaps',
    'These are the questionnaire answers that are &ldquo;no&rdquo; today. Each ships in the Console with the product manager who owns it.', [
    ('Multi-factor login an organization can enforce.', 'The customer who asked in public needed it to pass an audit.', ['Console']),
    ('Service accounts.', 'Keys that belong to the project. Today, removing a team member disables every key they created.', ['Console', 'APIs']),
    ('An admin audit log.', 'Who changed a role, made a key or signed in, exportable through the API.', ['Console', 'APIs']),
    ('One switch for model training.', 'Today, opting out is a flag on every request, or a call to Deepgram.', ['Console', 'APIs'])],
    'A buyer can answer the identity section of a questionnaire with yes, and point to where.') + phase('Weeks 8 to 12', 'Start the slow work',
    'Federal readiness takes longer than twelve weeks. The job here is to start the clock on the right route.', [
    ('A software bill of materials with every self-hosted release.', 'Only one rival mentions one at all. Deepgram already ships FIPS-validated images, so this is a lead to extend.', ['Self-hosted images', 'Security']),
    ('FedRAMP: a decision memo, not a promise.', 'The 2026 rules add an entry tier that a SOC 2 Type II report qualifies for. The memo recommends a tier, a route and a budget.', ['Leadership', 'Security']),
    ('Say where FIPS applies.', 'Validated images exist for self-hosted. State plainly what holds for the hosted API and for Dedicated.', ['Docs and site', 'Managed endpoint'])],
    'Leadership decides on FedRAMP with real numbers, and self-hosted customers pull a bill of materials without asking.') + '</div>'

INDEX = ('<div class="w hero"><h1>Frictionless enterprise procurement, in twelve weeks.</h1>'
  '<p class="lead">Deepgram&rsquo;s posting for Senior Product Manager, Enterprise asks for someone who can take that goal and derive a 12-week plan without asking what to do first. This is mine. I built it in one day from Deepgram&rsquo;s public pages, with AI agents doing the reading.</p>'
  '<div class="bottom"><div><b>The bottom line</b><span>Deepgram already has more of the enterprise package than a buyer&rsquo;s security reviewer can see.</span></div>'
  '<div><b>So the order is</b><span>Show what exists. Then close the login and access gaps. Then start the slow federal work.</span></div>'
  '<div><b>Done means</b><span>A reviewer gets from first visit to approval without emailing anyone at Deepgram.</span></div></div>'
  '<div class="next"><a class="btn" href="prototype.html">Try the prototype</a><a class="btn ghost" href="evidence.html">Read the evidence</a></div></div>'

  '<section class="w" id="package"><div class="shead"><div><h2>What a security reviewer finds</h2>'
  '<p>The posting says buyers judge readiness as a package: identity, security, compliance and the experience their teams touch. This is that package as a reviewer meets it on Deepgram&rsquo;s public pages, read on ' + READ + '.</p></div>'
  '<div class="seg" role="group" aria-label="Board view"><button type="button" aria-pressed="true" data-view="today">Today</button><button type="button" aria-pressed="false" data-view="after">After week 12</button></div></div>'
  '<div class="board" data-view="today" id="board">' + cols + '</div>' + TALLY +
  '<p class="note" style="margin-top:14px">&ldquo;Not found&rdquo; means not found on public pages. Deepgram may hold any of these privately. The buyer&rsquo;s reviewer sees the same blank. <a href="evidence.html">Sources are on the evidence page.</a></p></section>'

  '<section class="w" id="weeks"><div class="shead"><div><h2>The twelve weeks</h2><p>Four phases that overlap. The first is cheap and fast on purpose: it tests this plan against what I cannot see from outside.</p></div></div>'
  + GANTT + PHASES + '</section>'

  '<section class="w"><div class="two"><div><h2>What I would cut</h2><ul class="plain">'
  '<li><b>Automated user provisioning.</b><span>Only two rivals offer it. It follows single sign-on, not the other way round.</span></li>'
  '<li><b>Custom roles.</b><span>Three fixed roles answer most questionnaires. An auditor role is the first I would add.</span></li>'
  '<li><b>ISO 27001.</b><span>Four rivals claim it. It is an audit program that belongs to the security lead, not a product feature.</span></li>'
  '<li><b>Full FedRAMP authorization.</b><span>It takes longer than twelve weeks at any tier. The memo starts it.</span></li></ul></div>'
  '<div><h2>What would change this plan</h2><ul class="plain">'
  '<li><b>If most stalled deals are federal,</b><span>the FedRAMP memo moves to week 3 and the access work waits.</span></li>'
  '<li><b>If single sign-on is held back by quality, not staffing,</b><span>its launch slips and the trust center goes first alone.</span></li>'
  '<li><b>If security already has a trust center under way,</b><span>I join that work instead of starting one.</span></li>'
  '<li><b>If sales names a blocker that is not on this page,</b><span>it goes to the top.</span></li></ul></div></div></section>'

  '<section class="w"><div class="two"><div><h2>How I would measure it</h2><p class="lead">Four numbers, reported every two weeks.</p>'
  '<p class="note" style="margin-top:12px">I can see no baseline for any of them from outside. Setting the baselines is week 1 work.</p></div>'
  '<ul class="plain"><li><b>Days a deal spends in security review.</b><span>The number this role exists to move.</span></li>'
  '<li><b>Share of document requests served without a person.</b><span>The trust center&rsquo;s job.</span></li>'
  '<li><b>Share of enterprise accounts on single sign-on with multi-factor login.</b><span>Adoption, not launch.</span></li>'
  '<li><b>Security questionnaires answered from the trust center alone.</b><span>Each one is hours a sales engineer gets back.</span></li></ul></div>'
  '<div class="next"><a class="btn" href="prototype.html">See week 5 as a working page</a><a class="btn ghost" href="how.html">How I built this with AI</a></div></section>')

BOARD_JS = ('<script>(function(){var b=document.getElementById("board"),bs=document.querySelectorAll(".seg button"),t=document.querySelectorAll(".tally");'
  'function set(v){b.dataset.view=v;bs.forEach(function(x){x.setAttribute("aria-pressed",x.dataset.view===v)});'
  't.forEach(function(x){x.hidden=!x.classList.contains(v)});'
  'b.querySelectorAll(".item.moved").forEach(function(i){i.classList.remove("changed");void i.offsetWidth;if(v==="after")i.classList.add("changed")})}'
  'bs.forEach(function(x){x.addEventListener("click",function(){set(x.dataset.view)})});set("today")})();</script>')

page('index.html', 'Frictionless enterprise procurement in twelve weeks · Richard J. Valeo',
     'A 12-week plan for Deepgram’s Senior Product Manager, Enterprise role, by Richard J. Valeo. Unofficial, built from public pages.', INDEX, BOARD_JS)

# ---------------------------------------------------------------- the evidence
def a(url, text): return '<a href="%s">%s</a>' % (url, text)
NF = '<span class="note">Not found</span>'
RIV = [
 ('us', 'Deepgram', 'https://developers.deepgram.com/trust-security/data-privacy-compliance', 'Not found', 'Type 1 and 2. Report by request.', 'Not documented', NF, 'Request logs only', 'None, by its own account', '140-3 images for self-hosted', NF),
 ('', 'AssemblyAI', 'https://www.assemblyai.com/security', 'Yes. Reports behind an NDA.', 'Type 2', '$199 a month per connection', 'States it has none', 'Activity logs', NF, NF, NF),
 ('', 'ElevenLabs', 'https://compliance.elevenlabs.io/', 'Yes. Summary report, certificates and questionnaire are public.', 'Type 2', 'Enterprise plan', 'Enterprise plan', 'Enterprise plan, by API', 'Entry tier, September 2026', NF, NF),
 ('', 'OpenAI API', 'https://trust.openai.com/', 'Yes. Report behind a request.', 'Type 2', 'Depends on plan', 'On custom plans', 'By API', 'Moderate, April 2026', NF, NF),
 ('', 'Speechmatics', 'https://speechmatics.safebase.us/', 'Yes. Reports behind a request.', 'Type 2', '$280 a month, Enterprise add-on', NF, NF, NF, NF, 'On request'),
 ('', 'Cartesia', 'https://trust.cartesia.ai/', 'Yes. Every report behind a request.', 'Type 2', 'Enterprise plan', NF, NF, NF, NF, NF),
 ('', 'Amazon Transcribe', 'https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-compliance.html', 'Amazon&rsquo;s own portal', 'In scope', 'Through the cloud account', 'Through the cloud account', 'Yes', 'Moderate and High', '140-3 endpoints', NF),
 ('', 'Google Cloud Speech-to-Text', 'https://cloud.google.com/security/compliance/services-in-scope', 'Google&rsquo;s own portal', 'In scope', 'Through the cloud account', 'Through the cloud account', 'Yes', 'High', '140-3', NF),
 ('', 'Microsoft Azure AI Speech', 'https://learn.microsoft.com/en-us/azure/compliance/offerings/cloud-services-in-audit-scope', 'Microsoft&rsquo;s own portal', 'Unclear for this service', 'Through the cloud account', 'Through the cloud account', 'Not checked', 'High', NF, NF),
]
rows = ''.join('<tr%s><td><b>%s</b></td>%s</tr>' % (' class="us"' if c else '', a(u, n), ''.join('<td>%s</td>' % x for x in cells)) for c, n, u, *cells in RIV)
EVID = ('<div class="w hero"><h1>The evidence.</h1><p class="lead">Everything on this site comes from pages any visitor can open, read on ' + READ + '. I created no account, submitted no form and tested no system.</p></div>'
  '<section class="w"><h2>Where Deepgram already leads</h2><ul class="plain">'
  '<li><b>Validated cryptography for self-hosted customers.</b><span>FIPS 140-3 images have been generally available since July 28, 2026. No independent rival I read publishes a FIPS claim at all. ' + a('https://developers.deepgram.com/changelog/2026/7/28', 'Changelog') + '</span></li>'
  '<li><b>More ways to deploy than any independent rival.</b><span>Shared cloud, endpoints in the EU, Australia and India, single-tenant with a 99.9% uptime commitment, self-hosted, and air-gapped. ' + a('https://developers.deepgram.com/trust-security/your-data', 'Your Data') + ', ' + a('https://deepgram.com/dedicated', 'Dedicated') + '</span></li>'
  '<li><b>Federal sales groundwork is in place.</b><span>Contract vehicles, a reseller and open federal roles. What is missing is the authorization those buyers file. ' + a('https://deepgram.com/solutions/government', 'Government page') + '</span></li>'
  '<li><b>The basics are stated plainly.</b><span>Encryption, per-request zero retention, a public subprocessor list and a public status page. ' + a('https://deepgram.com/privacy/subprocessors', 'Subprocessors') + ', ' + a('https://status.deepgram.com', 'Status') + '</span></li></ul></section>'
  '<section class="w"><div class="shead"><div><h2>Deepgram beside eight rivals</h2><p>What a buyer&rsquo;s reviewer can establish from each vendor&rsquo;s public pages. Each name links to that vendor&rsquo;s own security or trust page.</p></div></div>'
  '<div class="tw"><table><thead><tr><th>Vendor</th><th>Trust center</th><th>SOC 2</th><th>Single sign-on</th><th>Automated provisioning</th><th>Audit log</th><th>FedRAMP</th><th>FIPS</th><th>Bill of materials</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
  '<p class="note" style="margin-top:14px">&ldquo;Not found&rdquo; means not found on public pages, not that the vendor lacks it. An AI research agent gathered the rival rows from each vendor&rsquo;s own pages. I checked the Deepgram row against saved page text, and I have not checked the rival rows line by line.</p></section>'
  '<section class="w"><div class="two"><div><h2>What changed for federal buyers in 2026</h2><p class="lead">Three rule changes make the federal route shorter than it was, and one makes Deepgram&rsquo;s FIPS work timely.</p></div><ul class="plain">'
  '<li><b>FedRAMP added an entry tier.</b><span>A SOC 2 Type II report qualifies a vendor to submit for it. The older Moderate level is now called Class C. ' + a('https://www.fedramp.gov/2026-07-30-fedramp-certification-paths-are-heating-up/', 'FedRAMP, July 30, 2026') + '</span></li>'
  '<li><b>The old process is closing.</b><span>FedRAMP stops accepting new applications under it on June 11, 2027. ' + a('https://www.fedramp.gov/20x/', 'FedRAMP 20x') + '</span></li>'
  '<li><b>The older FIPS standard has sunset.</b><span>FIPS 140-2 validations moved to the historical list on September 21, 2026. New federal work needs 140-3, which Deepgram has for self-hosted. ' + a('https://csrc.nist.gov/projects/fips-140-3-transition-effort', 'NIST') + '</span></li>'
  '<li><b>Bills of materials are now asked for agency by agency.</b><span>The government-wide attestation rule was rescinded in January 2026, and the minimum contents were updated in July. ' + a('https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom', 'CISA') + ', ' + a('https://www.dwt.com/blogs/privacy--security-law-blog/2026/02/omb-changes-course-on-software-security', 'analysis') + '</span></li></ul></div></section>'
  '<section class="w"><div class="two"><div><h2>What is not on this page</h2></div><div><p>While reading, I found eight places where Deepgram&rsquo;s public pages disagree with each other, and a few details that look unannounced.</p>'
  '<p>Those are in a findings report I will send to Deepgram directly. A public page is the wrong place for them.</p>'
  '<div class="next"><a class="btn" href="index.html">Back to the plan</a><a class="btn ghost" href="how.html">How the research was run</a></div></div></div></section>')
page('evidence.html', 'The evidence · Richard J. Valeo', 'Deepgram’s public enterprise readiness beside eight rivals, with sources.', EVID)

# ---------------------------------------------------------------- how
def step(who, cls, title, text): return '<div class="step"><span class="who %s">%s</span><b>%s</b><span>%s</span></div>' % (cls, who, title, text)
HOW = ('<div class="w hero"><h1>How I built this.</h1><p class="lead">The posting says to expect a walk through a workflow I built, and where I drew the line between AI and my own judgment. Here is that walk, for this site.</p></div>'
  '<section class="w"><h2>The workflow</h2><div class="flow">'
  + step('Me', 'me', 'Pick the target', 'Deepgram&rsquo;s newest posting. I had it read in full before anything else was planned.')
  + step('AI', 'ai', 'Read everything public', 'Two research agents: one on Deepgram, one on eight rivals. 410 documentation pages and 231 changelog entries, searched.')
  + step('AI', 'ai', 'Check each finding', 'Every Deepgram claim was checked against the saved page text. Nine reported contradictions became eight.')
  + step('Me', 'me', 'Make the calls', 'What the plan leads with, what it cuts, and what stays off a public page.')
  + step('AI', 'ai', 'Build', 'The plan, the prototype and a private findings report, with me reviewing each.')
  + '</div><p class="note" style="margin-top:16px">The lead agent was Claude. It ran the two research agents, did the checking and wrote the pages. One working day, ' + READ + '.</p></section>'
  '<section class="w"><div class="two"><div><h2>The rules the agents worked under</h2><ul class="plain">'
  '<li><b>Every claim carries its source.</b><span>A page address and where on the page. The page text is saved, so any claim can be checked again.</span></li>'
  '<li><b>&ldquo;Not found&rdquo; is never rewritten as &ldquo;missing&rdquo;.</b><span>The agents had to say where they looked. Only a statement by Deepgram itself counts as confirmed absent.</span></li>'
  '<li><b>Read only.</b><span>No account, no login, no form, no testing of any system.</span></li>'
  '<li><b>Separate agents for Deepgram and for rivals.</b><span>So what one vendor says about another never stood in for that vendor&rsquo;s own page.</span></li></ul></div>'
  '<div><h2>Where the AI was wrong or thin</h2><ul class="plain">'
  '<li><b>One contradiction did not survive checking.</b><span>A change in the customer count between two announcements has an innocent explanation. It was dropped.</span></li>'
  '<li><b>A third-party tutorial contradicted Deepgram&rsquo;s own docs.</b><span>The research agent flagged it as unreliable, and nothing from it was used.</span></li>'
  '<li><b>Two directories credit Deepgram with certifications it does not claim.</b><span>Not used. Deepgram&rsquo;s own pages are the source for what Deepgram holds.</span></li>'
  '<li><b>The rival rows are thinner than the Deepgram row.</b><span>They were not checked line by line, and the evidence page says so.</span></li></ul></div></div></section>'
  '<section class="w"><div class="two"><div><h2>Where my judgment came in</h2><p class="lead">The agents can read 600 pages in an hour. They cannot decide what a hiring team should be shown.</p></div><ul class="plain">'
  '<li><b>Read the company as its buyer would, before pitching anything.</b><span>A plan that opens with &ldquo;build a trust center&rdquo; is a guess. One that opens with &ldquo;buyers cannot see what you have&rdquo; is a finding.</span></li>'
  '<li><b>Report what turned up.</b><span>If I find holes, I bring them up. The findings went into a report.</span></li>'
  '<li><b>Keep that report off the public site.</b><span>Some of it looks unannounced. It goes to Deepgram directly.</span></li>'
  '<li><b>Say what I cannot see.</b><span>The plan has a section on what would change it, because I have no view of the pipeline.</span></li>'
  '<li><b>Stand behind the output.</b><span>I read every page of this site before sending it. If something here is wrong, that is mine, not the agent&rsquo;s.</span></li></ul></div>'
  '<div class="next"><a class="btn" href="why.html">Why me</a><a class="btn ghost" href="index.html">Back to the plan</a></div></section>')
page('how.html', 'How I built this · Richard J. Valeo', 'The AI workflow behind this plan, what was checked, and where judgment came in.', HOW)

# ---------------------------------------------------------------- why me
def row(ask, have): return '<tr><td><b>%s</b></td><td>%s</td></tr>' % (ask, have)
WHY = ('<div class="w hero"><h1>Why me.</h1><p class="lead">I have never held the title Product Manager. I have been the product owner and builder of tools that security-conscious organizations work in, and I have been the buyer who could not get a tool approved.</p></div>'
  '<section class="w"><h2>What the posting asks, and what I have done</h2><div class="tw"><table><thead><tr><th style="width:32%">The posting asks for</th><th>What I have done</th></tr></thead><tbody>'
  + row('Enterprise product for security-conscious customers', 'I co-built the requirements app that ten vendor teams work in on a tolling modernization program. I built its role-based access: groups, inherited roles, a preview of every access change before it is saved, and refusals that say why. It fails closed without a key. ' + a('https://rjvaleo.github.io/case-rtm-tool.html', 'Case study'))
  + row('Understanding procurement psychology', 'I have been the blocked buyer. On that program any add-on needed a security review, and I had no admin rights. So I built the planning board myself, as a single file that runs offline on locked-down networks. ' + a('https://rjvaleo.github.io/case-pi-dashboard.html', 'Case study'))
  + row('Compliance experience', 'SOX change control twice, at a publicly traded retailer and at a bank. I set segregation-of-duties controls so nobody could both submit and approve a production change. The retailer&rsquo;s go-live landed on time.')
  + row('Front-end and UX sensibility', 'I started as a front-end developer and spent eight years as an agency producer shipping sites for American Express, Citi and Toyota. The prototype on this site is how I think a reviewer&rsquo;s afternoon should feel. ' + a('prototype.html', 'Prototype'))
  + row('An AI-native working style', 'This site. Also four music products shipped with AI agents behind more than 9,000 automated tests, and a loop where local models work coding jobs against hidden tests. I check the agents&rsquo; numbers: a reported 682 tests turned out to be 384. ' + a('https://rjvaleo.github.io/how-i-work.html', 'How I work'))
  + row('Autonomy, with imperfect requirements', 'I run the release train for those ten vendor teams. Nobody asked for the planning board or the interviews with every lead before planning. Both are now how the program plans.')
  + row('Range across engineering, design and sales', 'Twenty years between developers, designers and clients: agency accounts, then delivery at A+E Networks, Meta and Eptura.')
  + '</tbody></table></div></section>'
  '<section class="w"><div class="two"><div><h2>The gap, plainly</h2></div><div><p class="lead">I have not shipped FedRAMP, FIPS or single sign-on.</p>'
  '<p>I have shipped access control and audit-ready change control, and I know what it is to wait on a vendor&rsquo;s security answers. I learn a new domain by reading everything and then sitting with the people who run it. This site is the first half of that, done in a day.</p>'
  '<p>I also know voice. At Meta I produced the recordings that trained its AI voices, and supported the voice in the Ray-Ban Stories glasses through launch.</p>'
  '<div class="next"><a class="btn" href="https://rjvaleo.github.io/">See my work</a><a class="btn ghost" href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></div></div></div></section>')
page('why.html', 'Why me · Richard J. Valeo', 'Richard J. Valeo’s record against Deepgram’s Senior Product Manager, Enterprise role.', WHY)

# ---------------------------------------------------------------- prototype (markup here, behaviour in assets/proto.js)
PROTO = open(os.path.join(HERE, '_proto.html'), encoding='utf-8').read()
page('prototype.html', 'Trust center prototype · Richard J. Valeo', 'A clickable prototype of a self-serve trust center for a buyer’s security reviewer. Sample data.', PROTO, '<script src="assets/proto.js"></script>')
