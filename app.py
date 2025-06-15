from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_UP

app = Flask(__name__)

# Fungsi pembulatan ke 6 desimal sesuai aturan sekolah
def round_school_6(x):
    d = Decimal(str(x))
    sign = -1 if d < 0 else 1
    d = abs(d)

    # Ambil digit ke-7
    str_d = str(d.quantize(Decimal('0.0000000001')))  # 10 digit
    int_part, dec_part = str_d.split('.')
    seventh = int(dec_part[6]) if len(dec_part) > 6 else 0

    # Ganti logika di sini
    if seventh < 8:
        result = d.quantize(Decimal('0.000001'), rounding=ROUND_DOWN)
    else:
        result = d.quantize(Decimal('0.000001'), rounding=ROUND_UP)

    return float(result) * sign

# Fungsi f(x)
def f(x):
    return x**3 - 9*x**2 + 18*x - 6

# Implementasi Metode Secant dengan pembulatan khusus
def secant(x0, x1, e, N):
    output = []
    step = 0
    condition = True

    x_values = [x0, x1]
    f_values = [f(x0), f(x1)]

    while condition:
        if f(x0) == f(x1):
            output.append('Divide by zero error!\n')
            break

        f0 = round_school_6(f(x0))
        f1 = round_school_6(f(x1))

        try:
            x2 = x0 - (x1 - x0) * f0 / (f1 - f0)
        except ZeroDivisionError:
            output.append('Divide by zero error during iteration!\n')
            break

        x2 = round_school_6(x2)
        fx2 = round_school_6(f(x2))

        x_values.append(x2)
        f_values.append(fx2)

        print(f"Step {step}")
        print(f"  f(x1) asli       = {f(x1)}")
        print(f"  f(x1) round()    = {round(f(x1), 6)}")
        print(f"  f(x1) round_down = {round_school_6(f(x1))}")
        print(f"  f(x2) asli       = {f(x2)}")
        print(f"  f(x2) round()    = {round(f(x2), 6)}")
        print(f"  f(x2) round_down = {round_school_6(f(x2))}")

        output.append(
            'Iteration-%d, xₙ = %0.6f, f(xₙ) = %.6f, xₙ₊₁ = %.6f, f(xₙ₊₁) = %.6f\n' %
            (
                step,
                round_school_6(x1),
                round_school_6(f(x1)),
                x2,
                fx2
            )
        )

        x0 = x1
        x1 = x2
        step += 1

        if step > N:
            output.append('Not Convergent!\n')
            break

        condition = abs(f(x2)) > e

    output.append('Required root is: %0.8f\n' % x2)
    return x2, x_values, f_values, output

# Plot fungsi
def plot_function(func_name, f_value):
    plot_filename = f'function_plot_{func_name.replace(" ", "_").replace("^", "pow")}.png'
    plot_path = os.path.join('static', plot_filename)

    x = np.linspace(0, 6, 400)
    y = f(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f'f(x) = {func_name}', color='blue')
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    plt.title('Function Graph')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.ylim(-10, 10)
    plt.xlim(0, 6)
    plt.xticks(np.arange(0, 7, 1))
    plt.yticks(np.arange(-10, 11, 2))
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

            root, x_values, f_values, output = secant(x0, x1, e, N)
            plot_path = plot_function('x^3-9x^2+18x-6', f(root))

            return render_template('results.html', output=output, plot_path=plot_path)

        except ValueError:
            return render_template('index.html', error="Please enter valid numerical values.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)