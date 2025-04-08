# -*- coding: utf-8 -*-
import sys

COST_CONTABIL_PFA_LUNAR = 200
COST_SUPLIMENTAR_CONTABIL_PFA_DECLARATIE_VENIT = 100
CHELTUIELI_DEDUCTIBILE_ANUALE = 0 # $E$14
# Pentru cine vrea să contribuie la pensie mai mult decât minimul:
SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_LUNAR = 9000
COST_CONTABIL_MICRO_ANUAL = 4000 # $E$12

# 2. desfășoară activități, principale sau secundare, corespunzătoare codurilor
# CAEN: 5821 – Activități de editare a jocurilor de calculator,
# 5829 – Activități de editare a altor produse software,
# 6201 – Activități de realizare a soft-ului la comandă (software orientat client),
# 6209 – Alte activități de servicii  privind tehnologia informației,
# CAEN: 5510 – Hoteluri și alte facilități de cazare similare,
# 5520 – Facilități de cazare pentru vacanțe și perioade de scurtă durată,
# 5530 – Parcuri pentru rulote, campinguri și tabere,
# 5590 – Alte servicii de cazare,
# 5610 – Restaurante,
# 5621 – Activități de alimentație (catering) pentru evenimente,
# 5629 – Alte servicii de alimentație n.c.a.,
# 5630 – Baruri și alte activități de servire a băuturilor,
# 6910 – „Activități juridice” – numai pentru activitățile avocaților,
# 8621 – Activități de asistență medicală generală,
# 8622 – Activități de asistență medicală specializată,
# 8623 – Activități de asistență stomatologică,
# 8690 – Alte activități referitoare la sănătatea umană.”
CAEN_LA_ALIN_1_B = "Da"   # Dacă este da, impozitul micro devine 3% din venit

SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_ANUAL = (
  SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_LUNAR * 12
)

SALARIU_MINIM_BRUT_LUNAR = 4050 # $B$17
SALARIU_MINIM_BRUT_ANUAL = SALARIU_MINIM_BRUT_LUNAR * 12 # $C$17

PRAG_CONTRIBUTIE_6_SALARII = SALARIU_MINIM_BRUT_LUNAR * 6 # $E$6
PRAG_CONTRIBUTIE_12_SALARII = SALARIU_MINIM_BRUT_LUNAR * 12 # $E$7
PRAG_CONTRIBUTIE_24_SALARII = SALARIU_MINIM_BRUT_LUNAR * 24 # $E$8
PRAG_CONTRIBUTIE_60_SALARII = SALARIU_MINIM_BRUT_LUNAR * 60 # $E$10

# Procente impozit
IMPOZIT_VENIT = 0.10 # $B$14
CONTRIBUTIE_CASS = 0.10 # $B$12
CONTRIBUTIE_CAS = 0.25 # $B$10
IMPOZIT_MICRO = 0.01 # $B$7
IMPOZIT_MICRO_PESTE_PRAG = 0.03 # $B$6
IMPOZIT_DIVIDENDE = 0.10 # $B$8

# PFA
COST_CONTABIL_PFA_ANUAL = 12 * COST_CONTABIL_PFA_LUNAR + COST_SUPLIMENTAR_CONTABIL_PFA_DECLARATIE_VENIT # $E$13

# SRL + Salariu minim
CAS_CASS_SALARIU_MINIM_LUNAR = (
  (SALARIU_MINIM_BRUT_LUNAR - 200) * (CONTRIBUTIE_CAS + CONTRIBUTIE_CASS)
)
CONTRIBUTIE_ASIGURATIORIE_MUNCA_SALARIU_MINIM_LUNAR = (SALARIU_MINIM_BRUT_LUNAR - 200) * 0.0225 # $B$21
CONTRIBUTIE_ASIGURATIORIE_MUNCA_SALARIU_MINIM_ANUAL = CONTRIBUTIE_ASIGURATIORIE_MUNCA_SALARIU_MINIM_LUNAR * 12 # $C$21
TAXE_SALARIU_MINIM = (
  (
      CAS_CASS_SALARIU_MINIM_LUNAR +
      ((SALARIU_MINIM_BRUT_LUNAR - 200) - CAS_CASS_SALARIU_MINIM_LUNAR - 600) * IMPOZIT_VENIT +
      CONTRIBUTIE_ASIGURATIORIE_MUNCA_SALARIU_MINIM_LUNAR
  ) * 12
) # $B$20

PRAG_IMPOZIT_MICRO = 300000 # $B$9

