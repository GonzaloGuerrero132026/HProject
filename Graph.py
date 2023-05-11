import random
import pandas as pd
import networkx as nx
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys

Town_list = []
dict_postcodes_bycounty = {}
dct_PopulationPercent = {}
dct_CountyAndPopulation = {}

def ToDoOnce():
    global Town_list 
    global dict_postcodes_bycounty 
    df = pd.read_csv('AddressInfo.csv', index_col=[0])
    groupby_County = df.groupby('County')
    counties_df=pd.DataFrame(groupby_County["County"].first())
    counties_list = counties_df["County"].values.tolist()
    for element in counties_list:
        dict_postcodes_bycounty[element] = groupby_County.get_group(element).reset_index(drop=True)
    groupby_Town = df.groupby('District')
    Town_df=pd.DataFrame(groupby_Town["District"].first())
    Town_list = Town_df["District"].values.tolist()
    for element in counties_list:
        dict_postcodes_bycounty[element] = groupby_County.get_group(element).reset_index(drop=True)
    groupby_Town = df.groupby('District')
    Town_df=pd.DataFrame(groupby_Town["District"].first())
    Town_list = Town_df["District"].values.tolist()
    global dct_CountyAndPopulation 
    for County in dict_postcodes_bycounty:
        Population_PerCounty = 0
        for row in range(len(dict_postcodes_bycounty[County].index)):
            Population_PerCounty = Population_PerCounty + dict_postcodes_bycounty[County]["Population"][row]
        dct_CountyAndPopulation[County] = Population_PerCounty
    global dct_PopulationPercent 
    dct_PopulationPercent = dct_CountyAndPopulation.copy()
    Total_Population = 0
    for element in dct_CountyAndPopulation:
        Total_Population = Total_Population + dct_CountyAndPopulation[element]
    for element in dct_PopulationPercent:
        dct_PopulationPercent[element] = float(dct_CountyAndPopulation[element] / Total_Population)
    return 0

ToDoOnce()

def Random_Person():
    # define lists of names and surnames
    Male_names = ["Gonzalo","William", "George", "Charles", "Henry", "Edward", "Arthur", "Frederick", "Alfred", "Albert", "David", "James", "John", "Thomas", "Richard", "Robert", "Stephen", "Peter", "Paul", "Simon", "Andrew", "Michael", "Mark", "Philip", "Timothy", "Nigel", "Oliver", "Harry", "Jack", "Tom", "Benjamin", "Joseph", "Luke", "Adam", "Samuel", "Daniel", "Matthew", "Christopher", "Nicholas", "Jonathan", "Edward", "Marcus", "Dominic", "Gareth", "Vincent", "Francis", "Patrick", "Anthony", "Martin", "Sebastian", "Oscar", "Leo", "Alexander", "Max", "Isaac", "Ethan", "Noah", "Jacob", "Mason", "Logan", "Lucas", "Caleb", "Elijah"]
    Female_names = ["Elizabeth", "Victoria", "Mary", "Anne", "Catherine", "Charlotte", "Sarah", "Caroline", "Louisa", "Alexandra", "Alice", "Emma", "Sophia", "Isabella", "Olivia", "Emily", "Ava", "Mia", "Lily", "Chloe", "Amelia", "Isla", "Ella", "Isabelle", "Grace", "Megan", "Lily", "Hannah", "Jessica", "Lucy", "Eleanor", "Eva", "Rosie", "Matilda", "Scarlett", "Freya", "Phoebe", "Abigail", "Poppy", "Florence", "Sienna", "Daisy", "Zara", "Ellie", "Sophie", "Millie", "Holly", "Imogen", "Charlotte", "Molly", "Maisie", "Jasmine", "Layla", "Harriet", "Annabelle", "Georgia", "Ivy", "Aria", "Aurora", "Gracie", "Martha", "Amelie", "Emilia", "Iris", "Clara", "Luna", "Nova", "Zoe", "Nora", "Lydia", "Violet", "Beatrice", "Evelyn", "Mabel", "Alice", "Harper", "Olive", "Thea", "Aria", "Aisha"]
    Surnames = ['Smith', 'Jones', 'Taylor', 'Brown', 'Wilson', 'Evans', 'Wright', 'Robinson', 'Thompson', 'White', 'Green', 'Hall', 'Wood', 'Lewis', 'Harris', 'Martin', 'Clarke', 'Jackson', 'Scott', 'Young', 'Allen', 'King', 'Wright', 'Bailey', 'Baker', 'Bell', 'Bennett', 'Brooks', 'Butler', 'Carter', 'Chapman', 'Cook', 'Cooper', 'Cox', 'Davies', 'Davis', 'Dixon', 'Edwards', 'Ellis', 'Fisher', 'Foster', 'Fox', 'Gray', 'Griffiths', 'Hamilton', 'Harrison', 'Hart', 'Hayes', 'Hill', 'Holmes', 'Hughes', 'Hunter', 'Jackson', 'James', 'Jenkins', 'Johnson', 'Johnston', 'Jones', 'Kelly', 'Kennedy', 'King', 'Knight', 'Lee', 'Lloyd', 'Long', 'Martin', 'Mason', 'Matthews', 'McDonald', 'Miller', 'Mitchell', 'Moore', 'Morgan', 'Morris', 'Murphy', 'Murray', 'Nelson', 'Parker', 'Phillips', 'Powell', 'Price', 'Reid', 'Reynolds', 'Richards', 'Richardson', 'Roberts', 'Robertson', 'Robinson', 'Rogers', 'Rose', 'Ross', 'Russell', 'Ryan', 'Scott', 'Shaw', 'Simpson', 'Smith', 'Stevens', 'Stewart', 'Sullivan', 'Taylor', 'Thomas', 'Thompson', 'Turner', 'Walker', 'Wallace', 'Ward', 'Watson', 'Webb', 'Welch', 'West', 'White', 'Williams', 'Williamson', 'Wilson', 'Wood', 'Woods', 'Wright']

    # randomly select a name and a gender
    if random.choice([True, False]):
        name = random.choice(Male_names)
        surname = random.choice(Surnames)
        gender = "Male"
    else:
        name = random.choice(Female_names)
        surname = random.choice(Surnames)
        gender = "Female"
    # return the name and gender
    return (name, surname , gender)

