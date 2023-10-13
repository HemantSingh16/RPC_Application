from concurrent import futures
import time
import multiprocessing
import grpc
import game_pb2
import game_pb2_grpc
import random
 
missile_info_availaible=False
soldier_waiting=0
status_availaible=False
status_waiting=0
current_live=0
was_hit_waiting=0

lock=multiprocessing.Lock()
class GameServicer(game_pb2_grpc.GameServicer):
    def __init__(self) -> None:
        super().__init__()
        self.soldiers=[]
        self.dead_soldiers=[]
        self.missile_info={}
        self.status_msg={}
        self.count=0
        self.commander=-1
        

    def Join_Battlefield(self, request, context):
        id = request.id
        x = request.x
        y = request.y
        speed = request.speed
        is_commander=request.is_commander
        if is_commander:
            self.commander={"id":id,
                            "x": x,
                            "y":y,
                            "speed": speed,
                            "is_commander":is_commander,}
        


        self.soldiers.append({
            "id": id,
            "x": x,
            "y":y,
            "speed": speed,
            "is_commander":is_commander,

        })
        
        void=game_pb2.void()
        return void

    def missile_approaching(self, request, context):
        global current_live
        current_live=len(self.soldiers)

        print(f'The missile id is {request.m_id} and missile type is {request.m_type} and the coordinates are ({request.x},{request.y})')
        self.missile_info["m_id"]=request.m_id
        self.missile_info["x"]=request.x
        self.missile_info["y"]=request.y
        self.missile_info["t"]=request.t
        self.missile_info["m_type"]=request.m_type
        global missile_info_availaible
        missile_info_availaible=True
        void=game_pb2.void()
        return void

    def get_missile_coordinates(self, request, context):
        global missile_info_availaible
        while not missile_info_availaible:
            pass
        
        m_id=self.missile_info["m_id"]
        x=self.missile_info["x"]
        y=self.missile_info["y"]
        t=self.missile_info["t"]
        m_type=self.missile_info["m_type"]
        missile_info=game_pb2.missile_info(m_id=m_id,x=x,y=y,t=t,m_type=m_type)
        
        #with lock:
            #self.count+=1
        #while self.count<=len(self.soldiers):
            #pass
        #self.count=0
        global soldier_waiting
        with lock:
            soldier_waiting+=1
        
        while soldier_waiting < len(self.soldiers):
            pass
        time.sleep(1)
        with lock:
            if soldier_waiting==len(self.soldiers):
                missile_info_availaible=False
                soldier_waiting=0

        time.sleep(1)
        return missile_info
    
    def status_all(self, request, context):
        print(f'Got the query {request.query} from the commander')
        self.status_msg["query"]=request.query
        void=game_pb2.void()
        global status_availaible
        status_availaible=True
        return void

    def get_status_msg(self, request, context):
        global status_availaible
        while not status_availaible:
            pass
        query=self.status_msg["query"]
        status_msg=game_pb2.status(query=query)
        global status_waiting
        with lock:
            status_waiting+=1

        while status_waiting < len(self.soldiers):
            pass
        time.sleep(1)
        with lock:
            if status_waiting == len(self.soldiers):
                status_availaible=False
                status_waiting=0
        
        time.sleep(1)

        return status_msg
    
    def send_current_pos(self, request, context):
        s_id=request.s_id
        current_x=request.x
        current_y=request.y
        for alive_soldiers in self.soldiers:
            if alive_soldiers["id"]==s_id:
                alive_soldiers["x"]=current_x
                alive_soldiers["y"]=current_y
                print(f"New position of soldier {s_id} is ({current_x},{current_y})")
                break
        void=game_pb2.void()
        return void
    
    def was_hit(self, request, context):
        global current_live
        global was_hit_waiting
        id=request.id
        flag=request.flag
        
        with lock:
            was_hit_waiting +=1
            for alive_soldiers in self.soldiers:
                if alive_soldiers["id"]==id:
                    if not flag:
                        self.soldiers.remove(alive_soldiers)
                        self.dead_soldiers.append(alive_soldiers)
        while was_hit_waiting < current_live:
            pass
        time.sleep(1)

        with lock:
            if was_hit_waiting==current_live:
                was_hit_waiting=0
        
        void=game_pb2.void()
        return void
    
    def get_alive_soldier(self, request, context):
        soldier_info=[]
        for i in self.soldiers:
            soldier_info.append(game_pb2.soldier_info(id=i["id"],x=i["x"],y=i["y"],speed=i["speed"],is_commander=i["is_commander"]))
        return game_pb2.Alive_soldier_values(values=soldier_info)
    
    def get_dead_soldier(self, request, context):
        dead_soldier_info=[]
        for i in self.dead_soldiers:
            dead_soldier_info.append(game_pb2.soldier_info(id=i["id"],x=i["x"],y=i["y"],speed=i["speed"],is_commander=i["is_commander"]))
        return game_pb2.Dead_soldier_values(values=dead_soldier_info)
    

    def elect_new_commander(self, request, context):
        
        if len(self.soldiers)==0:
            void=game_pb2.void()
            return void

        new_commander=random.choice(self.soldiers)
        new_commander["is_commander"]=True


        self.commander=new_commander
        print("New commander election taking place")
        
        void=game_pb2.void()
        return void
    
    def get_commander_info(self, request, context):
        time.sleep(1)
        commander_info=game_pb2.soldier_info(id=self.commander["id"],x=self.commander["x"],y=self.commander["y"],speed=self.commander["speed"],is_commander=self.commander["is_commander"])
        return commander_info
        
    
        





    







        #missile_info = game_pb2.missile_info(
            #m_id=request.m_id, x=request.x, y=request.y, time=request.time, m_type=request.m_type)

        #for i in self.soldiers:
            #print(f'Sending missile coordinates to Soldier id: {i["id"]}')
            #if i["channel"]!= context and not i["channel"].closed():
                #soldier_stub = i["stub"]
                #soldier_stub.missile_approaching(request)
        return request
        
def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(), server)
    server.add_insecure_port("0.0.0.0:50055")
    server.start()
    server.wait_for_termination()


if __name__=="__main__":
    
    run()
