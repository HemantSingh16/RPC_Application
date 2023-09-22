from concurrent import futures
import time

import grpc
import game_pb2
import game_pb2_grpc

class GameServicer(game_pb2_grpc.GameServicer):
    def missile_approaching():
        pass


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    run()
