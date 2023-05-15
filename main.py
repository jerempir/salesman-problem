import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import  messagebox
from template import Main_template
from alg import annealing_alg,neighbor_alg, annealing_algF, ant_alg
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
def on_closing():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"): root.destroy()

root = tk.Tk()
root.geometry("1000x500")
root.protocol("WM_DELETE_WINDOW", on_closing)
style = ThemedStyle(root)
style.set_theme("adapta") #scidgrey
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)



# Создаем две вкладки в нотбуке
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
notebook.add(tab1, text='Алгоритм ближайшего соседа')
notebook.add(tab2, text='Алгоритм отжига')
notebook.add(tab3, text='Муравьиный алгоритм')

neighbor_window = Main_template.myWindow(tab1,'#cad7e8') #''#9BB7D4')
neighbor_table = Main_template.myTable(neighbor_window.middle_left_frame,['Вершина 1', 'Вершина 2', 'Вес'])
neighbor_result = Main_template.myResult(neighbor_window.bottom_left_frame)
neighbor_canvas = Main_template.canvas(neighbor_window.top_right_frame,neighbor_table,neighbor_result)
neighbor_startButton = Main_template.Button(neighbor_window.top_left_frame,'Начать алгоритм', neighbor_alg.nearest_neighbor, neighbor_canvas)
neighbor_clearButton = Main_template.Button(neighbor_window.top_left_frame,'Стереть данные',neighbor_canvas.clear_canvas,True)

annealing_window = Main_template.myWindow(tab2,'#d7e8d5')
annealing_table = Main_template.myTable(annealing_window.middle_left_frame,['Вершина 1', 'Вершина 2', 'Вес'])
annealing_result = Main_template.myResult(annealing_window.bottom_left_frame)
annealing_canvas = Main_template.canvas(annealing_window.top_right_frame,annealing_table,annealing_result)
annealing_stemp = Main_template.labeledSpinbox(annealing_window.top_left_frame,"Начальная температура",10,1000,1000,10)
annealing_fTemp = Main_template.labeledSpinbox(annealing_window.top_left_frame,"Конечная температура",0,1000,1e-8,1)
annealing_coolVal = Main_template.labeledSpinbox(annealing_window.top_left_frame,"Коэффициент охлаждения",0,1,0.003,0.001)
annealing_startButton = Main_template.Button(annealing_window.top_left_frame,'Начать алгоритм',annealing_alg.solve_tsp_with_simulated_annealing,[annealing_canvas,annealing_stemp,annealing_fTemp,annealing_coolVal])
annealing_clearButton = Main_template.Button(annealing_window.top_left_frame,'Стереть данные',annealing_canvas.clear_canvas,True)

ant_window = Main_template.myWindow(tab3,'#e8caca')
ant_table = Main_template.myTable(ant_window.middle_left_frame,['Вершина 1', 'Вершина 2', 'Вес'])
ant_result = Main_template.myResult(ant_window.bottom_left_frame)
ant_canvas = Main_template.canvas(ant_window.top_right_frame,ant_table,ant_result)
ant_value = Main_template.labeledSpinbox(ant_window.top_left_frame,'Количество муравьев',1,1000,10,5)
ant_iter = Main_template.labeledSpinbox(ant_window.top_left_frame,'Количество поколений',1,1000,45,5)
ant_alpha = Main_template.labeledSpinbox(ant_window.top_left_frame,'Альфа значение',1,10,1,1)
ant_beta = Main_template.labeledSpinbox(ant_window.top_left_frame,'Бета значение',1,10,5,1)
ant_decay = Main_template.labeledSpinbox(ant_window.top_left_frame,'Скорость распада феромона',0,10,0.1,0.1)
ant_pherconst = Main_template.labeledSpinbox(ant_window.top_left_frame,'Мощность феромона',0,10,2,1)
ant_startButton = Main_template.Button(ant_window.top_left_frame,'Начать алгоритм',ant_alg.ant_alg,[ant_canvas,ant_value,ant_iter,ant_decay,ant_alpha,ant_beta,ant_pherconst])
ant_clearButton = Main_template.Button(ant_window.top_left_frame,'Стереть данные',ant_canvas.clear_canvas,True)
root.mainloop()