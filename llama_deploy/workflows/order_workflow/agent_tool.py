from typing import Dict
import requests
import json
import random
import os 
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
MOBILE = os.getenv("MOBILE")
x_team = os.getenv("X_TEAM")
HEADERS = {'Content-type': 'application/json', 'x-team': x_team, 'mobile': MOBILE}


def create_order_tool(
        product_id: str = None,
        product_name: str = None,
        **kwargs
    ) -> Dict:
    """Use the tool to create orders.
    This function requies the below action input as inputs and 
    refer Structure response examples for format

    Action input:
        product_id (str): product id provided by the user
        product_name (str): product name provided by the user

    Structure response examples:
    { product_id: 'example_product_id', product_name: 'example_product_name' }
    """

    if product_id is None:
        return "Ask user to provide product id"
    
    if product_name is None:
        return "Ask user to provide product name"
    
    URL = BASE_URL + "order"
    
    id = random.randint(1000, 9999)

    data = {
        "id": str(id),
        "mobile": MOBILE,
        "productId": str(product_id),
        "productName": str(product_name)
    }

    response = requests.post(url=URL, data=json.dumps(data), headers=HEADERS)

    return json.loads(response.content)


def view_orders_tool(
        **kwargs
    ) -> Dict:
    """Use the tool to view all orders.

    Action input:
        None

    Structure response examples:
    None
    """
    
    URL = BASE_URL + "orders"

    response = requests.get(url=URL, headers=HEADERS)

    result = json.loads(response.content)

    result = str(f'The list of the orders {result["orders"]}')

    return result


def order_status_tool(
        order_id: str = None,
        **kwargs
    ) -> Dict:
    """Use the tool to view the order status.

    Action input:
        order_id (str): order id provided by the user

    Structure response examples:
    { 'order_id': 'example_order_id' }
    """
    
    if order_id is None:
        return "Ask user to provide order id"
    
    URL = BASE_URL + "order-status"

    params = { 'orderId': str(order_id), 'mobile': MOBILE}

    response = requests.get(url=URL, headers=HEADERS, params=params)

    result = json.loads(response.content)

    result = str(f'The status of the order is {result["status"]}. API response {result}')

    return result

if __name__ == "__main__":
    # print(create_order_tool(product_id="XUA9241", product_name="Samsung S22 Ultra"))
    # print(view_orders_tool())
    # print(order_status_tool(order_id="8104"))
    pass