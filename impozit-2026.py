# -*- coding: utf-8 -*-
import sys

# Contabil PFA anual
contabil_pfa_anual = 12 * 200 + 450

# Cheltuieli deductibile anuale $E$14
cheltuieli_deductibile_anuale=0

##############################################################

# Contributie CAS $B$10
CONTRIBUTIE_CAS=0.25

# Contributie CASS $B$12
CONTRIBUTIE_CASS=0.10

# PFA Impozit venit $B$14
IMPOZIT_VENIT=0.10

# Salariu minim brut 2026 $B$17
SALARIU_MINIM_BRUT=4050

#############################################################

# 6 salarii minime $E$6
PRAG_CONTRIBUTIE_6_SALARII=SALARIU_MINIM_BRUT*6

# 12 salarii minime $E$7
PRAG_CONTRIBUTIE_12_SALARII=SALARIU_MINIM_BRUT*12

# 24 salarii minime $E$8
PRAG_CONTRIBUTIE_24_SALARII=SALARIU_MINIM_BRUT*24

# 72 salarii minime $E$10
PRAG_CONTRIBUTIE_72_SALARII=SALARIU_MINIM_BRUT*72

#############################################################

def main(argv: list[str]) -> None:

    # Venit lunar EUR A27
    venit_lunar_eur = int(argv[0])
    # Venit lunar RON B27
    venit_lunar_ron=venit_lunar_eur*5.0453

    # Venit anual ron C27
    venit_anual_ron=venit_lunar_ron*12

    # Venit impozabil D27
    venit_impozabil=venit_anual_ron-cheltuieli_deductibile_anuale-contabil_pfa_anual

    # CAS E27
    if venit_impozabil > PRAG_CONTRIBUTIE_24_SALARII:
        venit_cas = PRAG_CONTRIBUTIE_24_SALARII
    elif venit_impozabil>PRAG_CONTRIBUTIE_12_SALARII:
        venit_cas = PRAG_CONTRIBUTIE_12_SALARII
    else:
        venit_cas = 0

    cas_pensie = venit_cas * CONTRIBUTIE_CAS

    # CASS G27
    if venit_impozabil>PRAG_CONTRIBUTIE_72_SALARII:
        venit_cass=PRAG_CONTRIBUTIE_72_SALARII
    elif venit_impozabil>PRAG_CONTRIBUTIE_6_SALARII:
        venit_cass=venit_impozabil
    else:
        venit_cass=PRAG_CONTRIBUTIE_6_SALARII
    cass_sanatate = venit_cass * CONTRIBUTIE_CASS

    # Impozit venit F27
    impozit_venit=(venit_impozabil-cas_pensie-cass_sanatate)*IMPOZIT_VENIT

    total_taxe = cas_pensie + cass_sanatate + impozit_venit

    # total taxe H27
    total_cheltuieli=total_taxe + contabil_pfa_anual

    print(f"Total cheltuieli PFA: {total_cheltuieli:.2f} RON")

if __name__ == "__main__":
    main(sys.argv[1:])