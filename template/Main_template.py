import tkinter as tk

from tkinter import simpledialog
import tkinter.ttk as ttk
class myWindow:
    def __init__(self, root, color):
        self.root = root
        self.color = color
        # Создаем два главных фрейма
        self.left_frame = ttk.Frame(self.root, height=250, width=500)
        self.right_frame = ttk.Frame(self.root, height=250, width=500)

        self.left_frame.pack(side='left',fill="both", expand=False)
        self.right_frame.pack(side='right',fill="both", expand=True)

        # Задаем пропорции растяжения для колонок grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Задаем обработчик изменения размера окна
        self.root.bind("<Configure>", self.on_resize)


        # Создаем два фрейма в левом фрейме
        self.top_left_frame = ttk.LabelFrame(self.left_frame, text='Input area', height=125, width=250)
        self.middle_left_frame = ttk.LabelFrame(self.left_frame, text='Table area',  height=125, width=250)
        self.bottom_left_frame = ttk.LabelFrame(self.left_frame, text='Result area',  height=125, width=250)
        self.top_left_frame.pack(side="top", fill="both", expand=False)
        self.middle_left_frame.pack(side="top", fill="both", expand=False)
        self.bottom_left_frame.pack(side="bottom", fill="both", expand=False)

        # Создаем два фрейма в правом фрейме
        self.top_right_frame = ttk.LabelFrame(self.right_frame, text='Canvas area',  height=125, width=500)
        self.top_right_frame.pack(side="top", fill="both", expand=True)


    def on_resize(self, event):
        # Получаем текущую ширину окна
        width = self.root.winfo_width()

        # Вычисляем новую ширину левого и правого фреймов
        left_width = int(width / 3)
        right_width = width - left_width

        # Изменяем ширину колонок grid
        self.root.columnconfigure(0, minsize=left_width)
        self.root.columnconfigure(1, minsize=right_width)
class Button:
    def __init__(self, root,text,command,arg):
        self.arg = arg
        self.command = command
        self.root = root
        self.text = text
        button = ttk.Button(self.root, text=self.text, command=lambda: self.command(self.arg))
        button.pack()


class labeledSpinbox():
    def __init__(self, root,label_text, spinbox_from, spinbox_to, spinbox_default,spinbox_step):
        self.root = root
        self.label_text = label_text
        self.spinbox_from = spinbox_from
        self.spinbox_to = spinbox_to
        self.spinbox_default = spinbox_default
        self.spinbox_step = spinbox_step
        # Создаем виджет Label
        self.widget_frame = ttk.Frame(self.root)
        self.widget_frame.pack(side=tk.TOP)
        self.label = ttk.Label(self.widget_frame, text=self.label_text,font=("Arial", 10))
        self.label.pack(side=tk.LEFT)
        # Создаем виджет Spinbox
        self.spinbox = ttk.Spinbox(self.widget_frame, from_=self.spinbox_from, to=self.spinbox_to, increment=self.spinbox_step,font=("Arial", 10))
        self.spinbox.delete(0, tk.END)  # удаляем стандартное значение
        self.spinbox.insert(0, spinbox_default)  # устанавливаем стандартное значение
        self.spinbox.pack(side=tk.LEFT)
    def get(self):
        return self.spinbox.get()



