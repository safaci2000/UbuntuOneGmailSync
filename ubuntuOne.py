#!/usr/bin/env python
from desktopcouch.records.server import CouchDatabase  
from desktopcouch.records.record import Record as CouchRecord 

def main():
    database = CouchDatabase("people", create=True)
    record = CouchRecord({  
          "email": "segphault@arstechnica.com",  
          "nickname": "segphault",  
          "name": "Ryan Paul"  
    }, "http://somewhere/couchdb/person")
    database.put_record(record)


if __name__ == '__main__':
    main()


