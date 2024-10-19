import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def findplayer_pitcher(name): 

    url = "https://baseballdata.jp/dashboard.html"

    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5',
      'cache-control': 'max-age=0',
      'cookie': '_ga=GA1.2.775436963.1726697493; _gid=GA1.2.255534317.1727637030; __gads=ID=1344c65a8ab42a29:T=1726697492:RT=1727638745:S=ALNI_MbkC4vByU2c_tzgq-YNHoAjF0popQ; __gpi=UID=00000ef014b31854:T=1726697492:RT=1727638745:S=ALNI_MZ8-yE38sWXzNClc9kCbnTyo3MnZA; __eoi=ID=33387305699d5f20:T=1726697492:RT=1727638745:S=AA-AfjbAK0WFL_P0gz_Lrpyk4pLu; FCNEC=%5B%5B%22AKsRol-n7autghwkVclQvVLKxJpT19DONxlVhFfhUIKxp2QTBamfN_J4uSJNmQJhwkQ1_VbjhaGlDJpOc_v19PcqgBfwveBcfMgolENWxjIh1nYG43vsW3dyJ_sLexMvD6peaXLMqGS1kDFf_bT5tk1yN_b10UTWPA%3D%3D%22%5D%5D',
      'if-modified-since': 'Sun, 29 Sep 2024 14:18:01 GMT',
      'if-none-match': '"c1067-62342c17a50bc-gzip"',
      'priority': 'u=0, i',
      'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    players = soup.find_all("p")

    bytes_text = name.encode('utf-8')
    latin_text = bytes_text.decode('latin1', errors='replace')

    found = False
    player_id = ""
    type = ""

    for player in players:
        if player.find('a'):
            player_name = player.get_text(strip=True)
            if is_in(player_name, latin_text) == True:
                found = True
                player_id = player.a['href'][-13:-6]
                type = "P"
                break
                
    if not found:
        player_id, type = findplayer_batter(name)

    return player_id, type

def findplayer_batter(name):
    url = "https://baseballdata.jp/dashboard2.html"

    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5',
      'cookie': '_ga=GA1.2.775436963.1726697493; _gid=GA1.2.255534317.1727637030; __gads=ID=1344c65a8ab42a29:T=1726697492:RT=1727645603:S=ALNI_MbkC4vByU2c_tzgq-YNHoAjF0popQ; __gpi=UID=00000ef014b31854:T=1726697492:RT=1727645603:S=ALNI_MZ8-yE38sWXzNClc9kCbnTyo3MnZA; __eoi=ID=33387305699d5f20:T=1726697492:RT=1727645603:S=AA-AfjbAK0WFL_P0gz_Lrpyk4pLu; FCNEC=%5B%5B%22AKsRol-gFSpuyC-Er0_aEd4n8Au2dKrZaJlDVt9TKaWigqxslTjWlLaolWSyfdXjL91c2uDoxB9gfcFbbRzkMC9sLkPcLlyg3s9SYXCIPeHI9SIU8OLwu-v1nQ7FV1GoKM2kKHj9nLoM8e9QkDD1VvVRuRr5iVcOlw%3D%3D%22%5D%5D',
      'if-modified-since': 'Sun, 29 Sep 2024 14:18:27 GMT',
      'if-none-match': '"20502d-62342c30ce18c-gzip"',
      'priority': 'u=0, i',
      'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    players = soup.find_all("p")

    bytes_text = name.encode('utf-8')
    latin_text = bytes_text.decode('latin1', errors='replace')

    found = False
    player_id = ""
    type = "B"

    for player in players:
        if player.find('a'):
            player_name = player.get_text(strip=True)
            if is_in(player_name, latin_text) == True:
                found = True
                player_id = player.a['href'][-13:-6]

                break
                
    if not found:
        print("Player not found.")
        quit()

    return player_id, type

def is_in(full_str, sub_str):
    if re.findall(sub_str, full_str):
        return True
    else:
        return False

def on_base_by_img(img):
    base = ""
    if img['src'][:-4] == "norun":
        base = "000"
    elif img['src'][:-4] == "run1":
        base = "001"
    elif img['src'][:-4] == "run2":
        base = "010"
    elif img['src'][:-4] == "run3":
        base = "100"
    elif img['src'][:-4] == "run12":
        base = "011"
    elif img['src'][:-4] == "run23":
        base = "110"
    elif img['src'][:-4] == "run13":
        base = "101"
    else:
        base = "111"
    return base

