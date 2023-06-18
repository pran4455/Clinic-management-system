# graph DS to match symptoms with doctors
class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node, node_type):
        if node not in self.graph:
            self.graph[node] = {"node_type": node_type, "neighbors": []}

    def add_edge_doctor(self, node1, node2, node3):
        if node1 in self.graph and node2 in self.graph and node3 in self.graph:
            self.graph[node1]["neighbors"].append([node2, node3])
            self.graph[node2]["neighbors"].append([node1, node3])
            self.graph[node3]["neighbors"].append([node1, node2])

    def add_edge_disease(self, node1, node2, node3="-", node4="-"):
        if (
            node1 in self.graph
            and node2 in self.graph
            and node3 in self.graph
            and node4 in self.graph
        ):
            self.graph[node1]["neighbors"].extend([node2, node3, node4])
            self.graph[node2]["neighbors"].extend([node1, node3, node4])
            self.graph[node3]["neighbors"].extend([node1, node2, node4])
            self.graph[node4]["neighbors"].extend([node1, node2, node3])
        elif (
            node3 not in self.graph
            and node2 in self.graph
            and node3 in self.graph
            and node4 in self.graph
        ):
            self.graph[node1]["neighbors"].extend([node2, node4])
            self.graph[node2]["neighbors"].extend([node1, node4])
            self.graph[node4]["neighbors"].extend([node1, node2])
        elif (
            node4 not in self.graph
            and node2 in self.graph
            and node3 in self.graph
            and node4 in self.graph
        ):
            self.graph[node1]["neighbors"].extend([node2, node3])
            self.graph[node2]["neighbors"].extend([node1, node3])
            self.graph[node3]["neighbors"].extend([node1, node2])
        elif (
            node1 in self.graph
            and node2 in self.graph
            and node3 not in self.graph
            and node4 not in self.graph
        ):
            self.graph[node1]["neighbors"].extend([node2])
            self.graph[node2]["neighbors"].extend([node1])

    def find_disease(self, symptoms):
        diseases, diseases_all = [], []
        for symptom in symptoms:
            if symptom in self.graph:
                # print(symptom,self.graph[symptom])
                for j in self.graph[symptom]["neighbors"]:
                    diseases_all.append(j)
        # print(diseases_all)

        for disease in diseases_all:
            # print(self.graph[disease])
            sym = []
            for j in self.graph[disease]["neighbors"]:
                if type(j) == str:
                    sym.append(j)
            # print("\n\n",sym,symptoms)
            if sorted(sym) == sorted(symptoms) and disease not in diseases:
                diseases.append(disease)
        # print("fianl",diseases)
        if diseases != []:
            return diseases
        max_count = 1

        for disease in diseases_all:
            dc = diseases_all.count(disease)
            if disease not in diseases:
                if dc == max_count:
                    diseases.append(disease)

                elif dc > max_count:
                    max_count = dc
                    diseases = [disease]
                    # diseases.append(disease)

        # print(diseases)
        if diseases != []:
            return diseases
        else:
            for disease in diseases_all:
                if disease not in diseases:
                    diseases.append(disease)
            return diseases

    def get_matching_doctors(self, diseases, age):
        doctors = []
        for disease in diseases:
            # print(self.graph[disease]["neighbors"])
            for k in self.graph[disease]["neighbors"]:
                if len(k) == 2 and k[0][0] <= age <= k[0][1]:
                    doctors.append(k[1])
        return doctors
