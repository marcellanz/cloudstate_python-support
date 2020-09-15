import grpc


import logging

from cloudstate.test.shoppingcart.shoppingcart_pb2 import GetShoppingCart, AddLineItem
from cloudstate.test.shoppingcart.shoppingcart_pb2_grpc import ShoppingCartStub

from cloudstate.test.run_test_server import run_test_server

logger = logging.getLogger()


def evaluate_shoppingcart_server(host: str, port: int):
    logger.info(f"host: {host}")
    logger.info(f"port: {port}")
    server_hostport = f"{host}:{port}"
    logger.info(f"connecting on {server_hostport}")
    channel = grpc.insecure_channel(server_hostport)

    stub = ShoppingCartStub(channel)
    request = GetShoppingCart(user_id="leeroy")
    response = stub.GetCart(request)
    logger.info(f"resp: {response}")

    stub.AddItem(
        AddLineItem(user_id="leeroy", product_id="0", name="beer", quantity=24)
    )
    response = stub.GetCart(request)
    logger.info(f"resp: {response}")


def test_shoppingcart():
    server_thread = run_test_server(port=8080)
    evaluate_shoppingcart_server("localhost", 8080)
    server_thread.stop()
