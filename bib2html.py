import bibtexparser, sys

def pages(e):
    if 'pages' in e:
        return e['pages'].replace('--', '-')
    else:
        print('no pages in', e['ID'])
        return "xx-xx"

def clean(s):
    return s.replace('{', '').replace('}', '')

def treat(a):
    coma = a.find(',')
    if coma == -1:
        return a
    surname = a[0:coma]
    firstname = a[coma+2:]
    return firstname + surname

def make_author_list(list):
    sep = ''
    res = ''
    for author in list:
        res += sep + author
        sep = ' and '
    return res

def print_author(e,f):
    authors = e['author'].replace('\n', ' ')
    authors = authors.replace("\\'e", "&eacute;")
    authors = authors.replace("\\`e", "&egrave;")
    authors = authors.replace("\\^{\\i}", "&icirc;")    
    authors = clean(authors)

    author_list = authors.split(' and ')
    author_clean = [ treat(a) for a in author_list]
    print('        ' + make_author_list(author_clean) + '.', file=f)
    
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
    print('        <a href="' + url + '"  target="autre"><sup>' + t + '</sup></a>', file=f)

def print_publisher(e,f):
    if 'publisher' not in e:
        publisher = ''
    else:
        publisher = ', ' + e['publisher']
    print(publisher, end='', file=f)

def print_booktitle(e,f):
    if 'series' in e:
        if 'url' in e:
            print('      <a target="new" href="' + e['url'] + '">' + e['series'] + '</a>', end='', file=f)
        else:
            print('      <span class="media">' + e['series'] + '</span>', end='', file=f)
        if 'volume' in e:    
            print(', Vol. ' + e['volume'], end='', file=f)
    else:
        print('No series in', e['ID'])

def print_proctitle(e,f):
    if 'booktitle' in e:
        print('      <span class="media">' + e['booktitle'] + '</span>', end='', file=f)
    else:
        print('No booktitle in', e['ID'])

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
    print('        ' + e['volume'] + num + ':' + pages(e) + ', '+ e['year'], end='', file=f)

def print_journals(l, f):
    if len(l) == 0:
        return
    print('      <h2 class="category">Journal / <span class="francais">Revue</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <header>' + clean(e['title']) + '.</header>', file=f)
        print('        <span class="media">' + e['journal'] + '</span>', end='', file=f)

        vol_num(e,f)

        print_publisher(e, f)
        print('.', file=f)            
        print_doi(e, f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)

def print_chapters(l, f):
    if len(l) == 0:
        return
    print('      <h2 class="category">Book Chapter / <span class="francais">Chapitre de livre</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <span class="pubtitle">' + e['title'] + '.</span>', file=f)
        print_doi(e, f)
        print('<br>', file=f)

        print_booktitle(e, f)

        print(', pp. ' + pages(e), end='', file=f)
        if 'year' not in e:
            print('Not year in', e['ID'])
        else:
            print(', '+ e['year'], end='', file=f)

        print_publisher(e, f)
        print('.', file=f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)
    
def print_proc(l, f):
    if len(l) == 0:
        return
    print('      <h2 class="category">Conference Proceedings / <span class="francais">Actes de Conférences</span></h2>', file=f)
    print('', file=f)
    print('      <section>', file=f)
    
    for e in l:
        print('', file=f)
        print('      <article>', file=f)
        print_author(e, f)
        print('        <span class="pubtitle">' + clean(e['title']) + '.</span>', file=f)
        print_doi(e, f)
        print('<br>', file=f)

        print_proctitle(e, f)
        print_lncs(e,f)
        
        print(', pp. ' + pages(e), end='', file=f)
        if 'year' in e:
            print(', '+ e['year'], end='', file=f)
        else:
            print('No year in', e['ID'])

        print_publisher(e, f)
        print('.', file=f)
        
        print('      </article>', file=f)

    print('      </section>', file=f)

def bib(year):    
    bibfilename = 'mallet' + year + '.bib'
    year = '20' + year

    with open(bibfilename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    with open('mallet' + year + '.shtml', 'w') as f:
        print('<!DOCTYPE HTML>', file=f)
        print('<html>', file=f)
        print('  <head>', file=f)
        print('    <title>Fr&eacute;d&eacute;ric Mallet\'s publications (2013)</title>', file=f)
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

        journals = [b for b in bib_database.entries if b['ENTRYTYPE']=='article']
        print_journals(journals, f)

        chapters = [b for b in bib_database.entries if b['ENTRYTYPE']=='inbook']
        print_chapters(chapters, f)

        proc = [b for b in bib_database.entries if b['ENTRYTYPE']=='inproceedings']
        print_proc(proc, f)
        

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


