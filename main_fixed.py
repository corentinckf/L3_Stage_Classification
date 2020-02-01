#############################################################################
#Nom code : main.py
#Description : code principal
    #- Parser
    #- [...]
#Auteurs : Chien Kan Foon Brandon - Corre Stanislas- Chien Kan Foon Corentin
#############################################################################

import networkx as nx
import matplotlib.pyplot as plt
#import pandas as pd 
from networkx.algorithms import isomorphism
import time

edges_filename = 'mutag_data/MUTAG_A.txt'
edgesLabels_filename = 'mutag_data/MUTAG_edge_labels.txt'
graphInds_filename = 'mutag_data/MUTAG_graph_indicator.txt'
graphsLabels_filename = 'mutag_data/MUTAG_graph_labels.txt'
nodesLabels_filename = 'mutag_data/MUTAG_node_labels.txt'

#Fonction get_NodesLabels :
    # Récupère dans le fichier DS_node_labels.txt la liste des labels des noeuds et la renvoie
    # WARNING : Noeud 1 a pour index 0 dans cette liste
def get_NodesLabels(file_name):
    file_object = open(file_name, 'r')
    nodesLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            nodesLabels_list.append(int(line_content))
    return nodesLabels_list

#Fonction get_EdgesLabels :
    # Récupère dans le fichier DS_edge_labels.txt la liste des labels des liens et la renvoie
    # WARNING : Lien 1 a pour index 0 dans cette liste
def get_EdgesLabels(file_name):
    file_object = open(file_name, 'r')
    edgesLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            edgesLabels_list.append(int(line_content))
    return edgesLabels_list

#Fonction get_GraphLabel :
    # Récupère dans le fichier DS_graph_labels.txt la liste qui associe le graphe à l'index i à sa classe
    # WARNING : Graph 1 a pour index 0 dans cette liste
def get_GraphLabels(file_name):
    file_object = open(file_name, 'r')
    graphLabels_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            graphLabels_list.append(int(line_content))
    return graphLabels_list

#Fonction get_GraphIndicator :
    # Récupère dans le fichier DS_graph_indicator.txt la liste qui associe le noeud à d'index i au graph auquel il appartien
    # WARNING : Indicator 1 a pour index 0 dans cette liste
def get_GraphIndicator(file_name):
    file_object = open(file_name, 'r')
    graphIndicator_list = []
    while 1:
        line_content = file_object.readline().strip()
        if not line_content:
            #eof
            break
        else:
            graphIndicator_list.append(int(line_content))
    return graphIndicator_list

#Fonction get_Edges :
    # Récupère dans le fichier DS_A.txt la liste des liens et la renvoie sous la forme lien : [noeud:int,noeud:int]
    # WARNING : Lien 1 a pour index 0 dans cette liste
def get_Edges(file_name):
    file_object = open(file_name, 'r')
    edges_list = []
    while 1:
        line_content = file_object.readline().strip().replace(',', '')
        if not line_content:
            #eof
            break
        else:
            temp_list = list(map(int,line_content.split())) #Conversion de [string,string] à [int,int]
            edges_list.append(temp_list)
    return edges_list

#Fonction list_Edges&Labels:
    #Crée la liste : [("noeud","noeud"), "label"]
def list_EdgeLabels(edges_filename, edgesLabels_filename):
    list = []
    edges = get_Edges(edges_filename)
    labels = get_EdgesLabels(edgesLabels_filename)
    for i in range(0, len(edges)):
        list.append([edges[i],labels[i]])
    return list

#Fonction get_GraphNodes :
    #Renvoie la liste des noeuds convertis en leurs labels du graph avec l'id en paramètre de la fonction
def get_GraphNodes(graph_id,indicator_nodes_list):
    nodes_list = [] 
    for i in range(0,len(indicator_nodes_list)):
        if(indicator_nodes_list[i]==graph_id):
            nodes_list.append(i+1)
    return nodes_list

#Fonction get_GraphEdges :
    #Renvoie la liste des liens du graph en fonction de sa liste de noeuds
def get_GraphEdges(graph_nodes_list,file_name):
    edges_list = []
    global_edges_list = get_Edges(file_name)
    for i in range(0,len(global_edges_list)):
        if global_edges_list[i][0] in graph_nodes_list or global_edges_list[i][1] in graph_nodes_list :
            edges_list.append(global_edges_list[i])
    return edges_list

#Fonction node_to_Label:
    #Renvoies la liste des labels de la liste de noeuds
def node_to_Label(nodes_list,global_labels_list):
    labels_list = []
    for i in nodes_list:
        labels_list.append(global_labels_list[int(i)-1])
    return labels_list

#Fonction edgelist_to_label:
    #Renvoies la liste des labels de la liste des liens
