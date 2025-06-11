import numpy as np
import matplotlib.pyplot as plt

# Defining Function
def f(x):
    return x**3 - 9*x**2 + 18*x - 6

# Implementing Secant Method
def secant(x0, x1, e, N):
    print('\n\n*** SECANT METHOD IMPLEMENTATION ***')
    step = 1
    condition = True
    
    # Menyimpan nilai x dan f(x) untuk setiap iterasi
    x_values = [x0, x1]
    f_values = [f(x0), f(x1)]
    
    while condition:
        if f(x0) == f(x1):
            print('Divide by zero error!')
            break
        
        x2 = x0 - (x1 - x0) * f(x0) / (f(x1) - f(x0)) 
        x_values.append(x2)
        f_values.append(f(x2))
        
        print('Iteration-%d, x1 = %0.6f, f(x1) = %0.6f, x2 = %0.6f, f(x2) = %0.6f' % (step, x1, f(x1), x2, f(x2)))
        
        x0 = x1
        x1 = x2
        step += 1
        
        if step > N:
            print('Not Convergent!')
            break
        
        condition = abs(f(x2)) > e
    
    print('\nRequired root is: %0.8f' % x2)
    return x2, x_values, f_values  # Mengembalikan akar yang ditemukan dan nilai x dan f(x)

# Function to plot the function
def plot_function():
    x = np.linspace(0, 10, 400)  # Rentang x untuk grafik
    y = f(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='f(x) = x^3 - 9x^2 + 18x - 6', color='blue')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.title('Grafik Fungsi')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.legend()
    plt.show()

# Input Section
x0 = float(input('Enter First Guess: '))
x1 = float(input('Enter Second Guess: '))
e = float(input('Tolerable Error: '))
N = int(input('Maximum Step: '))

# Starting Secant Method
root, x_values, f_values = secant(x0, x1, e, N)

# Print all x and f(x) values
print("\nAll x values and their corresponding f(x) values:")
for i in range(len(x_values)):
    print(f"x{i} = {x_values[i]:.6f}, f(x{i}) = {f_values[i]:.6f}")

# Plot the function
plot_function()
