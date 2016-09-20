class Entry:
    def __init__(self, db, entry, f):
        self.db = db
        self.entry = entry
        self.f = f

    def getYear():
        if 'year' in self.entry:
            return self.entry['year']
        if getRef() is not None:
            return getRef().getYear()
        return None

    def getRef():
        if 'crossref' not in self.entry:
            return None
        res = self.db.entries[e['crossref']]
        print(res)
        return None
        
            
        
