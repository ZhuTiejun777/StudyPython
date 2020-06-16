#-*-coding:utf-8-*-
#-*-by zhutj 20200616-*-
URL = "http://192.168.3.192/newDzka/QA/Defect/GetDefects"

HEADERS = {
    "Cookie": "ASP.NET_SessionId=4nd3cyupojx4bmdiy5exhn51; __RequestVerificationToken_L25ld0R6a2E1=Cv0VAGIt7UAYSQZcygUTKrj36e8-aJWnTv23MG4wlkZ8RUazDqjrBJ7BAaQxlCm1SdCfL9uNAlg8KIrBCF-FzpFyXGkrcQ4-k2CbNiGQa_M1; PowerProject2Auth=CD35E5AE58D521C27A7AEDC4A3EE92F0139039C299D142ED361D2D6B83E8F828EC1AD8D822FE645C9A864FADD57A732747B9D272F1DCF89307FE5CEBD25E2B001A9BA98E1351FFC234E8FD94B2E2350AA260DA26C4AB7BE105BBACB36B96CD14;",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

DATA = {
    "relate": "所有缺陷",
    "state": "新问题",
    "dateType": "提交时间",
    "versionType": "发现版本",
    "sort": "提交日期",
    "order": "desc",
}
