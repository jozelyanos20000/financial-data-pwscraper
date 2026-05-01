import logging

logging.info("Checking for Swedish keywords...")

# Keywords for reports section
REPORTS_KEYWORDS = [
    'report archive','finansiella rapporter', 'rapporter och presentationer', 'rapporter', 'delarsrapporter', 'arsredovisningar', 'arsrapporter', 'finansiell information', 'reglerad information', 'regulatorisk information',
    'finansiella publikationer', 'financial reports','finansiell rapportering', 'delrapporter', 'financial reports', 'press release', 'kvartalsrapport', 'bolagsrapporter', 'halvarsrapport',
    'ekonomisk rapport', 'resultatrapport', 'publiceringar', 'rapporter', 'ekonomisk information'
]

# Keywords for investor section
INVESTOR_KEYWORDS = [
    'investors','investerare', 'investerarrelationer', 'aktiemarknad', 'aktieagare', 'bolagsstamma', 'investor relations', 'investerarkontakter', 'agare',
    'aktieagare', 'stakeholders', 'kapitalmarknad', 'aktieinformation', 'finansinformation', 'agare och investerare', 'kapitalforvaltning',
    'investerarinformation', 'aktieagarrapport'
]