class canvas:
    def __init__(self, root,table,result):
        self.root = root
        self.table = table
        self.result = result
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack(fill="both", expand=True)
        self.circle_count = 0
        self.circle_mass = []
        self.edges_mass = []
        self.best_way = []
        self.best_weight=0
        self.counter = 0
        # Привязываем функцию рисования к событию нажатия мыши
        self.canvas.bind("<Button-1>", self.draw_circle)
        self.canvas.bind("<Button-3>", self.circle_delete)
        self.canvas.bind("<Button-2>", self.show_data)


    # Функция, которая рисует круг на холсте
    def show_data(self,event):
        print(self.edges_mass)
        print(self.circle_mass)
    def draw_circle(self, event):
        self.best_edges_delete()
        self.all_edges_hidden(False)
        x, y = event.x, event.y
        r = 20
        overlapping_circles = self.canvas.find_enclosed(x - r-25, y - r-25, x + r+25, y + r+25)  # поиск перекрывающихся кругов
        if not overlapping_circles:  # если нет пересечений
            self.circle_mass.append([self.circle_count,[int(x),int(y)]])
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='red',tags='oval')
            self.canvas.create_text(x, y, text=str(self.circle_count), font=('Arial', 12, 'bold'),tags='text')
            self.edges_mass = self.table.check_data(self.edges_mass)

            self.draw_edges(self.circle_count)
            self.circle_count += 1
            self.table.update_data(self.edges_mass)
        self.canvas.tag_raise('oval')
        self.canvas.tag_raise('text')


    def draw_edges(self, id):
        l = len(self.circle_mass)
        for i in range(l-1):
            x1, y1 = self.circle_mass[l-1][1]
            x2, y2 = self.circle_mass[i][1]
            id1 = self.circle_mass[l-1][0]
            id2 = self.circle_mass[i][0]
            self.canvas.create_line(x1, y1, x2, y2, width=1, fill="black",tags='lines')
            weight = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            self.edges_mass.append([id1,id2,int(weight)])

    def circle_delete(self, event):
        self.edges_mass = self.table.check_data(self.edges_mass)
        x = event.x
        y = event.y
        r = 20
        objects = self.canvas.find_overlapping(x-r,y-r,x+r,y+r)
        for obj in objects:
            if self.canvas.type(obj) == 'oval':
                coords = self.canvas.coords(obj)
                circle_x = (coords[0] + coords[2]) // 2
                circle_y = (coords[1] + coords[3]) // 2
                for oval in self.circle_mass:
                    if oval[1][0] == circle_x and oval[1][1] == circle_y:
                        self.delId = oval[0]
                        self.circle_mass.remove(oval)
                        self.edges_delete()
            self.canvas.delete(obj)
        self.table.update_data(self.edges_mass)
    def edges_delete(self):
        l = len(self.edges_mass)
        self.edges_mass = [inner_lst for inner_lst in self.edges_mass if self.delId not in inner_lst]

    def all_edges_hidden(self,Bool):
        items = self.canvas.find_withtag("lines")
        for item in items:
            if Bool:
                self.canvas.itemconfig(item, state='hidden')
            else:
                self.canvas.itemconfig(item, state='normal')
    def best_edges_delete(self):
        items = self.canvas.find_withtag("bestlines")
        for item in items:
          self.canvas.delete(item)

    def draw_best_way(self):
        self.result.update_data_res(self.best_way,self.best_weight,self.counter)
        coordinates = []
        for i in self.best_way:
            for j in self.circle_mass:
                if j[0] == i:
                    coordinates.append(j[1])
        coordinates.append(coordinates[0])
        for i in range(len(coordinates)-1):
            self.canvas.create_line(coordinates[i][0], coordinates[i][1], coordinates[i+1][0], coordinates[i+1][1], width=2, fill="red",tags='bestlines')
        self.canvas.tag_raise('text')
    def clear_canvas(self,bool):
        self.canvas.delete("all")
        self.edges_mass = []
        self.circle_mass = []
        self.best_way = []
        self.best_weight = 0
        self.circle_count=0
        self.counter = 0
        self.table.update_data(self.edges_mass)
        self.result.update_data_res(self.best_way,self.best_weight,self.counter)

class myTable:
    def __init__(self,root,headers):
        self.root = root
        self.headers = headers
        self.changed_mass = []
        self.changed_val = []
        self.table = ttk.Treeview(self.root, columns=self.headers, show='headings')
        for header in self.headers:
            self.table.heading(header, text=header.title())
        for col in self.table["columns"]:
            self.table.column(col, width=100)
        self.table.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.table.bind("<Double-1>", self.update_cell)

    def update_data(self,mass):
        self.table.delete(*self.table.get_children())
        for row in mass:
            self.table.insert("", "end", values=row)
    def check_data(self,list1):
        if len(self.changed_mass):
            for i in range(len(list1)):
                if list1[i] in self.changed_mass:
                    list1[i][2] = self.changed_val.pop(0)
            self.changed_mass = []
            self.changed_val = []
        return list1
    def update_cell(self,event):
        # Получаем ссылку на таблицу и на выбранную строку
        self.table = event.widget
        self.item = self.table.selection()[0]
        # Получаем индекс выбранной колонки и имя выбранного столбца
        self.column = self.table.identify_column(event.x)
        self.column_name = self.table.heading(self.column)['text']
        # Получаем старое значение ячейки и запрашиваем у пользователя новое значение
        self.old_value = self.table.set(self.item, self.column)
        self.id1 = self.table.set(self.item, '#1')
        self.id2 = self.table.set(self.item, '#2')

        self.new_value = simpledialog.askstring('Изменение значения', f'Введите новое значение для {self.column_name}:',initialvalue=self.old_value)

        # Обновляем значение ячейки, если пользователь ввёл новое значение
        if self.new_value:
            self.changed_mass.append([int(self.id1),int(self.id2),int(self.old_value)])
            self.changed_val.append(int(self.new_value))
            self.table.set(self.item, self.column, self.new_value)
class myResult:
    def __init__(self,root):
        self.root = root
        self.visited = []
        self.best_weight = 0
        self.counter = 0
        self.text = tk.Text(self.root,width=40)
        self.text.delete("1.0", 'end')
        self.text.insert(1.0, f"Путь: {self.visited}\n")
        self.text.insert(2.0, f"Общий вес пути: {self.best_weight}\n")
        self.text.insert(3.0, f"Количество поколений: {self.counter}\n")
        self.text.pack()
    def update_data_res(self,vis,wg,counter):
        self.visited = vis
        self.best_weight = wg
        self.counter = counter
        self.text.delete("1.0", 'end')
        self.text.insert(1.0,f"Путь: {self.visited}\n")
        self.text.insert(2.0, f"Общий вес пути: {self.best_weight}\n")

        if self.counter:
            self.text.insert(2.0, f"Количество поколений: {self.counter}\n")