def GetEtnicity():
    ethnicities = ["White", "Black or African American", "Asian", "Hispanic or Latino", "Native American or American Indian", "Pacific Islander or Native Hawaiian", "Other"]
    random_ethnicity = random.choice(ethnicities)
    return random_ethnicity

def get_option(prob_dict):
    total_prob = sum(prob_dict.values())
    threshold = random.uniform(0, total_prob)
    cum_prob = 0
    for option, prob in prob_dict.items():
        cum_prob += prob
        if cum_prob > threshold:
            return option

def GetRandomAddressInfo():
    global dct_PopulationPercent
    County_selected = get_option(dct_PopulationPercent)
    global dict_postcodes_bycounty
    random_row= random.randint(0,len(dict_postcodes_bycounty[County_selected])-1)
    info_row_selected = dict_postcodes_bycounty[County_selected].iloc[[random_row]].reset_index(drop=True)
    Address=info_row_selected["Address"][0] 
    Postcode=info_row_selected["Postcode"][0] 
    Town=info_row_selected["District"][0] 
    County=info_row_selected["County"][0] 
    return Address,Postcode,Town,County

def GetBirthPlace(Town):
    random_number = random.randint(1, 2)
    if random_number == 1:
        BirthPlace = Town
    elif random_number == 2:
        List = Town_list
        BirthPlace = random.choice(List)    
    return BirthPlace

def GetPersonInfo():
    Name,Surname,Sex = Random_Person()
    Etnicity = GetEtnicity()
    Address,Postcode,Town,County = GetRandomAddressInfo()
    BirthPlace = GetBirthPlace(Town)
    Info = [Name,Surname,BirthPlace,Sex,Etnicity,Address,Postcode,Town,County]
    return Info

#5 people takes one minute aprox
def GetDataBase(NumberOfPeople):
    COLUMN_NAMES =["First name","Surname","Birth Place","Sex","Etnicity","Address","Postcode","Town","County"]
    df = pd.DataFrame(columns=COLUMN_NAMES)
    for number in range(NumberOfPeople):
        person = GetPersonInfo()
        df.loc[len(df)] = person
    return df

