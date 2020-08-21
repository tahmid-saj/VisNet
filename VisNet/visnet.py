import sys
#from localgraphclustering import *

#import time
#import numpy as np


from flask import Flask, render_template, jsonify, request, redirect, Response
import random, json

app = Flask(__name__)

nodes_py = [""] * 280
edges_py = [""] * 443
edges_source_py = [""] * 443
edges_target_py = [""] * 443
edges_s = [""] * 443
edges_t = [""] * 443
randnet_nodes = [""] * 1000
randnet_edges = [""] * 5000
randnet_nodea = [0] * 5000
randnet_nodeb = [0] * 5000
randnet_node_a = [0] * 1000
smallnet_nodes = [""] * 20
smallnet_edges = [""] * 50
smallnet_nodea = [0] * 50
smallnet_nodeb = [0] * 50
# edgespy = [[0, 1, 2, 3], [0, 5, 6, 20], [1, 2, 3, 20], [4, 7, 8, 20], [8, 9, 20, 20], [3, 7, 1, 2], [1, 3, 20, 20], [1, 8, 5, 2], [1, 4, 8, 20], [2, 20, 20, 20], [2, 20, 20, 20], [3, 4, 5, 20], [6, 8, 0, 5], [3, 4, 20, 20], [9, 4, 3, 20], [3, 4, 20, 20], [2, 3, 20, 20], [9, 20, 20, 20], [6, 20, 20, 20]]
# edgespy = [[0, 1, 2, 3], [0, 5, 6], [1, 2, 3], [4, 7, 8], [8, 9], [3, 7, 1, 2], [1, 3], [1, 8, 5, 2], [1, 4, 8], [2], [2], [3, 4, 5], [6, 8, 0, 5], [3, 4], [9, 4, 3], [3, 4], [2, 3], [9], [6]]
# edgeslength = [0] * 20
node_at = 0
edge_at = 0
rand_node = 0
rand_connections = 0
edge_mean = [0] * len(edges_py)
edge_std = [0] * len(edges_py)
edge_riskone = 0
edge_risktwo = 0
#numnodes = len(open('IP_nodes.txt').readlines())
#numedges = len(open('IP_edges_source.txt').readlines())

