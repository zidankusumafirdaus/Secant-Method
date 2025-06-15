from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Difining the function
def f(x):
    return x**3 - 9*x**2 + 18*x - 6

# Implementation The Secant Method
def secant(x0, x1, e, N):
    output = []
    step = 0
    condition = True
    
    # x and f(x) values for each iteration
    x_values = [x0, x1]
    f_values = [f(x0), f(x1)]
    
    while condition:
        # If the first and second guesses are the same
        if f(x0) == f(x1):
            output.append('Divide by zero error!\n')
            break
        
        x2 = x0 - (x1 - x0) * f(x0) / (f(x1) - f(x0)) 
        x_values.append(x2)
        f_values.append(f(x2))
        
        output.append('Iteration-%d, x1 = %0.6f, f(x1) = %0.6f, x2 = %0.6f, f(x2) = %0.6f\n' % (step, x1, f(x1), x2, f(x2)))
        
        x0 = x1
        x1 = x2
        step += 1
        
        # If the Step > Maximum Steps
        if step > N:
            output.append('Not Convergent!\n')
            break
        
        condition = abs(f(x2)) > e
    output.append('Required root is: %0.8f\n' % x2)
    return x2, x_values, f_values, output

# Function to plot the function graph
def plot_function(func_name, f_value):
    # Create a filename
    plot_filename = f'function_plot_{func_name.replace(" ", "_").replace("^", "pow")}.png'
    plot_path = os.path.join('static', plot_filename)
    
    # Adjust the range for visualization
    x = np.linspace(0, 6, 400)
    y = f(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f'f(x) = {func_name}', color='blue')
    
    # Draw x and y axes
    plt.axhline(0, color='black', lw=1)  # Horizontal line for x-axis
    plt.axvline(0, color='black', lw=1)  # Vertical line for y-axis
    
    # Set title and labels
    plt.title('Function Graph')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    
    # Set limits for y-axis
    plt.ylim(-10, 10)  # Set y-limits for better visibility
    plt.xlim(0, 6)  # Set x-limits for better visibility
    
    # Customize ticks
    plt.xticks(np.arange(0, 7, 1))  # Set x-ticks from 0 to 6
    plt.yticks(np.arange(-10, 11, 2))  # Set y-ticks from -10 to 10
    
    plt.grid()
    plt.legend()
    
    plt.savefig(plot_path)
    plt.close()
    return plot_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            x0 = float(request.form['x0'])
            x1 = float(request.form['x1'])
            e = float(request.form['e'])
            N = int(request.form['N'])
            
            # Starting Secant Method
            root, x_values, f_values, output = secant(x0, x1, e, N)

            # Generate the plot with the function name and the last f(x) value
            plot_path = plot_function('x^3-9x^2+18x-6', f(root))

            return render_template('results.html', output=output, plot_path=plot_path)
        
        except ValueError:
            return render_template('index.html', error="Please enter valid numerical values.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
