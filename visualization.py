import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
import time

class Visualization:
    def __init__(self):
        self.start_time = time.time()
        self.stats = {
            'num_constraints': 0,
            'num_variables': 0,
            'solutions_found': 0,
            'execution_time': 0
        }

    def update_stats(self, num_constraints, num_variables, solutions_found):
        self.stats['num_constraints'] = num_constraints
        self.stats['num_variables'] = num_variables
        self.stats['solutions_found'] = solutions_found
        self.stats['execution_time'] = time.time() - self.start_time

    def create_house_layout(self, solution):
        """Create a visual layout of the houses and their attributes."""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Create house positions
        house_positions = {
            1: (1, 0),
            2: (2, 0),
            3: (3, 0),
            4: (4, 0),
            5: (5, 0)
        }
        
        # Create custom colormap for houses
        colors = ['red', 'green', 'ivory', 'yellow', 'blue']
        
        # Draw houses
        for house_num in range(1, 6):
            x, y = house_positions[house_num]
            house_color = solution['color'][house_num-1]
            
            # Draw house
            rect = Rectangle((x-0.4, y-0.4), 0.8, 0.8, 
                            edgecolor='black', facecolor=house_color, alpha=0.7)
            ax.add_patch(rect)
            
            # Add house number
            ax.text(x, y+0.4, f'House {house_num}', ha='center', va='center', 
                    fontsize=12, fontweight='bold')
            
            # Add attributes
            attributes = [
                ("Nationality", solution['nationality'][house_num-1]),
                ("Color", solution['color'][house_num-1]),
                ("Candy", solution['candy'][house_num-1]),
                ("Drink", solution['drink'][house_num-1]),
                ("Pet", solution['pet'][house_num-1])
            ]
            
            for i, (attr, value) in enumerate(attributes):
                ax.text(x, y-0.2-i*0.2, f"{attr}: {value}", ha='center', va='center',
                        fontsize=10)
        
        ax.set_xlim(0, 6)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        plt.title('Zebra Puzzle Solution Layout')
        plt.show()

    def create_constraint_graph(self):
        """Create a graph showing the relationships between constraints."""
        G = nx.DiGraph()
        
        # Add nodes
        nodes = {
            'nationalities': ['Englishman', 'Spaniard', 'Norwegian', 'Ukrainian', 'Japanese'],
            'colors': ['red', 'green', 'ivory', 'yellow', 'blue'],
            'candies': ['Hershey', 'Kit Kat', 'Smarties', 'Snickers', 'Milky Way'],
            'drinks': ['water', 'orange juice', 'tea', 'coffee', 'milk'],
            'pets': ['dog', 'fox', 'snails', 'horse', 'zebra']
        }
        
        # Add nodes to graph
        for category in nodes:
            for item in nodes[category]:
                G.add_node(item)
        
        # Add edges based on constraints
        constraints = [
            ('Englishman', 'red'),  # The Englishman lives in the red house
            ('Spaniard', 'dog'),   # The Spaniard owns the dog
            ('Norwegian', 'first'),  # The Norwegian lives in the first house
            ('green', 'ivory'),    # The green house is immediately to the right of the ivory house
            ('Hershey', 'fox'),    # The man who eats Hershey bars lives in the house next to the man with the fox
            ('Kit Kat', 'yellow'),  # Kit Kats are eaten in the yellow house
            ('Norwegian', 'blue'),  # The Norwegian lives next to the blue house
            ('Smarties', 'snails'),  # The Smarties eater owns snails
            ('Snickers', 'orange juice'),  # The Snickers eater drinks orange juice
            ('Ukrainian', 'tea'),  # The Ukrainian drinks tea
            ('Japanese', 'Milky Way'),  # The Japanese eats Milky Ways
            ('Kit Kat', 'horse'),  # Kit Kats are eaten in a house next to the house where the horse is kept
            ('coffee', 'green'),   # Coffee is drunk in the green house
            ('milk', 'middle')     # Milk is drunk in the middle house
        ]
        
        # Add edges to graph
        for edge in constraints:
            G.add_edge(edge[0], edge[1])
        
        # Draw graph
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        
        # Draw nodes with different colors for each category
        colors = {
            'nationalities': 'lightblue',
            'colors': 'lightgreen',
            'candies': 'lightyellow',
            'drinks': 'lightpink',
            'pets': 'lightgray'
        }
        
        for category in nodes:
            nx.draw_networkx_nodes(G, pos, 
                                 nodelist=nodes[category],
                                 node_color=colors[category],
                                 node_size=2000)
        
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Constraint Relationships')
        plt.axis('off')
        plt.show()

    def create_solution_matrix(self, solution):
        """Create a matrix showing the final solution."""
        categories = ['Nationality', 'Color', 'Candy', 'Drink', 'Pet']
        houses = range(1, 6)
        
        # Create matrix
        matrix = np.zeros((5, 5), dtype=object)
        
        for i, house in enumerate(houses):
            matrix[0, i] = solution['nationality'][i]
            matrix[1, i] = solution['color'][i]
            matrix[2, i] = solution['candy'][i]
            matrix[3, i] = solution['drink'][i]
            matrix[4, i] = solution['pet'][i]
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create table data
        table_data = []
        # Add empty header row
        table_data.append([''] + ['House 1', 'House 2', 'House 3', 'House 4', 'House 5'])
        
        # Add category names as first column
        for i, category in enumerate(categories):
            row_data = [category] + [str(item) for item in matrix[i]]
            table_data.append(row_data)
        
        # Create table
        table = ax.table(cellText=table_data, loc='center', cellLoc='center')
        
        # Adjust table properties
        for (row, col), cell in table.get_celld().items():
            if row == 0 or col == 0:  # Header row or first column
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#40465e')
            else:
                if row % 2 == 0:
                    cell.set_facecolor('#f1f1f1')
                else:
                    cell.set_facecolor('w')
        
        # Add color coding for each category
        category_colors = {
            'Nationality': '#e3f2fd',
            'Color': '#e8f5e9',
            'Candy': '#fff3e0',
            'Drink': '#fce4ec',
            'Pet': '#f3f3f3'
        }
        
        # Apply colors to cells
        for i, category in enumerate(categories):
            for j in range(1, 6):
                table[(i+1, j)].set_facecolor(category_colors[category])
        
        # Hide axes
        ax.axis('off')
        
        plt.title('Zebra Puzzle Solution Matrix')
        plt.show()

    def create_step_by_step(self, solution):
        """Create a step-by-step visualization of the solution process."""
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Create timeline
        timeline = [
            "1. Initialize problem with 5 houses",
            "2. Add variables and domains",
            "3. Add AllDifferent constraints",
            "4. Add specific constraints",
            "5. Solve problem",
            "6. Find solution"
        ]
        
        # Create timeline visualization
        for i, step in enumerate(timeline):
            ax.text(0.1, 0.9 - i*0.1, f"{i+1}. {step}",
                    fontsize=12, transform=ax.transAxes)
        
        # Add solution highlight
        ax.text(0.1, 0.3, "Solution Found!",
                fontsize=14, fontweight='bold', color='green',
                transform=ax.transAxes)
        
        ax.axis('off')
        plt.title('Solution Process Timeline')
        plt.show()

    def create_statistics(self):
        """Create a statistics visualization."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create statistics data
        stats_data = [
            ("Number of Constraints", self.stats['num_constraints']),
            ("Number of Variables", self.stats['num_variables']),
            ("Solutions Found", self.stats['solutions_found']),
            ("Execution Time (s)", f"{self.stats['execution_time']:.2f}")
        ]
        
        # Create table
        table_data = [[f"{key}", f"{value}"] for key, value in stats_data]
        table = ax.table(cellText=table_data, loc='center', cellLoc='center')
        
        # Adjust table properties
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#40465e')
            else:
                cell.set_facecolor('#f1f1f1')
        
        ax.axis('off')
        plt.title('Solution Statistics')
        plt.show()

    def create_summary(self, solution):
        """Create a summary visualization highlighting key relationships."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Find key relationships
        zebra_house = solution['pet'].index('zebra') + 1
        water_house = solution['drink'].index('water') + 1
        
        # Create summary points
        summary_points = [
            f"The zebra is in house {zebra_house}",
            f"Water is drunk in house {water_house}",
            "Key relationships:",
            "- The Englishman lives in the red house",
            "- The Spaniard owns the dog",
            "- The Norwegian lives in the first house"
        ]
        
        # Create summary visualization
        for i, point in enumerate(summary_points):
            if i == 0:
                ax.text(0.1, 0.9 - i*0.1, point,
                        fontsize=14, fontweight='bold',
                        transform=ax.transAxes)
            else:
                ax.text(0.1, 0.9 - i*0.1, point,
                        fontsize=12,
                        transform=ax.transAxes)
        
        ax.axis('off')
        plt.title('Solution Summary')
        plt.show()

