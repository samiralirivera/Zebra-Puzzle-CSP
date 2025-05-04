from constraint import Problem, AllDifferentConstraint
from visualization import Visualization

def solve_zebra_puzzle():
    # Create the problem instance
    problem = Problem()
    
    # Define the variables and their domains
    houses = range(1, 6)  # 1 to 5
    
    # Nationalities
    nationalities = ['Englishman', 'Spaniard', 'Norwegian', 'Ukrainian', 'Japanese']
    problem.addVariables(nationalities, houses)
    
    # Colors
    colors = ['red', 'green', 'ivory', 'yellow', 'blue']
    problem.addVariables(colors, houses)
    
    # Candies
    candies = ['Hershey', 'Kit Kat', 'Smarties', 'Snickers', 'Milky Way']
    problem.addVariables(candies, houses)
    
    # Drinks
    drinks = ['water', 'orange juice', 'tea', 'coffee', 'milk']
    problem.addVariables(drinks, houses)
    
    # Pets
    pets = ['dog', 'fox', 'snails', 'horse', 'zebra']
    problem.addVariables(pets, houses)
    
    # Add all different constraints
    problem.addConstraint(AllDifferentConstraint(), nationalities)
    problem.addConstraint(AllDifferentConstraint(), colors)
    problem.addConstraint(AllDifferentConstraint(), candies)
    problem.addConstraint(AllDifferentConstraint(), drinks)
    problem.addConstraint(AllDifferentConstraint(), pets)
    
    # Add specific constraints
    # The Englishman lives in the red house
    problem.addConstraint(lambda e, r: e == r, ('Englishman', 'red'))
    
    # The Spaniard owns the dog
    problem.addConstraint(lambda s, d: s == d, ('Spaniard', 'dog'))
    
    # The Norwegian lives in the first house
    problem.addConstraint(lambda n: n == 1, ('Norwegian',))
    
    # The green house is immediately to the right of the ivory house
    problem.addConstraint(lambda g, i: g == i + 1, ('green', 'ivory'))
    
    # The man who eats Hershey bars lives in the house next to the man with the fox
    problem.addConstraint(lambda h, f: abs(h - f) == 1, ('Hershey', 'fox'))
    
    # Kit Kats are eaten in the yellow house
    problem.addConstraint(lambda k, y: k == y, ('Kit Kat', 'yellow'))
    
    # The Norwegian lives next to the blue house
    problem.addConstraint(lambda n, b: abs(n - b) == 1, ('Norwegian', 'blue'))
    
    # The Smarties eater owns snails
    problem.addConstraint(lambda s, sn: s == sn, ('Smarties', 'snails'))
    
    # The Snickers eater drinks orange juice
    problem.addConstraint(lambda s, o: s == o, ('Snickers', 'orange juice'))
    
    # The Ukrainian drinks tea
    problem.addConstraint(lambda u, t: u == t, ('Ukrainian', 'tea'))
    
    # The Japanese eats Milky Ways
    problem.addConstraint(lambda j, m: j == m, ('Japanese', 'Milky Way'))
    
    # Kit Kats are eaten in a house next to the house where the horse is kept
    problem.addConstraint(lambda k, h: abs(k - h) == 1, ('Kit Kat', 'horse'))
    
    # Coffee is drunk in the green house
    problem.addConstraint(lambda c, g: c == g, ('coffee', 'green'))
    
    # Milk is drunk in the middle house
    problem.addConstraint(lambda m: m == 3, ('milk',))
    
    # Get solutions
    solutions = problem.getSolutions()
    
    # Format and print the solution
    if solutions:
        solution = solutions[0]
        
        # Find where the zebra and water are
        zebra_house = solution['zebra']
        water_house = solution['water']
        
        print("\nSolution:")
        print("-" * 50)
        print(f"The zebra is in house {zebra_house}")
        print(f"Water is drunk in house {water_house}")
        print("-" * 50)
        
        # Print full solution
        print("\nFull solution:")
        print("House | Nationality | Color | Candy | Drink | Pet")
        print("-" * 50)
        
        # Prepare data for visualization
        solution_data = {
            'nationality': [],
            'color': [],
            'candy': [],
            'drink': [],
            'pet': []
        }
        
        for house in houses:
            nationality = next(k for k, v in solution.items() if v == house and k in nationalities)
            color = next(k for k, v in solution.items() if v == house and k in colors)
            candy = next(k for k, v in solution.items() if v == house and k in candies)
            drink = next(k for k, v in solution.items() if v == house and k in drinks)
            pet = next(k for k, v in solution.items() if v == house and k in pets)
            
            solution_data['nationality'].append(nationality)
            solution_data['color'].append(color)
            solution_data['candy'].append(candy)
            solution_data['drink'].append(drink)
            solution_data['pet'].append(pet)
            
            print(f"{house:5} | {nationality:11} | {color:5} | {candy:9} | {drink:13} | {pet:6}")
        
        # Create visualizations
        print("\nGenerating visualizations...")
        visualizer = Visualization()
        
        # Update statistics
        num_constraints = len(problem._constraints)
        num_variables = len(problem._variables)
        solutions_found = len(solutions)
        visualizer.update_stats(num_constraints, num_variables, solutions_found)
        
        # Create all visualizations
        visualizer.create_house_layout(solution_data)
        visualizer.create_constraint_graph()
        visualizer.create_solution_matrix(solution_data)
        visualizer.create_step_by_step(solution_data)
        visualizer.create_statistics()
        visualizer.create_summary(solution_data)
    else:
        print("No solution found")

if __name__ == "__main__":
    solve_zebra_puzzle()
