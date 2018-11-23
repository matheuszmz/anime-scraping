import time, os, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from models import db, Anime, Episodios


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options)


def remove_li_vazios(li_all):
    lista = []
    for li in li_all:
        if li.get_attribute('class') != 'd-none':
            lista.append(li)
    return lista


def atualiza_base_animes(driver=driver):
    driver.get('https://punchsubs.net/principal') #pagina inicial
    driver.maximize_window()
    time.sleep(1)

    try:
        driver.find_element_by_class_name('close').click()
    except NoSuchElementException:
        pass

    time.sleep(1)
    btn = driver.find_element_by_xpath('//*[@id="navbarCollapse"]/ul/li[2]/a')
    btn.click()
    time.sleep(2)

    check = True
    while check == True:
        #animes
        ul = driver.find_element_by_class_name('list')

        li_all = ul.find_elements_by_xpath('./li')

        for li in li_all:
            try:
                eps = li.find_element_by_xpath('./a/div/p[3]').text
                eps = eps.replace(' episódios', '')
                eps = int(eps)
                
                anime = Anime.create(
                    nome = li.find_element_by_xpath('./a/div/p[2]').text,
                    genero = li.get_attribute('data-genero'),
                    numeroEpisodio = eps,
                    imagem = li.find_element_by_xpath('./a/img').get_attribute('src'),
                    link = li.find_element_by_xpath('./a').get_attribute('href'),
                    status = 0
                )
                
            except NoSuchElementException:
                print('Anime {} já adicionado.'.format(
                    li.find_element_by_xpath('./a/div/p[2]').text)
                    )
        
        #paginação
        ul = driver.find_element_by_class_name('pagination')

        li_all = ul.find_elements_by_xpath('./li')

        for i in range(len(li_all)):
            if li_all[i].get_attribute('class') == 'active' and i == len(li_all):
                check = False
                break
            elif li_all[i].get_attribute('class') == 'active' and i != len(li_all):
                li_all[i + 1].click()
                break


def atualiza_episodios(anime, driver=driver):
    try:
        driver.get(anime.link)
        driver.maximize_window()
        
        check = True
        while check == True:
            ul = driver.find_element_by_class_name('list')
            li_all = ul.find_elements_by_xpath('./li')

            for li in li_all:
                try:
                    ep = li.find_element_by_xpath('./div[2]/p').text
                    li.find_element_by_xpath('./div[2]/p').click()
                    time.sleep(1)
                    href = driver.find_element_by_xpath('//*[@id="nav-hd"]/ul/a[2]')
                    href = href.get_attribute('href')

                    Episodios.create(
                        anime_id = anime.id,
                        episodio = ep,
                        link = href
                    )

                    btn = driver.find_element_by_class_name('close')
                    btn.click()
                    time.sleep(1)
                except peewee.OperationalError:
                    pass

            #paginação
            ul = driver.find_element_by_class_name('pagination')

            li_all = ul.find_elements_by_xpath('./li')
            li_all = remove_li_vazios(li_all)

            for i in range(len(li_all)):
                if li_all[i].get_attribute('class') == 'active' and li_all[i + 1].get_attribute('class') == 'disabled':
                    check = False
                    break
                elif li_all[i].get_attribute('class') == 'active' and li_all[i + 1].get_attribute('class') != 'disabled':
                    li_all[i + 1].click()
                    break
        anime.status = 1
        anime.save()
    except NoSuchElementException:
        pass


def atualiza_link_de_video(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    script = soup.find_all('script')[6].text
    script = script.split('\n')
    for link in script:
        if link.find("'type': 'video/mp4', 'src': ") > 0:
            n = link.find("'type': 'video/mp4', 'src': ")
            link = link[n:]
            n = link.find("h")
            link = link[n:].replace("'}],", "")
            n = link.find("mp4")
            return link[:n + 3]
        else:
            pass

'''
animes = Anime.select()
for anime in animes:
    if anime.status == 0 and anime.numeroEpisodio > 0:
        print('{}'.format(anime.nome))
        atualiza_episodios(anime)
'''

i = 1
episodios = Episodios.select()
for episodio in episodios:
    if episodio.video == '':
        episodio.video = atualiza_link_de_video(episodio.link)
        print(episodio.video)
        time.sleep(2)
        i += 1
    if i == 10:
        break
