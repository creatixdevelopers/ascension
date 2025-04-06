import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_API_KEY

one_time_products = stripe.Product.search(
    query="active:'true' AND name:'One-Time Payment'"
)
if one_time_products.data:
    one_time_product = one_time_products.data[0]
    one_time_prices = stripe.Price.list(product=one_time_product.id, active=True)
    if one_time_prices.data:
        one_time_price = one_time_prices.data[0]
    else:
        raise Exception("No active price found for One-Time Payment product")
else:
    raise Exception("No product named One-Time Payment found")

monthly_subscription_products = stripe.Product.search(
    query="active:'true' AND name:'Daily Subscription'"
)
if monthly_subscription_products.data:
    monthly_subscription_product = monthly_subscription_products.data[0]
    monthly_subscription_prices = stripe.Price.list(
        product=monthly_subscription_product.id, active=True
    )
    if monthly_subscription_prices.data:
        monthly_subscription_price = monthly_subscription_prices.data[0]
    else:
        raise Exception("No active price found for Monthly Subscription product")
else:
    raise Exception("No product named Monthly Subscription found")
