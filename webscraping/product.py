

class Product:

    def __init__(self, name, price, genre='', typeProduct='', promotion=False):
        self.name = name
        self.price = price
        self.genre = genre
        self.typeProduct = typeProduct
        self.promotion = promotion

    def getProduct(self):
        produto = {
            "name": self.name,
            "price": self.price,
            "genre": self.genre,
            "typeProduct": self.typeProduct,
            "promotion": self.promotion
        }

        return produto
