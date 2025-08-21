import json
import random
class Item():
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Items():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Items,cls).__new__(cls)
            print("new instance created")
        else:
            print("instance exsits")    
        return cls.instance
    def __init__(self):
        self.item_list:list
        item_dict:dict
        with open(r"module\items.json","r") as reader:
            item_dict = json.load(reader)
        for _, sub_dict in enumerate(item_dict):
            for key, value in enumerate(sub_dict):
                self.item_list.append(Item(name=key,description=value))
    
    def get_n_items(self,n:int):
        sub_items:list
        for i in range(n):
            sub_items.append(self.item_list[random.randint(0,len(self.item_list))])
        return sub_items