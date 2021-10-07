
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .models import Transdata
from .forms import UploadFileForm
from django.http import HttpResponse
import requests
import csv
from io import TextIOWrapper, StringIO


def kddi_trance(request):
    print("kddi_trance entered")
    return render(request, 'trans_scraip/index.html')


def deleteData_all():
    Transdata.objects.all().delete()
    return render(request, 'trans_scraip/index.html')


def csvexport(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'attachment;  filename="transRepo.csv"'
    # 文字化け対策(BOM)
    # response.write("\xEF\xBB\xBF")
    writer = csv.writer(response, delimiter=',')
    writer.writerow(['日付', '店舗', '氏名','出発駅', '到着駅', '最安/最楽', '特急あり/なし', '片道','往復', '合計料金', '経路詳細'])

    for items in Transdata.objects.all():
        writer.writerow([
                items.date,
                items.shop,
                items.name,
                items.departure,
                items.destination,
                items.fast_low,
                items.tokyu,
                items.oneway,
                items.roundway,
                items.sumPrise,
                items.discription,
            ])

    return response


def csvimport(request):
    if 'csv' in request.FILES:
        form = UploadFileForm(request.POST, request.FILES)

        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        header = next(csv_file)

        Data_list = []
        # Trans_list = []

        for line in csv_file:
            print(line)
            datas = []
            for item in line:
                if item != '':
                    datas.append(item)
                else:
                    datas.append(0)

            # Yahoo!検索でスクレイピング
            Trans_data = transdata_all(datas[3], datas[4],datas[5], datas[6])
            print(Trans_data)

            # TEMPLATE渡す用
            transdata_tmp = []
            # Transdata.objects.create(
            transdata_tmp.append(datas[0])
            transdata_tmp.append(datas[1])
            transdata_tmp.append(datas[2])
            transdata_tmp.append(datas[3])
            transdata_tmp.append(datas[4])
            transdata_tmp.append(datas[5])
            transdata_tmp.append(datas[6])
            transdata_tmp.append(int(Trans_data['fare_summary']))
            transdata_tmp.append(int(Trans_data['fare_summary'])*2)
            transdata_tmp.append(int(Trans_data['fare_summary'])*2)
            transdata_tmp.append(Trans_data['lines'])
            # )

            # テンプレートに渡すデータ
            Data_list.append(transdata_tmp)

            # DB登録用
            transdata = {}
            transdata = Transdata(
                date = datas[0],
                shop = datas[1],
                name = datas[2],
                departure = datas[3],
                destination = datas[4],
                fast_low = datas[5],
                tokyu = datas[6],
                oneway = int(Trans_data['fare_summary']),
                roundway = int(Trans_data['fare_summary'])*2,
                sumPrise = int(Trans_data['fare_summary'])*2,
                discription = Trans_data['lines'],
            )
            transdata.save()

        # print(Trans_list)
        # print(Data_list)

        return render(request, 'trans_scraip/import.html', { 'Data_list': Data_list })
    else:
        return render(request, 'trans_scraip/import.html')


def transdata_all(dep, des, fast_low, tk):
    #出発駅の入力
    departure_station = dep
    #到着駅の入力
    destination_station = des

    # =============
    # 特急なし
    # =============
    #最短URLフッター
    fast_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=07&hh=09&m1=3&m2=0&shin=&ex=&hb=1&al=1&lb=1&sr=1&type=4&ws=3&s=0&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"
    #最安URLフッター
    low_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=07&hh=09&m1=3&m2=0&shin=&ex=&hb=1&al=1&lb=1&sr=1&type=4&ws=3&s=1&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"

    # =============
    # 特急あり
    # =============
    #最短URLフッター
    tk_fast_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=07&hh=09&m1=3&m2=0&shin=&ex=&hb=1&al=1&lb=1&sr=1&type=4&ws=3&s=0&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"
    #最安URLフッター
    tk_low_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=07&hh=09&m1=3&m2=0&shin=1&ex=1&hb=1&al=1&lb=1&sr=1&type=4&ws=3&s=1&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"

    #最短の取得先URL
    #    fast_route_url = "https://transit.yahoo.co.jp/search/print?from=%E5%BE%B3%E9%87%8D&flatlon=&to=%E5%B9%B3%E7%94%B0%E7%94%BA&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=03&hh=14&m1=4&m2=2&shin=1&ex=1&hb=1&al=1&lb=1&sr=1&type=1&ws=3&s=0&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"


    if(tk == 'あり'):
        #最短の取得先URL
        fast_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + tk_fast_url_foot
        #最安の取得先URL
        low_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + tk_low_url_foot
    else:
        #最短の取得先URL
        fast_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + fast_url_foot
        #最安の取得先URL
        low_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + low_url_foot

    if(fast_low == '最短'):
        #Requestsを利用してWebページを取得する
        route_response = requests.get(fast_route_url)
        # BeautifulSoupを利用してWebページを解析する
        route_soup = BeautifulSoup(route_response.text, 'html.parser')
        #経路のサマリーを取得
        route_summary = route_soup.find("div",class_ = "routeSummary")
        #所要時間を取得
        required_time = route_summary.find("li",class_ = "time").get_text()
        #乗り換え回数を取得
        transfer_count = route_summary.find("li", class_ = "transfer").get_text()
        #料金を取得
        # fare_summary = route_summary.find("li", class_ = "fare").get_text()
        fare_summary = route_summary.select_one("#srline > div.routeSummary > ul > li.fare > span.mark").get_text().replace('円', '').replace(',', '')
        #乗り換えの詳細情報を取得
        route_detail = route_soup.find("div",class_ = "routeDetail")
    else:
        #Requestsを利用してWebページを取得する
        route_response = requests.get(low_route_url)
        # BeautifulSoupを利用してWebページを解析する
        route_soup = BeautifulSoup(route_response.text, 'html.parser')
        #経路のサマリーを取得
        route_summary = route_soup.find("div",class_ = "routeSummary")
        #所要時間を取得
        required_time = route_summary.find("li",class_ = "time").get_text()
        #乗り換え回数を取得
        transfer_count = route_summary.find("li", class_ = "transfer").get_text()
        #料金を取得
        # fare_summary = route_summary.find("li", class_ = "fare").get_text()
        fare_summary = route_summary.select_one("#srline > div.routeSummary > ul > li.fare > span.mark").get_text().replace('円', '').replace(',', '')
        #乗り換えの詳細情報を取得
        route_detail = route_soup.find("div",class_ = "routeDetail")

    #=================
    #最短ルート
    #=================
    #乗換駅の取得
    stations = []
    stations_tmp = route_detail.find_all("div", class_="station")
    for station in stations_tmp:
        # print(station.get_text().replace('\n',''))
        stations.append(station.get_text().replace('\n',''))

    #乗り換え路線の取得
    lines = []
    lines_tmp = route_detail.find_all("li", class_="transport")
    for line in lines_tmp:
        # print(line.find("div").get_text().replace('\n',''))
        lines.append(line.find("div").get_text().replace('\n',''))

    # 経路詳細テキストの作成
    description_route = make_discription(lines)

    #路線ごとの料金を取得
    fars = []
    fars_tmp = route_detail.find_all("p", class_="fare")
    for fare in fars_tmp:
        fars.append(fare.get_text().replace('\n',''))

    return {
            'required_time': required_time,
            'transfer_count': transfer_count,
            'fare_summary': fare_summary,
            'stations': stations,
            'lines': description_route,
            'fars': fars,
            }


def make_discription(lines):
    discription_text = ''

    for index, line in enumerate(lines):
        discription_text += "[経路" + str(index+1) + "] " + line + "\n"
    return discription_text

def transdata(request):
    #出発駅の入力
    #    departure_station = "瑞穂運動場東"
    departure_station = request.POST.get('startStation')
    #到着駅の入力
    #    destination_station = "平田町"
    destination_station = request.POST.get('endStation')

    print(departure_station)
    print(destination_station)
    #最短URLフッター
    fast_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=03&hh=13&m1=4&m2=9&shin=1&ex=1&hb=1&al=1&lb=1&sr=1&type=1&ws=3&s=0&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"

    #最安URLフッター
    low_url_foot = "&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=03&hh=13&m1=4&m2=9&shin=1&ex=1&hb=1&al=1&lb=1&sr=1&type=1&ws=3&s=1&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"

    #最短の取得先URL
    #    fast_route_url = "https://transit.yahoo.co.jp/search/print?from=%E5%BE%B3%E9%87%8D&flatlon=&to=%E5%B9%B3%E7%94%B0%E7%94%BA&tlatlon=&viacode=&viacode=&viacode=&ym=202110&y=2021&m=10&d=03&hh=14&m1=4&m2=2&shin=1&ex=1&hb=1&al=1&lb=1&sr=1&type=1&ws=3&s=0&ei=&fl=1&tl=3&expkind=1&mtf=&out_y=&mode=&c=&searchOpt=&stype=&ticket=ic&userpass=0&passtype=&detour_id=&fromgid=&togid=&dispym=&dispd=&disptime=&disptype=&dispcnt=&dispbf=&no=1"

    #最短の取得先URL
    fast_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + fast_url_foot

    #最安の取得先URL
    low_route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station + low_url_foot

    #Requestsを利用してWebページを取得する
    fast_route_response = requests.get(fast_route_url)
    low_route_response = requests.get(low_route_url)

    # BeautifulSoupを利用してWebページを解析する
    fast_route_soup = BeautifulSoup(fast_route_response.text, 'html.parser')
    low_route_soup = BeautifulSoup(low_route_response.text, 'html.parser')

    #経路のサマリーを取得
    fast_route_summary = fast_route_soup.find("div",class_ = "routeSummary")
    low_route_summary = fast_route_soup.find("div",class_ = "routeSummary")

    #所要時間を取得
    fast_required_time = fast_route_summary.find("li",class_ = "time").get_text()
    low_required_time = low_route_summary.find("li",class_ = "time").get_text()
    #乗り換え回数を取得
    fast_transfer_count = fast_route_summary.find("li", class_ = "transfer").get_text()
    low_transfer_count = low_route_summary.find("li", class_ = "transfer").get_text()
    #料金を取得
    fast_fare_summary = fast_route_summary.find("li", class_ = "fare").get_text()
    low_fare_summary = low_route_summary.find("li", class_ = "fare").get_text()

    #乗り換えの詳細情報を取得
    fast_route_detail = fast_route_soup.find("div",class_ = "routeDetail")
    low_route_detail = low_route_soup.find("div",class_ = "routeDetail")

    #=================
    #最短ルート
    #=================
    #乗換駅の取得
    fast_stations = []
    fast_stations_tmp = fast_route_detail.find_all("div", class_="station")
    for fast_station in fast_stations_tmp:
        # print(station.get_text().replace('\n',''))
        fast_stations.append(fast_station.get_text().replace('\n',''))

    #乗り換え路線の取得
    fast_lines = []
    fast_lines_tmp = fast_route_detail.find_all("li", class_="transport")
    for fast_line in fast_lines_tmp:
        # print(line.find("div").get_text().replace('\n',''))
        fast_lines.append(fast_line.find("div").get_text().replace('\n',''))

    #路線ごとの料金を取得
    fast_fars = []
    fast_fars_tmp = fast_route_detail.find_all("p", class_="fare")
    for fast_fare in fast_fars_tmp:
        print(fast_fare.get_text().replace('\n',''))
        fast_fars.append(fast_fare.get_text().replace('\n',''))


    #=================
    #最安ルート
    #=================
    #乗換駅の取得
    low_stations = []
    low_stations_tmp = low_route_detail.find_all("div", class_="station")
    for low_station in low_stations_tmp:
        # print(station.get_text().replace('\n',''))
        low_stations.append(low_station.get_text().replace('\n',''))

    #乗り換え路線の取得
    low_lines = []
    low_lines_tmp = low_route_detail.find_all("li", class_="transport")
    for low_line in low_lines_tmp:
        # print(line.find("div").get_text().replace('\n',''))
        low_lines.append(low_line.find("div").get_text().replace('\n',''))

    #路線ごとの料金を取得
    low_fars = []
    low_fars_tmp = low_route_detail.find_all("p", class_="fare")
    for low_fare in low_fars_tmp:
        print(low_fare.get_text().replace('\n',''))
        low_fars.append(low_fare.get_text().replace('\n',''))


    # 最短ルート乗り換え詳細情報の出力
    print("======乗り換え情報======")
    for fast_station,fast_line,fast_fare in zip(fast_stations,fast_lines,fast_fars):
    # for station,line,estimated_time,fare in zip(stations,lines,estimated_times,fars):
        print(fast_station)
        print( " | " + fast_line + " " + fast_fare)
        print("")
        print("")
        print("")
        print("======"+departure_station+"から"+destination_station+"=======")
        print("所要時間："+fast_required_time)
        print(fast_transfer_count)
        print("料金："+fast_fare)

    return render(
        request,
        'trans_scraip/transdata.html',
        {
            'departure_station': departure_station,
            'destination_station': destination_station,
            'fast_stations': fast_stations,
            'fast_lines': fast_lines,
            'fast_fars': fast_fars,
            'fast_required_time': fast_required_time,
            'fast_transfer_count': fast_transfer_count,
            'fast_fare_summary': fast_fare_summary,
            'low_stations': low_stations,
            'low_lines': low_lines,
            'low_fars': low_fars,
            'low_required_time': low_required_time,
            'low_transfer_count': low_transfer_count,
            'low_fare_summary': low_fare_summary,
        },
    )
