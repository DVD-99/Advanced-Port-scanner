from requests import get
from bs4 import BeautifulSoup
import sqlite3
import re

i = 0
data_containers = []

connection = sqlite3.connect("vulnerability.db")
cursor = connection.cursor()
try:
    cursor.execute("SELECT COUNT(*) FROM cve;")
    i = cursor.fetchone()[0]
except sqlite3.OperationalError:
    sql_command = "CREATE TABLE cve (cve_id VARCHAR(50),des LONGTEXT,day VARCHAR(50),rate VARCHAR(50));"
    cursor.execute(sql_command)


url = "https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all&startIndex="+str(i)+"&orderBy=modifiedDate&orderDir=asc"
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
a = html_soup.find('div',{'class':"col-sm-12 col-lg-3"})
b = int(re.sub("[,.]","",a.strong.text))

if (b%20 != 0):
    b -= (b%20)
while (i < b):
    string = "https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all&startIndex="+str(i)+"&orderBy=modifiedDate&orderDir=asc"
    url = string
    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    data_containers.append(html_soup.find_all('tr', {'data-testid' : True}))
    i += 20


for data in data_containers:
    for d in data:
        rate = d.find('td',{'nowrap':True}).span.text
        ratev = rate.replace("\r\n", "").strip()
        
        ids = d.strong.a.text
        #cve_id.append(ids)

        des = d.p.text
        #desc.append(des)

        day = d.td.span.text
        #date.append(day)

        cursor.execute("INSERT INTO cve (cve_id,des,day,rate) VALUES (?,?,?,?)",(ids ,des ,day ,ratev))

connection.commit()
