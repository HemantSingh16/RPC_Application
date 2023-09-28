import grpc
import game_pb2
import game_pb2_grpc
import multiprocessing
import time
import random
import logging
from colorama import init,Fore, deinit, Style

# Initializing Logging

logging.basicConfig(filename='output.log', level = logging.INFO, filemode= "w",format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Defining Soldier class
class Soldier:
    def __init__(self,id,x_coord,y_coord,speed,is_commander):
        self.soldier_id=id
        self.x_coord=x_coord
        self.y_coord=y_coord
        self.soldier_speed=speed
        self.is_commander = is_commander
        
    # Function to check if the soldier is in danger based on the missile coordinates  
    def in_danger(self,all_missile_affected_coord):
        current_location=(self.x_coord,self.y_coord)
        if current_location in all_missile_affected_coord:
            return True
        else:
            return False 

    # Function to take shelter to avoid the missile attack  
    def take_shelter(self,all_missile_affected_coord,N):
        logging.info(f"Soldier {self.soldier_id} is taking shelter as it is in danger")
        possible_move=[]
        # Calculating all possible moves
        all_possible_moves=[(min(N-1,self.x_coord+self.soldier_speed),self.y_coord),
                            (max(0,self.x_coord-self.soldier_speed),self.y_coord),
                            (self.x_coord,min(N-1,self.y_coord+self.soldier_speed)),
                            (self.x_coord,max(0,self.y_coord-self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (min(N-1,self.x_coord+self.soldier_speed),max(0,self.y_coord-self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),min(N-1,self.y_coord+self.soldier_speed)),
                            (max(0,self.x_coord-self.soldier_speed),max(0,self.y_coord-self.soldier_speed))]
        
        # Checking if all possible move is in affected coordinates or not

        for i in all_possible_moves:
            if i not in all_missile_affected_coord:
                possible_move.append(i)
        
        print(f"All possible moves for soldier {self.soldier_id} = {possible_move} ")
        if not possible_move:
            pos=random.choice(all_possible_moves)   
        else:
            pos=random.choice(possible_move)
        
        # Updating the coordinates of the soldier
        self.x_coord=pos[0]
        self.y_coord=pos[1]

    # Function to check if the soldier is alive or not

    def check_alive_or_not(self,all_missile_affected_coord):
        current_position=(self.x_coord,self.y_coord)
        # If cuurent position of soldier is in missile affected coordinates then the soldier is dead or else alive 
        if current_position in all_missile_affected_coord:
            return False
        else:
            return True

# Defining the Commander class which is subclass of Soldier class because a Commander will also be a soldier but it will have some extra features

class Commander(Soldier):
    def __init__(self, id, x_coord, y_coord, speed,is_commander):
        super().__init__(id, x_coord, y_coord, speed,is_commander)

    # Generating missile coordinates
    
    def genereate_missile_coordinates_and_type(self,N):
        x=random.randint(0,N-1)
        y=random.randint(0,N-1)
        type=random.randint(1,4)
        return x,y,type

    # Generating the print layout on screen in output
    
    def print_layout(self,soldier_list, commander_pos, missile_list,all_missile_affected_coord, N):

        pass

# All the processes created from main process will execute this function

def run_client(soldier_id,is_commander,x_coord,y_coord,speed,N,T,t,count_of_processes,M,lock,alive_soldiers_count):
    
    # Establishing GRPC Channel for Communication with the game server

    channel=grpc.insecure_channel('172.17.85.252:50055')
    stub = game_pb2_grpc.GameStub(channel)


    # Here each process will acquire a lock to increment the value of the shared variable count_of_processes
    with lock:
        count_of_processes.value += 1

    # Calculating the number of Iterations that will be performed

    count_of_iterations=T//t
    iterations=1
    
    # Here the Soldier is joining battle field, ie he is sending his info to the server that is being registered at the server

    soldier_info=game_pb2.soldier_info(id=soldier_id,x=x_coord,y=y_coord,speed=speed,is_commander=is_commander)
    response=stub.Join_Battlefield(soldier_info)

    # If the process is a commander then commander object will be created and if they are soldier then soldier object created
    if is_commander:
        soldier = Commander(soldier_id,x_coord,y_coord,speed,is_commander)

    else:
        soldier = Soldier(soldier_id,x_coord,y_coord,speed,is_commander)
    

    missile_id=0

    # Here all the proccess will get stuck until all the process have joined the battlefield, it is done to provide synchronization

    while(count_of_processes.value <= M):
        if count_of_processes.value==M:
            break


    # Here a the processes will be in while loop until the total number of itertions are not performed

    while iterations<=count_of_iterations:
        
        if soldier.is_commander:  # the soldier checks if it is commander

            # This part of code would only be executed by the commander

            logging.info(f'{soldier_id} is commander')

            # Commander generating the missile coordinates and types randomly and broadcasting it to all alive soldiers

            x,y,m_type=soldier.genereate_missile_coordinates_and_type(N)
            missile_id +=1
            missile_info=game_pb2.missile_info(m_id=missile_id,x=x,y=y,t=t,m_type=m_type)
            missile=stub.missile_approaching(missile_info) # RPC call to broadcast missile info 
            void=game_pb2.void()
            
            logging.info(f'Commander generating missile of type {m_type} and on coordinates ({x},{y})')
            m_type-=1
            all_missile_affected_coord=[(a,b) for a in range(max(0, x - m_type), min(N-1, x + m_type)+1) for b in range(max(0, y - m_type), min(N-1, y + m_type)+1)]
            
            # Printing layout before taking evasion

            # Getting the values of alive soldiers and dead soldiers from the server

            void=game_pb2.void()
            alive_soldiers_values=stub.get_alive_soldier(void)
            dead_soldiers_values=stub.get_dead_soldier(void)
            print("********************Before taking Evasive action********************")

            # Printing Dead Soldiers

            dead_soldier_list=[]
            for sol in dead_soldiers_values.values:
                dead_soldier_list.append(sol.id)
            print(f"dead_soldier_list:  {dead_soldier_list} iteration: {iterations}")

            # Priniting the alive soldiers on the output

            alive_soldiers_list=[]
            print("Alive soldiers:")
            for sol in alive_soldiers_values.values:
                alive_soldiers_list.append([sol.x, sol.y,sol.id])
            alive_soldiers_count.value=len(alive_soldiers_list)
            commander_coord=[soldier.x_coord,soldier.y_coord,soldier.soldier_id]
            com_coord=(soldier.x_coord,soldier.y_coord,soldier.soldier_id)
            for i in alive_soldiers_list:
                if i == commander_coord:
                    alive_soldiers_list.remove(i)
            
            alive_soldiers_tuple=tuple(tuple(inner_list) for inner_list in alive_soldiers_list)         
            missile_list=[[x,y]]
            all_missile_affected_list=[list(t) for t in all_missile_affected_coord]
            soldier.print_layout(alive_soldiers_tuple,com_coord,missile_list ,all_missile_affected_list, N)


            # Commander fetching the missile info from the server

            missile_info_recieved=stub.get_missile_coordinates(void)
            missile_x=missile_info_recieved.x
            missile_y=missile_info_recieved.y
            missile_type=missile_info_recieved.m_type-1
            
            # if the soldier is in danger then they will take shelter

            if soldier.in_danger(all_missile_affected_coord):
                soldier.take_shelter(all_missile_affected_coord,N) # Local function call

            # Commander broadcasting a status all query to all soldiers to ask them to give their status    
            status=game_pb2.status(query="Give your status")
            logging.info(f"Commander broadcasting status message to all the soldiers")
            statuss=stub.status_all(status) # RPC call to broadcast status message to all the soldiers

            # Fetching status 
            void=game_pb2.void()
            query=stub.get_status_msg(void)
            status_query=query.query


            print(f"Soldier number {soldier.soldier_id} Recieved status from commander which is {status_query}")

            # If ther is a valid Status query 
            if status_query!=" ":
                life_status=soldier.check_alive_or_not(all_missile_affected_coord) # Checking Life status
                current_pos=game_pb2.position(s_id=soldier.soldier_id,x=soldier.x_coord,y=soldier.y_coord)
                print(f"The soldier number {soldier.soldier_id} is {life_status} ")
                rec=stub.send_current_pos(current_pos) # RPC call to send the current position to the server
                hit_info=game_pb2.hit_info(id=soldier.soldier_id,flag=life_status)
                stub.was_hit(hit_info) # RPC call to send the was hit info as a reply to status msg to the server
            else:
                print("status query is null")
            status_query=" "

            # Again fetching the value of alive soldiers and dead soldiers that might have changed after the missile attack

            void=game_pb2.void()
            alive_soldiers_values=stub.get_alive_soldier(void)
            dead_soldiers_values=stub.get_dead_soldier(void)
                
            print("********************After taking Evasive action********************")

            # Printing the dead soldiers and the number of iteration taken place

            dead_soldier_list=[]
            for sol in dead_soldiers_values.values:
                dead_soldier_list.append(sol.id)
            print(f"dead_soldier_list:  {dead_soldier_list} iteration: {iterations}")

            # Printing alive soldiers after the missile attack on output

            alive_soldiers_list=[]
            print("Alive soldiers:")
            for sol in alive_soldiers_values.values:
                alive_soldiers_list.append([sol.x, sol.y,sol.id])
            alive_soldiers_count.value=len(alive_soldiers_list)
            commander_coord=[soldier.x_coord,soldier.y_coord,soldier.soldier_id]
            c_coord=(soldier.x_coord,soldier.y_coord,soldier.soldier_id)
            for i in alive_soldiers_list:
                if i == commander_coord:
                    alive_soldiers_list.remove(i)
            alive_soldiers_tuple=tuple(tuple(inner_list) for inner_list in alive_soldiers_list)           
            missile_list=[[missile_x,missile_y]]
            all_missile_affected_list=[list(t) for t in all_missile_affected_coord]
            if not alive_soldiers_list:
                # For the case where there is no alive soldiers in the game
                co_coord=()
                print("all died")
                print(f"Soldier list :{alive_soldiers_tuple}\n commander coordinates {co_coord} \n missile list:{missile_list} \n all_missile_affected_coordinates {all_missile_affected_list}")
                soldier.print_layout(alive_soldiers_tuple,co_coord,missile_list ,all_missile_affected_list, N)
            else:     
                soldier.print_layout(alive_soldiers_tuple,c_coord,missile_list ,all_missile_affected_list, N)

            # If the commander dies 
            if not life_status:      
                void=game_pb2.void()
                logging.info("Electing new commander because current commander has died")
                new_commander=stub.elect_new_commander(void) # RPC call to server to elect new commander
                break # As the soldier has died it breaks out of the loop and this process terminates

            
        else:
            # This part of code will only be executed by Soldiers 
  
            void=game_pb2.void()

            missile_info_recieved=stub.get_missile_coordinates(void) #RPC call to recieve the missile info, sent from commander
            
            logging.info(f"{soldier.soldier_id} recieved missile info from commander")

            missile_x=missile_info_recieved.x
            missile_y=missile_info_recieved.y
            missile_type=missile_info_recieved.m_type-1
            

            #print(f'Successfully got missile info from commander where missile type = {missile_type}')
            
            all_missile_affected_coord=[(x,y) for x in range(max(0, missile_x - missile_type), min(N-1, missile_x + missile_type)+1) for y in range(max(0, missile_y - missile_type), min(N-1, missile_y + missile_type)+1)]
            
            # If soldier is in danger then it will take shelter or else it will 
            if soldier.in_danger(all_missile_affected_coord):
                soldier.take_shelter(all_missile_affected_coord,N)


            void=game_pb2.void()
            query=stub.get_status_msg(void)
            status_query=query.query
            if status_query != " ":
                logging.info(f"Soldier number {soldier.soldier_id} Recieved status from commander")
                life_status=soldier.check_alive_or_not(all_missile_affected_coord)
                current_pos=game_pb2.position(s_id=soldier.soldier_id,x=soldier.x_coord,y=soldier.y_coord)
                rec=stub.send_current_pos(current_pos) # RPC call to send current position of soldier to server so that it can be updated on server
                hit_info=game_pb2.hit_info(id=soldier.soldier_id,flag=life_status)
                stub.was_hit(hit_info) #RPC call to send the reply to the status query
            status_query=" "

            if not life_status:
                logging.info(f'The soldier number {soldier.soldier_id} has died ')
                break

            void=game_pb2.void()
            time.sleep(1)

            com_info=stub.get_commander_info(void) # Rpc call to fetch the information of current commander 
            if com_info.id == soldier.soldier_id:
                logging.info(f"The new commander selected after election is Soldier number {soldier.soldier_id}")
                soldier = Commander(com_info.id,com_info.x,com_info.y,com_info.speed,com_info.is_commander) # Creating the commander object for the soldier as it has become the new commander

        iterations += 1
        time.sleep(1)      



if __name__=="__main__":
    logging.info("Program Execution Started.")
    speed=[]
    processes=[]
    # Getting Hyperparameter as user input as it is programmable

    N=int(input("Enter the battelfield size ")) # Fetching the size of matrix
    M=int(input("Enter the number of soldiers ")) # Fetching the number of soldiers
    t=int(input("Enter the time after which missiles should be dropped ")) #  Fteching value of t
    T=int(input("Enter the total time in which the game should end ")) # Fetching value of T
    print("Please enter the speed only in the range of 0-4 ") # Fetching speed of each soldier
    for i in range(0,M):
        temp=int(input("enter the speed of soldier "+str(i)+" "))
        if temp>=0 and temp<=4:
            speed.append(temp)
        else:
            while temp<0 or temp>4:
                print("Incorrect speed entered ")
                temp=int(input("enter the correct speed of soldier "+str(i)+" "))
            speed.append(temp)
    
    
    all_coord=[(x,y) for x in range(N) for y in range(N)] # Generating the coordinates of NxN matrix
    if M> len(all_coord):
        raise ValueError("The number of soldiers cannot be greater than total coordinates on the battlefield ")
    random_coordinates=random.sample(all_coord,M)


    #is_alive=multiprocessing.Array('i',1*M)
    count_of_processes=multiprocessing.Value('i',0)
    q=multiprocessing.Queue()
    lock=multiprocessing.Lock()
    alive_soldiers_count=multiprocessing.Value('i',M)
    #is_dead=multiprocessing.Array('i',0*M)


    commander=random.randint(0,M-1) #Selecting the cmmander randomly
    for i in range(0,M):
        is_commander = (i==commander)

        # Creating number of process which is equal to total number of Soldiers and out of them one of them is choosen as commander and for that process the value of is_commander will be True
        process=multiprocessing.Process(target=run_client, args=(i,is_commander,random_coordinates[i][0],random_coordinates[i][1],speed[i],N,T,t,count_of_processes,M,lock,alive_soldiers_count))
        processes.append(process)
        process.start()


    for process in processes: #Waiting for all process to finish
        process.join()

    # If the number of soldiers after the game is greater than 50% of the soldiers which were thhere at the start then Game won or else lost
    if alive_soldiers_count.value>=M*0.5:
        print("Game won")
    else:
        print("Game Lost")
    

            
