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

    '''def Join_Battlefield():
        print("Join Battlefield Request made")
        with lock:
            id=request.id
            x=request.x
            y=request.y
            speed=request.speed
            channel=context.channel
            self.soldiers.append([id,(x,y),speed,channel])
            print(f'Soldier id {request.id} joined the battlefield successfully')
        
        return request'''
    """def Join_Battlefield(self, request_iterator, context):
        for request in request_iterator:
            id=request.id
            x=request.x
            y=request.y
            speed=request.speed
            response_channel=context._channel
            print(f'Soldier number {request.id} joined the battlefield')
            self.soldiers.append([id,(x,y),speed,context])"""
    def Join_Battlefield(self, request_iterator, context):
        for request in request_iterator:
            id = request.id
            x = request.x
            y = request.y
            speed = request.speed

            # You can print the message without issues
            print(f'Soldier number {id} joined the battlefield')

            # Append soldier information to the list (assuming you want to store them)
            self.soldiers.append({
                "id": id,
                "position": (x, y),
                "speed": speed,
                "context": context,
            })
            



    def DisconnectClient(self, request, context):
        # When a client disconnects, remove them from the list
        id = request.client_id
        self.soldiers = [(id,(request.x,request.y),request.speed, channel) for cid, channel in self.connected_clients if cid != client_id]
    

    """def missile_approaching(self, request, context):
        print(f'The missile id is {request.m_id} and missile type is {request.m_type}')
        missile_info=game_pb2.missile_info(m_id=request.m_id,x=request.x,y=request.y,time=request.t,m_type=request.m_type)
        for i in self.soldiers:
            #stub=game_pb2_grpc.GameServiceStub(i[3])
            missile_info=game_pb2.missile_info(m_id=request.m_id,x=request.x,y=request.y,time=request.t,m_type=request.m_type)
            print(f'The missile id is {missile_info.m_id} and missile type is {missile_info.m_type}')
            print(missile_info.m_id,missile_info,m_type)
            i[3].write(missile_info)
            #stub.missile_approaching(missile_info)
        return missile_info"""

    def missile_approaching(self, request, context):
        print(f'The missile id is {request.m_id} and missile type is {request.m_type}')
        missile_info = game_pb2.missile_info(
        m_id=request.m_id, x=request.x, y=request.y, time=request.time, m_type=request.m_type)

        for i in self.soldiers:
            print(f'Soldier id: {i["id"]}')
        
        # Create a stub for the soldier if you don't already have one
            if i[3] is None:
                i[3] = game_pb2_grpc.GameServiceStub(i[2])

        # Send the missile info to the soldier using the stub's write method
            i[3].write(missile_info)

    # It's generally a good practice to return a response message, but it depends on your use case.
    # If you want to return a response, create it and return it here.
        response = game_pb2.missile_info(
        m_id=request.m_id, x=request.x, y=request.y, time=request.time, m_type=request.m_type)
        return response
        
def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    lock=multiprocessing.Lock
    run()