@app.route('/', methods=['GET', 'POST1', 'POST0', 'POST2', 'POST3'])
def index():
    rand_node = random.randint(1, len(nodes_py))
    nodes_file = open('IP_nodes.txt', 'r')
    edges_source_file = open('IP_edges_source.txt', 'r')
    edges_target_file = open('IP_edges_target.txt', 'r')
    edges_file = open('IP_edges.txt', 'w')

    for i in range(len(nodes_py)):
        nodes_py[i] = nodes_file.readline()

    for e in range(len(edges_py)):
        edges_source_py[e] = edges_source_file.readline()
        edges_target_py[e] = edges_target_file.readline()
        edges_py[e] = str(edges_source_file.readline()) + ":" + str(edges_target_file.readline())
        edges_file.write(edges_py[e])

    nodes_file.close()
    edges_source_file.close()
    edges_target_file.close()
    edges_file.close()


    #for i in range(len(nodes_py)):
    #    nodes_py[i] = i

    #for c in range(len(edgeslength)):
    #    edgeslength[c] = len(edgespy[c])

    #for e in range(len(edges_py)):
    #    if e == 0:
    #        edges_py[e] = 0
    #    else:
    #        edges_py[e] = random.randint(1, len(nodes_py))

    # POST request
    if request.method == 'POST1':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    elif request.method == 'POST0':
        time = request.get_json()['time']

        nodes_file_time = open('IP_nodes' + str(time) + '.txt', 'w')
        edges_source_file_time = open('IP_edges_source' + str(time) + '.txt', 'w')
        edges_target_file_time = open('IP_edges_target' + str(time) + '.txt', 'w')

        for n in range(len(nodes_py)):
            nodes_file_time.write(nodes_py[n])

        if time % 5 == 0:
            for a in range(len(edges_py)):
                a_ = random.randint(0, 442)
                b_ = random.randint(0, 442)

                edges_source_py[a] = edges_source_py[a_]
                edges_target_py[a] = edges_target_py[b_]

                edges_source_file_time.write(edges_source_py[a])
                edges_target_file_time.write(edges_target_py[a])

                nodes_file_time.close()
                edges_source_file_time.close()
                edges_target_file_time.close()

                return render_template('index.html', title='Home', nodes_py=nodes_py, edges_py=edges_py, edges_source_py=edges_source_py, edges_target_py=edges_target_py, node_at=node_at, edge_at=edge_at, rand_node=rand_node, edge_mean=edge_mean, edge_std=edge_std)
        else:
            for a in range(len(edges_py)):
                edges_source_file_time.write(edges_source_py[a])
                edges_target_file_time.write(edges_target_py[a])

            nodes_file_time.close()
            edges_source_file_time.close()
            edges_target_file_time.close()

            return 'OK', 200

    elif request.method == 'POST2':
        print("Time stamp A: " + request.get_json()['val11'])  # parse as JSON
        print("Time stamp B: " + request.get_json()['val12'])
        print("Time stamp C: " + request.get_json()['val13'])

        time_a = int(request.get_json()['val11'])
        time_b = int(request.get_json()['val12'])
        time_c = int(request.get_json()['val13'])

        edge_wk1 = [0] * len(edges_py)
        edge_wk2 = [0] * len(edges_py)

        nodes_file_time_a = open('IP_nodes' + str(time_a) + '.txt', 'r')
        edges_source_file_time_a = open('IP_edges_source' + str(time_a) + '.txt', 'r')
        edges_target_file_time_a = open('IP_edges_target' + str(time_a) + '.txt', 'r')

        nodes_file_time_b = open('IP_nodes' + str(time_b) + '.txt', 'r')
        edges_source_file_time_b = open('IP_edges_source' + str(time_b) + '.txt', 'r')
        edges_target_file_time_b = open('IP_edges_target' + str(time_b) + '.txt', 'r')

        nodes_file_time_c = open('IP_nodes' + str(time_c) + '.txt', 'r')
        edges_source_file_time_c = open('IP_edges_source' + str(time_c) + '.txt', 'r')
        edges_target_file_time_c = open('IP_edges_target' + str(time_c) + '.txt', 'r')

        M = [[0] * len(edges_py)] * (time_b - time_a)

        for i in range(time_a, time_b):
            nodes_file_time_i = open('IP_nodes' + str(i) + '.txt', 'r')
            edges_source_file_time_i = open('IP_edges_source' + str(i) + '.txt', 'r')
            edges_target_file_time_i = open('IP_edges_target' + str(i) + '.txt', 'r')

            k = 0
            for b in edges_source_file_time_b:
                k = k + 1
                for e in edges_source_file_time_i:
                    if b == e:
                        edge_wk1[k] = edge_wk1[k] + 1
                        M[k][i] = edge_wk1[k]

                        edge_mean[k] = 0
                        edge_mean[k] = int((edge_wk1[k] * 100 / (time_b - time_a)))
                        edge_std[k] = int(int((((edge_wk1[k]) ^ 2) / (time_b - time_a))) / (1/2))
                        if k != 0 and edge_mean[k] > edge_mean[k - 1]:
                           edge_riskone = k



            #print(edge_riskone)

            nodes_file_time_i.close()
            edges_source_file_time_i.close()
            edges_target_file_time_i.close()

        #func_risk(edge_riskone)

        N = [[0] * len(edges_py)] * (time_c - time_b)

        for i in range(time_b, time_c):
            nodes_file_time_i = open('IP_nodes' + str(i) + '.txt', 'r')
            edges_source_file_time_i = open('IP_edges_source' + str(i) + '.txt', 'r')
            edges_target_file_time_i = open('IP_edges_target' + str(i) + '.txt', 'r')

            k = 0
            for c in edges_source_file_time_c:
                k = k + 1
                for e in edges_source_file_time_i:
                    if c == e:
                        edge_wk1[k] = edge_wk1[k] + 1
                        N[k][i] = edge_wk1[k]

                        edge_mean[k] = 0
                        edge_mean[k] = int((edge_wk1[k] * 100 / (time_c - time_b)))
                        edge_std[k] = int(int((((edge_wk1[k]) ^ 2) / (time_c - time_b))) / (1 / 2))
                        if k != 0 and edge_mean[k] > edge_mean[k - 1]:
                            edge_risktwo = k

            #print(edge_risktwo)

            nodes_file_time_i.close()
            edges_source_file_time_i.close()
            edges_target_file_time_i.close()

        #func_risk(edge_risktwo)
        #edge_w1 = [0] * len(edges_py)
        #edge_w2 = [0] * len(edges_py)

        #M = [[0] * len(edges_py)] * time
        #N = [[0] * len(nodes_py)] * time

        # For ta to tb
        #----for i in range(time):
        #    for k in range(len(edges_py)):
        #        # if edge list in i network has k, then:
        #        edge_w1[k] += 1 # 1 = C in the algorithm.
        #        M[i][k] = 1
        #        edge_mean[k] = 0
        #        edge_mean[k] = 0
        #        edge_mean[k] = int((edge_w1[k] / time))
        #        edge_std[k] = int(int((((edge_w1[k]) ^ 2) / time)) / (1/2)) # wrong formula
        #        if k != 0 and edge_mean[k] > edge_mean[k - 1]:
        #             edge_risk1 = k

        # repeat for tb to tc

        # after all
        #mean1list
        #mean2list
        #std1list
        #std2list

        #for edge in edge_tb:
            # val of edge = (mean2 - mean1*2) * (std2 - std1*2)
            # if val >  5: red, >4: blue ...
            # update the edge file of tb network.

        # load the csv file of tb network.
        # send the network to js to handle the visualization.



        #func_risk(edge_risk1)

        #for i in range(time, time + 5):
        #    for k in range(len(edges_py)):
        #        edge_w2[k] += (k + 1000)
        #        N[i][k] = edge_w2[k]
        #        edge_mean[k] = 0
        #        edge_mean[k] = 0
        #        edge_mean[k] = int((edge_w2[k] / 5))
        #        edge_std[k] = int(int((((edge_w2[k]) ^ 2) / 5)) / (1/2))
        #        if k != 0 and edge_mean[k] > edge_mean[k - 1]:
        #            edge_risk2 = k

        #func_risk(edge_risk2)

        #edge_w = [0] * numedges
        #edge_mean = [0] * numedges
        #edge_std = [0] * numedges

        #M = [[0 for x in range(numedges)] for y in range(time)]

        #for i in range(time):
        #    for k in range(numedges):
        #        edge_w[k] += k
        #        M[k][i] = edge_w[k]
        #        edge_mean[k] = (edge_w[k] / time)
        #        edge_std[k] = (edge_w[k]/time)^(1/2)

        #node_mean = [0] * numnodes
        #node_std = [0] * numnodes
        #time = request.get_json()
        #N = [[0 for x in range(numnodes)] for y in range(time)]

        #for i in range(time):
        #    for k in range(numnodes):
        #        M[k][i] = k
        #        node_mean[k] = (k / time)
        #        node_std[k] = (node_mean[k] / time) ^ (1 / 2)

        nodes_file_time_a.close()
        edges_source_file_time_a.close()
        edges_target_file_time_a.close()

        nodes_file_time_b.close()
        edges_source_file_time_b.close()
        edges_target_file_time_b.close()

        nodes_file_time_c.close()
        edges_source_file_time_c.close()
        edges_target_file_time_c.close()

        return 'OK', 200

    # GET request
    elif request.method == 'POST3':
        print(request.get_json())  # parse as JSON

        time = int(request.get_json()['time'])
        node_degree = [0] * len(nodes_py)

        nodes_file_a = open('IP_nodes.txt', 'a')
        edges_source_file_a = open('IP_edges_source.txt', 'a')
        edges_target_file_a = open('IP_edges_target.txt', 'a')

        M = [[0] * len(nodes_py)] * time

        for i in range(time):
            for k in range(len(nodes_py)):
                node_degree[k] = k
                M[i][k] = node_degree[k]
                edge_mean[k] = 0
                edge_mean[k] = 0
                edge_mean[k] = int((node_degree[k] / time))
                edge_std[k] = int(int((((node_degree[k]) ^ 2) / time)) / (1 / 2))
                if k != 0 and node_degree[k] > node_degree[k - 1]:
                    node_risk = k

        #func_risk(node_risk)

        # edge_w = [0] * numedges
        # edge_mean = [0] * numedges
        # edge_std = [0] * numedges

        # M = [[0 for x in range(numedges)] for y in range(time)]

        # for i in range(time):
        #    for k in range(numedges):
        #        edge_w[k] += k
        #        M[k][i] = edge_w[k]
        #        edge_mean[k] = (edge_w[k] / time)
        #        edge_std[k] = (edge_w[k]/time)^(1/2)

        # node_mean = [0] * numnodes
        # node_std = [0] * numnodes
        # time = request.get_json()
        # N = [[0 for x in range(numnodes)] for y in range(time)]

        # for i in range(time):
        #    for k in range(numnodes):
        #        M[k][i] = k
        #        node_mean[k] = (k / time)
        #        node_std[k] = (node_mean[k] / time) ^ (1 / 2)

        nodes_file_a.close()
        edges_source_file_a.close()
        edges_target_file_a.close()

        return 'OK', 200

    else:
        return render_template('index.html', title='Home', nodes_py=nodes_py, edges_py=edges_py, edges_source_py=edges_source_py, edges_target_py=edges_target_py,
                               node_at=node_at, edge_at=edge_at, rand_node=rand_node, edge_mean=edge_mean, edge_std=edge_std)

