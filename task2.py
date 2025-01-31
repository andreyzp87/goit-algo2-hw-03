import csv
from BTrees.OOBTree import OOBTree
import timeit
from typing import Dict, Any


class ItemStorage:
    def __init__(self):
        self.tree = OOBTree()
        self.tree_key = OOBTree()
        self.dict = {}

    def add_item_to_tree(self, id, item):
        self.tree.update({id: item})
        self.tree_key.update({(item['Price'], id): item})

    def add_item_to_dict(self, id, item):
        self.dict[id] = item

    def range_query_tree(self, min_price, max_price):
        result = []
        for _, item in self.tree.items():
            if min_price <= item['Price'] < max_price:
                result.append(item)
        return result

    def range_query_key_tree(self, min_price, max_price):
        return list(self.tree_key.items((min_price,), (max_price,)))

    def range_query_dict(self, min_price, max_price):
        return [item for item in self.dict.values() if min_price <= item['Price'] < max_price]


def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            data.append({
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            })
        return data



if __name__ == "__main__":
    data = load_data('generated_items_data.csv')
    storage = ItemStorage()

    for item in data:
        storage.add_item_to_tree(item['ID'], item)
        storage.add_item_to_dict(item['ID'], item)

    min_price = 100.0
    max_price = 200.0
    num_iterations = 100

    tree_time = timeit.timeit(
        lambda: storage.range_query_tree(min_price, max_price),
        number=num_iterations
    )
    tree_items = storage.range_query_tree(min_price, max_price)

    key_tree_time = timeit.timeit(
        lambda: storage.range_query_key_tree(min_price, max_price),
        number=num_iterations
    )
    key_tree_items = storage.range_query_key_tree(min_price, max_price)

    dict_time = timeit.timeit(
        lambda: storage.range_query_dict(min_price, max_price),
        number=num_iterations
    )
    dict_items = storage.range_query_dict(min_price, max_price)

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds, found {len(tree_items)} items")
    print(f"Total range_query time for OOBTree (Price as key): {key_tree_time:.6f} seconds, found {len(key_tree_items)} items")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds, found {len(dict_items)} items")