from app import create_app
from app.api.products.models import Products
from app.api.orders.models import Orders, OrderDetail

app = create_app()