#def func_risk(edge_risk):

    #print(edge_risk)
    #return render_template('index.html', title='Home', edge_risk=edge_risk)

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`

    return render_template('index.html', title='Home', nodes_py=nodes_py, edges_py=edges_py, edges_source_py=edges_source_py, edges_target_py=edges_target_py, node_at=node_at, edge_at=edge_at, rand_node=rand_node, edge_mean=edge_mean, edge_std=edge_std)

@app.route('/randnetwork')
def randnetwork():
    rand_network_nodes = open('rand_network_nodes.txt', 'w')
    rand_network_edges = open('rand_network_edges.txt', 'w')

    for n in range(50):
        a_ = random.randint(1, 20)
        b_ = random.randint(1, 100)
        randnet_node_a[n] = a_
        randnet_nodes[n] = str(a_) + "." + str(b_)
        rand_network_nodes.write(randnet_nodes[n] + '\n')

    for e in range(1000):
        a_ = random.randint(1, 1000)
        b_ = random.randint(1, 1000)
        randnet_nodea[e] = a_
        randnet_nodeb[e] = b_
        randnet_edges[e] = str(a_) + "  " + str(b_)
        rand_network_edges.write(randnet_edges[e] + '\n')

    rand_network_nodes.close()
    rand_network_edges.close()

    return render_template('randnetwork.html', title='Random Network', randnet_nodes=randnet_nodes, randnet_edges=randnet_edges,
                           randnet_nodea=randnet_nodea, randnet_nodeb=randnet_nodeb, randnet_node_a=randnet_node_a)

@app.route('/smallnetwork')
def smallnetwork():
    small_network_nodes = open('small_network_nodes.txt', 'w')
    small_network_edges = open('small_network_edges.txt', 'w')

    # Call the global spectral partitioning algorithm.
    #eig2 = fiedler(g)

    # Round the eigenvector
    #output_sc = sweep_cut(g, eig2)

    # Extract the partition for g and store it.
    #eig2_rounded = output_sc[0]

    # Conductance before improvement
    #print("Conductance before improvement:", g.compute_conductance(eig2_rounded))

    # Start calling SimpleLocal
    #start = time.time()
    #output_SL_fast = SimpleLocal(g, eig2_rounded)
    #end = time.time()
    #print("running time:", str(end - start) + "s")

    # Conductance after improvement
    #print("Conductance after improvement:", g.compute_conductance(output_SL_fast[0]))

    #output_SL = output_SL_fast[0]

    for n in range(20):
        smallnet_nodes[n] = str(n)
        small_network_nodes.write(smallnet_nodes[n] + '\n')

    for e in range(50):
        a_ = random.randint(1, 20)
        b_ = random.randint(1, 20)
        portone = random.randint(1000, 9999)
        porttwo = random.randint(1000, 9999)
        smallnet_nodea[e] = a_
        smallnet_nodeb[e] = b_
        smallnet_edges[e] = "Port src: " + str(portone) + " Port dst: " + str(porttwo)
        small_network_edges.write(smallnet_edges[e] + '\n')

    small_network_nodes.close()
    small_network_edges.close()

    return render_template('smallnetwork.html', title='Small Network', smallnet_nodes=smallnet_nodes, smallnet_edges=smallnet_edges,
                           smallnet_nodea=smallnet_nodea, smallnet_nodeb=smallnet_nodeb)
