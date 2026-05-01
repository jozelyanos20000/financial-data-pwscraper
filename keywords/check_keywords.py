import fitz
from de_keywords import ANNUAL_KEYWORDS as keywords
pdf = fitz.open('Ringmetall_GB_2022_DE-3.pdf')
page_text = pdf[0].get_text()
translation_table = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZéÉöÖåÅäÄ",
    "abcdefghijklmnopqrstuvwxyzeeooaaaa"
)

page_text = page_text.translate(translation_table).lower()

for keyword in keywords:
    if keyword in page_text:
        print(keyword)
print(page_text)