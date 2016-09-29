import bibtexparser, sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
#from bibtexparser.customization import homogeneize_latex_encoding
import Entry

MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
def month(entry):
    if 'month' not in entry.entry:
        ref = entry.getRef()
        if ref is not None:
            return month(ref)
        else:
            return ''
        
    m = entry.entry['month']
    if m.isdigit():
        return MONTHS[int(m) - 1] + ' '
    else:
        return m + ' '
       
def pages(prefix, e):
    if 'pages' in e:
        return prefix + e['pages'].replace('--', '-')
    else:
        print('no pages in', e['ID'])
        return ''

def clean(s):
    return s.replace('{', '').replace('}', '')

def print_title(e,f):
    if 'url' not in e:
        print('        <span class="pubtitle">' + clean(e['title']) + '.</span>', file=f)
    else:
        print('        <a target="new" class="pubtitle" href="' + e['url'] +'">' + clean(e['title']) + '.</a>', file=f)    

def treat(a):
    ''' treat author name'''
    if 'Mallet' in a:
        return '<span class="moi">F. Mallet</span>'
    coma = a.find(',')
    if coma == -1:        
        return a
    surname = a[0:coma]
    firstname = a[coma+2:]
    return firstname + ' ' + surname

def make_author_list(l):
    res = l[0]
    if len(l)==1:
        return res
    
    for i in range(1, len(l) - 1):
        res = res + ', ' + l[i]
        
    return res + ' and ' + l[-1]

def print_author(e,f):
    authors = e['author'].replace('\n', ' ')
#    authors = authors.replace("\\'e", "&eacute;")
#    authors = authors.replace("\\`e", "&egrave;")
#    authors = authors.replace("\\^{\\i}", "&icirc;")    
    authors = clean(authors)

    author_list = authors.split(' and ')
    author_clean = [ treat(a) for a in author_list]
    print('        ' + make_author_list(author_clean) + '.', file=f)

def invited(e,f):
    if 'comment' in e:
        #if 'invited' in e['comment']:
        print(' <span class="invited">(' + e['comment'] + ')</span>', end='', file=f)

def print_doi(e,f): 
    if 'doi' in e:
        url = 'http://dx.doi.org/' + e['doi']
        t = 'DOI'
    else:
        if 'url' in e:
            url = e['url']
            t = 'HREF'
        elif 'ee' in e:
            url = e['ee']
            if url.startswith('http://dx.doi.org/'):
                t = 'DOI'
            else:
                t = 'HREF'
        else:
            print('no doi ' + e['ID'])
            return
    print('        <a href="' + url + '"  target="autre"><sup>' + t + '</sup></a>', end='', file=f)

def print_publisher(entry,f):
    p = entry.getPublisher()
    if p is not None:
        print(', ' + str(p), end='', file=f)

def print_booktitle(entry,f):
    title = entry.getProcTitle()

    e = entry.entry

    if title is not None:
        if 'url' in e:
            res = '<a target="new" href="' + e['url'] + '">' + title + '</a>'
        else:
            res = '<span class="media">' + title + '</span>'

    series = None
    if 'series' in e:
        series = e['series']
        if title is not None:
            res = res + ', ' + series
        else:
            res = series

    if 'volume' in e:    
        vol = 'Vol. ' + e['volume']
        if res is None:
            res = vol
        else:
            res += ', ' + vol

    if series is None and title is None:
        entry.missing('booktitle and series')
    else:
        print('      ' + res, end='', file=f)

def print_proctitle(entry,f):
    title = entry.getProcTitle()
    if title is None:
        entry.missing('booktitle')
    else:
        title = title.replace('International', 'Int.')
        title = title.replace('Conference', 'Conf.')
        title = title.replace('Symposium', 'Symp.')
        title = title.replace('Workshop', 'Work.')
        print('      <span class="media">' + title + '</span>', end='', file=f)

def print_lncs(e,f):
    if 'volume' not in e:
        print('No Volume in', e['ID'])
        return
    if 'series' in e:
        if e['series'] == 'Lecture Notes in Computer Science':
            print(', LNCS ' + e['volume'], end='', file=f)
        else:
            print(', ' + e['series'] + ' ' + e['volume'], end='', file=f)

def vol_num(e,f):
    if 'volume' not in e:
        return
    
    if 'number' in e:
        num = '(' + e['number'] + ')'
    else:
        num = ''
    print('        ' + e['volume'] + num + pages(':',e), end='', file=f)

def publisher_year(entry, f):
    print_publisher(entry, f)

    year = entry.getYear()
    if year is None:
        entry.missing('year')
    else:    
        print(', '+ month(entry) + year, end='', file=f)

    if 'isbn' in entry.entry:
        print(', ISBN: '+entry.entry['isbn'], end='', file=f)        
        
    print('.', file=f)            

