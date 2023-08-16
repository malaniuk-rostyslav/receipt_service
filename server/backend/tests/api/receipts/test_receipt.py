from datetime import datetime as dt
from datetime import timedelta
from typing import Dict, Tuple

from fastapi import status
from fastapi.testclient import TestClient

from ....db.models import constants
from ....db.models.receipt import association_receipt_product_table
from ....db.models.user import User
from ...conftest import TestSession
from ...db.factories.product import ProductFactory
from ...db.factories.receipt import ReceiptFactory
from ...db.factories.utils import fake

# Get today's date


def test_success_create_receipt(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    _, header = user_and_headers
    receipt_data = {
        "products": [{"name": fake.word(), "price": 5, "quantity": 2}],
        "payment": {"payment_type": constants.PaymentTypeEnum.CARD.value, "amount": 15},
    }
    response = client.post(f"/receipt", json=receipt_data, headers=header)
    assert response.status_code == status.HTTP_201_CREATED


def test_failed_create_receipt_not_correct_amount(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    _, header = user_and_headers
    receipt_data = {
        "products": [{"name": fake.word(), "price": 5, "quantity": 2}],
        "payment": {"payment_type": constants.PaymentTypeEnum.CARD.value, "amount": 9},
    }
    response = client.post(f"/receipt", json=receipt_data, headers=header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_success_get_my_receipts_created_at_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"created_at": datetime - timedelta(days=1)}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 1


def test_success_get_my_receipts_amount_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    receipt = ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"amount": receipt.amount - 1}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 1


def test_success_get_my_receipts_payment_type_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    receipt = ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"payment_type": receipt.payment_type}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 1


def test_failed_get_my_receipts_created_at_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"created_at": datetime + timedelta(days=1)}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 0


def test_failed_get_my_receipts_amount_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    receipt = ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"amount": receipt.amount + 1}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 0


def test_failed_get_my_receipts_payment_type_filter(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    ReceiptFactory(created_at=datetime, creator_id=user.id)
    query_params = {"payment_type": constants.PaymentTypeEnum.CASH.value}
    response = client.get(f"/receipt", headers=header, params=query_params)
    assert response.status_code == status.HTTP_200_OK
    receipts = response.json()
    assert receipts["total"] == 0


def test_success_get_my_receipt_by_id(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    receipt = ReceiptFactory(created_at=datetime, creator_id=user.id)
    product = ProductFactory(created_at=datetime, creator_id=user.id)
    with TestSession() as db:
        association_receipt_product = association_receipt_product_table.insert().values(
            receipt_id=receipt.id, product_id=product.id, quantity=5
        )
        db.execute(association_receipt_product)
        db.commit()
    response = client.get(f"/receipt/{receipt.id}", headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_failed_get_my_receipt_by_id_wrong_id(
    client: TestClient,
    db_session: TestSession,
    user_and_headers: Tuple[User, Dict[str, str]],
) -> None:
    user, header = user_and_headers
    datetime = dt.now()
    receipt = ReceiptFactory(created_at=datetime, creator_id=user.id)
    product = ProductFactory(created_at=datetime, creator_id=user.id)
    with TestSession() as db:
        association_receipt_product = association_receipt_product_table.insert().values(
            receipt_id=receipt.id, product_id=product.id, quantity=5
        )
        db.execute(association_receipt_product)
        db.commit()
    response = client.get(f"/receipt/{receipt.id+1}", headers=header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
