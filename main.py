from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
import pyperclip

from models.rate_currency import *
from controllers.product import *

#Изменение размера окна
Window.size = (300, 440)


class Container(MDBoxLayout):

    #Метод для копирования ссылки
    def copyProductLink(self):
        url_product_min_price = self.label_copy_link.text
        pyperclip.copy(url_product_min_price)
        Snackbar(
            text="Ссылка скопирована в буфер обмена",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(
                                Window.width - (10 * 2)
                        ) / Window.width
        ).open()

    #Метод для получения инфаормации о продукте
    def getInfoProduct(self, url_product):
        info_product = getInfo(url_product)
        if (info_product[0] != 0) and (info_product[1] != 0) and (info_product[2] != 0):
            product_name = info_product[0]
            product_price_currency = info_product[1]
            self.label_product_name.text = product_name
            self.label_product_price.text = "Старая цена: " + str(product_price_currency)
            price = info_product[2]
            Snackbar(
                text="Найден продукт",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (10 * 2)
                            ) / Window.width
            ).open()
            return price
        else:
            Snackbar(
                text="Ошибка в ссылке. Попробуйте заново",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (10 * 2)
                            ) / Window.width
            ).open()


    #Метод для получения минимальной цены
    def checkPrice(self):
        if self.text_input.text == "":
            Snackbar(
                text="Вставьте ссылку",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (10 * 2)
                            ) / Window.width
            ).open()
        else:
            url_product = self.text_input.text
            price = self.getInfoProduct(url_product)
            list_price = getMinPrice(url_product)
            if (list_price[0] != 0) and (list_price[1] != 0) and (list_price[2] != 0) and (list_price[3] != 0):
                min_price = list_price[0]
                diff = price-min_price
                try:
                    diff = float('{:.2f}'.format(diff))
                finally:
                    self.label_min_price.text = "Новая цена: " + str(min_price) + " . Вы можете сэкономить: " + str(diff) + " руб."
                    storeCode = list_price[1]
                    min_currency_from = list_price[2]
                    id_product = list_price[3]
                    url_product_min_price = "http://www.asos.com/%s/prd/%s?browseCurrency=%s" % (storeCode, id_product, min_currency_from)
                    self.label_copy_link.text = url_product_min_price
                    self.text_input_Url.disabled = 0
            else:
                Snackbar(
                    text="Ошибка в ссылке. Попробуйте заново",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                                        Window.width - (10 * 2)
                                ) / Window.width
                ).open()

    #Метод обновления валюты
    def updateRate(self):
        rate_currency()
        Snackbar(
            text="Курс валют обновлен",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=(
                                Window.width - (10 * 2)
                        ) / Window.width
        ).open()

class GrabberForAsosApp(MDApp):

    def build(self):
        return Container()

if __name__ == '__main__':
    GrabberForAsosApp().run()

