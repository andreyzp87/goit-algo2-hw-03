from collections import defaultdict, deque


class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        self.graph[v][u] = 0  # Зворотнє ребро

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)
        parent[source] = None

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u

        return sink in visited

    def edmonds_karp(self, source, sink):
        parent = {}
        max_flow = 0
        flows = defaultdict(lambda: defaultdict(int))

        while self.bfs(source, sink, parent):
            path_flow = float("inf")
            s = sink

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink

            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                flows[u][v] += path_flow
                v = parent[v]

        return max_flow, flows


def create_logistics_network():
    g = Graph()

    # Додаємо ребра від терміналів до складів
    terminal_to_warehouse = [
        ("T1", "W1", 25),
        ("T1", "W2", 20),
        ("T1", "W3", 15),
        ("T2", "W3", 15),
        ("T2", "W4", 30),
        ("T2", "W2", 10)
    ]

    # Додаємо ребра від складів до магазинів
    warehouse_to_store = [
        ("W1", "S1", 15),
        ("W1", "S2", 10),
        ("W1", "S3", 20),
        ("W2", "S4", 15),
        ("W2", "S5", 10),
        ("W2", "S6", 25),
        ("W3", "S7", 20),
        ("W3", "S8", 15),
        ("W3", "S9", 10),
        ("W4", "S10", 20),
        ("W4", "S11", 10),
        ("W4", "S12", 15),
        ("W4", "S13", 5),
        ("W4", "S14", 10)
    ]

    # Додаємо всі ребра до графа
    for u, v, c in terminal_to_warehouse + warehouse_to_store:
        g.add_edge(u, v, c)

    return g

def analyze_results(flows):
    # Аналіз потоків від терміналів до магазинів
    terminal_to_store_flows = defaultdict(lambda: defaultdict(int))

    for u in flows:
        if not u.startswith('T'):
            continue
        for v in flows[u]:
            if not v.startswith('W'):
                continue
            warehouse = v
            for store in flows[warehouse]:
                if not store.startswith('S'):
                    continue
                flow = min(flows[u][warehouse], flows[warehouse][store])
                terminal_to_store_flows[u][store] += flow

    return terminal_to_store_flows


def print_results(terminal_to_store_flows):
    print("\nТаблиця результатів потоків:")
    print("Термінал | Магазин | Фактичний потік")
    print("-" * 40)

    for terminal in sorted(terminal_to_store_flows):
        for store in sorted(terminal_to_store_flows[terminal]):
            flow = terminal_to_store_flows[terminal][store]
            print(f"{terminal:8} | {store:7} | {flow:14}")


def main():
    # Створюємо мережу
    g = create_logistics_network()

    # Додаємо супер-джерело та супер-стік
    source = "SOURCE"
    sink = "SINK"

    # З'єднуємо супер-джерело з терміналами
    g.add_edge(source, "T1", float("inf"))
    g.add_edge(source, "T2", float("inf"))

    # З'єднуємо магазини з супер-стоком
    for i in range(1, 15):
        g.add_edge(f"S{i}", sink, float("inf"))

    # Запускаємо алгоритм Едмондса-Карпа
    max_flow, flows = g.edmonds_karp(source, sink)

    # Аналізуємо результати
    terminal_to_store_flows = analyze_results(flows)

    # Виводимо результати
    print(f"\nМаксимальний потік: {max_flow}")
    print_results(terminal_to_store_flows)

    return max_flow, terminal_to_store_flows


if __name__ == "__main__":
    main()

    print('''
    Відповіді на запитання:
1. Найбільший потік забезпечує Термінал 1, оскільки він має більшу сумарну пропускну здатність до складів (60 одиниць проти 55 у Термінала 2).

2, 3 До магазинів S3, S9, S12, S13, S14 взагалі нічого не доходить (або буде мало доходити при пропорційному розподілі)
Все через обмежене постачання на склади W1 та W4, що мають тільки по одному терміналу для поповнення товарів

4. Вузькі місця системи:
- Обмежена пропускна здатність до складів W1 та W4
- Велике навантаження на склад W4

Рекомендації для оптимізації:
- Збільшити пропускну здатність між терміналами та складами W1 та W4
- Оптимізувати розподіл потоків між складами для більш рівномірного навантаження
    ''')