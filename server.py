from concurrent import futures
import time
import multiprocessing
import grpc
import game_pb2
import game_pb2_grpc

class GameServicer(game_pb2_grpc.GameServicer):
    def __init__(self) -> None:
        super().__init__()
        self.soldiers=[]

    def Join_Battlefield(self, request, context):
        print("Join Battlefield Request made")
        with lock:
            id=request.id
            x=request.x
            y=request.y
            speed=request.speed
            channel=context.channel
            self.soldiers.append([id,(x,y),speed,channel])
            print(f'Soldier id {request.id} joined the battlefield successfully')
        
        return request
    
    def DisconnectClient(self, request, context):
        # When a client disconnects, remove them from the list
        id = request.client_id
        self.soldiers = [(id,(request.x,request.y),request.speed, channel) for cid, channel in self.connected_clients if cid != client_id]
    

    def missile_approaching(self, request, context):
        for i in self.soldiers:
            stub=game_pb2_grpc.GameServiceStub(i[3])
            missile_info=game_pb2.missile_info(x=request.x,y=request.y,time=request.t,type=request.m_type)
            stub.missile_approaching(missile_info)
        



    


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    lock=multiprocessing.Lock
    run()
