
Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [note_python_NumPy](#note_python_numpy)
   * [ndim, shape, size, axis](#ndim-shape-size-axis)
      * [Illustration](#illustration)
      * [smaple code](#smaple-code)
   * [Reference](#reference)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)
   * [Table of Contents](#table-of-contents-1)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# note_python_NumPy
Take note of NumPy 

# ndim, shape, size, axis
[Python♪用語集：NumPyの配列に関する日本語表現](https://snowtree-injune.com/2020/06/13/shape-a0101/)

① i番目の次元、
　　※2次元配列の場合は行、列

② i番目の次元の長さ　（x.shape[i]）　
　　※2次元配列の場合は行数、列数

③ i軸　（axis = i）

④ 次元数　（x.ndim）

⑤ 形状（各次元の長さ）　（x.shape)

⑥ 全要素数　（x.size）

## Illustration 
まず、一目でわかるように用語の定義を図示したいと思います。なお、
①「 i番目の次元」

②「 i番目の次元の長さ」については、必要に応じて、

① 「0から始まるi番目の次元」

② 「0から始まるi番目の次元の長さ」と表記し、iがインデックスであることを明記したほうがよいと思います。

<img src="https://snowtree-injune.com/wp-content/uploads/2020/06/2745ffeffebdbdbecf394fde5a3cd635-722x1024.png"  width="400" height="600">


なお、2次元配列の場合には、
①「0番目の次元」→「行」、「1番目の次元」→「列」とし、

②「0番目の次元の長さ」→「行数」、「1番目の次元の長さ」→「列数」とします。

<img src="https://snowtree-injune.com/wp-content/uploads/2020/06/05ff01164e5a20c963ad4469e9852165-768x860.png"  width="300" height="450">

## smaple code
```
import numpy as np

x = np.arange(24)
x = x.reshape((2, 3, 4))
print(x)
print('x.ndim =', x.ndim)
print('x.shape =', x.shape)
print('x.shape[0] =', x.shape[0])
print('x.shape[1] =', x.shape[1])
print('x.shape[2] =', x.shape[2])
print('x.size =', x.size)
print('x[0].size =', x[0].size)
print('x[0, 0].size =', x[0, 0].size)
print('x[0, 0, 0].size =', x[0, 0, 0].size)
print('len(x) =', len(x))
print('len(x[0]) =', len(x[0]))
print('len(x[0, 0]) =', len(x[0, 0]))  
```


* * * * * * * * 

```
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
```

```
x.ndim = 3
x.shape = (2, 3, 4)
x.shape[0] = 2
x.shape[1] = 3
x.shape[2] = 4
x.size = 24
x[0].size = 12
x[0, 0].size = 4
x[0, 0, 0].size = 1
len(x) = 2
len(x[0]) = 3
len(x[0, 0]) = 4  
```


# Reference


<img src=""  width="800" height="800">

```
  
```

* []()  
```

```

* []()  
```

```

* []()  
![alt tag]()

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