def create_house_layout(solution):
    """Create a visual layout of the houses and their attributes."""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Create house positions
    house_positions = {
        1: (1, 0),
        2: (2, 0),
        3: (3, 0),
        4: (4, 0),
        5: (5, 0)
    }
    
    # Create custom colormap for houses
    colors = ['red', 'green', 'ivory', 'yellow', 'blue']
    
    # Draw houses
    for house_num in range(1, 6):
        x, y = house_positions[house_num]
        house_color = solution['color'][house_num-1]
        
        # Draw house
        rect = Rectangle((x-0.4, y-0.4), 0.8, 0.8, 
                        edgecolor='black', facecolor=house_color, alpha=0.7)
        ax.add_patch(rect)
        
        # Add house number
        ax.text(x, y+0.4, f'House {house_num}', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        
        # Add attributes
        attributes = [
            ("Nationality", solution['nationality'][house_num-1]),
            ("Color", solution['color'][house_num-1]),
            ("Candy", solution['candy'][house_num-1]),
            ("Drink", solution['drink'][house_num-1]),
            ("Pet", solution['pet'][house_num-1])
        ]
        
        for i, (attr, value) in enumerate(attributes):
            ax.text(x, y-0.2-i*0.2, f"{attr}: {value}", ha='center', va='center',
                    fontsize=10)
    
    ax.set_xlim(0, 6)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    plt.title('Zebra Puzzle Solution Layout')
    plt.show()

def create_constraint_graph():
    """Create a graph showing the relationships between constraints."""
    G = nx.DiGraph()
    
    # Add nodes
    nodes = {
        'nationalities': ['Englishman', 'Spaniard', 'Norwegian', 'Ukrainian', 'Japanese'],
        'colors': ['red', 'green', 'ivory', 'yellow', 'blue'],
        'candies': ['Hershey', 'Kit Kat', 'Smarties', 'Snickers', 'Milky Way'],
        'drinks': ['water', 'orange juice', 'tea', 'coffee', 'milk'],
        'pets': ['dog', 'fox', 'snails', 'horse', 'zebra']
    }
    
    # Add nodes to graph
    for category in nodes:
        for item in nodes[category]:
            G.add_node(item)
    
    # Add edges based on constraints
    constraints = [
        ('Englishman', 'red'),  # The Englishman lives in the red house
        ('Spaniard', 'dog'),   # The Spaniard owns the dog
        ('Norwegian', 'first'),  # The Norwegian lives in the first house
        ('green', 'ivory'),    # The green house is immediately to the right of the ivory house
        ('Hershey', 'fox'),    # The man who eats Hershey bars lives in the house next to the man with the fox
        ('Kit Kat', 'yellow'),  # Kit Kats are eaten in the yellow house
        ('Norwegian', 'blue'),  # The Norwegian lives next to the blue house
        ('Smarties', 'snails'),  # The Smarties eater owns snails
        ('Snickers', 'orange juice'),  # The Snickers eater drinks orange juice
        ('Ukrainian', 'tea'),  # The Ukrainian drinks tea
        ('Japanese', 'Milky Way'),  # The Japanese eats Milky Ways
        ('Kit Kat', 'horse'),  # Kit Kats are eaten in a house next to the house where the horse is kept
        ('coffee', 'green'),   # Coffee is drunk in the green house
        ('milk', 'middle')     # Milk is drunk in the middle house
    ]
    
    # Add edges to graph
    for edge in constraints:
        G.add_edge(edge[0], edge[1])
    
    # Draw graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    # Draw nodes with different colors for each category
    colors = {
        'nationalities': 'lightblue',
        'colors': 'lightgreen',
        'candies': 'lightyellow',
        'drinks': 'lightpink',
        'pets': 'lightgray'
    }
    
    for category in nodes:
        nx.draw_networkx_nodes(G, pos, 
                             nodelist=nodes[category],
                             node_color=colors[category],
                             node_size=2000)
    
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title('Constraint Relationships')
    plt.axis('off')
    plt.show()

def create_solution_matrix(solution):
    """Create a matrix showing the final solution."""
    categories = ['Nationality', 'Color', 'Candy', 'Drink', 'Pet']
    houses = range(1, 6)
    
    # Create matrix
    matrix = np.zeros((5, 5), dtype=object)
    
    for i, house in enumerate(houses):
        matrix[0, i] = solution['nationality'][i]
        matrix[1, i] = solution['color'][i]
        matrix[2, i] = solution['candy'][i]
        matrix[3, i] = solution['drink'][i]
        matrix[4, i] = solution['pet'][i]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create table data
    table_data = []
    # Add empty header row
    table_data.append([''] + ['House 1', 'House 2', 'House 3', 'House 4', 'House 5'])
    
    # Add category names as first column
    for i, category in enumerate(categories):
        row_data = [category] + [str(item) for item in matrix[i]]
        table_data.append(row_data)
    
    # Create table
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    
    # Adjust table properties
    for (row, col), cell in table.get_celld().items():
        if row == 0 or col == 0:  # Header row or first column
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor('#40465e')
        else:
            if row % 2 == 0:
                cell.set_facecolor('#f1f1f1')
            else:
                cell.set_facecolor('w')
    
    # Add color coding for each category
    category_colors = {
        'Nationality': '#e3f2fd',
        'Color': '#e8f5e9',
        'Candy': '#fff3e0',
        'Drink': '#fce4ec',
        'Pet': '#f3f3f3'
    }
    
    # Apply colors to cells
    for i, category in enumerate(categories):
        for j in range(1, 6):
            table[(i+1, j)].set_facecolor(category_colors[category])
    
    # Hide axes
    ax.axis('off')
    
    plt.title('Zebra Puzzle Solution Matrix')
    plt.show()

# Update requirements.txt
with open('requirements.txt', 'a') as f:
    f.write('matplotlib==3.7.1\nnetworkx==3.1\nnumpy==1.24.3\n')
