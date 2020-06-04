from srjbxx import jbxxlr, script, csh, dyywbh
import os

Path = os.path.dirname(os.path.abspath(__file__))
url = 'http://122.224.230.26:20054/login'
cookies = {
    "name": "login_token",
    "value": "bd83f2c7-fe1c-43e5-b5be-65866322b595"
}
mysql_dist = {
    "host":"192.168.3.110","port":3306,
    "user":"root","password":"zjport",
    "database":"tsn","charset":"utf8"
}
sql = "select business_no from tsn_shipping_export_base order by id desc limit 1"

page = jbxxlr(url, cookies)
eii_dist, eti_dist = csh(Path)
script(page, eii_dist, eti_dist)
dyywbh(mysql_dist, sql)

# if __name__ == '__main__':
#     script(page, eii_dist, eti_dist)
