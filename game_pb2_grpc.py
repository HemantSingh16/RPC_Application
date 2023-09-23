# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import game_pb2 as game__pb2


class GameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Join_Battlefield = channel.stream_stream(
                '/game.Game/Join_Battlefield',
                request_serializer=game__pb2.soldier_info.SerializeToString,
                response_deserializer=game__pb2.missile_info.FromString,
                )
        self.missile_approaching = channel.unary_unary(
                '/game.Game/missile_approaching',
                request_serializer=game__pb2.missile_info.SerializeToString,
                response_deserializer=game__pb2.missile_info.FromString,
                )
        self.status_all = channel.unary_unary(
                '/game.Game/status_all',
                request_serializer=game__pb2.status.SerializeToString,
                response_deserializer=game__pb2.status.FromString,
                )
        self.was_hit = channel.unary_unary(
                '/game.Game/was_hit',
                request_serializer=game__pb2.hit_info.SerializeToString,
                response_deserializer=game__pb2.void.FromString,
                )
        self.get_alive_soldier = channel.unary_unary(
                '/game.Game/get_alive_soldier',
                request_serializer=game__pb2.void.SerializeToString,
                response_deserializer=game__pb2.Alive_solier_values.FromString,
                )


class GameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Join_Battlefield(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def missile_approaching(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def status_all(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def was_hit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_alive_soldier(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Join_Battlefield': grpc.stream_stream_rpc_method_handler(
                    servicer.Join_Battlefield,
                    request_deserializer=game__pb2.soldier_info.FromString,
                    response_serializer=game__pb2.missile_info.SerializeToString,
            ),
            'missile_approaching': grpc.unary_unary_rpc_method_handler(
                    servicer.missile_approaching,
                    request_deserializer=game__pb2.missile_info.FromString,
                    response_serializer=game__pb2.missile_info.SerializeToString,
            ),
            'status_all': grpc.unary_unary_rpc_method_handler(
                    servicer.status_all,
                    request_deserializer=game__pb2.status.FromString,
                    response_serializer=game__pb2.status.SerializeToString,
            ),
            'was_hit': grpc.unary_unary_rpc_method_handler(
                    servicer.was_hit,
                    request_deserializer=game__pb2.hit_info.FromString,
                    response_serializer=game__pb2.void.SerializeToString,
            ),
            'get_alive_soldier': grpc.unary_unary_rpc_method_handler(
                    servicer.get_alive_soldier,
                    request_deserializer=game__pb2.void.FromString,
                    response_serializer=game__pb2.Alive_solier_values.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'game.Game', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Game(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Join_Battlefield(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/game.Game/Join_Battlefield',
            game__pb2.soldier_info.SerializeToString,
            game__pb2.missile_info.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def missile_approaching(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/game.Game/missile_approaching',
            game__pb2.missile_info.SerializeToString,
            game__pb2.missile_info.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def status_all(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/game.Game/status_all',
            game__pb2.status.SerializeToString,
            game__pb2.status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def was_hit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/game.Game/was_hit',
            game__pb2.hit_info.SerializeToString,
            game__pb2.void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_alive_soldier(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/game.Game/get_alive_soldier',
            game__pb2.void.SerializeToString,
            game__pb2.Alive_solier_values.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