def main_batter():
    print("下載中...")
    player_id, type = findplayer_pitcher(name)
    url = "https://baseballdata.jp/player" + type + "/" + player_id + "S.html"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.775436963.1726697493; _gid=GA1.2.255534317.1727637030; __gads=ID=1344c65a8ab42a29:T=1726697492:RT=1727663832:S=ALNI_MbkC4vByU2c_tzgq-YNHoAjF0popQ; __gpi=UID=00000ef014b31854:T=1726697492:RT=1727663832:S=ALNI_MZ8-yE38sWXzNClc9kCbnTyo3MnZA; __eoi=ID=33387305699d5f20:T=1726697492:RT=1727663832:S=AA-AfjbAK0WFL_P0gz_Lrpyk4pLu; FCNEC=%5B%5B%22AKsRol9QbdnpdJoPIdBIl7p5eo7fi5ZGlomGE-TfOGAxE8H-J8rBJcqC2dwUUMYhPOQB2W627rQFcY0EqyUNxf6BNX8mjUmDyl1dfJbm3TcXRIg__-wIO7Cq7VjxsS-5nndm35iB-CqQxnOFi6T5PWYVhWzUZSsy6w%3D%3D%22%5D%5D',
    'if-modified-since': 'Sun, 29 Sep 2024 13:38:54 GMT',
    'if-none-match': '"55cee-6234235a38422-gzip"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    dates = soup.find_all("th", class_ = "pnm")


    day_ids = []

    for date in dates:
        if date.find('a'):
            day_ids.append(date.a['href'])         

    pitch_by_pitch = []
    headers_extracted = False

    for day_id in day_ids:
        url = "https://baseballdata.jp/playerB/" + day_id
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}

        response = requests.request("GET", url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_ = "item")
        

        for item in items:
            if item.find("p", style = "margin:5px;"):
                thead = item.find('thead')
                tbodies = item.find_all('tbody')
                tbody = tbodies[3]
                td_pitcher = item.find("td", style = "background-color: #4a4848; ")
                div_cord = item.find("div", style = "position: absolute;top: 0px;left: 0px;width: 160px;height: 200px;")
                spans = div_cord.find_all("span")
                img = item.find("img")

                if not headers_extracted:
                    header_rows = thead.find_all('tr')
                    for row in header_rows:
                        headers = [th.get_text(strip=True) for th in row.find_all('th')]
                        headers.insert(0, "Date")
                        headers.insert(1, "Inning")
                        headers.insert(2, "Pitcher")
                        headers.insert(3, "Pitcher_Hand")
                        headers.extend(["cor_y", "cor_x", "Base", "Balls", "Strikes"])
                        pitch_by_pitch.append(headers)
                    headers_extracted = True

                data_rows = tbody.find_all('tr')
                for i, row in enumerate(data_rows):
                    data = [td.get_text(strip=True) for td in row.find_all('td')]
                    data.insert(0, url[-22:-18] + "-" + url[-18:-16] + "-" + url[-16:-14])
                    data.insert(1, td_pitcher.find_all('p')[0].get_text(strip=True)[:-2])
                    data.insert(2, td_pitcher.find_all('p')[2].get_text(strip=True))
                    data.insert(3, td_pitcher.find_all('p')[3].get_text(strip=True))
                    if i < len(spans):  
                        style_attr = spans[i]['style']

                        y_value = style_attr.split('top:')[1].split('px')[0].strip() if 'top:' in style_attr else "N/A"
                        x_value = style_attr.split('left:')[1].split('px')[0].strip() if 'left:' in style_attr else "N/A"

                    data.extend([y_value, x_value, str(on_base_by_img(img)), int(0), int(0)])
                    pitch_by_pitch.append(data)


    for i in range(2, len(pitch_by_pitch)):

        if pitch_by_pitch[i][4] == "1":
            pitch_by_pitch[i][11] = 0
            pitch_by_pitch[i][12] = 0
        
        else:
            pitch_by_pitch[i][11] = int(pitch_by_pitch[i][11])
            pitch_by_pitch[i][12] = int(pitch_by_pitch[i][12])

            if pitch_by_pitch[i-1][7] == "ボール":
                pitch_by_pitch[i][11] = pitch_by_pitch[i-1][11] + 1
            else:
                pitch_by_pitch[i][11] = pitch_by_pitch[i-1][11]

            if (pitch_by_pitch[i-1][7] == "見逃し" or 
                pitch_by_pitch[i-1][7] == "空振り" or 
                pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 0 or 
                pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 1):
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12] + 1
            
            elif pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 2:
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12]
            else:
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12]

    separate = name.split(" ")

    df = pd.DataFrame(pitch_by_pitch)
    file_path = "./" + separate[0] + separate[1] + "每球數據.csv"
    df.to_csv(file_path, index=False, mode='w')
    print("下載完成！")


