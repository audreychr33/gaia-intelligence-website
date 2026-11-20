"""Build the static company website in English and Greek.

Run from the repository root: python tools/build_site.py
It writes index.html, terrax/, gaia/, data-sources/, privacy/ and their Greek versions under el/,
plus privacy.html, which forwards the old address to privacy/.
The GAIA page body is today's page, kept as it is (tools/gaia_main_en.html), with the shared header and footer.
Only plain HTML and the local CSS/JS files are produced: no external requests, no inline styles or scripts
(the Content Security Policy blocks them).
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://axgaiaintelligence.com'
EMAIL = 'info@axgaiaintelligence.com'
# The Ter-AX application (its own server). Publish the site only once this address works.
APP_URL = 'https://tx.axgaiaintelligence.com/app/select'
SHOW_REPORT = False  # the report section of the Ter-AX page; hidden for now (user, 20/11/2026), comes back later
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self'; base-uri 'none'; "
       "form-action 'none'; object-src 'none'; frame-src 'none'; connect-src 'none';")

PAGES = {'home': '', 'terrax': 'terrax/', 'gaia': 'gaia/', 'data': 'data-sources/', 'privacy': 'privacy/'}

# Icons. The GAIA set is today's; the rest are Lucide (ISC licence) outlines.
ICON_LIBRARY = '''<svg class="icon-library" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <symbol id="icon-layers" viewBox="0 0 32 32"><path d="m3 10 13-7 13 7-13 7-13-7Zm0 7 13 7 13-7M3 24l13 7 13-7" transform="translate(0 -2)"></path></symbol>
    <symbol id="icon-map" viewBox="0 0 32 32"><path d="m3 6 8-3 10 4 8-3v22l-8 3-10-4-8 3V6Zm8-3v22M21 7v22"></path></symbol>
    <symbol id="icon-target" viewBox="0 0 32 32"><circle cx="16" cy="16" r="10"></circle><circle cx="16" cy="16" r="4"></circle><path d="M16 1v8m0 14v8M1 16h8m14 0h8"></path></symbol>
    <symbol id="icon-network" viewBox="0 0 32 32"><circle cx="23" cy="6" r="4"></circle><circle cx="7" cy="24" r="4"></circle><circle cx="25" cy="25" r="4"></circle><path d="m20 9-10 12m1 3h10M24 10l1 11"></path></symbol>
    <symbol id="icon-shield" viewBox="0 0 32 32"><path d="m16 3 11 4v9c0 7-11 13-11 13S5 23 5 16V7l11-4Z"></path><path d="m10 15 4 4 8-9"></path></symbol>
    <symbol id="icon-clock" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12"></circle><path d="M16 7v10l7 4"></path></symbol>
    <symbol id="icon-leaf" viewBox="0 0 32 32"><path d="M27 4C14 3 3 10 6 21s21 9 21-17ZM4 29l17-18"></path></symbol>
    <symbol id="icon-bars" viewBox="0 0 32 32"><path d="M3 29V17h5v12H3Zm10 0V9h5v20h-5Zm10 0V2h5v27h-5Z"></path></symbol>
    <symbol id="icon-satellite" viewBox="0 0 32 32"><path d="m12 12 8-3 4 8-8 4-4-9ZM3 10l6-3 4 9-6 3-4-9Zm20 10 6-3 3 8-6 3-3-8ZM18 4l2 5M16 21l-2 7"></path></symbol>
    <symbol id="icon-house" viewBox="0 0 24 24"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></symbol>
    <symbol id="icon-clipboard" viewBox="0 0 24 24"><rect width="8" height="4" x="8" y="2" rx="1"></rect><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><path d="m9 14 2 2 4-4"></path></symbol>
    <symbol id="icon-terrain" viewBox="0 0 24 24"><path d="m8 3 4 8 5-5 5 15H2L8 3z"></path></symbol>
    <symbol id="icon-pin" viewBox="0 0 24 24"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></symbol>
    <symbol id="icon-book" viewBox="0 0 24 24"><path d="M12 7v14"></path><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"></path></symbol>
    <symbol id="icon-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path></symbol>
    <symbol id="icon-briefcase" viewBox="0 0 24 24"><path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path><rect width="20" height="14" x="2" y="6" rx="2"></rect></symbol>
    <symbol id="icon-key" viewBox="0 0 24 24"><path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"></path><path d="m21 2-9.6 9.6"></path><circle cx="7.5" cy="15.5" r="5.5"></circle></symbol>
  </defs>
</svg>'''


def icon(name):
    return (f'<svg class="icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"><use href="#icon-{name}"></use></svg>')


def url(lang, page):
    return ('/el/' if lang == 'el' else '/') + PAGES[page]


T = {
    'en': {
        'skip': 'Skip to content', 'home_label': 'AX GAIA INTELLIGENCE home', 'primary': 'Primary',
        'nav': [('home', 'Company'), ('terrax', 'Ter-AX'), ('gaia', 'GAIA')], 'contact': 'Contact',
        'platform': 'Platform', 'open_tx': 'Open Ter-AX', 'talk': 'Talk to us', 'copy': 'Copy address', 'copied': 'Copied', 'lang_label': 'Language',
        'rights': 'All rights reserved.', 'data': 'Data &amp; Sources', 'privacy': 'Privacy Policy',
        'spacebic': ('AX GAIA INTELLIGENCE LTD participates in the Space BIC by ERATOSTHENES CoE, which is supported and funded by '
                     'the Cyprus Deputy Ministry of Research, Innovation and Digital Policy (DMRID).'),
    },
    'el': {
        'skip': 'Μετάβαση στο περιεχόμενο', 'home_label': 'AX GAIA INTELLIGENCE, αρχική', 'primary': 'Κύριο μενού',
        'nav': [('home', 'Εταιρεία'), ('terrax', 'Ter-AX'), ('gaia', 'GAIA')], 'contact': 'Επικοινωνία',
        'platform': 'Πλατφόρμα', 'open_tx': 'Άνοιγμα Ter-AX', 'talk': 'Επικοινωνήστε μαζί μας', 'copy': 'Αντιγραφή διεύθυνσης', 'copied': 'Αντιγράφηκε', 'lang_label': 'Γλώσσα',
        'rights': 'Με την επιφύλαξη παντός δικαιώματος.', 'data': 'Δεδομένα &amp; Πηγές', 'privacy': 'Πολιτική απορρήτου',
        'spacebic': ('Η AX GAIA INTELLIGENCE LTD συμμετέχει στο Space BIC του ERATOSTHENES CoE, που υποστηρίζεται και χρηματοδοτείται '
                     'από το Υφυπουργείο Έρευνας, Καινοτομίας και Ψηφιακής Πολιτικής (ΥΦΕΚΑΨΠ).'),
    },
}


def head(lang, page, title, description):
    alternates = ''.join(f'\n  <link rel="alternate" hreflang="{code}" href="{SITE}{url(code, page)}">' for code in ('en', 'el'))
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="no-referrer">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{SITE}{url(lang, page)}">{alternates}
  <link rel="alternate" hreflang="x-default" href="{SITE}{url('en', page)}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
  <link rel="stylesheet" href="/assets/typography.css">
  <link rel="stylesheet" href="/assets/index.css">
  <link rel="stylesheet" href="/assets/pages.css">
</head>
<body>
<a class="skip-link" href="#top">{T[lang]['skip']}</a>
{ICON_LIBRARY}
'''


def header(lang, page):
    t = T[lang]
    links = ''.join(f'<a href="{url(lang, key)}"{" aria-current=\"page\"" if key == page else ""}>{label}</a>' for key, label in t['nav'])
    contact = url(lang, 'home') + '#contact'
    # The main button fits the page: open Ter-AX on its own page, none on the GAIA page (in development), the platform elsewhere
    # (the platform holds Ter-AX today and GAIA services later, so the company pages do not single out one product).
    cta = {'terrax': (APP_URL, t['open_tx']), 'gaia': None}.get(page, (APP_URL, t['platform']))
    cta_link = f'<a href="{cta[0]}">{cta[1]}</a>' if cta else ''
    lang_switch = (f'<span class="lang" role="group" aria-label="{t["lang_label"]}">'
                   f'<a href="{url("en", page)}" hreflang="en" lang="en"{" aria-current=\"true\"" if lang == "en" else ""}>EN</a>'
                   f'<a href="{url("el", page)}" hreflang="el" lang="el"{" aria-current=\"true\"" if lang == "el" else ""}>ΕΛ</a></span>')
    return f'''<header class="nav">
  <div class="wrap nav-row"><a class="brand" href="{url(lang, 'home')}" aria-label="{t['home_label']}"><span class="brand-mark" aria-hidden="true"><img src="/assets/logo-dark.png" alt="" width="1024" height="1024"></span><span class="brand-text"><strong>AX GAIA</strong><span>INTELLIGENCE</span></span></a><nav class="links" aria-label="{t['primary']}">{links}<a href="{contact}">{t['contact']}</a>{lang_switch}{cta_link}</nav></div>
</header>
'''


def footer(lang):
    t = T[lang]
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer-meta"><span>© <span id="y"></span> AX GAIA INTELLIGENCE. {t['rights']}</span><span class="footer-links"><a href="{url(lang, 'data')}">{t['data']}</a> · <a href="{url(lang, 'privacy')}">{t['privacy']}</a></span></div>
    <div class="partner"><a href="https://spacebic.cy" target="_blank" rel="noopener noreferrer" aria-label="Space BIC by ERATOSTHENES CoE"><img src="/assets/spacebic-logo.png" alt="Space BIC by ERATOSTHENES CoE" width="210" loading="lazy"></a><p>{t['spacebic']}</p></div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def contact_section(lang):
    if lang == 'el':
        eyebrow, title = '04 / Επικοινωνία', 'Μιλήστε μαζί μας'
        note = 'Για ερωτήσεις για το Ter-AX, το GAIA ή ένα έργο, στείλτε μας email. Αν δεν ανοίξει πρόγραμμα email, αντιγράψτε τη διεύθυνση.'
    else:
        eyebrow, title = '04 / Contact', 'Get in touch'
        note = 'For questions about Ter-AX, GAIA or a project, email us. If no email app opens, copy the address.'
    return f'''  <section id="contact" class="contact section" aria-labelledby="contact-title">
    <div class="wrap contact-grid">
      <div><p class="eyebrow">{eyebrow}</p><h2 id="contact-title">{title}</h2></div>
      <div>
        <p>{note}</p>
        <div class="contact-links">
          <a class="button primary contact-email" href="mailto:{EMAIL}"><span>{EMAIL}</span><span aria-hidden="true">↗</span></a>
          <button class="button copy-email" type="button" data-copy="{EMAIL}" data-done="{T[lang]['copied']}" aria-label="{T[lang]['copy']}" title="{T[lang]['copy']}"><svg class="icon-copy" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2"></rect><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path></svg><svg class="icon-done" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg></button>
        </div>
      </div>
    </div>
  </section>
'''


# ---------------------------------------------------------------- Company home
HOME = {
    'en': {
        'title': 'AX GAIA INTELLIGENCE — Land and ground intelligence for Cyprus',
        'description': 'AX GAIA Intelligence builds Ter-AX, land and site intelligence from official data, and GAIA, space-enabled ground intelligence in development.',
        'eyebrow': 'Land and ground intelligence · Cyprus', 'h1': 'Understand a site<br>before you <em>commit to it.</em>',
        'intro': ('AX GAIA Intelligence helps you understand land in Cyprus. Ter-AX shows what official data says about any '
                  'parcel today — free. GAIA, in development, will show what lies beneath it.'),
        'p_eyebrow': '01 / Our products', 'p_h2': 'From the official map to the subsurface.',
        'p_intro': ('Two products with one aim: fewer surprises on the ground. Ter-AX brings together, in seconds, what public authorities '
                    'publish about a parcel. GAIA is being developed to combine satellite and ground-sensing data, to indicate what the maps cannot show.'),
        'tx_alt': 'Ter-AX official checks for a parcel, with identifying details blurred', 'live': 'Available', 'tx_kicker': 'Land &amp; site intelligence',
        'tx_text': 'Analyse any parcel in Cyprus in seconds — free, no sign-up: the planning zone and building limits, the official checks, what is on it today and what is nearby.',
        'tx_cta': 'Discover Ter-AX', 'g_alt': 'Conceptual illustration of Earth Observation over a construction site', 'dev': 'In development',
        'g_kicker': 'Ground intelligence',
        'g_text': ('A space-enabled ground intelligence platform for construction and infrastructure. It combines Earth Observation with '
                   'ground-sensing data to give early indications of potential ground risk and support better-targeted investigations.'),
        'g_cta': 'Discover GAIA',
        'w_eyebrow': '02 / How we work', 'w_h2': 'Clear answers.<br>Honest limits.',
        'w': [('book', 'Official sources first', 'Every figure comes from a public authority or a named open dataset, with its date and its limits shown next to it.'),
              ('check', 'What the data shows — and doesn’t', 'We don’t fill gaps with guesses: estimates are marked as indicative, missing data is shown as missing, and where a question needs a licensed professional, we say so plainly.'),
              ('layers', 'From surface to subsurface', 'Ter-AX brings together what is mapped about a parcel. GAIA is being developed to add what lies beneath it.')],
        'c_eyebrow': '03 / The company', 'c_h2': 'AX GAIA Intelligence',
        'c_text': ['AX GAIA Intelligence Ltd is a Cyprus company developing space-enabled land and ground intelligence.',
                   'It works with a network of advisers who test what we build against real projects.'],
    },
    'el': {
        'title': 'AX GAIA INTELLIGENCE — Πληροφορία για τη γη και το έδαφος στην Κύπρο',
        'description': 'Η AX GAIA Intelligence αναπτύσσει το Ter-AX, ανάλυση γης και τεμαχίου από επίσημα δεδομένα, και το GAIA, πληροφορία για το έδαφος από το διάστημα, σε ανάπτυξη.',
        'eyebrow': 'Πληροφορία για γη και έδαφος · Κύπρος', 'h1': 'Γνωρίστε ένα οικόπεδο<br><em>πριν δεσμευτείτε.</em>',
        'intro': ('Η AX GAIA Intelligence σας βοηθά να καταλάβετε τη γη στην Κύπρο. Το Ter-AX δείχνει τι λένε σήμερα τα επίσημα '
                  'δεδομένα για κάθε τεμάχιο — δωρεάν. Το GAIA, υπό ανάπτυξη, θα δείχνει τι κρύβεται κάτω από αυτό.'),
        'p_eyebrow': '01 / Τα προϊόντα μας', 'p_h2': 'Από τον επίσημο χάρτη στο υπέδαφος.',
        'p_intro': ('Δύο προϊόντα με έναν στόχο: λιγότερες εκπλήξεις στο έδαφος. Το Ter-AX συγκεντρώνει σε λίγα δευτερόλεπτα όσα δημοσιεύουν '
                    'οι δημόσιες αρχές για ένα τεμάχιο. Το GAIA αναπτύσσεται για να συνδυάζει δορυφορικά δεδομένα και μετρήσεις εδάφους, ώστε να δείχνει ό,τι δεν φαίνεται στους χάρτες.'),
        'tx_alt': 'Επίσημοι έλεγχοι του Ter-AX για ένα τεμάχιο, με θολωμένα τα στοιχεία ταυτότητας', 'live': 'Διαθέσιμο', 'tx_kicker': 'Ανάλυση γης &amp; τεμαχίου',
        'tx_text': 'Αναλύστε οποιοδήποτε τεμάχιο στην Κύπρο σε λίγα δευτερόλεπτα — δωρεάν, χωρίς εγγραφή: πολεοδομική ζώνη και όροι δόμησης, επίσημοι έλεγχοι, τι υπάρχει σήμερα και τι βρίσκεται κοντά.',
        'tx_cta': 'Γνωρίστε το Ter-AX', 'g_alt': 'Εννοιολογική απεικόνιση παρατήρησης της Γης πάνω από εργοτάξιο', 'dev': 'Σε ανάπτυξη',
        'g_kicker': 'Πληροφορία για το έδαφος',
        'g_text': ('Πλατφόρμα πληροφορίας για το έδαφος από το διάστημα, για κατασκευές και υποδομές. Συνδυάζει την παρατήρηση της Γης με '
                   'μετρήσεις εδάφους, για έγκαιρες ενδείξεις πιθανού εδαφικού κινδύνου και πιο στοχευμένες έρευνες.'),
        'g_cta': 'Γνωρίστε το GAIA',
        'w_eyebrow': '02 / Πώς δουλεύουμε', 'w_h2': 'Σαφείς απαντήσεις.<br>Ειλικρινή όρια.',
        'w': [('book', 'Πρώτα οι επίσημες πηγές', 'Κάθε στοιχείο προέρχεται από δημόσια αρχή ή ονομαστικό ανοιχτό σύνολο δεδομένων, με την ημερομηνία και τα όριά του δίπλα του.'),
              ('check', 'Τι δείχνουν τα δεδομένα — και τι όχι', 'Δεν καλύπτουμε κενά με εικασίες: οι εκτιμήσεις σημειώνονται ως ενδεικτικές, όσα λείπουν φαίνονται ότι λείπουν, και όπου ένα ερώτημα χρειάζεται αδειούχο επαγγελματία, το λέμε καθαρά.'),
              ('layers', 'Από την επιφάνεια στο υπέδαφος', 'Το Ter-AX συγκεντρώνει ό,τι είναι χαρτογραφημένο για ένα τεμάχιο. Το GAIA αναπτύσσεται για να προσθέσει ό,τι βρίσκεται από κάτω.')],
        'c_eyebrow': '03 / Η εταιρεία', 'c_h2': 'AX GAIA Intelligence',
        'c_text': ['Η AX GAIA Intelligence Ltd είναι κυπριακή εταιρεία που αναπτύσσει πληροφορία για τη γη και το έδαφος από το διάστημα.',
                   'Συνεργάζεται με ένα δίκτυο συμβούλων που ελέγχουν ό,τι αναπτύσσουμε σε πραγματικά έργα.'],
    },
}


def home(lang):
    c = HOME[lang]
    ways = ''.join(f'<article><span class="icon-box">{icon(i)}</span><h3>{h}</h3><p>{p}</p></article>' for i, h, p in c['w'])
    company = ''.join(f'<p>{p}</p>' for p in c['c_text'])
    body = f'''<main id="top" tabindex="-1">
  <section class="hero home-hero" aria-labelledby="hero-title">
    <div class="hero-art" aria-hidden="true"></div>
    <div class="wrap hero-inner">
      <div class="hero-copy">
        <p class="eyebrow"><span class="status-dot"></span>{c['eyebrow']}</p>
        <h1 id="hero-title">{c['h1']}</h1>
        <p class="intro">{c['intro']}</p>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="products-title">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">{c['p_eyebrow']}</p><h2 id="products-title">{c['p_h2']}</h2><p class="section-intro">{c['p_intro']}</p></div>
      <div class="products">
        <article class="product-card">
          <img src="/assets/terrax/overview-{lang}.webp" alt="{c['tx_alt']}" width="2400" height="1500" loading="lazy">
          <div class="product-body">
            <div class="product-title"><h3>Ter-<em>AX</em></h3><span class="badge badge-live">{c['live']}</span></div>
            <span class="product-kicker">{c['tx_kicker']}</span>
            <p>{c['tx_text']}</p>
            <div class="product-actions"><a class="button primary" href="{APP_URL}">{T[lang]['open_tx']} <span aria-hidden="true">↗</span></a><a class="button" href="{url(lang, 'terrax')}">{c['tx_cta']} <span aria-hidden="true">→</span></a></div>
          </div>
        </article>
        <article class="product-card">
          <img src="/assets/gaia-card.webp" alt="{c['g_alt']}" width="1152" height="768" loading="lazy">
          <div class="product-body">
            <div class="product-title"><h3>GAIA</h3><span class="badge badge-dev">{c['dev']}</span></div>
            <span class="product-kicker">{c['g_kicker']}</span>
            <p>{c['g_text']}</p>
            <a class="button" href="{url(lang, 'gaia')}">{c['g_cta']} <span aria-hidden="true">→</span></a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="impact section" aria-labelledby="work-title">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">{c['w_eyebrow']}</p><h2 id="work-title">{c['w_h2']}</h2></div>
      <div class="impact-cards">{ways}</div>
    </div>
  </section>

  <section class="section" aria-labelledby="company-title">
    <div class="wrap company-grid">
      <div><p class="eyebrow">{c['c_eyebrow']}</p><h2 id="company-title">{c['c_h2']}</h2></div>
      <div>{company}</div>
    </div>
  </section>

{contact_section(lang)}</main>
'''
    return head(lang, 'home', c['title'], c['description']) + header(lang, 'home') + body + footer(lang)


# ---------------------------------------------------------------- Ter-AX
TX = {
    'en': {
        'title': 'Ter-AX — Land and site intelligence for Cyprus · AX GAIA INTELLIGENCE',
        'description': 'Analyse any parcel in Cyprus from official data: the planning zone, official checks, the parcel today, what is nearby and a PDF report.',
        'eyebrow': 'Ter-AX · Land &amp; site intelligence', 'h1': 'Know a parcel<br>before you <em>commit to it.</em>',
        'lead': ('Find a parcel by address, sheet and plan, or on the map. Ter-AX gathers what the Department of Lands and Surveys, '
                 'the Geological Survey and other public bodies publish about it, and turns it into clear answers — in seconds.'),
        'cta': 'Open Ter-AX', 'see': 'See the report', 'fine': 'Free parcel analysis and report · Greek and English',
        'shot_alt': 'Ter-AX official checks for a parcel, identifying details blurred: planning and ownership, environment, ground and natural risks',
        'g_eyebrow': '01 / What you get', 'g_h2': 'Everything mapped about a parcel, on one screen.',
        'g': [('house', 'Planning zone', 'The planning zone and its official DLS limits — building density, site coverage, floors and height — and how much of the parcel each zone covers.'),
              ('clipboard', 'Official checks', 'Geological suitability, seismic zone, landslides, floods, Natura 2000, coast protection, state land and more — each marked Check or Clear, with its source.'),
              ('terrain', 'The parcel today', 'Structures on the DLS map and from satellite detection, the nearest mapped road, slope, elevation and land cover.'),
              ('pin', 'Near the parcel', 'The nearest pharmacy, school, shop, café, bus stop and park, with straight-line distances and every place on the map.')],
        's_eyebrow': '02 / How it works', 's_h2': 'Three steps.',
        's': [('01', 'Find the parcel', 'Search by address or place, by sheet / plan and parcel number as on the title deed, or click it on the map.'),
              ('02', 'Analyse', 'Ter-AX checks the official maps for that exact boundary — in seconds.'),
              ('03', 'Read and share', 'See the answers on screen and download the free report to share with a buyer, an architect or a partner.')],
        'r_eyebrow': '03 / The report', 'r_h2': 'A report you can share.',
        'r': ['The parcel: area, planning zone, development plan, valuation, access, slope and elevation',
              'Planning zone parameters, and what they do not take into account',
              'Official checks: what needs attention and what is not in the official maps', 'What is nearby, with distances',
              'Data sources and what the report is — and is not'],
        'r_note': 'Two pages, in Greek or English. It states clearly what it is: preliminary information from official public data — not a certification, permit or confirmation of what may be built.',
        'r_alt': 'First page of a free English Ter-AX report, with identifying details blurred',
        'w_eyebrow': '04 / Who it is for', 'w_h2': 'Built for the people who decide on land.',
        'w': [('briefcase', 'Developers and investors', 'Screen parcels quickly: what the zone allows, what is already there and which checks need a professional.'),
              ('key', 'Real-estate professionals', 'Describe a property accurately and hand clients a clear, sourced report.'),
              ('house', 'Owners and buyers', 'Understand a parcel before you sell or buy.')],
        'src': 'Built on data from the Department of Lands and Surveys, the Geological Survey Department, the Water Development Department, the Department of Environment, Copernicus and OpenStreetMap.',
        'src_cta': 'Data &amp; Sources', 'src_link': 'See all sources',
    },
    'el': {
        'title': 'Ter-AX — Ανάλυση γης και τεμαχίου στην Κύπρο · AX GAIA INTELLIGENCE',
        'description': 'Ανάλυση οποιουδήποτε τεμαχίου στην Κύπρο από επίσημα δεδομένα: πολεοδομική ζώνη, επίσημοι έλεγχοι, το τεμάχιο σήμερα, τι υπάρχει κοντά και αναφορά PDF.',
        'eyebrow': 'Ter-AX · Ανάλυση γης &amp; τεμαχίου', 'h1': 'Γνωρίστε ένα τεμάχιο<br><em>πριν δεσμευτείτε.</em>',
        'lead': ('Βρείτε ένα τεμάχιο με διεύθυνση, φύλλο και σχέδιο ή στον χάρτη. Το Ter-AX συγκεντρώνει ό,τι δημοσιεύουν το Τμήμα '
                 'Κτηματολογίου και Χωρομετρίας, η Γεωλογική Επισκόπηση και άλλοι δημόσιοι φορείς και το κάνει σαφείς απαντήσεις — σε δευτερόλεπτα.'),
        'cta': 'Άνοιγμα Ter-AX', 'see': 'Δείτε την αναφορά', 'fine': 'Δωρεάν ανάλυση τεμαχίου και αναφορά · Ελληνικά και Αγγλικά',
        'shot_alt': 'Επίσημοι έλεγχοι του Ter-AX για ένα τεμάχιο, με θολωμένα τα στοιχεία ταυτότητας: πολεοδομία και ιδιοκτησία, περιβάλλον, έδαφος και φυσικοί κίνδυνοι',
        'g_eyebrow': '01 / Τι παίρνετε', 'g_h2': 'Ό,τι είναι χαρτογραφημένο για ένα τεμάχιο, σε μία οθόνη.',
        'g': [('house', 'Πολεοδομική ζώνη', 'Η πολεοδομική ζώνη και τα επίσημα όριά της από το ΤΚΧ — συντελεστής δόμησης, κάλυψη, όροφοι και ύψος — και πόσο από το τεμάχιο καλύπτει κάθε ζώνη.'),
              ('clipboard', 'Επίσημοι έλεγχοι', 'Γεωλογική καταλληλότητα, σεισμική ζώνη, κατολισθήσεις, πλημμύρες, Natura 2000, ζώνη προστασίας ακτής, κρατική γη και άλλα — με «Προσοχή» ή «Καθαρό» και την πηγή.'),
              ('terrain', 'Το τεμάχιο σήμερα', 'Κτίσματα στον χάρτη του ΤΚΧ και από δορυφορική ανίχνευση, ο πλησιέστερος χαρτογραφημένος δρόμος, κλίση, υψόμετρο και κάλυψη γης.'),
              ('pin', 'Κοντά στο τεμάχιο', 'Το πλησιέστερο φαρμακείο, σχολείο, κατάστημα, καφετέρια, στάση και πάρκο, με ευθεία απόσταση και όλα τα σημεία στον χάρτη.')],
        's_eyebrow': '02 / Πώς δουλεύει', 's_h2': 'Τρία βήματα.',
        's': [('01', 'Βρείτε το τεμάχιο', 'Αναζήτηση με διεύθυνση ή τοποθεσία, με φύλλο / σχέδιο και αριθμό τεμαχίου όπως στον τίτλο, ή με κλικ στον χάρτη.'),
              ('02', 'Ανάλυση', 'Το Ter-AX ελέγχει τους επίσημους χάρτες για το συγκεκριμένο όριο — σε δευτερόλεπτα.'),
              ('03', 'Διαβάστε και μοιραστείτε', 'Δείτε τις απαντήσεις στην οθόνη και κατεβάστε τη δωρεάν αναφορά για να τη μοιραστείτε με αγοραστή, αρχιτέκτονα ή συνεργάτη.')],
        'r_eyebrow': '03 / Η αναφορά', 'r_h2': 'Μια αναφορά που μπορείτε να μοιραστείτε.',
        'r': ['Το τεμάχιο: εμβαδόν, πολεοδομική ζώνη, σχέδιο ανάπτυξης, εκτίμηση, πρόσβαση, κλίση και υψόμετρο',
              'Οι παράμετροι της πολεοδομικής ζώνης και τι δεν λαμβάνουν υπόψη',
              'Επίσημοι έλεγχοι: τι χρειάζεται προσοχή και τι δεν βρέθηκε στους επίσημους χάρτες', 'Τι υπάρχει κοντά, με αποστάσεις',
              'Πηγές δεδομένων και τι είναι — και τι δεν είναι — η αναφορά'],
        'r_note': 'Δύο σελίδες, στα ελληνικά ή στα αγγλικά. Λέει ξεκάθαρα τι είναι: προκαταρκτική πληροφόρηση από επίσημα δημόσια δεδομένα — όχι πιστοποίηση, άδεια ή επιβεβαίωση του τι μπορεί να κτιστεί.',
        'r_alt': 'Πρώτη σελίδα δωρεάν ελληνικής αναφοράς Ter-AX, με θολωμένα τα στοιχεία ταυτότητας',
        'w_eyebrow': '04 / Για ποιους', 'w_h2': 'Για όσους παίρνουν αποφάσεις για τη γη.',
        'w': [('briefcase', 'Developers και επενδυτές', 'Γρήγορος έλεγχος τεμαχίων: τι επιτρέπει η ζώνη, τι υπάρχει ήδη και ποιοι έλεγχοι χρειάζονται επαγγελματία.'),
              ('key', 'Επαγγελματίες ακινήτων', 'Ακριβής περιγραφή ενός ακινήτου και μια σαφής αναφορά με πηγές για τους πελάτες σας.'),
              ('house', 'Ιδιοκτήτες και αγοραστές', 'Γνωρίστε ένα τεμάχιο πριν πουλήσετε ή αγοράσετε.')],
        'src': 'Με δεδομένα από το Τμήμα Κτηματολογίου και Χωρομετρίας, τη Γεωλογική Επισκόπηση, το Τμήμα Αναπτύξεως Υδάτων, το Τμήμα Περιβάλλοντος, το Copernicus και το OpenStreetMap.',
        'src_cta': 'Δεδομένα &amp; Πηγές', 'src_link': 'Δείτε όλες τις πηγές',
    },
}


def terrax(lang):
    c = TX[lang]
    gets = ''.join(f'<article><span class="icon-box">{icon(i)}</span><h3>{h}</h3><p>{p}</p></article>' for i, h, p in c['g'])
    steps = ''.join(f'<li><span>{n}</span><h3>{h}</h3><p>{p}</p></li>' for n, h, p in c['s'])
    report = ''.join(f'<li>{x}</li>' for x in c['r'])
    report_section = f'''  <section id="report" class="section" aria-labelledby="report-title">
    <div class="wrap">
      <div class="report-grid">
        <div><p class="eyebrow">{c['r_eyebrow']}</p><h2 id="report-title">{c['r_h2']}</h2><p class="section-intro">{c['r_note']}</p></div>
        <ol class="report-list">{report}</ol>
      </div>
      <div class="report-paper"><img src="/assets/terrax/report-{lang}.webp" alt="{c['r_alt']}" width="2000" height="1696" loading="lazy"></div>
    </div>
  </section>''' if SHOW_REPORT else ''
    see_button = f'''<a class="button" href="#report">{c['see']} <span aria-hidden="true">↓</span></a>''' if SHOW_REPORT else ''
    who_eyebrow = c['w_eyebrow'] if SHOW_REPORT else c['w_eyebrow'].replace('04 /', '03 /')
    who = ''.join(f'<article><span class="icon-box">{icon(i)}</span><h3>{h}</h3><p>{p}</p></article>' for i, h, p in c['w'])
    body = f'''<main id="top" tabindex="-1">
  <section class="tx-hero" aria-labelledby="hero-title">
    <div class="wrap tx-hero-grid">
      <div>
        <p class="eyebrow"><span class="status-dot"></span>{c['eyebrow']}</p>
        <h1 id="hero-title">{c['h1']}</h1>
        <p class="lead">{c['lead']}</p>
        <div class="actions"><a class="button primary" href="{APP_URL}">{c['cta']} <span aria-hidden="true">↗</span></a>{see_button}</div>
        <p class="fine">{c['fine']}</p>
      </div>
      <figure><img class="shot" src="/assets/terrax/overview-{lang}.webp" alt="{c['shot_alt']}" width="2400" height="1500"></figure>
    </div>
  </section>

  <section class="impact section" aria-labelledby="get-title">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">{c['g_eyebrow']}</p><h2 id="get-title">{c['g_h2']}</h2></div>
      <div class="impact-cards tx-cards">{gets}</div>
    </div>
  </section>

  <section class="light section" aria-labelledby="steps-title">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">{c['s_eyebrow']}</p><h2 id="steps-title">{c['s_h2']}</h2></div>
      <ol class="steps">{steps}</ol>
    </div>
  </section>

{report_section}

  <section class="impact section" aria-labelledby="who-title">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">{who_eyebrow}</p><h2 id="who-title">{c['w_h2']}</h2></div>
      <div class="impact-cards">{who}</div>
    </div>
  </section>

  <section aria-label="{c['src_cta']}">
    <div class="wrap sources-line"><p>{c['src']} <a class="sources-link" href="{url(lang, 'data')}">{c['src_link']} <span aria-hidden="true">→</span></a></p></div>
  </section>
</main>
'''
    return head(lang, 'terrax', c['title'], c['description']) + header(lang, 'terrax') + body + footer(lang)


# ---------------------------------------------------------------- Data & Sources
DS = {
    'en': {
        'title': 'Data and Sources · AX GAIA INTELLIGENCE',
        'description': 'Where Ter-AX information comes from, how it is used, its limitations and an important notice.',
        'eyebrow': 'Data &amp; Sources', 'h1': 'Where our information comes from — and what it cannot tell you.',
        'intro': 'Ter-AX brings together data published by public bodies and named open datasets. This page lists every source, how we use it and its limits.',
        'updated': 'Last updated: 13 November 2026', 'h_sources': '1. Sources',
        'cols': ['Source', 'What we use', 'How it is kept', 'Licence or terms'],
        'rows': [('Department of Lands and Surveys', 'Parcels, planning zones and their building parameters, buildings, roads, rivers, streams and lakes, state land, coast protection zone, white zones, other protected sites, geological formations, historical land use, historical aerial photographs on the map, postal-code areas, EAC pylons and high-voltage lines; property details and General Valuation of a parcel (eServices); contracts of sale, transfers and foreign buyers (Statistics)', 'Local copy refreshed weekly; some layers read live', 'CC BY 4.0 (open data); INSPIRE layers: terms being confirmed'),
                 ('Geological Survey Department', 'Geological suitability zones, seismic zones, landslides, sinkholes, engineering boreholes', 'Local copy refreshed weekly', 'Terms being confirmed'),
                 ('Water Development Department', 'Flood zones (20, 100 and 500-year); drinking-water reservoir protection zones', 'Flood zones read from the official services; reservoir zones as a local copy', 'Flood zones: terms being confirmed; reservoir zones: CC BY 4.0'),
                 ('Department of Environment', 'Natura 2000 sites, mapped habitats; strategic noise maps 2022 for roads and airports (Climate &amp; energy)', 'Natura and habitats read from the official services; noise maps as a local copy', 'Natura and habitats: terms being confirmed; noise maps: CC BY 4.0'),
                 ('Copernicus / ESA', 'Elevation and slope (Copernicus DEM GLO-30), land cover (ESA WorldCover 2021)', 'Stored copy', 'Copernicus licence; CC BY 4.0'),
                 ('European Commission JRC (GHSL)', 'Built-up area (Statistics and map layer)', 'Stored copy of the published release', 'CC BY 4.0'),
                 ('Central Bank of Cyprus', 'Residential property price index by district and type (Statistics)', 'Stored copy, refreshed each quarter', 'Free to reuse with attribution; shown as published'),
                 ('Statistical Service (CYSTAT) / Eurostat', 'House price index, consumer prices and building permits (Statistics)', 'Stored copy, refreshed when new figures are published', 'CYSTAT terms (reuse with attribution); Eurostat reuse policy'),
                 ('Global Solar Atlas (World Bank Group / ESMAP, data © Solargis)', 'Solar potential: PV output, sunlight, best panel tilt (Climate &amp; energy)', 'Stored copy of the published release', 'CC BY 4.0'),
                 ('TerraClimate (Climatology Lab)', 'Climate 1991–2020: temperature, rain, humidity (Climate &amp; energy)', 'Stored copy of the published release', 'CC0 1.0'),
                 ('CHELSA (Swiss Federal Institute WSL)', 'Climate projections 2041–2070 from five climate models (Climate &amp; energy)', 'Stored copy of the published release', 'CC BY 4.0'),
                 ('European Environment Agency', 'Air quality 2023: fine particles (PM2.5) and nitrogen dioxide (Climate &amp; energy)', 'Stored copy of the published release', 'CC BY 4.0'),
                 ('Global Wind Atlas (DTU Wind Energy / World Bank Group)', 'Mean wind speed at 10 m and 100 m (Climate &amp; energy); Davis et al. 2023, BAMS 104(8)', 'Stored copy of the published release', 'CC BY 4.0'),
                 ('OpenStreetMap contributors', 'Nearby places; key distances (airports, hospitals, police, fire stations, bus stops, sea and more); the on-screen map (drawn with Protomaps)', 'Snapshot of the Cyprus extract, refreshed periodically', 'ODbL 1.0'),
                 ('Microsoft', 'Building footprints detected from satellite imagery', 'Stored copy of the published release', 'ODbL 1.0'),
                 ('Esri World Imagery (Vantor)', 'Satellite base map on screen only', 'Displayed, never stored or analysed', 'Esri terms of use')],
        'h_use': '2. How we use the data',
        'use': ['We measure: areas, distances and overlaps between the parcel boundary and each official layer.',
                'We calculate only from official parameters, for example area from zone density = zone area × building density.',
                'We do not estimate values, interpret development plans or decide permitted uses.',
                'When an official dataset is missing or does not answer, we say so instead of filling the gap.'],
        'h_limits': '3. Limitations',
        'limits': ['Ter-AX is a preliminary screening based on available mapped data.',
                   'It does not replace title or encumbrance searches, valuation, planning advice, planning or building permission, environmental assessment, ecological or geotechnical investigation, or confirmation of utility connections.',
                   'No mapped issue does not mean there is no risk, restriction or missing data.',
                   'Dataset dates and coverage vary. The date we retrieved data is not the date a rule took legal effect.',
                   'The DLS building map is incomplete and undated; satellite detection shows what is visible, not whether it is permitted or registered.',
                   'Distances are straight lines, not routes or legal access. OpenStreetMap data is community data and may be incomplete.'],
        'h_notice': '4. Important notice',
        'notice': ['Ter-AX is an independent service of AX GAIA Intelligence Ltd. It is not affiliated with, endorsed by or acting for the Department of Lands and Surveys or any other public body named on this page.',
                   'Information is provided for preliminary screening only. It is not planning, legal, valuation, engineering or investment advice. Confirm anything you rely on with a licensed architect, town planner, engineer or lawyer.'],
        'h_corr': '5. Corrections', 'corr': 'Found something wrong or out of date? Tell us and we will check it against the source.',
    },
    'el': {
        'title': 'Δεδομένα και Πηγές · AX GAIA INTELLIGENCE',
        'description': 'Από πού προέρχονται τα στοιχεία του Ter-AX, πώς χρησιμοποιούνται, οι περιορισμοί τους και σημαντική σημείωση.',
        'eyebrow': 'Δεδομένα &amp; Πηγές', 'h1': 'Από πού προέρχονται τα στοιχεία μας — και τι δεν μπορούν να σας πουν.',
        'intro': 'Το Ter-AX συγκεντρώνει δεδομένα που δημοσιεύουν δημόσιοι φορείς και ονομαστικά ανοιχτά σύνολα δεδομένων. Εδώ θα βρείτε κάθε πηγή, πώς τη χρησιμοποιούμε και τα όριά της.',
        'updated': 'Τελευταία ενημέρωση: 13 Νοεμβρίου 2026', 'h_sources': '1. Πηγές',
        'cols': ['Πηγή', 'Τι χρησιμοποιούμε', 'Πώς ενημερώνεται', 'Άδεια ή όροι'],
        'rows': [('Τμήμα Κτηματολογίου και Χωρομετρίας', 'Τεμάχια, πολεοδομικές ζώνες και οι όροι δόμησής τους, κτίρια, δρόμοι, ποτάμια, ρέματα και λίμνες, κρατική γη, ζώνη προστασίας ακτής, λευκές ζώνες, άλλες προστατευόμενες περιοχές, γεωλογικοί σχηματισμοί, ιστορική χρήση γης, παλιές αεροφωτογραφίες στον χάρτη, ταχυδρομικοί κώδικες, πυλώνες και γραμμές υψηλής τάσης ΑΗΚ· στοιχεία ακινήτου και Γενική Εκτίμηση τεμαχίου (eServices)· πωλητήρια έγγραφα, μεταβιβάσεις και ξένοι αγοραστές (Στατιστικά)', 'Τοπικό αντίγραφο με εβδομαδιαία ενημέρωση· ορισμένα επίπεδα απευθείας', 'CC BY 4.0 (ανοιχτά δεδομένα)· επίπεδα INSPIRE: οι όροι επιβεβαιώνονται'),
                 ('Γεωλογική Επισκόπηση', 'Ζώνες γεωλογικής καταλληλότητας, σεισμικές ζώνες, κατολισθήσεις, καταβόθρες, γεωτεχνικές γεωτρήσεις', 'Τοπικό αντίγραφο με εβδομαδιαία ενημέρωση', 'Οι όροι επιβεβαιώνονται'),
                 ('Τμήμα Αναπτύξεως Υδάτων', 'Ζώνες πλημμύρας (20, 100 και 500 ετών)· ζώνες προστασίας ταμιευτήρων πόσιμου νερού', 'Πλημμύρες απευθείας από τις επίσημες υπηρεσίες· ταμιευτήρες ως τοπικό αντίγραφο', 'Πλημμύρες: οι όροι επιβεβαιώνονται· ταμιευτήρες: CC BY 4.0'),
                 ('Τμήμα Περιβάλλοντος', 'Περιοχές Natura 2000, χαρτογραφημένοι οικότοποι· στρατηγικοί χάρτες θορύβου 2022 για δρόμους και αεροδρόμια (Κλίμα &amp; ενέργεια)', 'Natura και οικότοποι απευθείας από τις επίσημες υπηρεσίες· χάρτες θορύβου ως τοπικό αντίγραφο', 'Natura και οικότοποι: οι όροι επιβεβαιώνονται· χάρτες θορύβου: CC BY 4.0'),
                 ('Copernicus / ESA', 'Υψόμετρο και κλίση (Copernicus DEM GLO-30), κάλυψη γης (ESA WorldCover 2021)', 'Αποθηκευμένο αντίγραφο', 'Άδεια Copernicus· CC BY 4.0'),
                 ('Ευρωπαϊκή Επιτροπή JRC (GHSL)', 'Δομημένη επιφάνεια (Στατιστικά και επίπεδο χάρτη)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC BY 4.0'),
                 ('Κεντρική Τράπεζα Κύπρου', 'Δείκτης τιμών κατοικιών ανά επαρχία και τύπο (Στατιστικά)', 'Αποθηκευμένο αντίγραφο, ενημερώνεται κάθε τρίμηνο', 'Ελεύθερη χρήση με αναφορά· εμφανίζεται όπως δημοσιεύεται'),
                 ('Στατιστική Υπηρεσία (ΚΥΣΤΑΤ) / Eurostat', 'Δείκτης τιμών κατοικιών, τιμές καταναλωτή και άδειες οικοδομής (Στατιστικά)', 'Αποθηκευμένο αντίγραφο, ενημερώνεται όταν δημοσιεύονται νέα στοιχεία', 'Όροι ΚΥΣΤΑΤ (χρήση με αναφορά)· πολιτική επαναχρησιμοποίησης Eurostat'),
                 ('Global Solar Atlas (Ομάδα Παγκόσμιας Τράπεζας / ESMAP, δεδομένα © Solargis)', 'Ηλιακό δυναμικό: παραγωγή φωτοβολταϊκού, ηλιακή ακτινοβολία, βέλτιστη κλίση (Κλίμα &amp; ενέργεια)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC BY 4.0'),
                 ('TerraClimate (Climatology Lab)', 'Κλίμα 1991–2020: θερμοκρασία, βροχή, υγρασία (Κλίμα &amp; ενέργεια)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC0 1.0'),
                 ('CHELSA (Ελβετικό Ομοσπονδιακό Ινστιτούτο WSL)', 'Κλιματικές προβλέψεις 2041–2070 από πέντε κλιματικά μοντέλα (Κλίμα &amp; ενέργεια)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC BY 4.0'),
                 ('Ευρωπαϊκός Οργανισμός Περιβάλλοντος', 'Ποιότητα αέρα 2023: λεπτά σωματίδια (PM2.5) και διοξείδιο του αζώτου (Κλίμα &amp; ενέργεια)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC BY 4.0'),
                 ('Global Wind Atlas (DTU Wind Energy / Ομάδα Παγκόσμιας Τράπεζας)', 'Μέση ταχύτητα ανέμου στα 10 m και 100 m (Κλίμα &amp; ενέργεια)· Davis et al. 2023, BAMS 104(8)', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'CC BY 4.0'),
                 ('Συντελεστές OpenStreetMap', 'Κοντινά σημεία· βασικές αποστάσεις (αεροδρόμια, νοσοκομεία, αστυνομία, πυροσβεστική, στάσεις λεωφορείων, θάλασσα κ.ά.)· ο χάρτης στην οθόνη (σχεδιασμένος με Protomaps)', 'Στιγμιότυπο των δεδομένων της Κύπρου, με περιοδική ενημέρωση', 'ODbL 1.0'),
                 ('Microsoft', 'Περιγράμματα κτισμάτων από δορυφορική ανίχνευση', 'Αποθηκευμένο αντίγραφο της δημοσιευμένης έκδοσης', 'ODbL 1.0'),
                 ('Esri World Imagery (Vantor)', 'Δορυφορικό υπόβαθρο μόνο στην οθόνη', 'Εμφανίζεται, δεν αποθηκεύεται ούτε αναλύεται', 'Όροι χρήσης Esri')],
        'h_use': '2. Πώς χρησιμοποιούμε τα δεδομένα',
        'use': ['Μετράμε: εμβαδά, αποστάσεις και επικαλύψεις του ορίου του τεμαχίου με κάθε επίσημο επίπεδο.',
                'Υπολογίζουμε μόνο από επίσημους όρους, για παράδειγμα εμβαδόν βάσει συντελεστή = εμβαδόν ζώνης × συντελεστής δόμησης.',
                'Δεν εκτιμούμε αξίες, δεν ερμηνεύουμε σχέδια ανάπτυξης και δεν κρίνουμε επιτρεπόμενες χρήσεις.',
                'Όταν ένα επίσημο σύνολο δεδομένων λείπει ή δεν απαντά, το λέμε αντί να συμπληρώνουμε το κενό.'],
        'h_limits': '3. Περιορισμοί',
        'limits': ['Το Ter-AX είναι προκαταρκτικός έλεγχος με βάση τα διαθέσιμα χαρτογραφημένα δεδομένα.',
                   'Δεν αντικαθιστά έρευνα τίτλου και βαρών, εκτίμηση αξίας, πολεοδομική συμβουλή, πολεοδομική ή οικοδομική άδεια, περιβαλλοντική μελέτη, οικολογική ή γεωτεχνική διερεύνηση, ή επιβεβαίωση συνδέσεων με δίκτυα.',
                   'Η απουσία χαρτογραφημένου ζητήματος δεν σημαίνει ότι δεν υπάρχει κίνδυνος, περιορισμός ή ελλιπή δεδομένα.',
                   'Οι ημερομηνίες και η κάλυψη των δεδομένων διαφέρουν. Η ημερομηνία λήψης δεν είναι η ημερομηνία νομικής ισχύος ενός κανόνα.',
                   'Ο χάρτης κτιρίων του ΤΚΧ δεν είναι πλήρης ούτε χρονολογημένος· η δορυφορική ανίχνευση δείχνει τι φαίνεται, όχι αν ένα κτίσμα είναι νόμιμο ή εγγεγραμμένο.',
                   'Οι αποστάσεις είναι ευθείες, όχι διαδρομές ή νόμιμη πρόσβαση. Τα δεδομένα OpenStreetMap είναι κοινοτικά και μπορεί να μην είναι πλήρη.'],
        'h_notice': '4. Σημαντική σημείωση',
        'notice': ['Το Ter-AX είναι ανεξάρτητη υπηρεσία της AX GAIA Intelligence Ltd. Δεν συνδέεται, δεν εγκρίνεται και δεν ενεργεί για λογαριασμό του Τμήματος Κτηματολογίου και Χωρομετρίας ή άλλου δημόσιου φορέα που αναφέρεται σε αυτή τη σελίδα.',
                   'Οι πληροφορίες δίνονται μόνο για προκαταρκτικό έλεγχο. Δεν αποτελούν πολεοδομική, νομική, εκτιμητική, μηχανική ή επενδυτική συμβουλή. Επιβεβαιώστε ό,τι χρειάζεστε με αδειούχο αρχιτέκτονα, πολεοδόμο, μηχανικό ή δικηγόρο.'],
        'h_corr': '5. Διορθώσεις', 'corr': 'Βρήκατε κάτι λάθος ή παλιό; Πείτε μας και θα το ελέγξουμε με την πηγή.',
    },
}


def data_sources(lang):
    c = DS[lang]
    head_row = ''.join(f'<th scope="col">{x}</th>' for x in c['cols'])
    rows = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in c['rows'])
    li = lambda items: ''.join(f'<li>{x}</li>' for x in items)
    notice = ''.join(f'<p>{x}</p>' for x in c['notice'])
    body = f'''<main id="top" tabindex="-1">
  <section class="doc-hero" aria-labelledby="hero-title">
    <div class="wrap"><p class="eyebrow">{c['eyebrow']}</p><h1 id="hero-title">{c['h1']}</h1><p class="section-intro">{c['intro']}</p><p class="updated">{c['updated']}</p></div>
  </section>
  <section class="section" aria-labelledby="sources-title">
    <div class="wrap"><h2 id="sources-title">{c['h_sources']}</h2>
      <div class="table-box"><table class="sources-table"><thead><tr>{head_row}</tr></thead><tbody>{rows}</tbody></table></div>
    </div>
  </section>
  <section class="impact section">
    <div class="wrap doc-columns">
      <div><h2>{c['h_use']}</h2><ul class="doc-list">{li(c['use'])}</ul></div>
      <div><h2>{c['h_limits']}</h2><ul class="doc-list">{li(c['limits'])}</ul></div>
    </div>
  </section>
  <section class="section" aria-labelledby="notice-title">
    <div class="wrap"><h2 id="notice-title">{c['h_notice']}</h2><div class="notice">{notice}</div></div>
  </section>
  <section class="contact" aria-labelledby="corr-title">
    <div class="wrap corrections"><div><h2 id="corr-title">{c['h_corr']}</h2><p>{c['corr']}</p></div><a class="button" href="mailto:{EMAIL}?subject=Data%20correction">{EMAIL} <span aria-hidden="true">↗</span></a></div>
  </section>
</main>
'''
    return head(lang, 'data', c['title'], c['description']) + header(lang, 'data') + body + footer(lang)


# ---------------------------------------------------------------- GAIA (today's page)
GAIA_EL = [
    ('Space-enabled ground intelligence', 'Πληροφορία για το έδαφος από το διάστημα'),
    ('A clearer picture.<br>From space to<br><em>SUBSURFACE.</em>', 'Μια πιο καθαρή εικόνα.<br>Από το διάστημα<br><em>ΣΤΟ ΥΠΕΔΑΦΟΣ.</em>'),
    ('GAIA is a space-enabled ground intelligence platform for construction and infrastructure. It combines Earth Observation with ground-sensing data to provide early indications of potential ground risks and support better-targeted site and geotechnical investigations.',
     'Το GAIA είναι πλατφόρμα πληροφορίας για το έδαφος από το διάστημα, για κατασκευές και υποδομές. Συνδυάζει την παρατήρηση της Γης με μετρήσεις εδάφους, ώστε να δίνει έγκαιρες ενδείξεις πιθανών εδαφικών κινδύνων και να στηρίζει πιο στοχευμένες έρευνες πεδίου και γεωτεχνικές έρευνες.'),
    ('Explore GAIA', 'Γνωρίστε το GAIA'), ('>In development<', '>Σε ανάπτυξη<'),
    ('EARLY INSIGHT. BETTER-INFORMED DECISIONS.', 'ΕΓΚΑΙΡΗ ΓΝΩΣΗ. ΚΑΛΥΤΕΡΕΣ ΑΠΟΦΑΣΕΙΣ.'),
    ('01 / THE PLATFORM', '01 / Η ΠΛΑΤΦΟΡΜΑ'),
    ('Understand the ground.<br>Before the groundwork.', 'Γνωρίστε το έδαφος.<br>Πριν από τις εργασίες.'),
    ('GAIA brings together Earth Observation and ground-sensing data to provide early site intelligence and help identify where further investigation may be needed.',
     'Το GAIA συνδυάζει την παρατήρηση της Γης με μετρήσεις εδάφους, για έγκαιρη πληροφορία για τον χώρο και για να φαίνεται πού μπορεί να χρειάζεται περαιτέρω έρευνα.'),
    ('Early indicators', 'Έγκαιρες ενδείξεις'),
    ('Identify areas of variability, anomalies and potential ground concern early in project planning.', 'Εντοπισμός περιοχών με μεταβλητότητα, ανωμαλίες και πιθανά εδαφικά ζητήματα νωρίς στον σχεδιασμό του έργου.'),
    ('Site-wide perspective', 'Εικόνα για όλο τον χώρο'),
    ('Combine wide-area Earth Observation with complementary site-level information.', 'Συνδυασμός της παρατήρησης της Γης σε μεγάλη έκταση με συμπληρωματική πληροφορία για τον χώρο.'),
    ('Targeted investigation', 'Στοχευμένη έρευνα'),
    ('Support engineers in prioritising areas for further site and geotechnical investigation.', 'Υποστήριξη των μηχανικών στην επιλογή περιοχών για περαιτέρω έρευνα πεδίου και γεωτεχνική έρευνα.'),
    ('Earth Observation and ground sensing feed into GAIA analysis to support engineering decisions', 'Η παρατήρηση της Γης και οι μετρήσεις εδάφους τροφοδοτούν την ανάλυση του GAIA για τη στήριξη μηχανικών αποφάσεων'),
    ('<h3>Earth Observation</h3><p>Wide-area view of surface behaviour and change.</p>', '<h3>Παρατήρηση της Γης</h3><p>Εικόνα μεγάλης έκτασης για τη συμπεριφορά και τις αλλαγές της επιφάνειας.</p>'),
    ('<h3>Ground Sensing</h3><p>Site-level information on shallow subsurface conditions.</p>', '<h3>Μετρήσεις εδάφους</h3><p>Πληροφορία για τις συνθήκες του επιφανειακού υπεδάφους στον χώρο.</p>'),
    ('<p>Data integration<br>and analysis</p>', '<p>Συνδυασμός<br>και ανάλυση δεδομένων</p>'),
    ('<h3>Engineering decision support</h3><p>Clear, interpretable outputs to support planning and investigation.</p>', '<h3>Υποστήριξη μηχανικών αποφάσεων</h3><p>Σαφή, κατανοητά αποτελέσματα για τον σχεδιασμό και την έρευνα.</p>'),
    ('02 / HOW IT WORKS', '02 / ΠΩΣ ΔΟΥΛΕΥΕΙ'),
    ('From data to<br>decision-ready insights.', 'Από τα δεδομένα<br>σε γνώση για αποφάσεις.'),
    ('GAIA integrates satellite-derived ground behaviour with ground-sensing data to generate clear, site-specific indicators that support engineering decisions.',
     'Το GAIA συνδυάζει τη συμπεριφορά του εδάφους από δορυφόρο με μετρήσεις εδάφους, για σαφείς ενδείξεις για κάθε χώρο που στηρίζουν μηχανικές αποφάσεις.'),
    ('aria-label="GAIA process"', 'aria-label="Η διαδικασία του GAIA"'),
    ('Conceptual aerial view of a coastal investigation site', 'Εννοιολογική αεροφωτογραφία παράκτιου χώρου έρευνας'),
    ('Conceptual Earth Observation heatmap', 'Εννοιολογικός θερμικός χάρτης παρατήρησης της Γης'),
    ('Conceptual site data interpretation', 'Εννοιολογική ερμηνεία δεδομένων χώρου'),
    ('Conceptual construction and investigation site', 'Εννοιολογικός χώρος κατασκευής και έρευνας'),
    ('<h3>Collect</h3><p>Earth Observation data and complementary ground-sensing information.</p>', '<h3>Συλλογή</h3><p>Δεδομένα παρατήρησης της Γης και συμπληρωματικές μετρήσεις εδάφους.</p>'),
    ('<h3>Analyse</h3><p>Process and integrate datasets with machine-learning models to identify patterns, anomalies and areas of interest.</p>', '<h3>Ανάλυση</h3><p>Επεξεργασία και συνδυασμός δεδομένων με μοντέλα μηχανικής μάθησης για τον εντοπισμό μοτίβων, ανωμαλιών και περιοχών ενδιαφέροντος.</p>'),
    ('<h3>Interpret</h3><p>Generate clear, engineering-relevant outputs.</p>', '<h3>Ερμηνεία</h3><p>Σαφή αποτελέσματα, χρήσιμα για μηχανικούς.</p>'),
    ('<h3>Support</h3><p>Help prioritise further investigation and reduce uncertainty in early project stages.</p>', '<h3>Υποστήριξη</h3><p>Βοήθεια στην ιεράρχηση της περαιτέρω έρευνας και λιγότερη αβεβαιότητα στα πρώτα στάδια του έργου.</p>'),
    ('03 / IMPACT', '03 / ΟΦΕΛΟΣ'),
    ('Supporting safer,<br>smarter and more efficient<br>infrastructure development.', 'Για πιο ασφαλή,<br>έξυπνη και αποδοτική<br>ανάπτυξη υποδομών.'),
    ('By providing early insights on ground conditions, GAIA is designed to help reduce uncertainty, focus investigation efforts and support more informed decisions across the project lifecycle.',
     'Με έγκαιρη γνώση για τις συνθήκες του εδάφους, το GAIA σχεδιάζεται για να βοηθά να μειωθεί η αβεβαιότητα, να εστιαστούν οι έρευνες και να παίρνονται καλύτερες αποφάσεις σε όλη τη διάρκεια του έργου.'),
    ('<h3>Reduced<br>uncertainty</h3><p>Better understanding of ground conditions earlier.</p>', '<h3>Λιγότερη<br>αβεβαιότητα</h3><p>Καλύτερη γνώση των συνθηκών του εδάφους, νωρίτερα.</p>'),
    ('<h3>More efficient<br>investigations</h3><p>Focus resources where they are needed most.</p>', '<h3>Πιο αποδοτικές<br>έρευνες</h3><p>Οι πόροι πηγαίνουν εκεί που χρειάζονται περισσότερο.</p>'),
    ('<h3>More informed<br>decisions</h3><p>Support safer, more resilient and cost-effective projects.</p>', '<h3>Καλύτερες<br>αποφάσεις</h3><p>Πιο ασφαλή, ανθεκτικά και οικονομικά έργα.</p>'),
    ('Conceptual coastal construction site with an Earth Observation data overlay', 'Εννοιολογικό παράκτιο εργοτάξιο με επίστρωση δεδομένων παρατήρησης της Γης'),
    ('04 / DEVELOPMENT', '04 / ΑΝΑΠΤΥΞΗ'),
    ('Built for real-world<br>conditions.', 'Σχεδιασμένο για<br>πραγματικές συνθήκες.'),
    ('GAIA has moved through architecture design and indicator modelling and is now in pilot validation: its indicators are being tested against ground-sensing surveys and geotechnical data from a real site in Cyprus.',
     'Το GAIA πέρασε από τον σχεδιασμό της αρχιτεκτονικής και τη μοντελοποίηση δεικτών και βρίσκεται τώρα σε πιλοτική επικύρωση: οι δείκτες του ελέγχονται με μετρήσεις εδάφους και γεωτεχνικά δεδομένα από πραγματικό χώρο στην Κύπρο.'),
    ('<strong>Available today: Ter-AX</strong> — free parcel analysis from official data.', '<strong>Διαθέσιμο σήμερα: Ter-AX</strong> — δωρεάν ανάλυση τεμαχίου από επίσημα δεδομένα.'),
    ('href="/terrax/">Discover Ter-AX', 'href="/el/terrax/">Γνωρίστε το Ter-AX'), ('* Illustrations on this page are conceptual.', '* Οι εικόνες της σελίδας είναι ενδεικτικές.'),
    ('✓ Completed', '✓ Ολοκληρώθηκε'), ('● In progress', '● Σε εξέλιξη'), ('01 · Architecture design', '01 · Σχεδιασμός αρχιτεκτονικής'), ('02 · Indicator modelling', '02 · Μοντελοποίηση δεικτών'), ('03 · Pilot validation', '03 · Πιλοτική επικύρωση'),
    ('An AI framework that fuses satellite and ground-sensing data.', 'Ένα πλαίσιο τεχνητής νοημοσύνης που συνδυάζει δορυφορικά δεδομένα και μετρήσεις εδάφους.'), ('Engineering-relevant indicators of subsurface conditions.', 'Δείκτες για τις συνθήκες του υπεδάφους, χρήσιμοι για μηχανικούς.'), ('Testing the indicators against field surveys and geotechnical data at a real site in Cyprus.', 'Έλεγχος των δεικτών με μετρήσεις πεδίου και γεωτεχνικά δεδομένα σε πραγματικό χώρο στην Κύπρο.'),
]


def gaia(lang):
    main = (ROOT / 'tools' / 'gaia_main_en.html').read_text(encoding='utf-8').replace('src="assets/', 'src="/assets/').replace('href="#contact"', f'href="{url(lang, "home")}#contact"')
    if lang == 'el':
        for en, el in GAIA_EL:
            assert en in main, en
            main = main.replace(en, el)
    title = ('GAIA — Πληροφορία για το έδαφος από το διάστημα · AX GAIA INTELLIGENCE' if lang == 'el'
             else 'GAIA — Space-enabled ground intelligence · AX GAIA INTELLIGENCE')
    description = ('Το GAIA συνδυάζει την παρατήρηση της Γης με μετρήσεις εδάφους για έγκαιρη πληροφορία για τον χώρο και πιο στοχευμένες γεωτεχνικές έρευνες.'
                   if lang == 'el' else
                   'GAIA combines Earth Observation and ground-sensing data to provide early site intelligence and support better-targeted site and geotechnical investigations.')
    return head(lang, 'gaia', title, description) + header(lang, 'gaia') + main + '\n' + footer(lang)


# ---------------------------------------------------------------- Privacy Policy
PRIVACY = {
    'en': {
        'title': 'Privacy Policy · AX GAIA INTELLIGENCE',
        'description': 'How AX GAIA Intelligence Ltd handles personal data on this website and in email.',
        'eyebrow': 'Legal', 'h1': 'Privacy Policy', 'updated': 'Last updated: 11 November 2026',
        'intro': 'This policy explains what personal data is processed when you visit this website or email us, why, and what rights you have.',
        'sections': [
            ('1. Who we are', [
                'AX GAIA Intelligence Ltd, a company registered in Cyprus, is the controller of the personal data described here.',
                f'Contact for any privacy question: <a href="mailto:{EMAIL}">{EMAIL}</a>.',
                'This policy covers this website and email sent to us. The Ter-AX application at <a href="https://tx.axgaiaintelligence.com/">tx.axgaiaintelligence.com</a> has its own <a href="https://tx.axgaiaintelligence.com/privacy">Privacy Policy</a> and <a href="https://tx.axgaiaintelligence.com/terms">Terms of Use</a>.']),
            ('2. What we process and why', [
                '<strong>When you visit the website.</strong> Our hosting provider processes technical data such as your IP address, browser and device type, the pages requested and the time, to deliver the pages and keep the service secure. We do not receive or keep these records. Legal basis: our legitimate interest in running a secure website (GDPR Article 6(1)(f)).',
                '<strong>When you email us.</strong> We use your email address, your name and whatever you write, to reply and to deal with your request. Legal basis: steps you ask for before a possible agreement (Article 6(1)(b)) and our legitimate interest in answering enquiries (Article 6(1)(f)).']),
            ('3. What we do not do', [
                'There are no forms, accounts, cookies, analytics, advertising or tracking on this website.',
                'Fonts, images and scripts are served from this website itself; no third-party content is loaded when you open a page.',
                'We do not sell personal data or use it for marketing without your permission.']),
            ('4. Service providers', [
                'GitHub, Inc. hosts this website (GitHub Pages). Microsoft provides our email (Microsoft 365).',
                'These providers may process data outside the European Economic Area. Such transfers rely on the safeguards they offer, such as the EU–US Data Privacy Framework and the European Commission’s Standard Contractual Clauses.']),
            ('5. How long we keep it', [
                'Emails are kept for as long as needed to deal with your enquiry and any work that follows from it. We review old correspondence at least once a year and delete what is no longer needed, unless the law requires us to keep it.']),
            ('6. Your rights', [
                'You can ask to access, correct or delete your personal data, to restrict or object to its use, and to receive it in a portable form. Email us and we will reply within one month.',
                'You can also complain to the Office of the Commissioner for Personal Data Protection in Cyprus (<a href="https://www.dataprotection.gov.cy" target="_blank" rel="noopener noreferrer">dataprotection.gov.cy</a>).']),
            ('7. Other websites', [
                'Links to other websites, such as Space BIC, are covered by those websites’ own privacy policies.']),
            ('8. Changes', [
                'If this policy changes, we will update this page and the date at the top.']),
        ],
    },
    'el': {
        'title': 'Πολιτική απορρήτου · AX GAIA INTELLIGENCE',
        'description': 'Πώς η AX GAIA Intelligence Ltd χειρίζεται τα προσωπικά δεδομένα σε αυτή την ιστοσελίδα και στο email.',
        'eyebrow': 'Νομικά', 'h1': 'Πολιτική απορρήτου', 'updated': 'Τελευταία ενημέρωση: 11 Νοεμβρίου 2026',
        'intro': 'Η πολιτική αυτή εξηγεί ποια προσωπικά δεδομένα επεξεργάζονται όταν επισκέπτεστε την ιστοσελίδα ή μας στέλνετε email, για ποιο λόγο, και ποια δικαιώματα έχετε.',
        'sections': [
            ('1. Ποιοι είμαστε', [
                'Υπεύθυνη επεξεργασίας των προσωπικών δεδομένων που περιγράφονται εδώ είναι η AX GAIA Intelligence Ltd, εταιρεία εγγεγραμμένη στην Κύπρο.',
                f'Για κάθε ερώτηση σχετικά με το απόρρητο: <a href="mailto:{EMAIL}">{EMAIL}</a>.',
                'Η πολιτική καλύπτει αυτή την ιστοσελίδα και τα email που μας στέλνετε. Η εφαρμογή Ter-AX στο <a href="https://tx.axgaiaintelligence.com/">tx.axgaiaintelligence.com</a> έχει δική της <a href="https://tx.axgaiaintelligence.com/privacy">Πολιτική Απορρήτου</a> και <a href="https://tx.axgaiaintelligence.com/terms">Όρους Χρήσης</a>.']),
            ('2. Τι επεξεργαζόμαστε και γιατί', [
                '<strong>Όταν επισκέπτεστε την ιστοσελίδα.</strong> Ο πάροχος φιλοξενίας επεξεργάζεται τεχνικά στοιχεία, όπως τη διεύθυνση IP, τον τύπο browser και συσκευής, τις σελίδες που ζητήθηκαν και την ώρα, για να εμφανίσει τις σελίδες και να κρατήσει την υπηρεσία ασφαλή. Εμείς δεν λαμβάνουμε ούτε κρατάμε αυτά τα αρχεία. Νομική βάση: το έννομο συμφέρον μας να λειτουργεί η ιστοσελίδα με ασφάλεια (άρθρο 6(1)(στ) ΓΚΠΔ).',
                '<strong>Όταν μας στέλνετε email.</strong> Χρησιμοποιούμε τη διεύθυνση email, το όνομά σας και ό,τι μας γράψετε, για να σας απαντήσουμε και να ικανοποιήσουμε το αίτημά σας. Νομική βάση: ενέργειες που ζητάτε πριν από πιθανή συμφωνία (άρθρο 6(1)(β)) και το έννομο συμφέρον μας να απαντάμε σε ερωτήματα (άρθρο 6(1)(στ)).']),
            ('3. Τι δεν κάνουμε', [
                'Η ιστοσελίδα δεν έχει φόρμες, λογαριασμούς, cookies, στατιστικά επισκεψιμότητας, διαφημίσεις ή παρακολούθηση.',
                'Γραμματοσειρές, εικόνες και scripts φορτώνονται από την ίδια την ιστοσελίδα· όταν ανοίγετε μια σελίδα δεν φορτώνεται περιεχόμενο τρίτων.',
                'Δεν πουλάμε προσωπικά δεδομένα και δεν τα χρησιμοποιούμε για προώθηση χωρίς τη συγκατάθεσή σας.']),
            ('4. Πάροχοι υπηρεσιών', [
                'Η GitHub, Inc. φιλοξενεί την ιστοσελίδα (GitHub Pages). Η Microsoft παρέχει το email μας (Microsoft 365).',
                'Οι πάροχοι αυτοί μπορεί να επεξεργάζονται δεδομένα εκτός του Ευρωπαϊκού Οικονομικού Χώρου. Οι διαβιβάσεις αυτές στηρίζονται στις εγγυήσεις που προσφέρουν, όπως το Πλαίσιο Προστασίας Δεδομένων ΕΕ–ΗΠΑ και οι Τυποποιημένες Συμβατικές Ρήτρες της Ευρωπαϊκής Επιτροπής.']),
            ('5. Πόσο καιρό τα κρατάμε', [
                'Τα email κρατούνται όσο χρειάζεται για το ερώτημά σας και για όποια συνεργασία προκύψει. Ελέγχουμε την παλιά αλληλογραφία τουλάχιστον μία φορά τον χρόνο και διαγράφουμε ό,τι δεν χρειάζεται πια, εκτός αν ο νόμος μάς υποχρεώνει να το κρατήσουμε.']),
            ('6. Τα δικαιώματά σας', [
                'Μπορείτε να ζητήσετε πρόσβαση, διόρθωση ή διαγραφή των προσωπικών σας δεδομένων, περιορισμό ή εναντίωση στη χρήση τους, και να τα λάβετε σε φορητή μορφή. Στείλτε μας email και θα απαντήσουμε μέσα σε έναν μήνα.',
                'Μπορείτε επίσης να υποβάλετε παράπονο στο Γραφείο της Επιτρόπου Προστασίας Δεδομένων Προσωπικού Χαρακτήρα (<a href="https://www.dataprotection.gov.cy" target="_blank" rel="noopener noreferrer">dataprotection.gov.cy</a>).']),
            ('7. Άλλες ιστοσελίδες', [
                'Οι σύνδεσμοι προς άλλες ιστοσελίδες, όπως το Space BIC, διέπονται από τις δικές τους πολιτικές απορρήτου.']),
            ('8. Αλλαγές', [
                'Αν η πολιτική αλλάξει, θα ενημερώσουμε αυτή τη σελίδα και την ημερομηνία στην κορυφή.']),
        ],
    },
}


def privacy(lang):
    c = PRIVACY[lang]
    sections = ''.join(f'''
  <section class="section policy" aria-labelledby="p{i}">
    <div class="wrap"><h2 id="p{i}">{title}</h2>{''.join(f'<p>{x}</p>' for x in paras)}</div>
  </section>''' for i, (title, paras) in enumerate(c['sections'], 1))
    body = f'''<main id="top" tabindex="-1">
  <section class="doc-hero" aria-labelledby="hero-title">
    <div class="wrap"><p class="eyebrow">{c['eyebrow']}</p><h1 id="hero-title">{c['h1']}</h1><p class="section-intro">{c['intro']}</p><p class="updated">{c['updated']}</p></div>
  </section>{sections}
</main>
'''
    return head(lang, 'privacy', c['title'], c['description']) + header(lang, 'privacy') + body + footer(lang)


def privacy_forward():
    target = SITE + url('en', 'privacy')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta http-equiv="refresh" content="0; url={url('en', 'privacy')}">
  <link rel="canonical" href="{target}">
  <title>Privacy Policy · AX GAIA INTELLIGENCE</title>
</head>
<body><p>The Privacy Policy has moved to <a href="{url('en', 'privacy')}">{target}</a>.</p></body>
</html>
'''


def main():
    builders = {'home': home, 'terrax': terrax, 'gaia': gaia, 'data': data_sources, 'privacy': privacy}
    for lang in ('en', 'el'):
        for page, build in builders.items():
            out = ROOT / url(lang, page).lstrip('/') / 'index.html'
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(build(lang), encoding='utf-8', newline='\n')
            print('wrote', out.relative_to(ROOT))
    (ROOT / 'privacy.html').write_text(privacy_forward(), encoding='utf-8', newline='\n')
    sitemap = ''.join(f'  <url><loc>{SITE}{url(lang, page)}</loc></url>\n' for lang in ('en', 'el') for page in PAGES)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}</urlset>\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
