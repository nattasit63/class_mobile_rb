#!/usr/bin/python3
import rclpy
from rclpy.node import Node
import sys
from mobile_robot_interfaces.srv import Fleet
from std_msgs.msg import Int8MultiArray
import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools
import random



POINT_POS = [[900,330],[900,825],[615,825],[315,825],[615,1325],[315,1325],[615,1825],[315,1825],[615,2310],[315,2310],
              [1000,2310],[1385,2310],[1685,2310],[1385,1825],[1685,1825],[1385,1325],[1685,1325],[1385,825],[1685,825],[1100,330],[1100,825],[1000,1325]]
"""
    9   8     10    11  12
    7   6           13  14
    5   4     21    15  16
    3    2   1  20  17  18
             0  19
"""
EDGE_LIST = [['0','1'],['19','20'],['1','2'],['2','3'],['2','4'],['4','5'],['4','6'],['6','7'],['6','8'],
             ['8','9'],['8','10'],['10','11'],['11','12'],['11','13'],['13','14'],['13','15'],
             ['15','16'],['15','17'],['17','18'],['17','20'],['1','21'],['20','21'],['21','10'],['1','20']]

NEW_EDGE = [[0, 1],[1,20] ,[19, 20], [1, 2], [2, 3], [2, 4], [4, 5], [4, 6], [6, 7], [6, 8], [8, 9], [8, 10], [10, 11], [11, 12], [11, 13], [13, 14], [13, 15], [15, 16], [15, 17], [17, 18], [17, 20], [1, 21], [20, 21], [21, 10]]

MAPPING_TABLE_NODE = {1:3,3:5,5:7,7:9,2:18,4:16,6:14,8:12}

