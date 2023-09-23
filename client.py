import grpc
import game_pb2
import game_pb2_grpc
import multiprocessing
import time
import random

class Soldier:
    def __init__(self,id,x_coord,y_coord,speed,is_promoted):
        self.soldier_id=id
        self.x_coord=x_coord
        self.y_coord=y_coord
        self.soldier_speed=speed
        self.is_promoted = is_promoted
    

    def in_danger(self,all_missile_affected_coord):
        current_location=(self.x_coord,self.y_coord)
        if current_location in all_missile_affected_coord:
            return True
        else:
            return False 
    
    def move(self,all_missile_affected_coord):
        all_possible_moves=[(min(N-1,self.x_coord+self.soldier_speed),self.y_coord),
                            (max(0,self.x_coord-self.soldier_speed),self.y_coord),
                            (self.x_coord,min(N-1,self.y_coord+self.soldier_speed)),
                            (self.x_coord,max(0,self.y_coord-self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),max(0,self.y_coord-self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),max(0,self.y_coord-self.soldier_speed))]
        possible_move=[]
        for i in all_possible_moves:
            if i not in all_missile_affected_coord:
                possible_move.append(i)

        if not possible_move:
            (x,y)=random.choice(all_possible_moves)
        else:
            (x,y)=random.choice(possible_move)
        self.x_coord=x
        self.y_coord=y

        
        
        
    def take_shelter(self,all_missile_affected_coord):
        possible_move=[]
        #all_possible_moves=[(x,y) for x in range(max(0, self.x_coord - self.soldier_speed), min(N-1, self.x_coord+self.soldier_speed)) for y in range(max(0, self.y_coord - self.soldier_speed), min(N-1, self.y_coord+self.soldier_speed))]
        all_possible_moves=[(min(N-1,self.x_coord+self.soldier_speed),self.y_coord),
                            (max(0,self.x_coord-self.soldier_speed),self.y_coord),
                            (self.x_coord,min(N-1,self.y_coord+self.soldier_speed)),
                            (self.x_coord,max(0,self.y_coord-self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),max(0,self.y_coord-self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),max(0,self.y_coord-self.soldier_speed))]
        for i in all_possible_moves:
            if i not in all_missile_affected_coord:
                possible_move.append(i)
        
        if not possible_move:
            (x,y)=random.choice(all_possible_moves)
        else:
            (x,y)=random.choice(possible_move)
        self.x_coord=x
        self.y_coord=y



    
        

    def check_alive_or_not(self,all_missile_affected_coord,q,lock):
        current_position=(self.x_coord,self.y_coord)
        if current_position in all_missile_affected_coord:
            return True
        else:
            return False



class Commander(Soldier):
    def __init__(self, id, x_coord, y_coord, speed):
        super().__init__(id, x_coord, y_coord, speed,True)
    
    def genereate_missile_coordinates_and_type():
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        type=random.randint(1,4)
        return x,y,type

    def commander_election(alive_soldiers_values):
        if not alive_soldiers_values:
            return 0
        new_commander= random.choice(alive_soldiers_values)
        return new_commander
    
    def printLayout():
        pass






def run_client(soldier_id,is_commander,x_coord,y_coord,speed,N,T,t,lock):
    

    channel=grpc.insecure_channel('localhost:50051')
    stub=game_pb2_grpc.GameServiceStub(channel)

    with lock:
        count_of_processes=count_of_processes+1
    
    time=0

    if is_commander:
        commander = Commander(soldier_id,x_coord,y_coord,speed,True)
        is_commander_alive=True
    else:
        soldier = Soldier(soldier_id,x_coord,y_coord,speed)
        soldier.move()

    while(count_of_processes!=M):
        pass

    
    '''is_alive=[]
    # initially all the soldier are alive
    for i in range(M):
        is_alive.append(i)'''


    while time<T and is_commander_alive:
        if commander.is_promoted:
            x,y,type=commander.genereate_missile_coordinates_and_type()
            missile_info=game_pb2.missile_info(x=x,y=y,time=t,type=type)
            missile_info_recieved=stub.missile_approaching(missile_info)
            missile_x=missile_info_recieved.x
            missile_y=missile_info_recieved.y
            missile_type=missile_info_recieved.type
            all_missile_affected_coord=[(x,y) for x in range(max(0, missile_x - missile_type), min(N-1, missile_x+missile_type)) for y in range(max(0, missile_y - missile_type), min(N-1, missile_y+ missile_type))]


            if commander.in_danger(all_missile_affected_coord):
                commander.take_shelter(all_missile_affected_coord)


            else:
                commander.move(all_missile_affected_coord)
                
            


            status=game_pb2.status(query="Give your status")
            status_query=stub.status(status)
            if status_query=="Give me your status":
                life_status=commander.check_alive_or_not(all_missile_affected_coord,lock)
                hit_info=game_pb2.hit_info(id=commander.soldier_id,flag=life_status)
                stub.was_hit(hit_info)
            status_query=" "
            alive_soldiers_values=stub.get_alive_soldier()
            commander.printLayout()



            if not life_status:
                is_commander_alive=False
                new_commander=commander.commander_election(alive_soldiers_values)
                if new_commander:
                    is_commander_alive=True
                
                else:
                    commander = Commander(new_commander[0],new_commander[1][0],new_commander[1][0],new_commander[2],True)
                    break

            
            # write code to increase time and check whether game lost or won



        else:
            pass

if __name__=="__main__":
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


    #is_alive=multiprocessing.Array('i',1*M)
    count_of_processes=multiprocessing.Value('i',0)
    #q=multiprocessing.Queue()
    lock=multiprocessing.Lock()
    #is_dead=multiprocessing.Array('i',0*M)


    commander=random.randint(0,M-1)
    for i in range(M):
        is_commander = (i==commander)
        process=multiprocessing.Process(target=run_client, args=(i,is_commander,random_coordinates[i][0],random_coordinates[i][1],speed[i],N,T,t,count_of_processes,lock))
        processes.append(process)
        process.start()


    for process in processes:
        process.join()
    

            
