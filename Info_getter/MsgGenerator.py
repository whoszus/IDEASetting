import requests
from datetime import datetime
from bs4 import BeautifulSoup


class MsgGenerator:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }

    def get_ciba_info(self):
        '''
        从词霸中获取每日一句，带英文。
        :return:
        '''
        resp = requests.get('http://open.iciba.com/dsapi')
        if resp.status_code == 200 and self.isJson(resp):
            conentJson = resp.json()
            content = conentJson.get('content')
            note = conentJson.get('note')
            # print(f"{content}\n{note}")
            return f"{content}\n{note}\n"
        else:
            print("没有获取到数据")
            return None

    def get_dictum_info(self):
        '''
        获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: str 一句格言或者短语
        '''
        print('获取One 格言信息..')
        user_url = 'http://wufazhuce.com/'
        resp = requests.get(user_url, headers=self.headers)
        soup_texts = BeautifulSoup(resp.text, 'lxml')
        # 『one -个』 中的每日一句
        every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
        return every_msg + "\n"

    def get_weather_info(self, dictum_msg='', city_code='101030100', start_date='2018-01-01', sweet_words='来自最爱你的我'):
        '''
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :param dictum_msg: 发送给朋友的信息
        :param city_code: 城市对应编码
        :param start_date: 恋爱第一天日期
        :param sweet_words: 来自谁的留言
        :return: 需要发送的话。
        '''
        print('获取天气信息..')
        weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and self.isJson(resp) and resp.json().get('status') == 200:
            weatherJson = resp.json()
            # 今日天气
            today_weather = weatherJson.get('data').get('forecast')[1]
            # 今日日期
            today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
            # 今日天气注意事项
            notice = today_weather.get('notice')
            # 温度
            high = today_weather.get('high')
            high_c = high[high.find(' ') + 1:]
            low = today_weather.get('low')
            low_c = low[low.find(' ') + 1:]
            temperature = f"温度 : {low_c}/{high_c}"

            # 风
            fx = today_weather.get('fx')
            fl = today_weather.get('fl')
            wind = f"{fx} : {fl}"

            # 空气指数
            aqi = today_weather.get('aqi')
            aqi = f"空气 : {aqi}"

            # 在一起，一共多少天了，如果没有设置初始日期，则不用处理
            if start_date:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                day_delta = (datetime.now() - start_datetime).days
                delta_msg = f'宝贝这是我们在一起的第 {day_delta} 天。\n'
            else:
                delta_msg = ''

            today_msg = f'{today_time}\n{delta_msg}{notice}。\n{temperature}\n{wind}\n{aqi}\n{dictum_msg}{sweet_words if sweet_words else ""}\n'
            return today_msg

    def isJson(self, resp):
        '''
        判断数据是否能被 Json 化。 True 能，False 否。
        :param resp:
        :return:
        '''
        try:
            resp.json()
            return True
        except:
            return False


if __name__ == '__main__':
    # 直接运行
    print(MsgGenerator().get_ciba_info())
    generator = MsgGenerator()
    print(generator.get_dictum_info())