def euclidean_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points in 2D.
    """
    x1, y1 = point1[0],point1[1]
    x2, y2 = point2[0],point2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Fleet_manager(Node):

    def __init__(self):
        super().__init__('fleet_manager')
        self.gui_subscriber = self.create_subscription(Int8MultiArray,'gui/table_list',self.gui_callback,10)
        self.fleet_service = self.create_service(Fleet,'fleet_of_table',self.fleet_service_callback)
        self.gui_subscriber
        self.table = []

        #Initial Graph
        node_list = [str(x) for x in range(len(POINT_POS))]
        self.G = nx.Graph()
        for i in range(len(node_list)):
            self.G.add_node(i)
        for i in range(len(NEW_EDGE)):
                self.G.add_edge(NEW_EDGE[i][0],NEW_EDGE[i][1],weight=euclidean_distance(POINT_POS[NEW_EDGE[i][0]],POINT_POS[NEW_EDGE[i][1]]))
        nx.draw(self.G, pos=POINT_POS, with_labels=True , arrows = True)
        # plt.show()
        self.create_timer(1.0,self.timer_callback)

    def find_best_cost(self,robot_id,list_of_list_of_table):

        # print(f'what inpu : {robot_id},{list_of_list_of_table}')
        lowest_cost = 999999.0
        if robot_id==1:
            path_lowcost = []
            table_low = []
            for list_of_table in list_of_list_of_table:
                list_of_table.insert(0,0)
                list_of_table.append(0)

                path_1 = nx.astar_path(self.G, list_of_table[0], list_of_table[1], weight='weight')
                weight_1 = nx.astar_path_length(self.G, list_of_table[0], list_of_table[1], weight='weight')

                path_2 = nx.astar_path(self.G, list_of_table[1], list_of_table[2], weight='weight')
                weight_2 = nx.astar_path_length(self.G, list_of_table[1], list_of_table[2], weight='weight')

                path_3 = nx.astar_path(self.G, list_of_table[2], list_of_table[3], weight='weight')
                weight_3 = nx.astar_path_length(self.G, list_of_table[2], list_of_table[3], weight='weight')

                path_4 = nx.astar_path(self.G, list_of_table[3], list_of_table[4], weight='weight')
                weight_4 = nx.astar_path_length(self.G, list_of_table[3], list_of_table[4], weight='weight')

                sum_weight = weight_1+weight_2+weight_3+weight_4
                path_1 = path_1[:-1]
                path_2= path_2[:-1]
                path_3 = path_3[:-1]
                sum_path = path_1+path_2+path_3+path_4
                if sum_weight<=lowest_cost:
                    lowest_cost=sum_weight
                    path_lowcost=sum_path
                    table_low=list_of_table
            return lowest_cost,path_lowcost,table_low
        
        if robot_id==2:
            path_lowcost = []
            table_low = []
            for list_of_table in list_of_list_of_table:
                list_of_table.insert(0,19)
                list_of_table.append(19)

                path_1 = nx.astar_path(self.G, list_of_table[0], list_of_table[1], weight='weight')
                weight_1 = nx.astar_path_length(self.G, list_of_table[0], list_of_table[1], weight='weight')

                path_2 = nx.astar_path(self.G, list_of_table[1], list_of_table[2], weight='weight')
                weight_2 = nx.astar_path_length(self.G, list_of_table[1], list_of_table[2], weight='weight')

                path_3 = nx.astar_path(self.G, list_of_table[2], list_of_table[3], weight='weight')
                weight_3 = nx.astar_path_length(self.G, list_of_table[2], list_of_table[3], weight='weight')

                path_4 = nx.astar_path(self.G, list_of_table[3], list_of_table[4], weight='weight')
                weight_4 = nx.astar_path_length(self.G, list_of_table[3], list_of_table[4], weight='weight')

                sum_weight = weight_1+weight_2+weight_3+weight_4
                path_1 = path_1[:-1]
                path_2= path_2[:-1]
                path_3 = path_3[:-1]
                sum_path = path_1+path_2+path_3+path_4
                if sum_weight<=lowest_cost:
                    lowest_cost=sum_weight
                    path_lowcost=sum_path
                    table_low=list_of_table

            return lowest_cost,path_lowcost,table_low

    def gui_callback(self,msg):
        self.table = list(msg.data)
        self.mapping_table,self.mapping_table2 = [],[]

        # print(self.table)
        #Do fleet first robot
        print('-'*50)
        print('ID : ROBOT 1' )
        first_robot = self.table[0:3]
        for table in first_robot:
            self.mapping_table.append(MAPPING_TABLE_NODE[table])
        permutations = list(itertools.permutations(self.mapping_table))
        random.shuffle(permutations)
        random_table = [list(t) for t in permutations]
        weight,route,table_low = self.find_best_cost(robot_id=1,list_of_list_of_table=random_table)
        self.route = route 
        self.fleet_pos = [POINT_POS[i] for i in self.route]
        print(f'To go Station : {table_low}')
        print(f'Lowest Cost  : {weight}\nRoute of Lowest cost  : {route}')
        print(f'Pos : {self.fleet_pos}')

        #Do fleet second robot
        print('-'*50)
        print('ID : ROBOT 2' )
        second_robot = self.table[3::]
        print(second_robot)
        for table in second_robot:
            self.mapping_table2.append(MAPPING_TABLE_NODE[table])
        print(self.mapping_table2)
        permutations = list(itertools.permutations(self.mapping_table2))
        random.shuffle(permutations)
        random_table = [list(t) for t in permutations]
        # print(random_table)
        weight2,route2,table_low2 = self.find_best_cost(robot_id=2,list_of_list_of_table=random_table)
        self.route2 = route 
        self.fleet_pos2 = [POINT_POS[i] for i in self.route]
        print(f'To go Station : {table_low2}')
        print(f'Lowest Cost  : {weight2}\nRoute of Lowest cost  : {route2}')
        print(f'Pos : {self.fleet_pos2}')
        self.res_route = [self.route,self.route2]
        self.res_fleet_pos = [self.fleet_pos,self.fleet_pos2]




    def timer_callback(self):
        # if self.mapping_table!=[]:
        pass

    def fleet_service_callback(self,request,response):
        request = []
        response.fleet_station = self.res_route
        response.fleet_position = str(self.res_fleet_pos)
        # response.fleet_position =
        self.get_logger().info('Fleet Service has been response')
        return response



def main(args=None):
    rclpy.init(args=args)
    fleet = Fleet_manager()
    rclpy.spin(fleet)


if __name__ == '__main__':

    main()
    # node_list = [str(x) for x in range(len(POINT_POS))]
    # G = nx.Graph()
    # for i in range(len(node_list)):
    #     G.add_node(i)
    # for i in range(len(NEW_EDGE)):
    #         print(NEW_EDGE[i][0],NEW_EDGE[i][1])
    #         G.add_edge(NEW_EDGE[i][0],NEW_EDGE[i][1],weight=euclidean_distance(POINT_POS[NEW_EDGE[i][0]],POINT_POS[NEW_EDGE[i][1]]))
    
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, POINT_POS, edge_labels)
    # nx.draw(G, pos=POINT_POS, with_labels=True , arrows = True)
    # plt.show()