def main_pitcher():
    print("下載中...")
    player_id, type = findplayer_pitcher(name)
    url = "https://baseballdata.jp/player" + type + "/" + player_id + "S1.html"

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja-JP;q=0.6,ja;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.775436963.1726697493; _gid=GA1.2.255534317.1727637030; __gads=ID=1344c65a8ab42a29:T=1726697492:RT=1727842059:S=ALNI_MbkC4vByU2c_tzgq-YNHoAjF0popQ; __gpi=UID=00000ef014b31854:T=1726697492:RT=1727842059:S=ALNI_MZ8-yE38sWXzNClc9kCbnTyo3MnZA; __eoi=ID=33387305699d5f20:T=1726697492:RT=1727842059:S=AA-AfjbAK0WFL_P0gz_Lrpyk4pLu; FCNEC=%5B%5B%22AKsRol8pYdZTA7w3B-E3pSxlJpxlvwTzTNi8VMiFtrmc0ENlzMOXB7qvgSid8k3fHR355JavqcGBeombTnkqhNCSsjjmQeQRp0gTwVQqGFTdJPRYSiveJWEH7sdhbbKoXwNkS--Zyp-f0FvBfIgaiUcr6Z7I2OyInw%3D%3D%22%5D%5D',
    'if-modified-since': 'Tue, 01 Oct 2024 14:24:36 GMT',
    'if-none-match': '"9895-6236b14b5d2f7-gzip"',
    'priority': 'u=0, i',
    'referer': 'https://baseballdata.jp/playerP/1600127S1.html',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    dates = soup.find_all("td")


    day_ids = []

    for date in dates:
        if date.find('a'):
            day_ids.append(date.a['href'])

    pitch_by_pitch = []
    headers_extracted = False

    for day_id in day_ids:

        url = "https://baseballdata.jp/playerP/" + day_id[:-6] + "detail.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}

        response = requests.request("GET", url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_ = "item")

        for item in items:
            if item.find("p", style = "margin:5px;"):
                thead = item.find('thead')
                tbodies = item.find_all('tbody')
                tbody = tbodies[3]
                td_batter = item.find("td", style = "background-color: #4a4848; ")
                div_cord = item.find("div", style = "position: absolute;top: 0px;left: 0px;width: 160px;height: 200px;")
                spans = div_cord.find_all("span")
                img = item.find("img")

                if not headers_extracted:
                    header_rows = thead.find_all('tr')
                    for row in header_rows:
                        headers = [th.get_text(strip=True) for th in row.find_all('th')]
                        headers.insert(0, "Date")
                        headers.insert(1, "Inning")
                        headers.insert(2, "Batter")
                        headers.insert(3, "Batter_Hand")
                        headers.extend(["cor_y", "cor_x", "Base", "Balls", "Strikes"])
                        pitch_by_pitch.append(headers)
                    headers_extracted = True

                data_rows = tbody.find_all('tr')
                for i, row in enumerate(data_rows):
                    data = [td.get_text(strip=True) for td in row.find_all('td')]
                    data.insert(0, url[-27:-23] + "-" + url[-23:-21] + "-" + url[-21:-19])
                    data.insert(1, td_batter.find_all('p')[0].get_text(strip=True)[:-2])
                    data.insert(2, td_batter.find_all('p')[2].get_text(strip=True))
                    data.insert(3, td_batter.find_all('p')[3].get_text(strip=True))
                    base = on_base_by_img(img)
                    if i < len(spans):  # Ensure there's a matching span
                        style_attr = spans[i]['style']

                        y_value = style_attr.split('top:')[1].split('px')[0].strip() if 'top:' in style_attr else "N/A"
                        x_value = style_attr.split('left:')[1].split('px')[0].strip() if 'left:' in style_attr else "N/A"

                    data.extend([y_value, x_value, str(base), int(0), int(0)])
                    pitch_by_pitch.append(data)
 

    for i in range(2, len(pitch_by_pitch)):

        if pitch_by_pitch[i][4] == "1":
            pitch_by_pitch[i][11] = 0
            pitch_by_pitch[i][12] = 0
        
        else:
            # Ensure that we handle empty strings as 0
            pitch_by_pitch[i][11] = int(pitch_by_pitch[i][11])
            pitch_by_pitch[i][12] = int(pitch_by_pitch[i][12])

            if pitch_by_pitch[i-1][7] == "ボール":
                pitch_by_pitch[i][11] = pitch_by_pitch[i-1][11] + 1
            else:
                pitch_by_pitch[i][11] = pitch_by_pitch[i-1][11]

            if (pitch_by_pitch[i-1][7] == "見逃し" or 
                pitch_by_pitch[i-1][7] == "空振り" or 
                pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 0 or 
                pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 1):
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12] + 1
            
            elif pitch_by_pitch[i-1][7] == "ファウル" and pitch_by_pitch[i-1][12] == 2:
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12]
            else:
                pitch_by_pitch[i][12] = pitch_by_pitch[i-1][12]

    separate = name.split(" ")

    df = pd.DataFrame(pitch_by_pitch)
    file_path = "./" + separate[0] + separate[1] + "每球數據.csv" 
    df.to_csv(file_path, index=False, mode='w')
    print("下載完成！")


if __name__ == "__main__":
    name = str(input("球員的名字(姓氏 名字)："))
    player_id, type = findplayer_pitcher(name)
    if type == "B":
        main_batter()
    if type == "P":
        main_pitcher()
