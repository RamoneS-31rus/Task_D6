from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value): # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргуменит — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
    with open('news/templatetags/bad_words.txt', 'r', encoding='UTF8') as file:
        file = file.readlines()[0].split()
    if isinstance(value, str):
        for word in file:
            value = value.replace(word,'*****')
        return str(value)
    else:
        raise ValueError(f'Нельзя применять метод censor не к строке')