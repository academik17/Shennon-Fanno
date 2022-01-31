import sys
import os  
import binascii
import math
from tkinter import filedialog
from tkinter import *  
import os  
from tkinter import scrolledtext
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import urllib.request



def listtostr(a):
    s = ''
    for i in range(len(a)):
        s = s+str(a[i])
    return s
def coder(b, n):
    global max_i
    max_i = 0
    # Редактирование длины
    while len(b) % n != 0:
        b = b + '0'
    # Задание алфавита
    alph = [0]*(2**n)
    for i in range(2**n):
        alph[i] = str(bin(i))[2:]
        while len(alph[i]) < n:
            alph[i] = '0' + alph[i]
    # Задание матрицы частот(вероятностей)
    p = [0]*(2**n) 
    for i in range(2**n):
        for j in range(int(len(b)/n - 1)):
            if alph[i] == b[j*n:(j+1)*n]:
                p[i] += 1
    for i in range(2**n):
        p[i] = p[i]/(len(b)/n)
    # Удаление из алфавита невстречающихся элементов
    #print(len(p), len(alph))
    #print(len(b))
    k = 0
    index = []
    for i in range(len(p)):
        if p[i] == 0:
            k += 1
            index.append(i)
    for i in range(k):
        alph.pop(index[k-1-i])
        p.pop(index[k-1-i])
    # Удаление нулевых вероятностей
    '''for i in range(k):
        p.remove(0.0)'''
    # формирование массива
    b_mass = []
    for i in range(int(len(b)/n - 1)):
        b_mass.append(b[i*n:n*(i+1)])


    # Ранжирование
    for i in range(len(p)-1):
        max = p[i]
        for j in range(i,len(p)):
            if max < p[j]:
                max = p[j]
                max_i = j
        c = p[max_i]
        p[max_i] = p[i]
        p[i] = c
        d = alph[max_i]
        alph[max_i] = alph[i]
        alph[i] = d
    
    result = [alph, p, b_mass]
    return result



class Unit:
    '''
    Класс, представляет собой объект содержаний поля name, value, code
    :param name: имя объекта
    :param value: значение вероятности
    :param code: код объекта
    '''
    def __init__(self, name, value, code):
        self.name = name
        self.value = value
        self.code = code



#алгоритм Шеннона-Фано
def make_ShannonFano(probability):
    '''
    Функция, реализаующая алгоритм Шеннона-Фано
    :param probability: список объектов
    :param return: возвращает тот же список, но с присвоенными кодами
    '''
    summ = 0
    for i in probability:
        summ += i.value # получили сумму вероятностей
    
    group= summ/2   
    index = 0
    
    group1 = []
    group2 = []

    for i in probability:
        if index < group: 
            i.code += '0'
            group1.append(i)
            index += i.value
        else:
            i.code += '1'
            group2.append(i)    

    # рекурсия
    if len(group1) != 1:
        make_ShannonFano(group1)
    if len(group2) != 1:
        make_ShannonFano(group2)

    return probability


def main(b,n):
    cod = coder(b,n)
    probability = [] # Список кодируемых обЪектов
    alph = cod[0] # Алфавит
    p = cod[1] # Вероятности
    b_mass = cod[2] # Список кодируемых сиволов
    s_mass = [] # Список закодированных символов
    s = '' # Закодированное сообщение
    l_mean = 0 # средняя длина слова
    # Энтропия
    entropy = 0
    for i in range(len(p)):
        entropy += -p[i]*math.log2(p[i])

    # Кодирование
    for i in range(len(alph)):
        probability.append(Unit(alph[i], p[i], ''))
    result = make_ShannonFano(probability)

    # Вычисление средней длины
    for i in range(len(alph)):
        l_mean += p[i]*len(result[i].code)

    # Получене закодированного списка
    for i in range(len(b_mass)):
        for j in range(len(alph)):
            if b_mass[i] == alph[j]:
                s_mass.append(result[j].code)
                continue
    
    # Получене закодированного сообщения
    for i in range(len(s_mass)):
        s = s + s_mass[i] + ' '
    
    #effect = (n/l_mean)
    # Результат работы
    result_main = [result, s_mass, s, l_mean, b_mass, alph, entropy]
    return result_main

def decoder(s_mass, alph, code_a):
    decode = []
    for i in range(len(s_mass)):
        for j in range(len(alph)):
            if s_mass[i] == code_a[j]:
                decode.append(alph[j])
                continue
    return decode

limit = sys.getrecursionlimit()
sys.setrecursionlimit(3000)

def btn():
    x = ""
    global k
    global WayOpenFile
    global masNbits
    global data
    size = 4096
    bytesInfile = b''
    ftypes = [('Все файлы','*')]
    fOpen = filedialog.askopenfile(filetypes = ftypes)
    WayOpenFile = fOpen.name
    with open(WayOpenFile, 'rb') as f:
        for chunk in iter(lambda: f.read(32), b''):
            x += str(binascii.hexlify(chunk)).replace("b","").replace("'","")
    bits = bin(int(x,16))[2:]#.replace('0b','')

    n = 3
    r = main(bits,n)
    code_a = []
    for i in range(len(r[5])):
        code_a.append(r[0][i].code)
    Filecode = open('C:/Users/magom/Desktop/start_code.txt','w+')
    Filecode.write(listtostr(r[1]))
    Filecode.close()
    os.startfile('C:/Users/magom/Desktop/start_code.txt')
    Filecode = open('C:/Users/magom/Desktop/Shenon-Fano_code.txt','w+')
    Filecode.write(listtostr(r[4]))
    Filecode.close()
    os.startfile('C:/Users/magom/Desktop/Shenon-Fano_code.txt')
    txt1.delete(1.0, END)
    txt1.insert(INSERT, r[6]) 
    txt2.delete(1.0, END)
    txt2.insert(INSERT, n) 
    txt3.delete(1.0, END)
    txt3.insert(INSERT, r[3]) 

def btn2():
    img = Image.frombuffer('RGB', (320,240), hex('0b'+ s)) 
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",14)
    draw = ImageDraw.Draw(img)
    img.save("decode.jpg")   

window = Tk()  
window.title("Кодирование Шеннона-Фано")  
window.geometry('400x250')  
btn1 = Button(window, text="Выбрать файл и закодировать", command=btn)  
btn1.grid(column=1, row=0)  
lbl1 = Label(window, text="Энтропия: ")  
lbl1.grid(column=0, row=1)  
txt1 = scrolledtext.ScrolledText(window, width=19, height=1)  
txt1.grid(column=1, row=1)
lbl2 = Label(window, text="Средняя длина до: ")  
lbl2.grid(column=0, row=2)  
txt2 = scrolledtext.ScrolledText(window, width=19, height=1)  
txt2.grid(column=1, row=2)
lbl3 = Label(window, text="Средняя длина после: ")  
lbl3.grid(column=0, row=3)  
txt3 = scrolledtext.ScrolledText(window, width=19, height=1)  
txt3.grid(column=1, row=3)
btn2 = Button(window, text="Декодировать", command=btn2)  
btn2.grid(column=1, row=4) 
window.mainloop()