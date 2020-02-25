import os
import json
with open("\\".join(os.path.abspath(__file__).split("\\")[:-1])+"\\"+"province_city_xian.txt","rb") as f:
    tt=f.read().decode("utf8")
province_city_xian=json.loads(tt)
province_citys=province_city_xian["province_citys"]
city_xians=province_city_xian["city_xians"]
def get_province_num(province,txt,pp_city=False):
    zong={}
    zong["xian_num"]={}
    zong["city_num"]={}
    zong["province_num"]={}
    if len(province)<=2:
        h_province=province
    else:
        h_province=province.replace("市","").replace("省","").replace("自治区","").replace("回族","").replace("壮族","").replace("维吾尔","").replace("特别行政区","")
    num_province=txt.count(h_province)
    for city in province_citys[province]:
        if len(city)<=2:
            h_city=city
        else:
            h_city=city.replace("市","").replace("自治州","").replace("族","").replace("地区","").replace("☆","")
        num_city=txt.count(h_city)
        
        if h_city!=h_province:
            num_province+=num_city
        else:
            num_city=num_city-1

        zd_num_xian={}
        for xian in city_xians[city]:
            h_xian=xian.replace("县市","县").replace("市市","市")
            if len(h_xian)>2:
                h_xian=xian.replace("县","").replace("市","").replace("族自治","族").replace("自治","")
            num_xian=txt.count(h_xian)
            
            if h_xian!=h_province:
                num_province+=num_xian
            else:
                num_xian=num_xian-1
            if h_xian!=h_city:
                num_city+=num_xian
            else:
                num_xian=num_xian-1

            zd_num_xian[xian]=num_xian
        zong["xian_num"][city]=zd_num_xian
        zong["city_num"][city]=num_city
    zong["province_num"][province]=num_province
    cc=sorted([[k,v] for k,v in zong["city_num"].items()],key=lambda ls:ls[1],reverse=True)
    if pp_city:
        m_city=pp_city
        c_city=0
        xx=sorted([[k,v] for k,v in zong["xian_num"][m_city].items()],key=lambda ls:ls[1],reverse=True)
        if xx and xx[0][1]:
            m_xian=xx[0][0]
            c_xian=xx[0][1]
        else:
            m_xian=""
            c_xian=0
    elif cc and cc[0][1]:
        m_city=cc[0][0]
        c_city=cc[0][1]
        xx=sorted([[k,v] for k,v in zong["xian_num"][m_city].items()],key=lambda ls:ls[1],reverse=True)
        if xx and xx[0][1]:
            m_xian=xx[0][0]
            c_xian=xx[0][1]
        else:
            m_xian=""
            c_xian=0
    else:
        m_city=""
        c_city=0
        m_xian=""
        c_xian=0
    return province,num_province,m_city,c_city,m_xian,c_xian
def get_pcx(txt):
    tong_p=[]
    for province in province_citys:
        tong_p.append(get_province_num(province,txt.replace(" ","").replace("\r","").replace("\t","").replace("\n","")))
    return sorted(tong_p,key=lambda ls:ls[1],reverse=True)
def get_city(txt,h_zd=False):
    txt=txt.replace("北京时间","")
    h_province=""
    h_city=""
    h_xian=""
    if h_zd:
        cc=get_pcx(h_zd)
        if cc[0][1]:
            if cc[0][5]:
                return cc[0]
            elif cc[0][3]:
                return get_province_num(cc[0][0],(h_zd+txt).replace(" ","").replace("\r","").replace("\t","").replace("\n",""),cc[0][2])
            else:
                return get_province_num(cc[0][0],(h_zd+txt).replace(" ","").replace("\r","").replace("\t","").replace("\n",""))
    cc=get_pcx(txt)
    if cc[0][1]:
        return cc[0]
    else:
        return "",0,"",0,"",0

