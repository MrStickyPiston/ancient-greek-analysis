import unicodedata

def without_accents(s):
    return unicodedata.normalize(
        'NFC',
        ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c) or c in ALLOWED_ACCENTS)
    )

ALLOWED_ACCENTS = [
    # Spiriti
    b'\xcc\x93'.decode(),
    b'\xcc\x94'.decode(),

    # Iota subscript
    b'\xcd\x85'.decode()
]
