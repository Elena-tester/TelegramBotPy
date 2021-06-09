import urllib.request
import xml.etree.ElementTree as ET
from config import KEYS

class Cryptoconverter:
    @staticmethod
    def get_price(quote:str, base:str, str_amount:str):

        # область верификации входных параметров
        try:
            kQuote = KEYS.get(quote)
        except KeyError:
            raise ConvretionException(f"Не удалось обработать валюту {quote}")

        try:
            kBase = KEYS.get(base)
        except KeyError:
            raise ConvretionException(f"Не удалось обработать валюту {base}")
        try:
            amount = float(str_amount)
        except ValueError:
            raise ConvretionException(f"Не удалось обработать количество {str_amount}")

        # область получения курсов валют

        # import datetime
        # now = datetime.datetime.now()
        # r = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002")
        # альтернатива не взлетела r = requests.get('http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx/GetCursOnDateGetCursOnDate?On_date=' + str(now))
        # print(r.content)
        # оба в XML формате tText = json.loads(r.content)
        # print(tText)

        # http://librerussia.blogspot.com/2014/12/python-3-xml.html
        # import urllib.request
        # Получение курса валют от ЦБ РФ
        url = "http://www.cbr.ru/scripts/XML_daily.asp"
        webFile = urllib.request.urlopen(url)
        data = webFile.read()

        UrlSplit = url.split("/")[-1]
        ExtSplit = UrlSplit.split(".")[1]
        FileName = UrlSplit.replace(ExtSplit, "xml")

        with open(FileName, "wb") as localFile:
            localFile.write(data)

        webFile.close()

        # # https://python-scripts.com/parsing-lxml
        # from lxml import etree, objectify
        #
        # with open(FileName) as f:
        #     xml = f.read()
        #
        # root = objectify.fromstring(xml)
        # attrib = root.attrib
        #
        # print(attrib)
        # Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.

        # https://pythononline.ru/osnovy/parsing-xml-python
        # import xml.etree.ElementTree as ET
        # Парсинг курсов валют с определением параметоров интересующих нас
        root_node = ET.parse(FileName).getroot()

        # Предположим, что обе валюты - рубли
        # префикс n - номинал и v - значение
        nBase = 1
        nQuote = 1
        vBase = '01,0000'
        vQuote = '01,0000'

        for valute in root_node:

            tBase = False
            tQuote = False

            for tag in valute.findall('CharCode'):
                if tag.text == kBase:
                    tBase = True
                elif tag.text == kQuote:
                    tQuote = True

            if tBase:
                for tag in valute.findall('Nominal'):
                    nBase = tag.text

                for tag in valute.findall('Value'):
                    vBase = tag.text

            if tQuote:
                for tag in valute.findall('Nominal'):
                    nQuote = tag.text

                for tag in valute.findall('Value'):
                    vQuote = tag.text
            # value = tag.attrib['CharCode']

        # русский формат цифр переводим в европейский
        vBase = vBase[:-5] + "." + vBase[3:]
        vQuote = vQuote[:-5] + "." + vQuote[3:]

        rub = amount * float(vQuote) / float(nQuote)
        total = rub * float(nBase) / float(vBase)

        return total

class ConvretionException(Exception):
    pass