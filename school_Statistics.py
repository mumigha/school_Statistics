# -- coding:UTF-8 --
# File     : school_Statistics.py
# Time     : 2021/6/29 9:55
# end time : 2021/7/2  9:19
# @Author  : 阿牧
# B站名 :童年阿牧(分析折腾过程,有兴趣的小伙伴可以看看)
# AttributeError: 'str' object has no attribute 'get' 出现这个错误估计是被官网判断请求频繁等一会就好了
# 请求
import json as j
import xml
import xlwt
from fake_useragent import UserAgent
import requests
ua = UserAgent()
us = ua.random
url = "https://api.eol.cn/gkcx/api/?"
headers = {
    "Host": "api.eol.cn",
    "Referer": "https://gkcx.eol.cn/school/search",
    "User-Agent": f"{us}"
}
# 请求头部以及请求载荷
def request_school(page):
    reque_pay ={
        "access_token": "",
         "admissions": "",
         "central": "",
         "department": "",
         "dual_class": "",
         "f211": "",
         "f985": "",
         "is_doublehigh": "",
         "is_dual_class": "", "keyword": "",
         "nature": "",
         "page": f"{page}",
         "province_id": "",
         "ranktype": "",
         "request_type": 1,
         "school_type": "",
         "size": 20,
         "sort": "view_total",
         "top_school_id": "[766]",
         "type": "",
         "uri": "apidata/api/gk/school/lists"
         }
    try:
        open_url = requests.post(url, data=j.dumps(reque_pay), headers=headers)
        if open_url.status_code == 200:
            return open_url.json()
    except requests.ConnectionError as e:
        print("error", e.args)

# 基本信息
def news(json):
    if json:
        items = json.get("data")
        items_new = items.get("item")
        # print(items_new)
        for i in items_new:
            news_school = {}
            news_school["学校id"] = i.get("school_id")
            news_school["名字"] = i.get("name")
            # news_school["人气值"] = i.get("view_total")
            news_school["类型"] = i.get("type_name")
            news_school["科类"] = i.get("level_name")
            news_school["级别"] = i.get("dual_class_name") + "|" + i.get("nature_name")
            news_school["位置"] = i.get("address")
            news_school["招生咨询网站"] = i.get("answerurl")
            yield news_school
# 分数线与专业线
def math(lst,match_year,subject,province):
    math_headers = {
    "Host": "static-data.eol.cn",
    "Origin": "https://gkcx.eol.cn",
    "Referer": f"https://gkcx.eol.cn/school/{lst}/provinceline",
    "User-Agent": F"{us}"
}
    math_url = F"https://static-data.eol.cn/www/2.0/schoolprovinceindex/{match_year}/{lst}/{province}/{subject}/1.json"
    try:
        math_request = requests.get(math_url,headers=math_headers)
        if requests.status_codes == 200:
            return math_request.json()
    except requests.ConnectionError as m:
        print("errp" + m.args)
    try:
        math_get = math_request.json().get("data").get("item")
        for a_match in math_get:
            math_data = {}
            math_data["学校名字"] = school_name
            math_data["年份"] = a_match.get("year")
            math_data["录取批次"] = a_match.get("local_batch_name")
            math_data["招生类型"] = a_match.get("zslx_name")
            math_data["最低分/最低位次"] = a_match.get("min") +"/" + a_match.get("min_section")
            math_data["省控线"] = a_match.get("proscore")
            print("正在获取")
            yield math_data
    except AttributeError:
        print(school_name +":" +"暂时还没有其内容")
# 招生计划
def Enrollment_plan(lst,match_year,subject,province,E_batch):
    math_headers = {
    "Host": "static-data.eol.cn",
    "Origin": "https://gkcx.eol.cn",
    "Referer": f"https://gkcx.eol.cn/school/{lst}/provinceline",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400"
}
    E_url = F"https://static-data.eol.cn/www/2.0/schoolplanindex/{match_year}/{lst}/{province}/{subject}/{E_batch}/1.json"
    try:
        E_request = requests.get(E_url,headers=math_headers)
        if requests.status_codes == 200:
            return E_request.json()
    except requests.ConnectionError as m:
        print("errp" + m.args)
    try:
        E_get = E_request.json().get("data").get("item")
        for E_match in E_get:
            E_data = {}
            E_data["学校名字"] = school_name
            E_data["专业名称"] = E_match.get("spname")
            E_data["学科门类"] = E_match.get("level2_name")
            E_data["计划招生"] = E_match.get("num")
            E_data["学制"] = E_match.get("length")
            yield E_data
    except AttributeError:
        print(school_name +":" +"暂时还没有其内容")
