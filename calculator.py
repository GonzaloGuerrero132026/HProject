import tkinter as tk
from Graph import *
from GetAddressCsv import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

def CheckIfFileExists():
    filename = "AddressInfo.csv" # replace with the name of the file you want to check
    filepath = os.path.join(os.getcwd(), filename)  # get the absolute path to the file
    if os.path.exists(filepath):
        return 0
    else:
        CreateFileAddress()

CheckIfFileExists()

#List of variables that i would need
Graphs_dict = {}
df_selector = 0 
df_dictionary = {}
agg_cols = []
group_cols = []
df_dictionary_Attributes = {}
df_selector_Attributes = 0 

# Create a window
window = tk.Tk()
window.title("Calculator")

# Set the background color of the window to black
window.configure(bg="black")

# Create a text box to display input and output
text_box = tk.Entry(window, width=40, borderwidth=5)
text_box.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Define functions for button clicks
def button_click(number):
    current = text_box.get()
    text_box.delete(0, tk.END)
    text_box.insert(0, str(current) + str(number))

def button_clear():
    text_box.delete(0, tk.END)
    global df_selector
    global df_dictionary
    global Graphs_dict
    global  agg_cols
    global  group_cols
    global  df_dictionary_Attributes 
    global  df_selector_Attributes
    Graphs_dict = {}
    df_selector = 0 
    df_dictionary = {}
    agg_cols = []
    group_cols = []
    df_dictionary_Attributes = {}
    df_selector_Attributes = 0
    button_ShowPeopleDF.config(state='disabled')
    button_SelectAttributesAndGraph.config(state='disabled')
    button_Graph.config(state='disabled')
    button_Assortativity.config(state='disabled')
    button_Modularity.config(state='disabled')

def button_GenerateDF():
    first_number = int(text_box.get())
    df = GetDataBase(first_number)
    global df_selector
    global df_dictionary
    global ActDataFrame
    global Operation
    Operation = "GenerateDF"
    ActDataFrame  = df
    df_selector = df_selector + 1
    df_dictionary["df" + str(df_selector)] =  ActDataFrame
    text_box.delete(0, tk.END)
    button_ShowPeopleDF.config(state='normal')
    button_SelectAttributesAndGraph.config(state='normal')

def button_ShowPeopleDF():
    global df_selector
    global df_dictionary
    global ActDataFrame
    # Create a new window
    dataframe_window = tk.Toplevel(window)

     # Add a label to the window
    label = tk.Label(dataframe_window, text="Select a dataframe:")
    label.pack()

    # Add an option menu with the dataframe options
    var = tk.StringVar(dataframe_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(dataframe_window, var, *df_dictionary.keys())
    option_menu.pack()

    # Add a function to display the selected dataframe
    def show_selected_dataframe():
        selected_df = var.get()
        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, str(df_dictionary[selected_df]))

    # Add a button to display the selected dataframe
    button = tk.Button(dataframe_window, text="Show dataframe", command=show_selected_dataframe)
    button.pack()

    # Add a text widget to display the dataframe
    display_text = tk.Text(dataframe_window, height=10, width=50)
    display_text.pack(fill=tk.BOTH, expand=True)
    ActDataFrame  = pd.DataFrame()

