# Genetic algorithm
              genetic algorithms, Python, tkinter, algorithms

Реализован генетический алгоритм для решения задачи коммивояжера - поиска кратчайшего пути из начальной в конечную точку, проходя через все промежуточные точки.

В файле координаты.txt задаются координаты x, y, где первая пара координат начальная точка, последняя - конечная.

Особь содержит одну хромосому, которая состоит из генов - точек, в порядке прохода (первая и последняя фиксированные).

Функция рассчета качаства особи определяет длину пути из начальной точки до конечной.

Скрещивание одноточечное, мутация - свап генов местами.
