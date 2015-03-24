__author__='wangqi'
''' Modified relation class in myRelation.py for testing
'''
import mysql.connector
##from domain.Relation import Relation
##from domain.Key import Key
##from domain.FunctionalDependency import FunctionalDependency
from domain.myRelation import Relation

def create_schema(relations):
## connect with mysql
    uname = ''
    pwd = ''
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

## get primary key since there is only one element in frozenset
        my_pkey = ''
        for pkey in primary_key:
            my_pkey = pkey


## create attributes
        size = len(attributes)
        attr_count = 0
        for attr in attributes:
            attr_count = attr_count + 1
## create primary key
            if attr == my_pkey:
                if attr_count < size:
                    line = str(attr) + ' int primary key,'
                else:
                    line = str(attr) + ' int primary key);'
## create other attributes
            else:
                if attr_count < size:
                    line = str(attr) + ' int,'
                else:
                    line = str(attr) + ' int);'
            cmd = cmd + line
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
                    for key in fkey:
                        relnum = rellst[0]
                        rel_name = create_relation_name(relnum)
                        cmd = 'ALTER TABLE ' + r_name + ' add FOREIGN KEY ('+str(key)+') REFERENCES '+rel_name+'('+str(key)+');'
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
        primary_key = relation.primary_key
        attributes = relation.attributes
        non_key = attributes - primary_key
        
        R_PKey[counter] = primary_key
        primary_key = frozenset(primary_key)
        
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
    for key in primary_keys:
        for counter,non_key in R_Nonkey.iteritems():
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

##########test##########
r1 = Relation({'A','B','C'},{'A'})
r2 = Relation({'B','D','A'},{'B'})
r3 = Relation({'D','E'},{'D'})
myrelations = [r1,r2,r3]

create_schema(myrelations)

