# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from shoppingcart import shoppingcart_pb2 as shoppingcart_dot_shoppingcart__pb2


class ShoppingCartStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddItem = channel.unary_unary(
        '/com.example.shoppingcart.ShoppingCart/AddItem',
        request_serializer=shoppingcart_dot_shoppingcart__pb2.AddLineItem.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.RemoveItem = channel.unary_unary(
        '/com.example.shoppingcart.ShoppingCart/RemoveItem',
        request_serializer=shoppingcart_dot_shoppingcart__pb2.RemoveLineItem.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.GetCart = channel.unary_unary(
        '/com.example.shoppingcart.ShoppingCart/GetCart',
        request_serializer=shoppingcart_dot_shoppingcart__pb2.GetShoppingCart.SerializeToString,
        response_deserializer=shoppingcart_dot_shoppingcart__pb2.Cart.FromString,
        )


class ShoppingCartServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def AddItem(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveItem(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetCart(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ShoppingCartServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddItem': grpc.unary_unary_rpc_method_handler(
          servicer.AddItem,
          request_deserializer=shoppingcart_dot_shoppingcart__pb2.AddLineItem.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'RemoveItem': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveItem,
          request_deserializer=shoppingcart_dot_shoppingcart__pb2.RemoveLineItem.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'GetCart': grpc.unary_unary_rpc_method_handler(
          servicer.GetCart,
          request_deserializer=shoppingcart_dot_shoppingcart__pb2.GetShoppingCart.FromString,
          response_serializer=shoppingcart_dot_shoppingcart__pb2.Cart.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'com.example.shoppingcart.ShoppingCart', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))