def edgelist_to_label(edges_list,edges_filename, edgesLabels_filename):
    list = []
    list_edgeNLabel = list_EdgeLabels(edges_filename, edgesLabels_filename)
    for i in edges_list:
        for j in list_edgeNLabel:
            if int(i[0])==j[0][0] and int(i[1])==j[0][1]:    
                list.append(j[1])
    return list

#Fonction create_Graph : 
    #Crée et renvoie un graph de classe x en fonction d'une liste de noeuds et de liens
    # Rappel des types de noeuds : 
    # 0->C 1->N 2->O 3->F 4->I 5->Cl 6->Br
def create_Graph(nodes_list,edges_list,global_labels_list_node,global_labels_list_edge,edges_filename, edgesLabels_filename):
    G = nx.Graph()
    nodeslbls_list = node_to_Label(nodes_list,global_labels_list_node)
    for i in range(0,len(nodes_list)):
        G.add_node(nodes_list[i], atome=nodeslbls_list[i])

    edgeslbls_list = edgelist_to_label(edges_list,edges_filename, edgesLabels_filename)
    for i in range(0, len(edges_list)):
        G.add_edge(edges_list[i][0],edges_list[i][1], label=str(edgeslbls_list[i]))
    
    return G

#Fonction get_NodesByLabel
    #Renvoies la liste des noeuds correspondant au label demandé dans G
def get_NodesByLabel(G,label):
    list = []
    nodes = G.nodes.data()
    for i in nodes:
        if(i[1]['atome']==label):
            list.append(int(i[0]))
    return list

#Fonction get_EdgesByLabel
    #Renvoies la liste des liens correspondant au label demandé dans G
def get_EdgesByLabel(G,label):
    list = []
    edges = G.edges.data()
    for i in edges:
        if i[2]['label']==label:
            list.append((i[0],(i[1])))
    return list

#Fonction get_GraphClass
    # Renvoie le nombre des graphes de la classe 1,le nombre des graphes de la classe -1, le total des deux nombre
def get_GraphClass():
    graphlabelslist = get_GraphLabels(graphsLabels_filename)
    countC1 = 0
    countC2 = 0
    for i in range(0,len(graphlabelslist)):
        if graphlabelslist[i] == 1 :
            countC1 += 1
        else:
            countC2 += 1
    return countC1, countC2, countC1+countC2

#Fonction display_Graph
    #Affiche le graphe choisi
def display_subGraph(G):
    pos=nx.spring_layout(G)
    print("Noeuds graph :" + str(G.nodes))
    print("Liens graph :" + str(G.edges))

    #Coloration des noeuds
    

    # 0  C black
    print(get_EdgesByLabel(G,'0'))
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,0)],#MODDDDIFIER
                       node_color='black',
                       node_size=500,
                   alpha=0.8)
    # 1  N blue
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,1)],
                       node_color='dodgerblue',
                       node_size=500,
                   alpha=0.8)
    # 2  O red
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,2)],
                       node_color='red',
                       node_size=500,
                   alpha=0.8)
    # 3  F yellow
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,3)],
                       node_color='yellow',
                       node_size=500,
                   alpha=0.8)
    # 4  I purple
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,4)],
                       node_color='purple',
                       node_size=500,
                   alpha=0.8)
    # 5  Cl green
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,5)],
                       node_color='green',
                       node_size=500,
                   alpha=0.8)
    # 6  Br brown
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[str(i) for i in get_NodesByLabel(G,6)],
                       node_color='brown',
                       node_size=500,
                   alpha=0.8)

    #Coloration des liens

    #0  aromatic
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'0'),
                       edge_color='silver',
                       line_width=10,
                   alpha=1)
    #1  single
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'1'),
                       edge_color='dimgrey',
                       line_width=10,
                   alpha=1)
    #2  double
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'2'),
                       edge_color='slateblue',
                       line_width=10,
                   alpha=1)
    #3  triple
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'3'),
                       edge_color='crimson',
                       line_width=10,
                   alpha=1)
    plt.axis('off')
    plt.show() #visualisation pas possible sur repl
#Fonction display_Graph
    #Affiche le graphe choisi
