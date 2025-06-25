# Import libraries
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Handles creating a Pie chart based on the sentiment information
def pieChart(pos: int, neg: int, nu: int, container):
    for widget in container.winfo_children():
        widget.destroy()

    labels = ['Positive:\n {}'.format(pos), 'Negative:\n {}'.format(neg), 'Neutral:\n {}'.format(nu)]
    data = [pos, neg, nu]
    explode = [0.2 if x == max(data) else 0.0 for x in data]

    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(data, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
    ax.legend(wedges, labels, title="Sentiment", loc="upper left", bbox_to_anchor=(1, 1))

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Handles creating a Bar chart based on the sentiment information
def barChart(pos: int, neg: int, nu: int, container):
    for widget in container.winfo_children():
        widget.destroy()

    labels = ['Positive', 'Negative', 'Neutral']
    data = [pos, neg, nu]
    colors = ['green', 'red', 'gray']

    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    bars = ax.bar(labels, data, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')

    ax.set_ylabel('Count')
    ax.set_title('Sentiment Breakdown')

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Handles creating a Spider chart based on the sentiment information
def spiderChart(pos, neg, neu, parent_frame):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [pos, neg, neu]
    values += values[:1]  # to close the loop

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.fill(angles, values, color='skyblue', alpha=0.4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    for widget in parent_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Handles creating a PolarBar chart based on the sentiment information
def polarBarChart(pos, neg, neu, parent_frame):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [pos, neg, neu]
    theta = np.linspace(0.0, 2 * np.pi, len(values), endpoint=False)

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
    bars = ax.bar(theta, values, width=0.6, bottom=0.0, color=['green', 'red', 'gray'], alpha=0.6)

    ax.set_xticks(theta)
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    for widget in parent_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Handles creating a Doughnut chart based on the sentiment information
def doughnutChart(pos, neg, neu, parent_frame):
    values = [pos, neg, neu]
    labels = ['Positive', 'Negative', 'Neutral']
    colors = ['green', 'red', 'gray']

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')

    for widget in parent_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()




def total(pos:int, neg:int, nu:int):
    print(pos + neg + nu)