class MyClass:
    def __init__(self, data: dict[str,list]):
        # 遍历字典并将键值对转为私有属性
        for key, value in data.items():
            # 使用双下划线将键转换为私有属性
            # setattr(self, f"_{self.__class__.__name__}__{key}", value)
            key = key.lower()
            setattr(self, f"_{key}", value)

    def __repr__(self):
        # 打印类的私有属性（仅作为展示）
        return str(self.__dict__)
    
    def test(self):
        print(self._a)
        print(self._b)

# 示例字典
a = {"a": [1, 2, 3], "b": [4, 5, 6]}

# 创建对象并传入字典
obj = MyClass(a)
obj.test()
# # 访问私有属性（可以通过名称访问）
# print(obj._MyClass__a)  # 输出 [1, 2, 3]
# print(obj._MyClass__b)  # 输出 [4, 5, 6]

# 打印对象的字典形式，展示所有属性
print(obj)
