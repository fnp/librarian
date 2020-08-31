from lxml import etree
from . import (blocks, comments, drama, figures, footnotes, front, headers,
               masters, paragraphs, poetry, root, separators, styles, themes)


WL_ELEMENTS = {
    'meta': etree.ElementBase,
    'coverClass': etree.ElementBase,
    "developmentStage": etree.ElementBase,
    "coverBarColor": etree.ElementBase,
    "coverBoxPosition": etree.ElementBase, 
    "coverLogoUrl": etree.ElementBase,
   
    "utwor": root.Utwor,
    "dramat_wierszowany_l": masters.Master,
    "dramat_wierszowany_lp": masters.Master,
    "dramat_wspolczesny": masters.Master,
    "liryka_l": masters.Master,
    "liryka_lp": masters.Master,
    "opowiadanie": masters.Master,
    "powiesc": masters.Master,

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

    "dedykacja": paragraphs.Akap,
    "miejsce_czas": paragraphs.Akap,

    "uwaga": comments.Uwaga,

    "wers": poetry.Wers,
    "wers_wciety": poetry.WersWciety,
    "wers_cd": poetry.WersCd,
    "wers_akap": poetry.Wers,
    "zastepnik_wersu": poetry.ZastepnikWersu,
    "wers_do_prawej": poetry.Wers,
    
    "pa": footnotes.Footnote,
    "pe": footnotes.Footnote,
    "pr": footnotes.Footnote,
    "pt": footnotes.Footnote,

    "begin": themes.Begin,
    "end": themes.End,
    "motyw": themes.Motyw,

    "nota": blocks.Nota,

    "nota_red": comments.Abstrakt,
    "extra": comments.Abstrakt,
    "abstrakt": comments.Abstrakt,

    "naglowek_czesc": headers.NaglowekCzesc,
    "naglowek_akt": headers.NaglowekCzesc,
    "naglowek_scena": headers.NaglowekRozdzial,
    "naglowek_rozdzial": headers.NaglowekRozdzial,
    "naglowek_podrozdzial": headers.NaglowekPodrozdzial,
    "srodtytul": headers.NaglowekCzesc,

    "naglowek_listy": drama.NaglowekListy,

    "sekcja_asterysk": separators.SekcjaAsterysk,
    "sekcja_swiatlo": separators.SekcjaSwiatlo,
    "separator_linia": separators.SeparatorLinia,

    "wieksze_odstepy": styles.Wyroznienie,
    "mat": styles.Wyroznienie,
    "www": styles.Wyroznienie,
    "indeks_dolny": styles.Wyroznienie,

    "tabela": paragraphs.Akap,
    "tabelka": paragraphs.Akap,
    "wiersz": paragraphs.Akap,
    "kol": paragraphs.Akap,

    "ilustr": figures.Ilustr,

#    sklodowska-badanie-cial-radioaktywnych.xml
    "mrow": paragraphs.Akap,
    "mi": paragraphs.Akap,
    "mo": paragraphs.Akap,
    "msup": paragraphs.Akap,
    "mn": paragraphs.Akap,
    "mfrac": paragraphs.Akap,
    "mfenced": paragraphs.Akap,
}
