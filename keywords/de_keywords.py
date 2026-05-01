import logging

logging.info("Checking for German keywords...")

REPORTS_KEYWORDS = [
    'finanzberichte', 'financial reports',
    'jahresabschluesse', 'interim reports', 'annual financial reports',
    'geschaeftsberichte', 'interim financial', 'annual financial',
    'regulatorische informationen', 'regulatory information',
    'jahresberichte', 'annual reports',
    'veroffentlichungen', 'publications',
    'publikationen', 'publications',
    'dokumente', 'documents',
    'finanzinformationen', 'financial information',
    'regulierte informationen', 'regulated information',
    'unternehmensberichte', 'company reports',
    'berichte', 'reports',
    'kennzahlen', 'key figures'
]

INVESTOR_KEYWORDS = [
    'investoren', 'investors',
    'investor relations', 'investor relations',
    'bourse', 'bourse',
    'shareholders', 'shareholders',
    'stakeholders', 'stakeholders',
    'aktionäre', 'shareholders',
    'actionnaires', 'stakeholders'
]

INTERIM_KEYWORDS = [
    'halbjahresfinanzbericht', 'half yearly financial report',
    'half-year financial report', 'half year financial report',
    'quartalsmitteilung', 'quarterly statement',
    'interim report', 'interim statement', 'zwischenbericht',
    'halbjahresbericht', 'half year report',
    'konzernzwischenbericht', 'interim group report',
    'half yearly financial', 'halbjahrlicher finanzbericht',
    'quarterly report', 'quartalsbericht',
    'quartalsfinanzbericht', 'quartalszahlen',
    'zwischenbilanz'
]

ANNUAL_KEYWORDS = [
    'geschaftsbericht',
    'annual report', 'jahresbericht',
    'annual financial statement', 'jahresabschluss',
    'annual results', 'jahresergebnisse',
    'year end financial', 'jahresabschlussfinanzbericht',
    'end of-year report', 'jahresendbericht',
    'bilanz'
]