# 专业分数线
def Professional_score_line(lst,match_year,subject,province,E_batch):
    # 7代表本科一批
    # 6代表本科提取批
    # 10代表专科批

    math_headers = {
        "Host": "static-data.eol.cn",
        "Origin": "https://gkcx.eol.cn",
        "Referer": f"https://gkcx.eol.cn/school/{lst}/provinceline",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400"
    }
    E_url = F"https://static-data.eol.cn/www/2.0/schoolplanindex/{match_year}/{lst}/{province}/{subject}/{E_batch}/1.json"
    try:
        R_request = requests.get(E_url, headers=math_headers)
        if requests.status_codes == 200:
            return R_request.json()
    except requests.ConnectionError as m:
        print("errp" + m.args)
    try:
        R_get = R_request.json().get("data").get("item")
        for R_match in R_get:
            R_data = {}
            R_data["学校名字"] = school_name
            R_data["专业名称"] = R_match.get("spname")
            R_data["录取批次"] = R_match.get("level1_name")
            R_data["招生类型"] = R_match.get("zslx_name")
            R_data["平均分"] = R_match.get("average")
            yield R_data
    except AttributeError:
        print(school_name + ":" + "暂时还没有其内容")
# 第二单元
def manu(choose,data_id):
    lst = SCHOOL
    if choose == 1:
        match_year = 2019  # (可修改)
        subject = 2  # (1 = 理科 ) (2 = 文科) (可修改)
        province = 15  # (在id.txet中自己查询) (可修改)
    elif choose != 1:
        match_year = match_yearS  # (可修改)
        subject = subjectS  # (1 = 理科 ) (2 = 文科) (可修改)
        province = provinceS  # (在id.txet中自己查询) (可修改)
    mat = math(lst, match_year, subject, province) #ok
    en = Enrollment_plan(lst,match_year,subject,province,E_batch) #ok
    pr = Professional_score_line(lst,match_year,subject,province,E_batch) #ok
    if choose == 1:
        return data_id
    elif choose == 2:
        for one in mat:
            return one
    elif choose == 3:
        for two in en :
            return two
    elif choose == 4:
        for three in pr:
            return three
def save_josn(result,choose):
    if choose == 1:
        name_xls = "school_jiben"
    elif choose == 2:
        name_xls = "mat"
    elif choose == 3:
        name_xls = "Enrollment_plan"
    elif choose == 4 :
         name_xls = "Professional_score_line"
    else:
        print("出错了")
    open_file = open(f"{name_xls}.text", mode="a+", encoding="utf-8")
    new_json = j.dump(result, ensure_ascii=False, indent=4)
    write_txt = open_file.write(new_json)
    open_file.write("\n")
    open_file.close()
# xls数据保存(待完成)
# def save_data(choose,data):
#     # 创建excel工作表
#     workbook = xlwt.Workbook(encoding='utf-8')
#     worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
#     for label_new in data.keys():#提取key
#         for number_list in range(0,len(data) + 1):
#             worksheet.write(0, number_list, label=label_new)
#             for key, value in data.items():
#                 hang = 1
#                 worksheet.write(hang,number_list,value)
#                 hang +=1

    # workbook.save(f'{name_xls}.xls')
if __name__ == "__main__":
    print("数据来源： 高考数据库(https://gkcx.eol.cn/)")
    print("城市参数在ID里面")
    print("B站名: 童年阿牧(分享瞎折腾过程, 有兴趣的小伙伴可以看看)")
    print("获取基本信息输入:1")
    print("获取省内分数线输:2")
    print("获取计划招生输入:3")
    print("获取专业线分数输：4")
    choose = int(input("请输入查询数据:"))
    if choose!= 1:
        try:
            match_yearS = input("输入查询年份:")  # (可修改)
            subjectS = input("选择学科:") # (1 = 理科 ) (2 = 文科) (可修改)
            provinceS = input("输入查询省份ID:")  # (在id.txet中自己查询) (可修改)
        except (ValueError, UnboundLocalError):
            print("\033[0:31m 不要乱输入哦\033[0m")
            exit()
            print("\033[0:32m 获取成功，爬虫正在爬取，等待一会查看目录下文件即可\033[0m")

    else:
        print("\033[0:32m 获取成功，爬虫正在爬取，等待一会查看目录下文件即可\033[0m")
    for page in range(1,10):#更改获取页数，一共143页根据自己需求去获取
        json = request_school(page)
        rf = news(json)
        for data_id in rf:
            SCHOOL = data_id.get("学校id")
            school_name = data_id.get("名字")
            # 招生计划，分数线本科与专科判断
            benke_judge =  "普通本科" in data_id.values()
            if benke_judge == True:
                E_batch = 7
            elif benke_judge == False:
                E_batch = 10
            else:
                print(school_name + "还没有其内容")
            data = manu(choose,data_id)
            save_josn(data,choose)





