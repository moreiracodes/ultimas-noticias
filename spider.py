import requests
from bs4 import BeautifulSoup
import urllib
import locale
from datetime import datetime, timedelta
import sys


class Spider:
    def __init__(self):
        self._query = ''
        self._comeback_days = 2
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, new_query):
        ''' search query '''
        self._query = urllib.parse.quote_plus(new_query)

    def _getSoup(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0 \
            (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)' +
            'Gecko/2009021910 Firefox/3.0.7',
        }
        try:
            with requests.Session() as s:
                download = s.get(url, headers=headers)
                decoded_content = download.content.decode('UTF-8')

            soup = BeautifulSoup(decoded_content, 'html.parser')

        except Exception as e:
            print(f'Erro ao raspar dados: {e}')
            return False

        return soup

    def getEstadao(self):
        url = "https://busca.estadao.com.br/?tipo_conteudo=Todos&quando=nas-ultimas-24-horas&q=" + \
            str(self._query)
        soup = self._getSoup(url)
        content = soup.find_all(
            'section', {'class': 'col-md-6 col-sm-6 col-xs-12 col-margin'})

        news = {}
        for index, row in enumerate(content):

            _datetime = self.string_cleaner(
                row.span.find_next('span').get_text())

            news[index] = {
                'href': row.a['href'],
                'title': row.a['title'],
                'headline': row.p.get_text(),
                'author': row.span.get_text(),
                'datetime': _datetime,
            }

        return news

    def getValor(self):

        url = "https://valor.globo.com/busca/?q=" + \
            str(self._query) + "&page=1&order=recent&from=now-1d"
        soup = self._getSoup(url)
        content = soup.find_all(
            'div', {'class': 'widget--info__title product-color'})

        news = {}
        for index, row in enumerate(content):

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': row.parent.p.get_text(),
                'datetime': row.parent.css.select(
                    ".widget--info__meta")[0].get_text(),
            }

        return news

    def getFolhaSP(self):
        url = "https://search.folha.uol.com.br/search?q=" + \
            str(self._query) + "&periodo=24&sd=&ed=&site=todos"

        soup = self._getSoup(url)

        content = soup.find_all(
            'div', {'class': 'c-headline__content'})

        news = {}
        for index, row in enumerate(content):
            try:

                news[index] = {
                    'href': row.a['data-href'],
                    'title': self.string_cleaner(row.h2.get_text()),
                    'headline': self.string_cleaner(row.p.get_text()),
                    'datetime': self.string_cleaner(row.time.get_text()),
                }
                # else:
                #     break
                return news

            except Exception as err:
                print(f"Erro ao raspar Folha de SP: {err}")
                return False

    def getOGlobo(self):

        url = "https://oglobo.globo.com/busca/?q=" + \
            str(self._query) + "&order=recent&from=now-1d"
        soup = self._getSoup(url)
        content = soup.find_all(
            'div', {'class': 'widget--info__title product-color'})

        news = {}
        for index, row in enumerate(content):

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': self.string_cleaner(row.parent.p.get_text()),
                'datetime': row.parent.css.select(
                    ".widget--info__meta")[0].get_text(),
            }

            # else:
            #     break
            # print(news)
        return news

    def getValorInveste(self):

        url = "https://valorinveste.globo.com/busca/?q=" + \
            str(self._query) + "&order=recent&from=now-1d"
        soup = self._getSoup(url)
        content = soup.find_all(
            'div', {'class': 'widget--info__title product-color'})

        news = {}
        for index, row in enumerate(content):

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': self.string_cleaner(row.parent.p.get_text()),
                'datetime': row.parent.css.select(
                    ".widget--info__meta")[0].get_text(),
            }

        return news

    def getEInvestidor(self):

        url = "https://einvestidor.estadao.com.br/?s=" + \
            str(self._query)
        soup = self._getSoup(url)
        content = soup.find_all(
            'h2')

        news = {}
        for index, row in enumerate(content):

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': self.string_cleaner(row.parent.p.get_text()),
                'datetime': row.parent.css.select(
                    ".widget--info__meta")[0].get_text(),
            }

        return news

    def getPipeline(self):

        url = "https://pipelinevalor.globo.com/busca/?q=" + \
            str(self._query) + "&order=recent&from=now-1d"
        soup = self._getSoup(url)
        content = soup.find_all(
            'div', {'class': 'widget--info__title product-color'})

        news = {}
        for index, row in enumerate(content):

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': self.string_cleaner(row.parent.p.get_text()),
                'datetime': row.parent.css.select(
                    ".widget--info__meta")[0].get_text(),
            }

        return news

    def getNeofeed(self):

        url = "https://neofeed.com.br/?s=" + \
            str(self._query)
        soup = self._getSoup(url)
        content = soup.find_all('h3')

        news = {}
        for index, row in enumerate(content):

            # date
            _datetime = self.string_cleaner(row.parent.parent.parent.css.select(
                "span.date")[0].get_text())
            date = _datetime.split('/')

            day = date[0]
            mounth_str = str(date[1])
            year = date[2]

            datetime_str = f"{day}-{mounth_str}-{year}"
            datetime_format = '%d-%m-%y'

            datetime_obj = datetime.strptime(datetime_str, datetime_format)

            # timedelta
            previous_days = timedelta(days=self._comeback_days)
            now = datetime.now()

            isOld = datetime_obj < (now - previous_days)
            if (isOld):
                break

            news[index] = {
                'href': row.parent['href'],
                'title':  self.string_cleaner(row.get_text()),
                'headline': self.string_cleaner(row.parent.parent.parent.p.get_text()),
                'datetime': _datetime,
            }

        return news

    def getBrazilJournal(self):

        url = "https://braziljournal.com/?s=" + \
            str(self._query)
        soup = self._getSoup(url)
        content = soup.find_all('h2', {'class': 'boxarticle-infos-title'})

        news = {}
        for index, row in enumerate(content):
            if (index == 3):
                break
            news[index] = {
                'href': row.a['href'],
                'title':  self.string_cleaner(row.a.get_text()),
                'headline': '',
                'datetime': '',
            }

        return news

    def string_cleaner(self, text):
        text = str(text)
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.rstrip(' ')
        text = text.lstrip(' ')
        return text
