import grpc
import game_pb2
import game_pb2_grpc
import multiprocessing
import time
import random

class Soldier:
    def __init__(self,id,x_coord,y_coord,speed):
        self.soldier_id=id
        self.x_coord=x_coord
        self.y_coord=y_coord
        self.soldier_speed=speed

    def in_danger(x,y,type):
        pass

    def move():
        pass

    def take_shelter(x,y,type):
        pass


class Commander(Soldier):
    def __init__(self, id, x_coord, y_coord, speed,server_stub):
        self.server_stub=server_stub
        super().__init__(id, x_coord, y_coord, speed)
    
    def genereate_missile_coordinates_and_type():
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        type=random.randint(1,4)
        return x,y,type

    def commander_election(is_alive):
        current_alive_list=[]
        for i in range(len(is_alive)):
            if is_alive[i]==1:
                current_alive_list.append(i)
        return random.choice(current_alive_list)




    
    




    




def run_client(soldier_id,is_commander,x_coord,y_coord,speed,is_alive,N,T,t):
    lock=multiprocessing.Lock

    channel=grpc.insecure_channel('localhost:50051')
    stub=game_pb2_grpc.GameServiceStub(channel)

    with lock:
        count_of_processes=count_of_processes+1
    
    time=0

    if is_commander:
        commander = Commander(soldier_id,x_coord,y_coord,speed,stub)
        is_commander_alive=True
    else:
        soldier = Soldier(soldier_id,x_coord,y_coord,speed)
        soldier.move()

    while(count_of_processes!=M):
        pass


    if is_commander:
        while(time<T):
            while is_commander_alive:
                x,y,type=Commander.genereate_missile_coordinates_and_type()
                missile_info=game_pb2.missile_info(x=x,y=y,time=t,type=type)
                missile_info_recieved=stub.missile_approaching(missile_info)
                Commander.take_shelter(missile_info_recieved.x,missile_info_recieved.y,missile_info_recieved.type)
                
                #not sure right now
                stub.status_all()

                game_pb2.Hit_info(Commander.id,)
                

            newCommander=Commander.commander_election(is_alive)

    else:
        pass


                



                    
                




if __name__=="main":
    speed=[]
    
    
    processes=[]
    N=int(input("Enter the battelfield size"))
    M=int(input("Enter the number of soldiers"))
    t=int(input("Enter the time after which missiles should be dropped"))
    T=int(input("Enter the total time in which the game should end"))
    print("Please enter the speed only in the range of 0-3")
    for i in range(M):
        temp=int(input("enter the speed of each soldier "+str(i+1)))
        if temp>=0 and temp<=4:
            speed[i]=temp
        else:
            while temp<0 and temp>5:
                print("Incorrect speed entered")
                temp=int(input("enter the correct speed of soldier "+str(i+1)))
            speed[i]=temp
    
    
    all_coord=[(x,y) for x in range(N) for y in range(N)]
    if M> len(all_coord):
        raise ValueError("The number of soldiers cannot be greater than total coordinates on the battlefield")
    random_coordinates=random.sample(all_coord,M)


    is_alive=multiprocessing.Array('i',1*M)
    count_of_processes=multiprocessing.Value('i',0)
    #is_dead=multiprocessing.Array('i',0*M)


    commander=random.randint(0,M-1)
    for i in range(M):
        is_commander = (i==commander)
        process=multiprocessing.Process(target=run_client, args=(i,is_commander,random_coordinates[i][0],random_coordinates[i][1],speed[i],is_alive,N,T,t,count_of_processes))
        processes.append(process)
        process.start()


    for process in processes:
        process.join()
    

            
