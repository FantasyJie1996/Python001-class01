# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep


def page(url):
    # 模拟浏览器请求
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    return (requests.get(url, headers=header).text)


def page_analysis(page_resolution):
    movies = []

    bs_info = bs(page_resolution, 'html.parser')

    for info in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
        for name in info.find_all('span', attrs={'class': 'name'}):
            movie_title = name.text
        for tag in info.find_all('div'):
            for span_tag in tag.find_all('span', attrs={'class': 'hover-tag'}):
                if span_tag.text == '类型:':
                    movie_type = tag.text.split(':')[1].strip()
                elif span_tag.text == '上映时间:':
                    movie_time = tag.text.split(':')[1].strip()

        movie = [movie_title, movie_type, movie_time]
        movies.append(movie)

    return movies


if __name__ == '__main__':

    movie_list = []

    for i in range(10):   #循环10次，爬取10个页面的

        response_text = page(f'https://maoyan.com/films?showType=3&offset={30 * i}')

        movie_list_one = page_analysis(response_text)
        movie_list = movie_list + movie_list_one
        print(f'已爬取{i+1}页，剩余{9-i}页')
        sleep(10)
    print("end")

    movie1 = pd.DataFrame(data=movie_list)

    movie1.to_csv('./01_requests.csv', encoding='utf8', index=False, header=["名称","类型","上映时间"])