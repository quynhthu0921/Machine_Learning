from review109.product import Product
from review109.products import ListProduct

lp = ListProduct()
lp.add_product(Product(100, "Product 1", 200, 10))
lp.add_product(Product(200, "Product 2", 10, 15))
lp.add_product(Product(300, "Product 3", 90, 20))
lp.add_product(Product(150, "Product 4", 100, 8))
lp.add_product(Product(250, "Product 5", 150, 13))
print("List of Products:")
lp.print_products()
lp.desc_sort_products()
print("List of Product after descending sort")
lp.print_products()