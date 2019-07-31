import random
import math
from tkinter import *
from tkinter.filedialog import  *
import re
import copy
import time

root=Tk()

scale = 0
dots = []   # массив всех точек
firstgenerationsize = 300

def fromtxt():
    global dots
    global scale
    dots = []
    #   выделение из текстового файла регулярками координат
    a = list(float(x) for x in re.findall(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', open(askopenfilename(), "r").read()))
    i = 0
    scale = 0
    
    while i < len(a):
        temp = []
        temp.append(a[i])
        temp.append(a[i + 1])
        dots.append(temp)
        scale = max(scale, 320 // math.sqrt(temp[0]*temp[0]+temp[1]*temp[1]))
        i += 2
    for x in dots:    
        coords.insert(1.0, str(x) + '\n')
    scale = 320 // 9
    visualise()
def visualise(): 
    graph.delete("all")
    graph.create_line(550, 0, 550, 775,width=1,fill="black", arrow=FIRST)
    graph.create_line(0, 387, 1100, 387,width=1,fill="black", arrow=LAST)
    for x in dots:    
        x1 = int(x[0] * scale + 550)
        y1 = int(x[1] * scale * -1 + 387)
        x2 = x1 + 5
        y2 = y1 + 5
        if x == dots[0]:
            graph.create_rectangle(x1, y1, x2+5, y2+5, fill="blue")
        elif x == dots[-1]:
            graph.create_rectangle(x1, y1, x2+5, y2+5, fill="red")
        else:
            graph.create_rectangle(x1, y1, x2, y2, fill="green")
    

root.geometry('1205x900')
coords = Text(root, font = 12)
coords.place(x = 5, y = 5, width = 90, height = 890)


add = Button(root, text='Добавить\nкоординаты из .txt', font='12', command = fromtxt)
add.place(x = 100, y = 5, width = 180, height = 60)


desc = Label(root, font='12', text = 'Размер популяции:')
desc.place(x = 295, y = 8)
generationsize = 400
firstpop = Text(root, font='12',wrap = WORD)
firstpop.place(x = 295, y = 40, width = 220, height = 25)

desc = Label(root, font='12', text = 'Период стагнации:')
desc.place(x = 525, y = 8)
stag = Text(root, font='12',wrap = WORD)
stag.place(x = 525, y = 40, width = 220, height = 25)

desc = Label(root, font='12', text = 'Мутация %:')
desc.place(x = 755, y = 8)
mut = Text(root, font='12',wrap = WORD)
mut.place(x = 755, y = 40, width = 220, height = 25)

desc = Label(root, font='12', text = 'Метод скрещивания:')
desc.place(x = 985, y = 8)
var = 0
rbutton1 = Radiobutton(root, text='Одноточечное', variable = var, value=0, font='12', state = ACTIVE)
rbutton2 = Radiobutton(root, text='Двухточечное', variable = var, value=2, font='12', state = DISABLED)
rbutton3 = Radiobutton(root, text='Равномерное', variable = var, value=3, font='12', state = DISABLED)

rbutton2.place(x = 985, y = 62)
rbutton3.place(x = 985, y = 92)
rbutton1.place(x = 985, y = 32)


graph = Canvas(root, width=1100, height=774,bg="lightblue")
graph.place(x = 100, y = 120)
graph.create_line(550, 0, 550, 775,width=1,fill="black", arrow=FIRST)
graph.create_line(0, 387, 1100, 387,width=1,fill="black", arrow=LAST)







def selec():
    return random.choices(population, weights=list(1/x[len(dots)] for x in population))[0]

def normalize(name):
    for x in name:
        if name.count(x) > 1:
            index = name.index(x)
            i = 1
            while i < len(dots)-1:
                try:
                    name.index(dots[i])
                except:
                    name[index] = dots[i]
                    break
                i += 1
    return name


population = []




mutation = 0.05 # В процентах 

firstpop.insert(1.0, "220")
stag.insert(1.0, "15")
mut.insert(1.0, "0.4")


# forming 1st population
def start():
    visualise()
    generationsize = int(firstpop.get('1.0', END))
    stagnation = int(stag.get('1.0', END))
    mutation = float(mut.get('1.0', END))
    nofpop = 0
    global scale
    global population
    population = []
    
    for i in range(firstgenerationsize):
        a = [dots[0]]
        temp = random.sample(dots[1:len(dots)-1], len(dots)-2)
        for fasdf in range(len(dots)-2):
            a.append(temp[fasdf])
        a.append(dots[len(dots)-1])
        a.append(0)   
        population.append(a)

    #   рассчет качества
    for x in population:
        for i in range(len(x)-2):
            x2 = x[i+1][0]
            x1 = x[i][0]
            y2 = x[i+1][1]
            y1 = x[i][1]
            x[len(x)-1] += math.hypot(x2 - x1, y2 - y1)

    bestqalitylast = 100000000
    bestqualitycounter = 0
    bestofthebest = 0
    while bestqualitycounter < stagnation:
        newpopulation = []
        for i in range(generationsize // 2):
            mom = selec()
            dad = selec()
            
            div = random.randint(1, len(mom)-2)
            alisia = mom[0:div] + dad[div:len(dad)-1]
            gustav = dad[0:div] + mom[div:len(dad)-1]
            newpopulation.append(normalize(alisia))
            newpopulation.append(normalize(gustav))

        # mutation
        for x in newpopulation:
            if random.uniform(0, 100) <= mutation: 
                x[random.randint(1, len(x)-2)], x[random.randint(1, len(x)-2)] = x[random.randint(1, len(x)-2)], x[random.randint(1, len(x)-2)] 

        # quality 2nd gen
        for x in newpopulation:
            x.append(0)
            for i in range(len(x)-2):
                x2 = x[i+1][0]
                x1 = x[i][0]
                y2 = x[i+1][1]
                y1 = x[i][1]
                x[len(x)-1] += math.hypot(x2 - x1, y2 - y1)
        population = newpopulation
        qualityofpopulation = sum(x[len(dots)] for x in newpopulation)
        if qualityofpopulation < bestqalitylast:
            bestqualitycounter = 0
            bestqalitylast = qualityofpopulation
        else:
            bestqualitycounter += 1
        nofpop += 1
        
        for x in newpopulation:
            katoe = 0
            for i in range(len(newpopulation)):
                if newpopulation[katoe][-1] > newpopulation[katoe][-1]:
                    katoe = i
        bestofthebest = copy.deepcopy(newpopulation[i])
    

    

    for i in range(len(bestofthebest)-2):
        x1 = int(x[i][0] * scale + 550)
        y1 = int(x[i][1] * scale * -1 + 387)
        x2 = int(x[i+1][0] * scale + 550)
        y2 = int(x[i+1][1] * scale * -1 + 387)
        graph.create_line(x1, y1, x2, y2,width=2,fill="grey", arrow=LAST)
   
                      

strt = Button(root, text='Старт', font='Helvetica 14 bold', command = start)
strt.place(x = 100, y = 75, width = 180, height = 40)

root.mainloop()





















