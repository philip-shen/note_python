import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os
import mpl_tc_fonts

def test_font1():
    # 設定就只有這兩行而已
    plt.rcParams['font.family'] = 'san-serif'
    plt.rcParams['font.san-serif'] = ['Microsoft JhengHei'] 
    
    # 驗證
    fig, ax = plt.subplots()
    ax.set_title('簡單無腦中文標題使用中')
    plt.show()

def test_font2(font_file):
    fm_manager = fm.FontManager()
    for f in list([*fm_manager.ttflist, *fm_manager.afmlist]):
        if os.path.basename(f.fname) == font_file:
            print(f.name)

'''            
如果是在 Colab 上使用，對於不甚熟悉 Linux 操作跟文件結構的使用者會略微麻煩，
我有包好一個 package 內建 Noto 跟 CwTeX 字體，直接 import 就行：

https://github.com/Hsins/mpl-tc-fonts
'''            	
def test_font3():
    names = ['分類 A', '分類 B', '分類 C']
    values = [1, 10, 100]

    plt.figure(figsize=(9, 3))

    plt.subplot(131)
    plt.bar(names, values)
    plt.subplot(132)
    plt.scatter(names, values)
    plt.subplot(133)
    plt.plot(names, values)
    plt.suptitle('分類資料圖')
    plt.show()

if __name__ == "__main__":
    
    #test_font1()

    test_font3()

    font_file = 'timesbi.ttf' # 以 New Times Roman 為例
    test_font2(font_file)
    