import networkx as nx
import matplotlib.pyplot as plt

def gate_output(inputs, gate_type):
    if gate_type == "NOT": #inverter
        return int(not inputs[0])
    elif gate_type == "AND": #all inputs should be 1
        return int(not(0 in inputs))
    elif gate_type == "OR": #at least one 1
        return int(1 in inputs)
    elif gate_type == "NAND": #at least one 0
        return int(0 in inputs)  
    elif gate_type == "NOR": #all inputs should be 0 
        return int(not(1 in inputs) )
    elif gate_type == "XOR": #odd number of 1s
        return int((sum(inputs)%2)==1)
    else:
        return inputs
    
def execute_with_inputs(ckt, input_vector,output_file_path = False, print_details = False):
    i = 0
    output_vector = ""
    level_data = dict([(node, ckt.nodes[node]['level']) for node in list(ckt.nodes)])
    ordered = sorted(level_data, key=level_data.get)  
    for node in ordered:
        if list(ckt.predecessors(node)) == []:
            ckt.nodes[node]['value'] = int(input_vector[i])
            i = i + 1
            input_vector
            if print_details:
                print('Updated Node', node, "value to", ckt.nodes[node]['value']) 
        else:
            node_inputs = [ckt.nodes[inp]['value'] for inp in list(ckt.predecessors(node))]
            ckt.nodes[node]['value'] = gate_output(node_inputs, ckt.nodes[node]['gate'])
            if print_details:
                print('Updated Node', node, "value to", ckt.nodes[node]['value'])
        if list(ckt.successors(node)) == []:
            output = ckt.nodes[node]['value']
            output_vector = output_vector + str(output)
            if print_details:
                print("Output", node, ":", output)
                print("Output Vector:", output_vector, "\n")
    return output_vector

def simulate(netlist_file_path, input_file_path, output_file_path =False, 
             show_circuit = False, print_details = False):
    circuit = constructDAG(netlist_file_path)
    assign_levels(circuit)
    if show_circuit:
        details(circuit)
    apply_input(circuit, input_file_path, output_file_path, print_details)

def constructDAG(netlist):
    graph = nx.DiGraph()
    f = open(netlist, "r")
    for x in f:
        gatelist = x.split() 
#         print(x.split())
        gate = gatelist[0].split(":")[0]
        name = gatelist[0].split(":")[1]
        graph.add_node(name, gate = gate, value = 'X', level = "_")
        if gate != "IN":
            inp = gatelist[1:]
            for input_var in inp:
                graph.add_edges_from([(input_var, name)])
    return graph

def assign_levels(graph):
    for node in list(graph.nodes):
        if graph.nodes[node]["gate"] == "IN":
            graph.nodes[node]["level"] = 0
        else:
            lev = max([graph.nodes[x]["level"] for x in list(graph.predecessors(node))]) + 1
            graph.nodes[node]["level"] = lev
#     level_data = dict([(node, graph.nodes[node]['level']) for node in list(graph.nodes)])
#     print("Levels:", level_data)
#     ordered = sorted(level_data, key=level_data.get)
#     print("Nodes in order:", ordered)

def details(graph):
    print(list(graph.nodes))
    level_data = dict([(node, graph.nodes[node]['level']) for node in list(graph.nodes)])
    print("Levels:", level_data)
    ordered = sorted(level_data, key=level_data.get)
    print("Nodes in order:", ordered)
    input_nodes = [item[0] for item in level_data.items() if item[1] == 0]
    output_nodes = [item[0] for item in level_data.items() if item[1] == max(level_data.values())]
    print("Input Nodes:", input_nodes)
    print("Output Nodes: ", output_nodes)
    plt.figure()
    nx.draw_networkx(graph, arrows=True)
    
def apply_input(graph, input_file_path, output_file_path = False, print_details = False):
    ipfile = open(input_file_path, "r")
    op_vec_list = []
    for vector in ipfile:
        if print_details:
            print("Input Vector:", vector)
        output_vector = execute_with_inputs(graph, vector, output_file_path, print_details=print_details)
        op_vec_list.append(output_vector + "\n")
        if output_file_path != False:
            outputFile = open(output_file_path, 'w')
            outputFile.writelines(op_vec_list)
