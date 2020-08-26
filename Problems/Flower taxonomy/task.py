iris = {}


def add_iris(id_n, species, petal_length, petal_width, **kwargs):
    iris[id_n] = {'species': species, 'petal_length': petal_length, 'petal_width': petal_width}
    print(iris)
    
    #new_feature = {}
    for key, value in kwargs:
        print(key)
        print(value)
        iris[id_n][key] = value
    #     new_feature = {key: value}
    #     print(new_feature)
    # iris[id_n].update(new_feature)
    
    return iris

answer = add_iris(0, 'Iris versicolor', 4.0, 1.3, petal_hue='pale lilac')
print(answer)