##THIS IS THE GRAPH PART
def DoTheGraph(People,group_cols,agg_cols):
    # Define the columns to group by
    group_cols = group_cols

    # Define the columns to aggregate by finding the most common value
    agg_cols = agg_cols

    # Read the DataFrame from a CSV file
    df = People

    # Group the DataFrame by the selected columns and find the most common value in each aggregate column
    grouped_df = df.groupby(group_cols).agg(lambda x: Counter(x).most_common(1)[0][0])[agg_cols].reset_index()

    # Add a column for the count of rows in each group
    grouped_df['count'] = df.groupby(group_cols).size().values

    # Add a column for the node label (based on the most common values in the aggregate columns)
    grouped_df['node_label'] = grouped_df.apply(lambda x: '-'.join(x[agg_cols].astype(str)), axis=1)

    # Add a column for the node ID (based on the selected group columns)
    grouped_df['node_id'] = grouped_df.apply(lambda x: 'Node ' + str(x.name + 1), axis=1)

    # Create a new empty graph
    G = nx.Graph()

    # Add nodes to the graph for each group of rows, with size proportional to the number of people in the group
    for idx, row in grouped_df.iterrows():
        G.add_node(row['node_id'], label=row['node_id'], size=row['count'])

    # Add edges between nodes that share the same value in the selected columns
    for idx, row in grouped_df.iterrows():
        for idx2, row2 in grouped_df.iterrows():
            shared_cols = []  # create a list to store the index of the shared columns
            for element in range(len(agg_cols)):
                if idx < idx2 and row[agg_cols[element]] == row2[agg_cols[element]]:
                    shared_cols.append(element)
            if len(shared_cols) >= 1: # check if at least one column value is shared between the two nodes
                edge_label = "-".join([str(x+1) for x in shared_cols])  # create the label for the edge
                G.add_edge(row['node_id'], row2['node_id'], weight=1, label=edge_label)
    


    return G,agg_cols,group_cols,grouped_df

def DrawTheGraph(G,agg_cols,group_cols):
    fig, ax = plt.subplots(figsize=(8, 8),facecolor='lightgreen')
    ax.set_facecolor('lightyellow')
    # Define layout parameters
    k = 0.30
    iterations = 500
    # Draw the network graph
    pos = nx.kamada_kawai_layout(G)
    node_sizes = [d['size']*100 for n,d in G.nodes(data=True)]
    nx.draw_networkx(G, pos=pos, with_labels=True, node_size=node_sizes , ax=ax)
    # set the color of every edge to purple
    edge_colors = {(u, v): 'purple' for u, v in G.edges()}
    nx.set_edge_attributes(G, values=edge_colors, name='color')
    # draw the edges with purple color
    nx.draw_networkx_edges(G, pos, width=1, edge_color='purple')
    # Add edge labels
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        edge_labels[(u, v)] = d['label']
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10,bbox={'facecolor':'none', 'edgecolor':'none', 'alpha':0.7},font_color='orange')
    # For the legend
    legend_labels = [str(i+1) + ': ' + agg_cols[i] for i in range(len(agg_cols))]
    handles = [mpatches.Patch(facecolor='none', edgecolor='none', label=i)for i in legend_labels]
    plt.legend(handles=handles, loc='upper right', fontsize='medium')
    # Set the node labels to be the "node_label" attribute of each node
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels)

    plt.show()

    return 0

"""def GetAssortativity(G):
    
    G.remove_nodes_from(list(nx.isolates(G)))
    G.remove_edges_from(nx.selfloop_edges(G))

    # Calculate the degree assortativity coefficient
    r = nx.degree_assortativity_coefficient(G)

    if np.isnan(r):
        r = 0.0
    
    # Return the result
    return r"""

def GetAssortativity(G):
    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        return 0

    # Remove isolates
    G.remove_nodes_from(list(nx.isolates(G)))

    if not G.is_directed():
        largest_component = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_component)

    # Calculate the Newman assortativity
    numerator = 0
    denominator = 0
    m = G.number_of_edges()
    for u in G.nodes():
        du = nx.degree(G, u)
        numerator += du * nx.degree(G, u, weight='weight')
        denominator += du ** 2

    denominator /= m
    assortativity = (numerator / m - denominator) / (1 - denominator)

    return assortativity
 
def GetModularity(G):
    # Get the communities using the greedy modularity algorithm
    communities = list(greedy_modularity_communities(G))

    # Remove empty communities
    communities = [c for c in communities if len(c) > 0]    

    # Calculate the modularity of the partition
    Q = nx.algorithms.community.modularity(G, communities)

    # Return the result
    return Q

def GetMatrix(G):
    adj_matrix = nx.to_numpy_matrix(G)
    nodes = G.nodes()
    df_matrix = pd.DataFrame(adj_matrix, index=nodes, columns=nodes)
    pd.set_option('max_columns', None)
    pd.set_option("max_rows", None)
    return df_matrix

