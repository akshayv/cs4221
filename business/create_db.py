__author__='wangqi'
''' Modified relation class in myRelation.py for testing
'''
import mysql.connector
from domain.Relation import Relation

def create_schema(relations,datatype_dict, username ,password):
## connect with mysql
    uname = username
    pwd = password
    hst = 'localhost'
    conn = mysql.connector.connect(user=str(uname),password=str(pwd),host=str(hst))
    mycursor = conn.cursor()
    mycursor.execute('use test')

    counter = 0
    for relation in relations:
        counter = counter + 1
        r_name = create_relation_name(counter)

## create table
        cmd = 'CREATE TABLE ' + r_name + ' ('
        primary_key = relation.primary_key
        attributes = relation.attributes

## create attributes
        for attr in attributes:
            datatype = datatype_dict.get(attr)
            line = str(attr) + ' ' + datatype + ', '
            cmd = cmd + line

## create primary key
        temp = ''
        size = len(primary_key)
        pkey_count = 0
        for pkey in primary_key.attributes:
            pkey_count = pkey_count + 1
            if pkey_count < size:
                temp = temp + pkey + ','
            else:
                temp = temp + pkey
        cmd = cmd + 'PRIMARY KEY (' + temp + '));'

        mycursor.execute(cmd)
        print 'cmd BEFORE fkey: ',cmd
        cmd = ''

## create foreign key if applicable
    counter = 0
    for relation in relations:
        counter = counter + 1
        r_name = create_relation_name(counter)

        R_FKey = find_fkey_reln(relations)
        if counter in R_FKey:
            fkey_rel_lst = R_FKey.get(counter)

            for fkey_rel in fkey_rel_lst:
                for fkey,rellst in fkey_rel.iteritems():
                    temp = ''
                    size = len(fkey)
                    key_count = 0

                    for key in fkey:
                        key_count = key_count + 1
                        if key_count < size:
                            temp = temp + key + ','
                        else:
                            temp = temp + key

                    relnum = rellst[0]
                    rel_name = create_relation_name(relnum)
                    cmd = 'ALTER TABLE ' + r_name + ' add FOREIGN KEY ('+temp+') REFERENCES '+rel_name+'('+temp+');'
                    print 'cmd FOREIGN KEY: ',cmd
                    mycursor.execute(cmd)

def find_fkey_reln(relations):
    '''return <key,relation number list> pairs'''
    counter = 0
    R_PKey = dict()
    R_Attr = dict()
    R_Nonkey = dict()
    PKey_R = dict()
    R_FKey = dict()
    primary_keys = set()

    for relation in relations:
        counter = counter + 1
        primary_key = relation.primary_key.attributes
        attributes = relation.attributes
        non_key = attributes - primary_key

        primary_key = frozenset(primary_key)
        R_PKey[counter] = primary_key

        R_Attr[counter] = attributes
        R_Nonkey[counter] = non_key
## update <primarykey,relationNum> dict
        if primary_key in PKey_R:
            counterlst = PKey_R.get(primary_key)
        else:
            counterlst = []
        counterlst.append(counter)
        PKey_R[primary_key] = counterlst

## update primary_key set (set of frozenset)
        primary_keys.add(primary_key)

## process foreign key
    for cur_rel, key in R_PKey.iteritems():
        for counter,non_key in R_Attr.iteritems():
            if cur_rel == counter:
                continue
            if key.issubset(non_key):
                key_r = dict()
                key_r[key] = PKey_R.get(key)
                if counter in R_FKey:
                    keylst = R_FKey.get(counter)
                else:
                    keylst = []
                keylst.append(key_r)
                R_FKey[counter] = keylst
    return R_FKey

def create_relation_name(counter):
    result = 'R'+str(counter)
    return result

if __name__ == "__main__":
    r1 = Relation({'A','B','C'}, {})
    r1.primary_key = {'A'}
    r2 = Relation({'B','D','A'},{})
    r2.primary_key = {'B'}
    r3 = Relation({'D','E'}, {})
    r3.primary_key = {'D'}
    myrelations = [r1,r2,r3]
    datatypes = {'A':'int', 'B': 'varchar(255)', 'C': 'int', 'D':'date', 'E':'int'}
    create_schema(myrelations,datatypes, '', '')
