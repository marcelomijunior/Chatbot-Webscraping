from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from product import Product


class Scraping:
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = './webscraping/chromedriver_win32/chromedriver.exe'

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    def homePage(self, url='https://www.nuuvem.com/'):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        socialNetworks = []

        storeAddress = self.driver.find_element_by_tag_name(
            'address').text.split('\n')[1]

        footerSocial = self.driver.find_element_by_class_name(
            'footer-social-nav')
        aTags = footerSocial.find_elements_by_tag_name('a')

        for aTag in aTags:
            socialNetworks.append(aTag.get_attribute('href'))
            pass

        infoLoja = {"Endereço": storeAddress, "Acompanhne-nos": socialNetworks}

        return infoLoja

    def playstationProducts(self, url='https://www.nuuvem.com/lp/pt/playstation/'):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        produtos = []

        virtualCards = self.driver.find_elements_by_class_name('game-pass')

        for virtualCard in virtualCards:
            name = virtualCard.find_element_by_class_name(
                'card-name').text + " Playstation"
            price = virtualCard.find_element_by_class_name('price-gg').text

            produto = Product(
                name=name,
                price=price,
                typeProduct='Gift Card'
            ).getProduct()

            produtos.append(produto)
            pass

        playstationPlus = self.driver.find_elements_by_class_name('psnplus')

        for psnPlus in playstationPlus:
            name = "Playstation Plus " + \
                psnPlus.find_element_by_class_name('meses').text
            price = psnPlus.find_element_by_class_name(
                'buy-area').text.split('\n')[0]

            produto = Product(
                name=name,
                price=price,
                typeProduct='Gift Card'
            ).getProduct()

            produtos.append(produto)
            pass

        return produtos

    def xboxProducts(self, url='https://www.nuuvem.com/lp/pt/xbox/'):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        produtos = []

        giftsCard = self.driver.find_element_by_id('giftcard')
        giftsCards = giftsCard.find_elements_by_class_name('greencard')

        for card in giftsCards:
            name = 'Cartão Presente XBOX'
            price = card.find_element_by_class_name(
                'card-buy-area').text.split('\n')[0]

            produto = Product(
                name=name,
                price=price,
                typeProduct='Gift Card'
            ).getProduct()

            produtos.append(produto)
            pass

        gamePass = self.driver.find_element_by_id('gamepass')
        gamePasses = gamePass.find_elements_by_class_name('game-pass')

        for gamePass in gamePasses:
            name = "XBOX GAME PASS" + \
                gamePass.find_element_by_class_name('card-name').text
            price = gamePass.find_element_by_class_name(
                'card-buy-area').text.split('\n')[0]

            produto = Product(
                name=name,
                price=price,
                typeProduct='Gift Card'
            ).getProduct()

            produtos.append(produto)
            pass

        liveGold = self.driver.find_element_by_id('livegold')
        plansLiveGold = liveGold.find_elements_by_class_name('greencard')

        for gold in plansLiveGold:
            name = gold.find_element_by_tag_name('div').text
            price = gold.find_element_by_class_name(
                'card-buy-area').text.split('\n')[0]

            produto = Product(
                name=name,
                price=price,
                typeProduct='Gift Card'
            ).getProduct()

            produtos.append(produto)
            pass

        return produtos

    def pcGames(self, url='https://www.nuuvem.com/catalog/platforms/pc'):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        listProducts = []
        qtdPagesToRead = 3

        for i in range(qtdPagesToRead):
            self.driver.implicitly_wait(10)
            verMais = self.driver.find_element_by_class_name(
                'products-items--footer')
            verMaisATag = verMais.find_element_by_tag_name('a')

            games = self.driver.find_elements_by_class_name(
                'product__has__countdown')

            for game in games:
                produto = Product(
                    name=game.get_attribute('data-track-product-name'),
                    price="R$" +
                    game.get_attribute(
                        'data-track-product-price').replace('.', ','),
                    genre=game.get_attribute('data-track-product-genre'),
                    typeProduct='Game'
                ).getProduct()

                listProducts.append(produto)
                pass

            if i < qtdPagesToRead:
                verMaisATag.click()
                pass

            self.driver.implicitly_wait(10)
            pass

        return listProducts

    def pcGamesOnSale(self, url='https://www.nuuvem.com/catalog/platforms/pc/price/promo/sort/bestselling/sort-mode/desc'):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        listProducts = []
        qtdPagesToRead = 2

        for i in range(qtdPagesToRead):
            self.driver.implicitly_wait(10)
            verMais = self.driver.find_element_by_class_name(
                'products-items--footer')
            verMaisATag = verMais.find_element_by_tag_name('a')

            games = self.driver.find_elements_by_class_name(
                'product__has__countdown')

            for game in games:
                produto = Product(
                    name=game.get_attribute('data-track-product-name'),
                    price="R$" +
                    game.get_attribute(
                        'data-track-product-price').replace('.', ','),
                    genre=game.get_attribute('data-track-product-genre'),
                    typeProduct='Game',
                    promotion=True
                ).getProduct()

                listProducts.append(produto)
                pass

            if i < qtdPagesToRead:
                verMaisATag.click()
                pass

            self.driver.implicitly_wait(10)
            pass

        return listProducts

    def exit(self):
        self.driver.close()
        self.driver.quit()
        pass
