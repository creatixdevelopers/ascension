from datetime import datetime, timezone

import stripe
from fastapi import APIRouter, Request
from sqlalchemy import select

from app.config import settings
from app.models import Payment, User
from app.schemas.payment import CheckoutSchema, PaymentReadSchema
from app.services.auth import requires
from app.services.db import dbDep
from app.services.exceptions import BadRequest, ServerError
from app.services.stripe import monthly_subscription_price, one_time_price

router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/checkout")
@requires([])
async def post_checkout(request: Request, data: CheckoutSchema, db: dbDep):
    user = User.uget(db=db, uid=request.state.sub)
    if data.type not in ["one_time", "subscription"]:
        raise BadRequest("Invalid payment type")

    one_time_payment = data.type == "one_time"
    price_id = one_time_price.id if one_time_payment else monthly_subscription_price.id

    try:
        session = stripe.checkout.Session.create(
            success_url=f"{settings.DOMAIN}/payment-redirect?success=true",
            cancel_url=f"{settings.DOMAIN}/payment-redirect?success=false",
            customer_email=user.email,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment" if one_time_payment else "subscription",
        )
        return {"url": session.url}
    except Exception as e:
        print(e)
        ServerError("Failed to create checkout session")


@router.post("/webhook/")
async def post_webhook(request: Request, db: dbDep):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        data = event.data.object
    except Exception as e:
        raise ServerError("Failed to create webhook") from e

    if event["type"] == "checkout.session.completed":
        customer_email = data.get("customer_email")
        if not customer_email:
            raise ServerError("No customer email provided")

        subscription_id = data.get("subscription")  # Only for subscriptions
        payment_intent_id = data.get("payment_intent")

        user = User.get_by(db=db, first=True, email=customer_email)
        if not user:
            raise BadRequest(f"User {customer_email} not found")

        is_subscription = subscription_id is not None
        if is_subscription:
            subscription = stripe.Subscription.retrieve(subscription_id)
            valid_until_timestamp = (
                subscription.get("items", {})
                .get("data", [{}])[0]
                .get("current_period_end")
            )
            if not valid_until_timestamp:
                raise ServerError("Subscription date missing")
            valid_until = datetime.fromtimestamp(valid_until_timestamp, tz=timezone.utc)
            Payment.create(
                db=db,
                user_id=user.id,
                payment_id=subscription_id if is_subscription else payment_intent_id,
                type="subscription" if is_subscription else "one_time",
                data=data,
                valid_until=valid_until,
            )
        else:
            Payment.create(
                db=db,
                user_id=user.id,
                payment_id=subscription_id if is_subscription else payment_intent_id,
                type="subscription" if is_subscription else "one_time",
                data=data,
            )
        db.commit()
    elif event["type"] == "invoice.paid":
        # TODO: Handle invoice.paid event to add new payment for existing subscription
        print("invoice.paid")
    else:
        print(f"Unhandled event type: {event['type']}")
        return {}


@router.get("/user/{user_id}/", response_model=list[PaymentReadSchema])
@requires(["payment.read.all"])
async def get_payments_by_user(request: Request, db: dbDep, user_id: str):
    query = select(Payment).join(Payment.user).where(User.uid == user_id)
    payments = db.execute(query).scalars().all()
    return [payment for payment in payments]
