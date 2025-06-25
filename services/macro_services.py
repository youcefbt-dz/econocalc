def calculate_va(p, ci):
    return round(p - ci, 2)

def calculate_pib(va, tva, sub):
    return round(va + tva - sub, 2)

def calculate_pnb(pib, rfr, rfv):
    return round(pib + rfr - rfv, 2)

def calculate_pnn(pnb, am):
    return round(pnb - am, 2)
def calculate_inflation(cpi_new: float, cpi_old: float):
    if cpi_old == 0:
        return None  # لتجنب القسمة على صفر
    rate = ((cpi_new - cpi_old) / cpi_old) * 100
    return round(rate, 2)
def calculate_rn(pnn: float, indirect: float):
    return round(pnn - indirect, 2)

def calculate_rp(rn: float, pr: float, id_: float, tr: float):
    return round(rn - pr - id_ + tr, 2)

def calculate_rnd(rp: float, id_: float):
    return round(rp - id_, 2)
