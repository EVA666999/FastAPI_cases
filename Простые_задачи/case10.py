from app.models.models import Products, product_list
from fastapi import FastAPI
from fastapi import Query

app = FastAPI()

@app.post("/create_product")
async def create_user(product: Products):
    product_list.append(product)
    return product

@app.get('/product')
async def get_product_list():
    return product_list

@app.get('/product/{product_id}')
async def get_product_id(product_id: int):
    for product in product_list:
        if product.product_id == product_id:
            return product
    else:
        return {'message': 'Такого id не существует!'}

@app.get('/products/search')
async def found_product(keyword: str, limit: int, category: str = None):
    found_products = []
    for product in product_list:
        if keyword == product.name and category == product.category:
            found_products.append(product)
    return found_products[:limit]