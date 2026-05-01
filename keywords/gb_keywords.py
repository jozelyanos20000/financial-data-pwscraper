import logging

logging.info("Checking for English keywords...")


REPORTS_KEYWORDS = [
    'financial reports', 'results, reports', 'financial information', 'regulated information', 'regulatory information', 'financial publications', 'annual report', 'company reports', 'results', 'publications', 'financial', 'reports',
    'finanzbericht', 'regulatorische informationen', 'veröffentlichungen','publikationen' , 'dokumente', 'finanzen', 'bericht'  # German
    'rapporter', 'regulatorisk information','finansiella',  # Swedish
    'rapporten', 'regelgevende informatie', 'financieel',  # Dutch
    'rapporter', 'regulatorisk informasjon', 'økonomisk'  # Norwegian
]

# Keywords for investor section
INVESTOR_KEYWORDS = [
    'investors', 'investor relations', 'investoren', 'investisseurs', 'bourse' # French and German
    'investerare', 'beleggers', 'investorer',  # Swedish, Dutch, Norwegian
    'shareholders', 'stakeholders', 'aktionäre', 'actionnaires'  # Other synonyms
]



