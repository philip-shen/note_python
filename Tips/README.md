#

[朝飯前に学べる！便利なPythonのヒント100選【前編】updated at 2021-10-25](https://qiita.com/baby-degu/items/05cf809d4d992923020d#24-%E3%82%B9%E3%83%86%E3%83%83%E3%83%97%E9%96%A2%E6%95%B0%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E6%96%87%E5%AD%97%E5%88%97%E3%82%92%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9%E3%81%99%E3%82%8B)

# 8. Enumを使用して、同じ概念の関連項目を列挙する  
[8. Enumを使用して、同じ概念の関連項目を列挙する](https://qiita.com/baby-degu/items/05cf809d4d992923020d#8-enum%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E5%90%8C%E3%81%98%E6%A6%82%E5%BF%B5%E3%81%AE%E9%96%A2%E9%80%A3%E9%A0%85%E7%9B%AE%E3%82%92%E5%88%97%E6%8C%99%E3%81%99%E3%82%8B)

```
from enum import Enum
class Status(Enum):
    NO_STATUS = -1
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2
print(Status.IN_PROGRESS.name) # IN_PROGRESS
print(Status.COMPLETED.value) # 2
```

# 11. 辞書を読み取り可能な1行にマージする  
[11. 辞書を読み取り可能な1行にマージする](https://qiita.com/baby-degu/items/05cf809d4d992923020d#11-%E8%BE%9E%E6%9B%B8%E3%82%92%E8%AA%AD%E3%81%BF%E5%8F%96%E3%82%8A%E5%8F%AF%E8%83%BD%E3%81%AA1%E8%A1%8C%E3%81%AB%E3%83%9E%E3%83%BC%E3%82%B8%E3%81%99%E3%82%8B)

これは、Python 3.9から利用可能です。

```
first_dictionary = {'name': 'Fatos', 'location': 'Munich'}
second_dictionary = {'name': 'Fatos', 'surname': 'Morina', 'location': 'Bavaria, Munich'}
result = first_dictionary | second_dictionary
print(result)
# {'name': 'Fatos', 'location': 'Bavaria, Munich', 'surname': 'Morina'}
```

# 12. タプルの要素のインデックスを取得する  
[12. タプルの要素のインデックスを取得する](https://qiita.com/baby-degu/items/05cf809d4d992923020d#12-%E3%82%BF%E3%83%97%E3%83%AB%E3%81%AE%E8%A6%81%E7%B4%A0%E3%81%AE%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B)

```
books = ('Atomic habits', 'Ego is the enemy', 'Outliers', 'Mastery')
print(books.index('Mastery')) # 3
```

# 17. カスタム区切りを挿入した複数の値を出力する 
[17. カスタム区切りを挿入した複数の値を出力する](https://qiita.com/baby-degu/items/05cf809d4d992923020d#17-%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%A0%E5%8C%BA%E5%88%87%E3%82%8A%E3%82%92%E6%8C%BF%E5%85%A5%E3%81%97%E3%81%9F%E8%A4%87%E6%95%B0%E3%81%AE%E5%80%A4%E3%82%92%E5%87%BA%E5%8A%9B%E3%81%99%E3%82%8B)

```
print("29", "01", "2022", sep="/") # 29/01/2022
print("name", "domain.com", sep="@") # name@domain.com
```

# 18. 変数名の先頭に数字を使用できない  
[18. 変数名の先頭に数字を使用できない](https://qiita.com/baby-degu/items/05cf809d4d992923020d#18-%E5%A4%89%E6%95%B0%E5%90%8D%E3%81%AE%E5%85%88%E9%A0%AD%E3%81%AB%E6%95%B0%E5%AD%97%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84)

```
four_letters = "abcd" # this works
4_letters = "abcd" # this doesn't work
```

# 19. 変数名の先頭に演算子を使用できない  
[19. 変数名の先頭に演算子を使用できない](https://qiita.com/baby-degu/items/05cf809d4d992923020d#19-%E5%A4%89%E6%95%B0%E5%90%8D%E3%81%AE%E5%85%88%E9%A0%AD%E3%81%AB%E6%BC%94%E7%AE%97%E5%AD%90%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84)
```
+variable = "abcd" # this doesn't work
```

# 20. 数値の最初の桁に0を使用できない  
[20. 数値の最初の桁に0を使用できない](https://qiita.com/baby-degu/items/05cf809d4d992923020d#20-%E6%95%B0%E5%80%A4%E3%81%AE%E6%9C%80%E5%88%9D%E3%81%AE%E6%A1%81%E3%81%AB0%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84)
```
number = 0110 # this doesn't work
```

# 21. 変数名のどこにでもアンダースコアを使用できる  
[21. 変数名のどこにでもアンダースコアを使用できる](https://qiita.com/baby-degu/items/05cf809d4d992923020d#21-%E5%A4%89%E6%95%B0%E5%90%8D%E3%81%AE%E3%81%A9%E3%81%93%E3%81%AB%E3%81%A7%E3%82%82%E3%82%A2%E3%83%B3%E3%83%80%E3%83%BC%E3%82%B9%E3%82%B3%E3%82%A2%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%A7%E3%81%8D%E3%82%8B)

変数名のどこにでも、何回でも、使えるということです。
```
a______b = "abcd" # this works
_a_b_c_d = "abcd" # this also works
```

# 23. リストの順序を反転する 
[23. リストの順序を反転する](https://qiita.com/baby-degu/items/05cf809d4d992923020d#23-%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E9%A0%86%E5%BA%8F%E3%82%92%E5%8F%8D%E8%BB%A2%E3%81%99%E3%82%8B)
```
my_list = ['a', 'b', 'c', 'd']
my_list.reverse()
print(my_list) # ['d', 'c', 'b', 'a']
```

# 24. ステップ関数を使用して、文字列をスライスする  
[24. ステップ関数を使用して、文字列をスライスする](https://qiita.com/baby-degu/items/05cf809d4d992923020d#24-%E3%82%B9%E3%83%86%E3%83%83%E3%83%97%E9%96%A2%E6%95%B0%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E6%96%87%E5%AD%97%E5%88%97%E3%82%92%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9%E3%81%99%E3%82%8B)
```
my_string = "This is just a sentence"
print(my_string[0:5]) # This

# Take three steps forward
print(my_string[0:10:3]) # Tssu
```

# 25. スライスを反転する  
[25. スライスを反転する](https://qiita.com/baby-degu/items/05cf809d4d992923020d#25-%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9%E3%82%92%E5%8F%8D%E8%BB%A2%E3%81%99%E3%82%8B)
```
my_string = "This is just a sentence"
print(my_string[10:0:-1]) # suj si sih

# Take two steps forward
print(my_string[10:0:-2]) # sjs i
```

# 26. 開始または終了インデックスだけを使用して、部分スライスする  
[26. 開始または終了インデックスだけを使用して、部分スライスする](https://qiita.com/baby-degu/items/05cf809d4d992923020d#26-%E9%96%8B%E5%A7%8B%E3%81%BE%E3%81%9F%E3%81%AF%E7%B5%82%E4%BA%86%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E3%81%A0%E3%81%91%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E9%83%A8%E5%88%86%E3%82%B9%E3%83%A9%E3%82%A4%E3%82%B9%E3%81%99%E3%82%8B)
```
my_string = "This is just a sentence"
print(my_string[4:]) # is just a sentence
print(my_string[:3]) # Thi
```

# 27. フロア分割  
[27. フロア分割](https://qiita.com/baby-degu/items/05cf809d4d992923020d#27-%E3%83%95%E3%83%AD%E3%82%A2%E5%88%86%E5%89%B2)
```
print(3/2) # 1.5
print(3//2) # 1
```

# 28. 「==」と「is」の違い  
[28. 「==」と「is」の違い](https://qiita.com/baby-degu/items/05cf809d4d992923020d#28-%E3%81%A8is%E3%81%AE%E9%81%95%E3%81%84)
```
「is」は、2つの変数がメモリ内の同じオブジェクトを指しているか調べます。

「==」は、2つのオブジェクトが保持する値の同一性を比較します。
```

```
first_list = [1, 2, 3]
second_list = [1, 2, 3]

# Is their actual value the same?
print(first_list == second_list) # True

# Are they pointing to the same object in memory
print(first_list is second_list)
# False, since they have same values, but in different objects in
memory

third_list = first_list
print(third_list is first_list)
# True, since both point to the same object in memory
```

# 37. if-elifブロックは、最後にelseブロックがなくてもよい  
[37. if-elifブロックは、最後にelseブロックがなくてもよい](https://qiita.com/baby-degu/items/05cf809d4d992923020d#37-if-elif%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E3%81%AF%E6%9C%80%E5%BE%8C%E3%81%ABelse%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E3%81%8C%E3%81%AA%E3%81%8F%E3%81%A6%E3%82%82%E3%82%88%E3%81%84)

ただし、elifはその前にifステップが必要です。

```
def check_number(number):
if number > 0:
return "Positive"
elif number == 0:
return "Zero"
return "Negative"
print(check_number(1)) # Positive
```

# 38. sorted()を使用して、2つの文字列がアナグラムか調べる  
[38. sorted()を使用して、2つの文字列がアナグラムか調べる](https://qiita.com/baby-degu/items/05cf809d4d992923020d#38-sorted%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A62%E3%81%A4%E3%81%AE%E6%96%87%E5%AD%97%E5%88%97%E3%81%8C%E3%82%A2%E3%83%8A%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%8B%E8%AA%BF%E3%81%B9%E3%82%8B)

```
def check_if_anagram(first_word, second_word):
first_word = first_word.lower()
second_word = second_word.lower()
return sorted(first_word) == sorted(second_word)

print(check_if_anagram("testinG", "Testing")) # True
print(check_if_anagram("Here", "Rehe")) # True
print(check_if_anagram("Know", "Now")) # False
```

# 42. 辞書のキーと値を入れ替える  
[42. 辞書のキーと値を入れ替える](https://qiita.com/baby-degu/items/05cf809d4d992923020d#42-%E8%BE%9E%E6%9B%B8%E3%81%AE%E3%82%AD%E3%83%BC%E3%81%A8%E5%80%A4%E3%82%92%E5%85%A5%E3%82%8C%E6%9B%BF%E3%81%88%E3%82%8B)  
```
dictionary = {"a": 1, "b": 2, "c": 3}
reversed_dictionary = {j: i for i, j in dictionary.items()}
print(reversed_dictionary) # {1: 'a', 2: 'b', 3: 'c'}
```

# 47. リストの先頭に値を追加する  
```
append()を使用して、右から新しい値を挿入します。
```

```
insert()を使用して、新しい要素を挿入するインデックスと要素を指定できます。この場合は、先頭に挿入するため、インデックスは0を使用します。
```

```
my_list = [3, 4, 5]
my_list.append(6)
my_list.insert(0, 2)
print(my_list) # [2, 3, 4, 5, 6]
```

# 48. lambda関数は1行でしか記述できない 
[48. lambda関数は1行でしか記述できない]()
```
comparison = lambda x: if x > 3:
    print("x > 3")
else:
    print("x is not greater than 3")
```

次のエラーが発生します。

```
result = lambda x: if x > 3:
^
SyntaxError: invalid synta
```

# 49. lambdaの条件文にはelse部が必須である
[49. lambdaの条件文にはelse部が必須である](https://qiita.com/baby-degu/items/05cf809d4d992923020d#49-lambda%E3%81%AE%E6%9D%A1%E4%BB%B6%E6%96%87%E3%81%AB%E3%81%AFelse%E9%83%A8%E3%81%8C%E5%BF%85%E9%A0%88%E3%81%A7%E3%81%82%E3%82%8B)

```
comparison = lambda x: "x > 3" if x > 3
```
次のエラーが発生します。
```
comparison = lambda x: "x > 3" if x > 3
^
SyntaxError: invalid syntax
```
なお、これは条件式の機能であり、lambda 自体の機能ではありません。


[朝飯前に学べる！便利なPythonのヒント100選【後編】updated at 2021-10-25](https://qiita.com/baby-degu/items/532bea7be058c35f61a8)  


# 50. filter()は新しいオブジェクトを返す 
[50. filter()は新しいオブジェクトを返す](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#50-filter%E3%81%AF%E6%96%B0%E3%81%97%E3%81%84%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%82%92%E8%BF%94%E3%81%99)

```
my_list = [1, 2, 3, 4]
odd = filter(lambda x: x % 2 == 1, my_list)
print(list(odd)) # [1, 3]
print(my_list) # [1, 2, 3, 4]
```

# 51. map()は新しいオブジェクトを返す 
[51. map()は新しいオブジェクトを返す](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#51-map%E3%81%AF%E6%96%B0%E3%81%97%E3%81%84%E3%82%AA%E3%83%96%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%82%92%E8%BF%94%E3%81%99)

```
my_list = [1, 2, 3, 4]
squared = map(lambda x: x ** 2, my_list)
print(list(squared)) # [1, 4, 9, 16]
print(my_list) # [1, 2, 3, 4]
```

# 52. range()にはあまり知られていないステップパラメータがある  
[52. range()にはあまり知られていないステップパラメータがある](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#52-range%E3%81%AB%E3%81%AF%E3%81%82%E3%81%BE%E3%82%8A%E7%9F%A5%E3%82%89%E3%82%8C%E3%81%A6%E3%81%84%E3%81%AA%E3%81%84%E3%82%B9%E3%83%86%E3%83%83%E3%83%97%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%81%8C%E3%81%82%E3%82%8B) 

```
for number in range(1, 10, 3):
print(number, end=" ")
# 1 4 7
```

# 58. パラメータを何個でも指定して呼び出せるメソッドを定義する  
[58. パラメータを何個でも指定して呼び出せるメソッドを定義する](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#58-%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%82%92%E4%BD%95%E5%80%8B%E3%81%A7%E3%82%82%E6%8C%87%E5%AE%9A%E3%81%97%E3%81%A6%E5%91%BC%E3%81%B3%E5%87%BA%E3%81%9B%E3%82%8B%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89%E3%82%92%E5%AE%9A%E7%BE%A9%E3%81%99%E3%82%8B)

```
def get_sum(*arguments):
    result = 0
    for i in arguments:
        result += i
    return result

print(get_sum(1, 2, 3)) # 6
print(get_sum(1, 2, 3, 4, 5)) # 15
print(get_sum(1, 2, 3, 4, 5, 6, 7)) # 28
```

# 59. super()または親クラス名を使用して、親クラスのイニシャライザを呼び出す  
[59. super()または親クラス名を使用して、親クラスのイニシャライザを呼び出す](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#59-super%E3%81%BE%E3%81%9F%E3%81%AF%E8%A6%AA%E3%82%AF%E3%83%A9%E3%82%B9%E5%90%8D%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E8%A6%AA%E3%82%AF%E3%83%A9%E3%82%B9%E3%81%AE%E3%82%A4%E3%83%8B%E3%82%B7%E3%83%A3%E3%83%A9%E3%82%A4%E3%82%B6%E3%82%92%E5%91%BC%E3%81%B3%E5%87%BA%E3%81%99)

super()を使用して、親クラスのイニシャライザを呼び出すことができます。
```
class Parent:
    def __init__(self, city, address):
        self.city = city
        self.address = address
class Child(Parent):
    def __init__(self, city, address, university):
        super().__init__(city, address)
        self.university = university

child = Child('Zürich', 'Rämistrasse 101', 'ETH Zürich')
print(child.university) # ETH Zürich
```

親クラス名を使用して、親クラスを呼び出します。
```
class Parent:
    def __init__(self, city, address):
        self.city = city
        self.address = address
class Child(Parent):
    def __init__(self, city, address, university):
        Parent.__init__(self, city, address)
        self.university = university

child = Child('Zürich', 'Rämistrasse 101', 'ETH Zürich')
print(child.university) # ETH Zürich
```
なお、__init__()やsuper()を使用した親のイニシャライザの呼び出しは、子クラスのイニシャライザ内部だけで使用できます。


# 63. 文字列の文字の大文字と小文字を入れ替える 
[63. 文字列の文字の大文字と小文字を入れ替える](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#63-%E6%96%87%E5%AD%97%E5%88%97%E3%81%AE%E6%96%87%E5%AD%97%E3%81%AE%E5%A4%A7%E6%96%87%E5%AD%97%E3%81%A8%E5%B0%8F%E6%96%87%E5%AD%97%E3%82%92%E5%85%A5%E3%82%8C%E6%9B%BF%E3%81%88%E3%82%8B)

```
string = "This is just a sentence."
result = string.swapcase()
print(result) # tHIS IS JUST A SENTENCE.
```

# 72. タプルにリストとタプルをネストする 
[72. タプルにリストとタプルをネストする](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#72-%E3%82%BF%E3%83%97%E3%83%AB%E3%81%AB%E3%83%AA%E3%82%B9%E3%83%88%E3%81%A8%E3%82%BF%E3%83%97%E3%83%AB%E3%82%92%E3%83%8D%E3%82%B9%E3%83%88%E3%81%99%E3%82%8B)

```
mixed_tuple = (("a"*10, 3, 4), ['first', 'second', 'third'])
print(mixed_tuple[1]) # ['first', 'second', 'third']
print(mixed_tuple[0]) # ('aaaaaaaaaa', 3, 4)
```

# 73. リストに条件を満たす要素が出現する回数を簡単に数える  
[73. リストに条件を満たす要素が出現する回数を簡単に数える](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#73-%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AB%E6%9D%A1%E4%BB%B6%E3%82%92%E6%BA%80%E3%81%9F%E3%81%99%E8%A6%81%E7%B4%A0%E3%81%8C%E5%87%BA%E7%8F%BE%E3%81%99%E3%82%8B%E5%9B%9E%E6%95%B0%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E6%95%B0%E3%81%88%E3%82%8B)

```
names = ["Besim", "Albert", "Besim", "Fisnik", "Meriton"]
print(names.count("Besim")) # 2
```

# 74. slice()を使用して、最後のn個の要素を簡単に取得する 
[74. slice()を使用して、最後のn個の要素を簡単に取得する](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#74-slice%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E6%9C%80%E5%BE%8C%E3%81%AEn%E5%80%8B%E3%81%AE%E8%A6%81%E7%B4%A0%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B)

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
slicing = slice(-4, None)

# Getting the last 3 elements from the list
print(my_list[slicing]) # [4, 5, 6]

# Getting only the third element starting from the right
print(my_list[-3]) # 4
```

次のような通常のスライスタスクにもslice()を使用できます。
```
string = "Data Science"

# start = 1, stop = None (don't stop anywhere), step = 1
# contains 1, 3 and 5 indices
slice_object = slice(5, None)

print(string[slice_object]) # Science
```

# 77. ジャンプを使用してサブタプルを取得する 
[77. ジャンプを使用してサブタプルを取得する](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#77-%E3%82%B8%E3%83%A3%E3%83%B3%E3%83%97%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E3%82%B5%E3%83%96%E3%82%BF%E3%83%97%E3%83%AB%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B)

```
my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(my_tuple[::3]) # (1, 4, 7, 10)
```

# 78. インデックスから始まるサブタプルを取得する  
[78. インデックスから始まるサブタプルを取得する](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#78-%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E3%81%8B%E3%82%89%E5%A7%8B%E3%81%BE%E3%82%8B%E3%82%B5%E3%83%96%E3%82%BF%E3%83%97%E3%83%AB%E3%82%92%E5%8F%96%E5%BE%97%E3%81%99%E3%82%8B)
```
my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(my_tuple[3:]) # (4, 5, 6, 7, 8, 9, 10)
```

# 88. collectionsのCounterを使用して、文字列またはリストの要素数を数える  
[88. collectionsのCounterを使用して、文字列またはリストの要素数を数える](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#88-collections%E3%81%AEcounter%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E6%96%87%E5%AD%97%E5%88%97%E3%81%BE%E3%81%9F%E3%81%AF%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E8%A6%81%E7%B4%A0%E6%95%B0%E3%82%92%E6%95%B0%E3%81%88%E3%82%8B)

```
from collections import Counter

result = Counter("Banana")
print(result) # Counter({'a': 3, 'n': 2, 'B': 1})

result = Counter([1, 2, 1, 3, 1, 4, 1, 5, 1, 6])
print(result) # Counter({1: 5, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})
```

# 89. Counter を使用して、2つの文字列がアナグラムか調べる  
[89. Counter を使用して、2つの文字列がアナグラムか調べる](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#89-counter-%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A62%E3%81%A4%E3%81%AE%E6%96%87%E5%AD%97%E5%88%97%E3%81%8C%E3%82%A2%E3%83%8A%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%8B%E8%AA%BF%E3%81%B9%E3%82%8B) 

```
from collections import Counter

def check_if_anagram(first_string, second_string):
    first_string = first_string.lower()
    second_string = second_string.lower()
    return Counter(first_string) == Counter(second_string)

print(check_if_anagram('testinG', 'Testing')) # True
print(check_if_anagram('Here', 'Rehe')) # True
print(check_if_anagram('Know', 'Now')) # False
```

# 90. itertoolsのcountを使用して、要素数を数える  
[90. itertoolsのcountを使用して、要素数を数える](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#90-itertools%E3%81%AEcount%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E8%A6%81%E7%B4%A0%E6%95%B0%E3%82%92%E6%95%B0%E3%81%88%E3%82%8B)
```
from itertools import count
my_vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
current_counter = count()
string = "This is just a sentence."
for i in string:
    if i in my_vowels:
        print(f"Current vowel: {i}")
        print(f"Number of vowels found so far: {next(current_counter)}")
```

これがコンソールに出力される結果です。
```
Current vowel: i
Number of vowels found so far: 0
Current vowel: i
Number of vowels found so far: 1
Current vowel: u
Number of vowels found so far: 2
Current vowel: a
Number of vowels found so far: 3
Current vowel: e
Number of vowels found so far: 4
Current vowel: e
Number of vowels found so far: 5
Current vowel: e
Number of vowels found so far: 6
```

# 91. 頻度に基づいて、文字列またはリストの要素をソートする 
[91. 頻度に基づいて、文字列またはリストの要素をソートする](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#91-%E9%A0%BB%E5%BA%A6%E3%81%AB%E5%9F%BA%E3%81%A5%E3%81%84%E3%81%A6%E6%96%87%E5%AD%97%E5%88%97%E3%81%BE%E3%81%9F%E3%81%AF%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E8%A6%81%E7%B4%A0%E3%82%92%E3%82%BD%E3%83%BC%E3%83%88%E3%81%99%E3%82%8B)

collectionsモジュールのcounterは、デフォルトでは、頻度に基づいて要素をソートしません。
```
from collections import Counter
result = Counter([1, 2, 3, 2, 2, 2, 2])
print(result) # Counter({2: 5, 1: 1, 3: 1})
print(result.most_common()) # [(2, 5), (1, 1), (3, 1)]
```

# 93. copy()とdeepcopy()の違い  
[93. copy()とdeepcopy()の違い](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#93-copy%E3%81%A8deepcopy%E3%81%AE%E9%81%95%E3%81%84)

```
浅いコピーは、新しい複合オブジェクトを構築し、（可能な範囲で）元のオブジェクトへの参照を挿入します。
深いコピーは、新しい複合オブジェクトを構築し、再帰的に、元のオブジェクトにあるオブジェクトのコピーを挿入します。
```

```
浅いコピーは、新しいコレクションオブジェクトを構築し、元のオブジェクトにある子オブジェクトへの参照を挿入することです。基本的に、浅いコピーは1レベルの深さしかありません。コピー処理は再帰的に行わないため、子オブジェクト自体のコピーを作成しません。
深いコピーは、コピー処理を再帰的に行います。つまり、新しいコレクションオブジェクトを構築し、元のオブジェクトにある子オブジェクトのコピーを再帰的に挿入します。この方法でオブジェクトをコピーすると、オブジェクトツリー全体をウォークし、元のオブジェクトとそのすべての子オブジェクトの完全に独立したクローンを作成します。
```

```
first_list = [[1, 2, 3], ['a', 'b', 'c']]
second_list = first_list.copy()
first_list[0][2] = 831

print(first_list) # [[1, 2, 831], ['a', 'b', 'c']]
print(second_list) # [[1, 2, 831], ['a', 'b', 'c']]
```

```
import copy

first_list = [[1, 2, 3], ['a', 'b', 'c']]
second_list = copy.deepcopy(first_list)
first_list[0][2] = 831

print(first_list) # [[1, 2, 831], ['a', 'b', 'c']]
print(second_list) # [[1, 2, 3], ['a', 'b', 'c']]
```

# 99. sort()とsorted()の違い  
[99. sort()とsorted()の違い](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#99-sort%E3%81%A8sorted%E3%81%AE%E9%81%95%E3%81%84)

```
sort()は、元のリストをソートします。

sorted()は、ソートされた新しいリストを返します。
```

```
groceries = ['milk', 'bread', 'tea']

new_groceries = sorted(groceries)
# new_groceries = ['bread', 'milk', 'tea']
print(new_groceries)

# groceries = ['milk', 'bread', 'tea']
print(groceries)

groceries.sort()
# groceries = ['bread', 'milk', 'tea']
print(groceries)
```

# 100. uuidモジュールを使用して、一意のIDを生成する  
[100. uuidモジュールを使用して、一意のIDを生成する](https://qiita.com/baby-degu/items/532bea7be058c35f61a8#100-uuid%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E4%B8%80%E6%84%8F%E3%81%AEid%E3%82%92%E7%94%9F%E6%88%90%E3%81%99%E3%82%8B)

```
import uuid

# Generate a UUID from a host ID, sequence number, and the current time
print(uuid.uuid1()) # 308490b6-afe4-11eb-95f7-0c4de9a0c5af

# Generate a random UUID
print(uuid.uuid4()) # 93bc700b-253e-4081-a358-24b60591076a
```

# Troubleshooting


# Reference


* []()
![alt tag]()
<img src="" width="400" height="500">

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3