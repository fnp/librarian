from lxml import etree
from . import (blocks, comments, drama, figures, footnotes, front, headers,
               masters, paragraphs, poetry, ref, root, separators, styles, themes,
               tools, base)


WL_ELEMENTS = {
    'snippet': base.Snippet,
    'meta': etree.ElementBase,
    'coverClass': etree.ElementBase,
    "developmentStage": etree.ElementBase,
    "coverBarColor": etree.ElementBase,
    "coverBoxPosition": etree.ElementBase, 
    "coverLogoUrl": etree.ElementBase,
    "contentWarning": etree.ElementBase,
    "endnotes": etree.ElementBase,

    "utwor": root.Utwor,
    "dramat_wierszowany_l": masters.Master,
    "dramat_wierszowany_lp": masters.Master,
    "dramat_wspolczesny": masters.Master,
    "liryka_l": masters.Master,
    "liryka_lp": masters.Master,
    "opowiadanie": masters.Master,
    "powiesc": masters.Master,

    "blok": tools.WLElement,
    
    "autor_utworu": front.AutorUtworu,
    "dzielo_nadrzedne": front.DzieloNadrzedne,
    "nazwa_utworu": front.NazwaUtworu,
    "podtytul": front.Podtytul,

    "lista_osob": drama.ListaOsob,
    "lista_osoba": drama.ListaOsoba,
    "naglowek_osoba": drama.NaglowekOsoba,
    "osoba": drama.Osoba,

    "dlugi_cytat": blocks.DlugiCytat,
    "poezja_cyt": blocks.PoezjaCyt,
    "dlugi_cyt": blocks.DlugiCytat,  ### ???
    "ramka": blocks.Ramka,
    
    "slowo_obce": styles.SlowoObce,
    "tytul_dziela": styles.TytulDziela,
    "wyroznienie": styles.Wyroznienie,

    "akap": paragraphs.Akap,
    "akap_cd": paragraphs.Akap,
    "akap_dialog": paragraphs.Akap,

    "motto_podpis": front.MottoPodpis,

    "strofa": poetry.Strofa,

    "motto": front.Motto,

    "didaskalia": drama.Didaskalia,
    "kwestia": drama.Kwestia,
    "didask_tekst": drama.DidaskTekst,

    "dedykacja": blocks.Dedykacja,
    "miejsce_czas": drama.MiejsceCzas,

    "uwaga": comments.Uwaga,

    "wers": poetry.Wers,
    "wers_wciety": poetry.WersWciety,
    "wers_cd": poetry.WersCd,
    "wers_akap": poetry.WersAkap,
    "zastepnik_wersu": poetry.ZastepnikWersu,
    "wers_do_prawej": poetry.WersDoPrawej,
    "wers_srodek": poetry.WersSrodek,
    
    "pa": footnotes.PA,
    "pe": footnotes.PE,
    "pr": footnotes.PR,
    "pt": footnotes.PT,

    "ref": ref.Ref,

    "begin": themes.Begin,
    "end": themes.End,
    "motyw": themes.Motyw,

    "nota": blocks.Nota,

    "nota_red": comments.NotaRed,
    "extra": comments.Uwaga,
    "abstrakt": comments.Abstrakt,

    "naglowek_czesc": headers.NaglowekCzesc,
    "naglowek_akt": headers.NaglowekCzesc,
    "naglowek_scena": headers.NaglowekScena,
    "naglowek_rozdzial": headers.NaglowekRozdzial,
    "naglowek_podrozdzial": headers.NaglowekPodrozdzial,
    "srodtytul": headers.NaglowekCzesc,
    "podtytul_czesc": headers.PodtytulCzesc,
    "podtytul_akt": headers.PodtytulCzesc,
    "podtytul_scena": headers.PodtytulRozdzial,
    "podtytul_rozdzial": headers.PodtytulRozdzial,
    "podtytul_podrozdzial": headers.PodtytulPodrozdzial,

    "naglowek_listy": drama.NaglowekListy,

    "sekcja_asterysk": separators.SekcjaAsterysk,
    "sekcja_swiatlo": separators.SekcjaSwiatlo,
    "separator_linia": separators.SeparatorLinia,

    "wieksze_odstepy": styles.WiekszeOdstepy,
    "mat": styles.Mat,
    "www": styles.WWW,
    "indeks_dolny": styles.IndeksDolny,

    "tabela": figures.Tabela,
    "tabelka": figures.Tabela,
    "wiersz": figures.Wiersz,
    "kol": figures.Kol,

    "animacja": figures.Animacja,
    "ilustr": figures.Ilustr,

    "numeracja": tools.Numeracja,
    "rownolegle": tools.Rownolegle,
    "tab": tools.Tab,

    # Section
    "wywiad_pyt": blocks.WywiadPyt,
    "wywiad_odp": blocks.WywiadOdp,

    # Inline MathML, should really be namespaced.
    "mrow": etree.ElementBase,
    "mi": etree.ElementBase,
    "mo": etree.ElementBase,
    "msup": etree.ElementBase,
    "mn": etree.ElementBase,
    "mfrac": etree.ElementBase,
    "mfenced": etree.ElementBase,
}
