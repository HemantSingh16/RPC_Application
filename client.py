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
    def __init__(self, id, x_coord, y_coord, speed,is_promoted):
        super().__init__(id, x_coord, y_coord, speed,is_promoted)
    
    def genereate_missile_coordinates_and_type(self,N):
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        type=random.randint(1,4)
        return x,y,type

    def commander_election(self,alive_soldiers_values):
        if not alive_soldiers_values:
            return 0
        new_commander= random.choice(alive_soldiers_values)
        return new_commander
    
    def printLayout():
        pass

def run_client(soldier_id,is_commander,x_coord,y_coord,speed,N,T,t,count_of_processes,M,lock):
    

    channel=grpc.insecure_channel('localhost:50051')
    stub=game_pb2_grpc.GameStub(channel)

    with lock:
        count_of_processes.value += 1
        print(f'Count of process is {count_of_processes.value}')
    
    time=0

    # joining battle field

    soldier_info=game_pb2.soldier_info(id=soldier_id,x=x_coord,y=y_coord,speed=speed)
    join_response=stub.Join_Battlefield(iter([soldier_info]))
    print(f'Soldier {soldier_id} joined the battlefield')

    if is_commander:
        commander = Commander(soldier_id,x_coord,y_coord,speed,True)
        print(f'commander is {soldier_id}')
        is_commander_alive=True
    else:
        soldier = Soldier(soldier_id,x_coord,y_coord,speed,False)

    while(count_of_processes.value!=M):
        pass

    
    '''is_alive=[]
    # initially all the soldier are alive
    for i in range(M):
        is_alive.append(i)'''
    is_commander_alive=True
    missile_id=0
    while time<T and is_commander_alive:
        print("Game started")
        if soldier.is_promoted:
            x,y,m_type=commander.genereate_missile_coordinates_and_type(N)
            missile_id+=1
            missile_info=game_pb2.missile_info(m_id=missile_id,x=x,y=y,time=t,m_type=m_type)
            missile_info_recieved=stub.missile_approaching(missile_info)
            missile_x=missile_info_recieved.x
            missile_y=missile_info_recieved.y
            missile_type=missile_info_recieved.m_type
            print(f'Successfully got missile info from commander where missile type = {missile_type}')
            all_missile_affected_coord=[(x,y) for x in range(max(0, missile_x - missile_type), min(N-1, missile_x+missile_type)) for y in range(max(0, missile_y - missile_type), min(N-1, missile_y+ missile_type))]


            if commander.in_danger(all_missile_affected_coord):
                commander.take_shelter(all_missile_affected_coord)


            else:
                commander.move(all_missile_affected_coord)
                
            status=game_pb2.status(query="Give your status")
            status_query=stub.status_all(status)
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
            print("Inside Soldier")
            previous = 0
            while previous ==  0 or previous == join_response.m_id :
                #current= join_response.id 
                previous = join_response.m_id
            
            missile_x=join_response.x
            missile_y=join_response.y
            missile_type=join_response.m_type
            print(f'Recieved missile coordinates {x} , {y} for soldier id {soldier.soldier_id}')

            all_missile_affected_coord=[(x,y) for x in range(max(0, missile_x - missile_type), min(N-1, missile_x+missile_type)) for y in range(max(0, missile_y - missile_type), min(N-1, missile_y+ missile_type))]
            
            if soldier.in_danger(all_missile_affected_coord):
                soldier.take_shelter(all_missile_affected_coord)
            else:
                soldier.move(all_missile_affected_coord)

            status_query = ""
            #status_query=stub.status(status)
            while status_query=="":
                status_query=stub.status(status)
            
            life_status=commander.check_alive_or_not(all_missile_affected_coord,lock)
            hit_info=game_pb2.hit_info(id=commander.soldier_id,flag=life_status)
            stub.was_hit(hit_info)    
            status_query=" "
            alive_soldiers_values=stub.get_alive_soldier()  

        time += t
        time.sleep(1)      



if __name__=="__main__":
    speed=[]
    
    
    processes=[]
    N=int(input("Enter the battelfield size "))
    M=int(input("Enter the number of soldiers "))
    t=int(input("Enter the time after which missiles should be dropped "))
    T=int(input("Enter the total time in which the game should end "))
    print("Please enter the speed only in the range of 0-3 ")
    for i in range(M):
        temp=int(input("enter the speed of soldier "+str(i+1)))
        if temp>=0 and temp<=4:
            speed.append(temp)
        else:
            while temp<0 and temp>5:
                print("Incorrect speed entered ")
                temp=int(input("enter the correct speed of soldier "+str(i+1)))
            speed.append(temp)
    
    
    all_coord=[(x,y) for x in range(N) for y in range(N)]
    if M> len(all_coord):
        raise ValueError("The number of soldiers cannot be greater than total coordinates on the battlefield ")
    random_coordinates=random.sample(all_coord,M)


    #is_alive=multiprocessing.Array('i',1*M)
    count_of_processes=multiprocessing.Value('i',0)
    #q=multiprocessing.Queue()
    lock=multiprocessing.Lock()
    #is_dead=multiprocessing.Array('i',0*M)


    commander=random.randint(0,M-1)
    for i in range(M):
        is_commander = (i==commander)
        process=multiprocessing.Process(target=run_client, args=(i,is_commander,random_coordinates[i][0],random_coordinates[i][1],speed[i],N,T,t,count_of_processes,M,lock))
        processes.append(process)
        process.start()


    for process in processes:
        process.join()
    

            