def print_book(db, f):
    l = [b for b in db.entries if b['ENTRYTYPE']=='book']
    
    if len(l) == 0:
        return

    if 'author' not in l[0]:
        print('skip', l[0]['ID'])
        return
    
    print('      <h2 class="category">Book / <span class="francais">Livre</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        entry = Entry.Entry(db, e)
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <header>' + clean(e['title']) + '.</header>', file=f)

        publisher_year(entry,f)
        
        print_doi(e, f)
        print('      </article>', file=f)

    print('      </section>', file=f)

def print_thesis(db, f):
    l = [b for b in db.entries if b['ENTRYTYPE']=='phdthesis']
    
    if len(l) == 0:
        return
    
    print('      <h2 class="category">Thesis / <span class="francais">Thése</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        entry = Entry.Entry(db, e)
        
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <header>' + clean(e['title']) + '.</header>', file=f)
        print('        <span class="media">' + e['school'] + '</span>', end='', file=f)

        publisher_year(entry,f)
        
        print_doi(e, f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)
    
def print_journals(db, f):
    journals = [b for b in db.entries if b['ENTRYTYPE']=='article']
    
    if len(journals) == 0:
        return
    
    print('      <h2 class="category">Journal / <span class="francais">Revue</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in journals:
        entry = Entry.Entry(db, e)
        
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <header>' + clean(e['title']) + '.</header>', file=f)
        print('        <span class="media">' + e['journal'] + '</span>', end='', file=f)

        vol_num(e,f)

        publisher_year(entry,f)
        
        print_doi(e, f)
        invited(e, f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)

def print_chapters(db, f):
    chapters = [b for b in db.entries if b['ENTRYTYPE']=='inbook']

    if len(chapters) == 0:
        return
    
    print('      <h2 class="category">Book Chapter / <span class="francais">Chapitre de livre</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in chapters:
        entry = Entry.Entry(db, e)
        
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print_title(e, f)
        print_doi(e, f)
        invited(e, f)

        print('<br>', file=f)

        print_booktitle(entry, f)

        print(pages(', pp. ', e), end='', file=f)

        publisher_year(entry, f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)
    
def print_proc(db, f):
    l = [b for b in db.entries if b['ENTRYTYPE']=='inproceedings']

    if len(l) == 0:
        return
    
    print('      <h2 class="category">Conference Proceedings / <span class="francais">Actes de Conférences</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        entry = Entry.Entry(db, e)
        
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print_title(e, f)
        print_doi(e, f)
        invited(e, f)
        print('<br>', file=f)

        print_proctitle(entry, f)
        print_lncs(e,f)

        print(pages(', pp. ', e), end='', file=f)

        publisher_year(entry, f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)

def number(e):
    if 'number' not in e:
        print('Number not in', e['ID'])
        return 'RR-????'
    else:
        num = e['number']
        num = num.replace('{', '')
        num = num.replace('}', '')
        if 'ee' in e:
            return '<a href="' + e['ee'] + '">' + num + '</a>'
        return num;
    
def print_rr(db, f):
    unp = [b for b in db.entries if b['ENTRYTYPE']=='unpublished']
    rr = [b for b in db.entries if b['ENTRYTYPE']=='techreport']
    
    if len(unp) + len(rr) == 0:
        return
    
    print('      <h2 class="category">Other / <span class="francais">Autre</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in unp:       
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print_title(e,f)
        print_doi(e, f)
        print('      <span class="media">' + e['note'] + "</span>", end='', file = f)

        print(pages(', pp. ', e), end='', file=f)
        
        if 'year' in e:
            print(', '+ month(Entry.Entry(db, e)) + e['year'], end='', file=f)
        else:
            print('No year in', e['ID'])

        print('.', file=f)
        invited(e, f)
        
        print('      </article>', file=f)

    for e in rr:
        entry = Entry.Entry(db, e)
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print_title(e,f)
        print('      ' + e['type'] + ', ' + number(e), end='', file = f)

        if 'pages' in e:
            print(pages(', ', e) + ' pages', end='', file=f)
        if 'institution' in e:
            print(', ' + e['institution'], end='', file=f)
        if 'year' in e:
            print(', '+ month(entry) + e['year'], end='', file=f)
        else:
            print('No year in', e['ID'])

        print('.', file=f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)
    
def bib(year):    
    bibfilename = 'mallet' + year + '.bib'
    year = '20' + year

    with open(bibfilename) as bibtex_file:
        parser = BibTexParser()
        #parser.customization = homogeneize_latex_encoding
        parser.customization = convert_to_unicode
        db = bibtexparser.load(bibtex_file, parser=parser)

    with open('mallet' + year + '.shtml', 'w') as f:
        print('<!DOCTYPE HTML>', file=f)
        print('<html>', file=f)
        print('  <head>', file=f)
        print('    <title>Fr&eacute;d&eacute;ric Mallet\'s publications (' + year + ')</title>', file=f)
        print('    <META http-equiv="Content-Style-Type" content="text/css">', file=f)
        print('    <META http-equiv="Content-Type" content="text/html;charset=utf-8">', file=f)
        print('    <LINK href="../' + str(int(year) - 1) + '/" rel="Prev">', file=f)
        print('    <LINK href="../' + str(int(year) + 1) + '/" rel="Next">', file=f)
        print('    <LINK href="../fmpublis.css" rel="alternate stylesheet" type="text/css" title="2014">', file=f)
        print('    <LINK href="../fmpublis3.css" rel="stylesheet" type="text/css" title="2015">', file=f)
        print('    <META name="Author" lang=fr content="Frederic Mallet">', file=f)
        print('    <META name="keywords" lang="en" content="UML, Real-Time, MARTE, SysML">', file=f)
        print('    <META name="description" lang=fr content="publications Frederic Mallet ' + year + '">', file=f)
        print('  </head>', file=f)

        print('', file=f)

        print('  <body>', file=f)
        print('    <!--#include file="nav.html"-->', file=f)
        print('    <header class="top">', file=f)
        print('      <h1>Publications (' + year + ')</h1>', file=f)
        print('    </header>', file=f)
        print('', file=f)
        print('    <div class="content">', file=f)
        print('      <a href="' + bibfilename + '">BibTex</a>', file=f)

        print_book(db,f)
        print_thesis(db,f)
        print_journals(db, f)
        print_chapters(db, f)
        print_proc(db, f)
        print_rr(db, f)
        
        print('    <!--#include file="footer.html"-->', file=f)
        print('    </div>', file=f)
        print('  </body>', file=f)
        print('</html>', file=f)

if len(sys.argv) == 1:
    year = input('Bibtex year:')
    bib(year)
else:
    for year in sys.argv[1:]:
        bib(year)


