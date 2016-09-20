class Entry:
    def __init__(self, db, entry):
        self.db = db
        self.entry = entry

    def getPublisher(self):
        if 'publisher' in self.entry:
            return self.entry['publisher']
        ref = self.getRef()
        if ref is None:
            return None
        else:
            return ref.getPublisher()
        
    def getProcTitle(self):
        short = ''
        if 'booktitle' in self.entry:
            short = self.entry['booktitle']
        ref = self.getRef()
        if ref is None:
            return short
        else:
            return ref.getTitle() + ' (' + short + ')'

    def getTitle(self):
        return self.entry.get('title', None)
        
    def getYear(self):
        if 'year' in self.entry:
            return self.entry['year']
        ref = self.getRef()
        if ref is not None:
            return ref.getYear()
        else:
            return None

    def getRef(self):
        if 'crossref' not in self.entry:
            return None
        ref = self.entry['crossref']
        filtre = [b for b in self.db.entries if b['ID']==ref]
        if len(filtre)==0:
            return None
        if len(filtre)>1:
            print('Multi entries for', ref)
        return Entry(self.db, filtre[0])
        
            
    def missing(self, par):
        print('No', par, 'in', self.entry['ID'])

