# -*- coding: utf-8 -*-
"""Laboratorul 7 - enumerare spre root. Generat din programul
de laborator, cu codul scris de student."""
import argparse, io, json, os

GTFO = {'less', 'python3', 'perl', 'vim', 'cp', 'awk', 'vim.basic', 'find', 'bash', 'nmap'}

#  PARTEA A - aduna si grupeaza
# ---------------------------------------------------------------------------

def citeste_linii(cale):
    """Sarcina 1. Citeste un fisier si intoarce LISTA randurilor folositoare."""
    linii = []
    with open(cale, "r", encoding="utf-8") as f:
        for rand in f:
            rand_curat = rand.strip()
            if rand_curat and not rand_curat.startswith("#"):
                linii.append(rand_curat)
    return linii


def nume(cale):
    """Sarcina 2. Intoarce numele fisierului dintr-o cale."""
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    """Sarcina 3. Din fisierul SUID face o LISTA DE DICTIONARE."""
    linii = citeste_linii(cale)
    caile_unice = sorted(list(set(linii)))
    rezultat = []
    for c in caile_unice:
        n = nume(c)
        risc = "mare" if n in GTFO else "normal"
        rezultat.append({"cale": c, "nume": n, "risc": risc})
    return rezultat


def sudo_constatari(cale):
    """Sarcina 4. Din fisierul sudo face o lista de dictionare."""
    linii = citeste_linii(cale)
    rezultat = []
    for rand in linii:
        if " : " in rand:
            user, drept = rand.split(" : ", 1)
            risc = "mare" if "NOPASSWD" in drept else "normal"
            rezultat.append({"user": user, "drept": drept, "risc": risc})
    return rezultat


def cron_constatari(cale):
    """Sarcina 5. Din crontab face o lista de dictionare."""
    linii = citeste_linii(cale)
    rezultat = []
    for rand in linii:
        campuri = rand.split()
        if len(campuri) >= 6:
            user = campuri[5]
            comanda = " ".join(campuri[6:])
            rezultat.append({"user": user, "comanda": comanda})
    return rezultat


def enumereaza(dosar):
    """Sarcina 6. Aduna toate constatarile intr-un singur DICTIONAR."""
    return {
        "suid": suid_constatari(os.path.join(dosar, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(dosar, "sudo.txt")),
        "cron": cron_constatari(os.path.join(dosar, "crontab.txt"))
    }


def utilizatori_implicati(raport):
    """Sarcina 7. Intoarce MULTIMEA utilizatorilor care apar in raport."""
    useri_sudo = {item["user"] for item in raport["sudo"]}
    useri_cron = {item["user"] for item in raport["cron"]}
    return useri_sudo | useri_cron


# ---------------------------------------------------------------------------
#  PARTEA B - ce e nou fata de un sistem curat
# ---------------------------------------------------------------------------

def cai(fisier):
    """Sarcina 8. Intoarce MULTIMEA cailor dintr-un fisier."""
    return set(citeste_linii(fisier))


def suid_noi(acum, baza):
    """Sarcina 9. Ce e in acum, dar nu si in baza."""
    return acum - baza


def risc_pe_nume(multime_cai):
    """Sarcina 10. Fisa nume -> risc, ca DICTIONAR."""
    return {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in multime_cai}


def periculoase_noi(noi):
    """Sarcina 11. Lista cailor noi care sunt periculoase, sortata."""
    return sorted([c for c in noi if nume(c) in GTFO])
    raise NotImplementedError

#GATA BOSS, laboratorul 7 cu mindrie e gata)
# ===========================================================================
#
#   Sub randul urmator incepe programul care te verifica.
#   Nu e nevoie sa intelegi codul de mai jos si nu il modifica.
#
# ===========================================================================
#  


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print("%s: %d gasite, %d cu risc mare" % (categorie, len(lista), len(mari)))
    useri = utilizatori_implicati(raport)
    print("utilizatori implicati:", ", ".join(sorted(useri)))
    with io.open("enum.json", "w", encoding="utf-8") as fis:
        json.dump(raport, fis, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