def display_Graph(nb_graph):
    G = create_Graph(get_GraphNodes(nb_graph,get_GraphIndicator(graphInds_filename)),get_GraphEdges(get_GraphNodes(nb_graph,get_GraphIndicator(graphInds_filename)),edges_filename),get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename)
    pos=nx.spring_layout(G)
    print("Noeuds graph :" + str(G.nodes))
    print("Liens graph :" + str(G.edges))

    #Coloration des noeuds

    # 0  C black
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,0),
                       node_color='black',
                       node_size=500,
                   alpha=0.8)
    # 1  N blue
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,1),
                       node_color='dodgerblue',
                       node_size=500,
                   alpha=0.8)
    # 2  O red
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,2),
                       node_color='red',
                       node_size=500,
                   alpha=0.8)
    # 3  F yellow
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,3),
                       node_color='yellow',
                       node_size=500,
                   alpha=0.8)
    # 4  I purple
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,4),
                       node_color='purple',
                       node_size=500,
                   alpha=0.8)
    # 5  Cl green
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,5),
                       node_color='green',
                       node_size=500,
                   alpha=0.8)
    # 6  Br brown
    nx.draw_networkx_nodes(G,pos,
                       nodelist=get_NodesByLabel(G,6),
                       node_color='brown',
                       node_size=500,
                   alpha=0.8)

    #Coloration des liens

    #0  aromatic
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'0'),
                       edge_color='silver',
                       line_width=10,
                   alpha=1)
    #1  single
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'1'),
                       edge_color='dimgrey',
                       line_width=10,
                   alpha=1)
    #2  double
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'2'),
                       edge_color='slateblue',
                       line_width=10,
                   alpha=1)
    #3  triple
    nx.draw_networkx_edges(G,pos,
                       edgelist=get_EdgesByLabel(G,'3'),
                       edge_color='crimson',
                       line_width=10,
                   alpha=1)

    plt.axis('off')
    plt.show() #visualisation pas possible sur repl



#Fonction qui , pour chaque graphe créé, compare si le sous graphe 'subgraph' choisi correspond à l'ensemble des graphes 'nbgraph' de la base de données sous forme de liste
def compare(nb_graph,subgraph):
    start_time = time.time()
    list = []
    county=0
    fsgC1 = 0
    fsgC2 = 0
    totAppSg = 0
    noFsgC1 = 0
    noFsgC2 = 0
    totNAppSg = 0
    confianceC1 = 0
    confianceC2 = 0
    print("Liste des résultats  : ('id_graph','Sous-graphe isomorphique ? Y/N')")
    for i in range(1,nb_graph+1):

        G = create_Graph(get_GraphNodes(i,get_GraphIndicator(graphInds_filename)),get_GraphEdges(get_GraphNodes(i,get_GraphIndicator(graphInds_filename)),edges_filename),get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename) # Créer un graphe 
        GM = isomorphism.GraphMatcher(G,subgraph,node_match= lambda n1,n2 : n1['atome']==n2['atome'], edge_match= lambda e1,e2: e1['label'] == e2['label']) # GM = GraphMatcher
        if GM.subgraph_is_isomorphic(): # Retourne un booléen si le sougraphe est isomorphe
            list.append((i,'Oui'))
            county+=1 
            
            if get_GraphLabels(graphsLabels_filename)[i] == 1:
                fsgC1+=1
            else:
                fsgC2+=1
                
        else:
            list.append((i,"Non"))
    list.append(("yes :", county))
    list.append(("no :", nb_graph-county))
    end_time = time.time()
    noFsgC1 = get_GraphClass()[0]-fsgC1
    noFsgC2 = get_GraphClass()[1]-fsgC2
    totAppSg = fsgC1+fsgC2
    totNAppSg =noFsgC1+noFsgC2

    #############################
    # Table de contingence fictive, à modifier si nécessaire
    Ctge_Table = [
    [fsgC1, fsgC2, totAppSg],
    [noFsgC1, noFsgC2, totNAppSg ], 
    [get_GraphClass()[0], get_GraphClass()[1], get_GraphClass()[2] ]]

    Ctge_Table_df = pd.DataFrame(Ctge_Table,
                                 index=['Sg','~Sg', ''],
                                 columns=['Graphe (1)',' Gaphe (-1)', 'Total Apparition'])

    print('/n')
    print(Ctge_Table_df)
    print('/n')
    #print("Confiance du SG dans la classe C1" + fsgC1/get_GraphClass()[0])
    print('/n')
    #print("Confiance du SG dans la classe C2" + fsgC2/get_GraphClass()[1])
    print('/n')
    #############################
    
    return list,"Temps éxécution : " + str(end_time-start_time) + "seconde(s)"

#Test avec le sous-graphe cyclique ("1")---("2")---("3")---("4")---("5")---("6"):
subgraph_nodes = ["1","2","3","4","5","6"]
subgraph_edges = [("1","2"), ("1", "6"), ("2","3"),("3","4"), ("4", "5"), ("5","6")]
subgraph_test = create_Graph(subgraph_nodes,subgraph_edges,get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename)
print('\n')
print(subgraph_test.edges.data())
print(get_EdgesByLabel(subgraph_test,0))
# print(compare(188, subgraph_test))

# subgraph_nodes = ["3353","3354","3355"]
# subgraph_edges = [("3353","3354"), ("3353","3355")]
# subgraph_test = create_Graph(subgraph_nodes,subgraph_edges,get_NodesLabels(nodesLabels_filename),get_EdgesLabels(edgesLabels_filename),edges_filename, edgesLabels_filename)
# print('\n')
# print(subgraph_test.nodes.data())
#print(compare(188, subgraph_test))

# Graphe 63
# some math labels

display_Graph(180)
display_subGraph(subgraph_test)

#Graphe 150
#display_Graph(150)