def foaie_de_calcul_pfa(venit_euro: int) -> int:

    # b27
    venit_lunar_ron = venit_euro * 4.95

    # c27
    venit_anual_ron_brut = venit_lunar_ron * 12

    # d27
    venit_anual_ron_impozabil = venit_anual_ron_brut - CHELTUIELI_DEDUCTIBILE_ANUALE - COST_CONTABIL_PFA_ANUAL

    # e27
    if venit_anual_ron_impozabil > PRAG_CONTRIBUTIE_24_SALARII:
        baza_cas = PRAG_CONTRIBUTIE_24_SALARII
    elif venit_anual_ron_impozabil > PRAG_CONTRIBUTIE_12_SALARII:
        baza_cas = PRAG_CONTRIBUTIE_12_SALARII
    else:
        baza_cas = 0
    if baza_cas < SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_ANUAL:
        baza_cas = SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_ANUAL
    cas = baza_cas * CONTRIBUTIE_CAS

    # g27
    if venit_anual_ron_impozabil > PRAG_CONTRIBUTIE_60_SALARII:
        baza_cass = PRAG_CONTRIBUTIE_60_SALARII
    elif venit_anual_ron_impozabil > PRAG_CONTRIBUTIE_6_SALARII:
        baza_cass = venit_anual_ron_impozabil
    else:
        baza_cass = 0
    cass=baza_cass * CONTRIBUTIE_CASS

    # f27
    impozit_venit = (venit_anual_ron_impozabil - cas - cass) * IMPOZIT_VENIT

    total_impozit = cas + impozit_venit + cass
    total_costuri = total_impozit + COST_CONTABIL_PFA_ANUAL
    return total_costuri

def foaie_de_calcul_micro(venit_euro: int) -> int:

    # b27
    venit_lunar_ron = venit_euro * 4.95

    # c27
    venit_anual_ron_brut = venit_lunar_ron * 12

    # an27
    if venit_anual_ron_brut > PRAG_IMPOZIT_MICRO or CAEN_LA_ALIN_1_B == 'Da':
        fractie_impozit_micro = IMPOZIT_MICRO_PESTE_PRAG
    else:
        fractie_impozit_micro = IMPOZIT_MICRO
    impozit_micro = venit_anual_ron_brut * fractie_impozit_micro

    # AO27
    impozit_dividende = (
        venit_anual_ron_brut
        - CHELTUIELI_DEDUCTIBILE_ANUALE
        - COST_CONTABIL_MICRO_ANUAL
        - (SALARIU_MINIM_BRUT_ANUAL + CONTRIBUTIE_ASIGURATIORIE_MUNCA_SALARIU_MINIM_ANUAL)
        - impozit_micro
    ) * IMPOZIT_DIVIDENDE

    # AP27
    venit_persoana_fizica = (
        venit_anual_ron_brut
        - COST_CONTABIL_MICRO_ANUAL
        - TAXE_SALARIU_MINIM
        - impozit_micro
        - impozit_dividende
    )

    # AQ27
    if venit_persoana_fizica > PRAG_CONTRIBUTIE_24_SALARII:
        baza_cass = PRAG_CONTRIBUTIE_24_SALARII
    elif venit_persoana_fizica > PRAG_CONTRIBUTIE_12_SALARII:
        baza_cass = PRAG_CONTRIBUTIE_12_SALARII
    elif venit_persoana_fizica > PRAG_CONTRIBUTIE_6_SALARII:
        baza_cass = PRAG_CONTRIBUTIE_6_SALARII
    else:
        baza_cass = 0
    cass = baza_cass * CONTRIBUTIE_CASS

    if SALARIU_MINIM_BRUT_ANUAL < SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_ANUAL:
        cas_voluntar = (
            SALARIU_PENTRU_CONTRIBUTIE_VOLUNTARA_PENSIE_ANUAL - SALARIU_MINIM_BRUT_ANUAL
        ) * CONTRIBUTIE_CAS
    else:
        cas_voluntar = 0

    # AR27
    total_cheltuieli = (
        TAXE_SALARIU_MINIM + impozit_micro + impozit_dividende + cass
        + COST_CONTABIL_MICRO_ANUAL + cas_voluntar
    )
    return total_cheltuieli

def main(argv: list[str]) -> None:
    venit = int(argv[0])
    print(f'Total cheltuieli PFA, ron: {foaie_de_calcul_pfa(venit)}')
    print(f'Total cheltuieli micro, ron: {foaie_de_calcul_micro(venit)}')

if __name__ == "__main__":
    main(sys.argv[1:])