def button_SelectAttributesAndGraph():
    global agg_cols
    global group_cols 
    global df_selector_Attributes
    global df_dictionary_Attributes
    # Create a new window
    column_selector_window = tk.Toplevel(window)
    # Add a label to the window
    label = tk.Label(column_selector_window, text="Select a dataframe:")
    label.pack()
    # Add an option menu with the dataframe options
    var = tk.StringVar(column_selector_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(column_selector_window, var, *df_dictionary.keys())
    option_menu.pack()
    # Add a function to display the column selector
    def show_selected_dataframe():
        selected_df = var.get()
        display_text.delete('1.0', tk.END)
        # Clear the contents of group_cols and agg_cols
        group_cols = []
        agg_cols = []

        # Remove the previous checkbuttons and show selected options button, if they exist
        for widget in column_selector_window.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                widget.destroy()
            if isinstance(widget, tk.Button) and widget["text"] == "Lock selected columns":
                widget.destroy()
        # Create checkboxes for each column in the selected dataframe
        group_vars = tk.LabelFrame(column_selector_window, text='Group Columns')
        group_vars.pack(side='left', fill='y')
        for col in df_dictionary[selected_df].columns:
            group_var = tk.BooleanVar()
            group_check = tk.Checkbutton(group_vars, text=col, variable=group_var)
            group_check.pack(anchor='w')
            group_cols.append((col, group_var))

        agg_vars = tk.LabelFrame(column_selector_window, text='Aggregate Columns')
        agg_vars.pack(side='right', fill='y')
        for col in df_dictionary[selected_df].columns:
            agg_var = tk.BooleanVar()
            agg_check = tk.Checkbutton(agg_vars, text=col, variable=agg_var)
            agg_check.pack(anchor='w')
            agg_cols.append((col, agg_var))
        # Add a button to display the selected columns
        def show_selected_columns():
            group_columns_alpha = []
            agg_columns_alpha = []
            group_columns = []
            agg_columns = []
            group_columns = [col[0] for col in group_cols if col[1].get()]
            agg_columns = [col[0] for col in agg_cols if col[1].get()]
            #display_text.delete('1.0', tk.END)
            #display_text.insert(tk.END, f"Group Columns: {group_columns}\nAggregate Columns: {agg_columns}")
            group_columns_alpha = group_columns.copy()
            agg_columns_alpha = agg_columns.copy()
            df_dictionary_Attributes[selected_df] = (group_columns_alpha,agg_columns_alpha)
            display_text.delete('1.0', tk.END)
            display_text.insert(tk.END, f"Group Columns: {df_dictionary_Attributes[selected_df][0]}\nAggregate Columns: {df_dictionary_Attributes[selected_df][1]}")
            
        button = tk.Button(column_selector_window, text="Lock selected columns", command=show_selected_columns)
        button.pack()
    # Add a button to display the selected dataframe and checkboxes for selecting columns
    button = tk.Button(column_selector_window, text="Show Column Options", command=show_selected_dataframe)
    button.pack()

    # Add a text widget to display the selected columns
    display_text = tk.Text(column_selector_window, height=10, width=50)
    display_text.pack()

    button_Graph.config(state='normal')

def button_Graph():
    global Graphs_dict
    # Create a new window
    Graph_window = tk.Toplevel(window)
     # Add a label to the window
    label = tk.Label(Graph_window, text="Select a dataframe:")
    label.pack()
    # Add an option menu with the dataframe options
    var = tk.StringVar(Graph_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(Graph_window, var, *df_dictionary.keys())
    option_menu.pack()
    # Add a function to display the selected dataframe
    def show_selected_Graph(): 
        selected_df = var.get()
        G,agg_cols1,group_cols1,grouped_df = DoTheGraph(pd.DataFrame(df_dictionary[selected_df]),df_dictionary_Attributes[selected_df][0],df_dictionary_Attributes[selected_df][1])
        Graphs_dict[selected_df] = G
        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, str(grouped_df))
        DrawTheGraph(G,agg_cols1,group_cols1) # Draw the figure
    # Add a button to display the selected dataframe
    button = tk.Button(Graph_window, text="Show Graph and Nodes Info", command=show_selected_Graph)
    button.pack()

    # Add a text widget to display the dataframe
    display_text = tk.Text(Graph_window, height=10, width=50)
    display_text.pack(fill=tk.BOTH, expand=True)

    button_Assortativity.config(state='normal')
    button_Modularity.config(state='normal')
    button_Matrix.config(state='normal')
    
def button_Assortativity():
    global df_selector
    global df_dictionary
    global ActDataFrame
    global Graphs_dict
    # Create a new window
    dataframe_window = tk.Toplevel(window)

     # Add a label to the window
    label = tk.Label(dataframe_window, text="Select a dataframe:")
    label.pack()

    # Add an option menu with the dataframe options
    var = tk.StringVar(dataframe_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(dataframe_window, var, *df_dictionary.keys())
    option_menu.pack()

    # Add a function to display the selected dataframe
    def show_selected_dataframe():
        selected_df = var.get()
        Assortativity = GetAssortativity(Graphs_dict[selected_df])
        display_text.delete('1.0', tk.END)
        if Assortativity == 0 :
            Message = f"A value of {Assortativity} indicates that there is no preference for nodes to be connected to others with similar or different attributes. This means that the network is neither assortative nor disassortative, and the connections between nodes are random with respect to their attributes."
            display_text.insert(tk.END, Message)
        elif Assortativity>0 and Assortativity<0.5:
            Message = f"A value of {Assortativity} indicates that there is a weak preference for nodes to be connected to others with similar attributes, but the effect is not strong."
            display_text.insert(tk.END, Message)
        elif Assortativity>=0.5 and Assortativity<1:
            Message = f"A value of {Assortativity} indicates that there is a strong preference for nodes to be connected to others with similar attributes."
            display_text.insert(tk.END, Message)
        elif Assortativity == 1 :
            Message = f"A value of {Assortativity} indicates that nodes in the network are perfectly assortative, meaning that nodes with the same attribute values are connected to each other, and nodes with different attribute values are not connected to each other at all. In other words, the network is completely segregated by node attributes, and there are no connections between nodes with different attribute values."
            display_text.insert(tk.END, Message)
        elif Assortativity<0 and Assortativity>=-0.5:
            Message = f"A value of {Assortativity} suggests that there is some tendency for nodes with different attributes to be connected to each other, but the effect is relatively weak and the network is still relatively heterogeneous with respect to the attributes of its nodes."
            display_text.insert(tk.END, Message)
        elif Assortativity<-0.5 and Assortativity >-1:
            Message = f"A value of {Assortativity} indicates that nodes in the network are disassortative, meaning that nodes with different attribute values are more likely to be connected to each other than nodes with the same attribute values."
            display_text.insert(tk.END, Message)
        elif Assortativity == -1:
            Message = f"A value of {Assortativity} suggests a high degree of segregation in the network, with nodes forming groups or clusters based on their attribute values. This can have important implications for the function and dynamics of the network, as nodes with different attribute values may be less likely to interact and influence each other."
            display_text.insert(tk.END, Message)

    # Add a button to display the selected dataframe
    button = tk.Button(dataframe_window, text="Calculate the Assortativity", command=show_selected_dataframe)
    button.pack()

    # Add a text widget to display the dataframe
    display_text = tk.Text(dataframe_window, height=10, width=50)
    display_text.pack(fill=tk.BOTH, expand=True)
    ActDataFrame  = pd.DataFrame()
    
def button_Modularity():
    global df_selector
    global df_dictionary
    global ActDataFrame
    global Graphs_dict
    # Create a new window
    dataframe_window = tk.Toplevel(window)

     # Add a label to the window
    label = tk.Label(dataframe_window, text="Select a dataframe:")
    label.pack()

    # Add an option menu with the dataframe options
    var = tk.StringVar(dataframe_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(dataframe_window, var, *df_dictionary.keys())
    option_menu.pack()

    # Add a function to display the selected dataframe
    def show_selected_dataframe():
        selected_df = var.get()
        Modularity = GetModularity(Graphs_dict[selected_df])
        display_text.delete('1.0', tk.END)
        if Modularity == 0 :
            Message = f"A modularity score of {Modularity} indicates that the network has no significant community structure and is randomly connected. This can occur when there are no clear subgroups or communities in the network, or when the community structure is too weak to be detected by the modularity algorithm."
            display_text.insert(tk.END, Message)
        elif Modularity>0 and Modularity<0.5:
            Message = f"A modularity score of {Modularity} indicates a network with some degree of community structure, but the structure is not very strong or well-defined, and there is room for improvement in identifying clearer subgroups or communities within the network."
            display_text.insert(tk.END, Message)
        elif Modularity>=0.5 and Modularity<1:
            Message = f"A modularity score of {Modularity} indicates a network with a strong degree of community structure. This means that there are clear and well-defined subgroups or communities of nodes within the network that are more densely connected to each other than to the rest of the network."
            display_text.insert(tk.END, Message)
        elif Modularity == 1 :
            Message = f"A modularity score of {Modularity} indicates that the network is perfectly divided into separate communities with no connections between them. "
            display_text.insert(tk.END, Message)
        elif Modularity<0 and Modularity>=-0.5:
            Message = f"A modularity score of {Modularity} indicates a network that has less community structure than a random network."
            display_text.insert(tk.END, Message)
        elif Modularity<-0.5 and Modularity >-1:
            Message = f"A modularity score of {Modularity} indicates a network that has a structure that is significantly different from a random network, but the structure is not organized into communities. This means that there may be some patterns of connectivity in the network, but they do not form clear subgroups or communities of nodes."
            display_text.insert(tk.END, Message)
        elif Modularity == -1:
            Message = f"A modularity score of {Modularity} indicates a network where all nodes are more connected to each other than would be expected by chance, and there is no clear separation or division into subgroups or communities. This means that every node in the network is connected to every other node, creating a highly connected and densely packed network."
            display_text.insert(tk.END, Message)

    # Add a button to display the selected dataframe
    button = tk.Button(dataframe_window, text="Calculate Modularity", command=show_selected_dataframe)
    button.pack()

    # Add a text widget to display the dataframe
    display_text = tk.Text(dataframe_window, height=10, width=50)
    display_text.pack(fill=tk.BOTH, expand=True)
    ActDataFrame  = pd.DataFrame()

def button_Matrix():
    global df_selector
    global df_dictionary
    global ActDataFrame
    global Graphs_dict
    # Create a new window
    dataframe_window = tk.Toplevel(window)

     # Add a label to the window
    label = tk.Label(dataframe_window, text="Select a dataframe:")
    label.pack()

    # Add an option menu with the dataframe options
    var = tk.StringVar(dataframe_window)
    var.set('df1')  # Set the default value to df1
    option_menu = tk.OptionMenu(dataframe_window, var, *df_dictionary.keys())
    option_menu.pack()

    # Add a function to display the selected dataframe
    def show_selected_dataframe():
        selected_df = var.get()
        Matrix = GetMatrix(Graphs_dict[selected_df])
        display_text.delete('1.0', tk.END)
        display_text.insert(tk.END, Matrix)

    # Add a button to display the selected dataframe
    button = tk.Button(dataframe_window, text="Show Matrix", command=show_selected_dataframe)
    button.pack()

    # Add a text widget to display the dataframe
    display_text = tk.Text(dataframe_window, height=10, width=500)
    display_text.config(wrap=tk.NONE)
    display_text.pack(fill=tk.BOTH, expand=True)
    ActDataFrame  = pd.DataFrame()

# Define buttons
button_1 = tk.Button(window, text="1", padx=40, pady=20, command=lambda: button_click(1),highlightbackground="#333333", fg="black", bd=0)
button_2 = tk.Button(window, text="2", padx=40, pady=20, command=lambda: button_click(2),highlightbackground="#333333", fg="black", bd=0)
button_3 = tk.Button(window, text="3", padx=40, pady=20, command=lambda: button_click(3),highlightbackground="#333333", fg="black", bd=0)
button_4 = tk.Button(window, text="4", padx=40, pady=20, command=lambda: button_click(4),highlightbackground="#333333", fg="black", bd=0)
button_5 = tk.Button(window, text="5", padx=40, pady=20, command=lambda: button_click(5),highlightbackground="#333333", fg="black", bd=0)
button_6 = tk.Button(window, text="6", padx=40, pady=20, command=lambda: button_click(6),highlightbackground="#333333", fg="black", bd=0)
button_7 = tk.Button(window, text="7", padx=40, pady=20, command=lambda: button_click(7),highlightbackground="#333333", fg="black", bd=0)
button_8 = tk.Button(window, text="8", padx=40, pady=20, command=lambda: button_click(8),highlightbackground="#333333", fg="black", bd=0)
button_9 = tk.Button(window, text="9", padx=40, pady=20, command=lambda: button_click(9),highlightbackground="#333333", fg="black", bd=0)
button_0 = tk.Button(window, text="0", padx=40, pady=20, command=lambda: button_click(0),highlightbackground="#333333", fg="black", bd=0)
button_Assortativity = tk.Button(window, text="Assortativity", padx=39, pady=20, command=button_Assortativity,highlightbackground="orange", fg="black", bd=0, state='disabled')
button_Modularity = tk.Button(window, text="Modularity", padx=41, pady=20, command=button_Modularity,highlightbackground="orange", fg="black", bd=0, state='disabled')
button_Graph = tk.Button(window, text="Graph", padx=40, pady=20, command=button_Graph,highlightbackground="orange", fg="black", bd=0, state='disabled')
button_ShowPeopleDF= tk.Button(window, text="Show People DF", padx=41, pady=20, command=button_ShowPeopleDF,highlightbackground="orange", fg="black", bd=0, state='disabled')
button_clear = tk.Button(window, text="Clear", padx=41, pady=20, command=button_clear,highlightbackground="orange", fg="black", bd=0)
button_GenerateDF = tk.Button(window, text="GenerateDF", padx=41, pady=20, command=button_GenerateDF,highlightbackground="orange", fg="black", bd=0)
button_SelectAttributesAndGraph= tk.Button(window, text="SelectAttributes", padx=41, pady=20, command=button_SelectAttributesAndGraph,highlightbackground="orange", fg="black", bd=0, state='disabled')
button_Matrix = tk.Button(window, text="Show Matrix", padx=41, pady=20, command=button_Matrix,highlightbackground="orange", fg="black", bd=0, state='disabled')

# Add buttons to the window
button_1.grid(row=4, column=0)
button_2.grid(row=4, column=1)
button_3.grid(row=4, column=2)

button_4.grid(row=3, column=0)
button_5.grid(row=3, column=1)
button_6.grid(row=3, column=2)

button_7.grid(row=2, column=0)
button_8.grid(row=2, column=1)
button_9.grid(row=2, column=2)

button_0.grid(row=5, column=0)
button_clear.grid(row=1, column=0)
button_Assortativity.grid(row=3, column=3)
button_Modularity.grid(row=4, column=3)
button_Graph.grid(row=1, column=3)
button_ShowPeopleDF.grid(row=1, column=2)
button_GenerateDF.grid(row=1, column=1)
button_SelectAttributesAndGraph.grid(row=2, column=3)
button_Matrix.grid(row=5, column=2)


# Run the window
window.mainloop()
