#!/usr/bin/python3
# -*- coding: windows-1252 -*-
import sys
import subprocess
import sqlite3

def untuple(list):
    return [i[0] for i in list]

def listtree(connection, id):
    listid = set((id,))
    bid = set((id,))
    checked = set()
    c = connection.cursor()
    loop = 1
    while bid:
        loop = loop + 1
        b = set()
        for i in bid:
            query = 'SELECT tid FROM links WHERE sid=%d;' %i
            c.execute(query)
            bl = c.fetchall()
            checked.add(i)
            if bl:
                bl = set(untuple(bl))
                listid = listid | bl
                b = b | bl
            else:
                continue
        bid = b - checked
        if (loop > 2) | (len(listid) > 1000):
            break 
    l = list(listid - set((id,)))
    l.sort()
    return l
    

# def printsentence(main, translations):
#     print("\n") 
#     print ("%s\t%s" %(main[0], main[1]))
#     for i in translations:
#         print ("%s\t%s" %(i[0], i[1]))

def printsentence(main, translations):
    #print("\n")
    translationString = [i[1] for i in translations]
    print("%s\t%s" %(main[1], '\\n'.join(translationString)))

level = int(sys.argv[1])
listl = sys.argv[2:]
frl = listl[0]
tol = listl[1]
print ("tatoebaToStarDict script alpha version")
print ("Ivan Mikhaylov 2016")
print ("Mode: " +" -> ".join(listl))
sl=''
for i in listl:
    if i[-1]==",":
        sl += "'%s', " % i[:-1]
    else:
        sl += "'%s'," % i
sl=sl[:-1]
listl=sl
conn = sqlite3.connect('tatoeba.db')
c = conn.cursor()
c2 = conn.cursor()

query = 'SELECT id FROM sentences WHERE lc=\'%s\'; ' %(frl, )
c.execute(query)
cl = 0
f = c.fetchone()
while (f != None):
    mains = []
    trans = []
    ids = int(f[0])
    query = 'SELECT lc, sentence FROM sentences WHERE id = %d;' % ids
    c2.execute(query)
    mains = c2.fetchone()
    mains = list(mains)
    tree = listtree(conn, ids)
    for i in tree:
        query = 'SELECT lc, sentence FROM sentences WHERE id = %d;' % i
        c2.execute(query)
        a = c2.fetchone()
        if a:
            if a[0] == tol:
                trans.append(list(a))
    if (len(mains) > 0) & (len(trans) > 0):
        printsentence(mains,trans)
        cl = cl+1
    f = c.fetchone()