
Table of Contents
=================

   * [Purpose](#purpose)
   * [playwright vs. puppeteer](#playwright-vs-puppeteer)
      * [対応ブラウザ](#対応ブラウザ)
      * [PythonやC#でも使いたい？](#pythonやcでも使いたい)
   * [Python と Playwright でブラウザを自動操作させるコードを自動生成したよ](#python-と-playwright-でブラウザを自動操作させるコードを自動生成したよ)
      * [選定した理由](#選定した理由)
      * [環境およびインストール](#環境およびインストール)
      * [iPhone や Android で動作を確認したい](#iphone-や-android-で動作を確認したい)
      * [ここまでのまとめ](#ここまでのまとめ)
      * [注意点](#注意点)
   * [Playwrightも知らないで開発してる君たちへ](#playwrightも知らないで開発してる君たちへ)
      * [比較一覧](#比較一覧)
   * [最新自動テストツール『Playwright for Python』さわってみた](#最新自動テストツールplaywright-for-pythonさわってみた)
      * [Playwright for Pythonでテストを書いてみる](#playwright-for-pythonでテストを書いてみる)
   * [h1 size](#h1-size)
      * [h2 size](#h2-size)
         * [h3 size](#h3-size)
            * [h4 size](#h4-size)
               * [h5 size](#h5-size)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# Purpose  
Take note about Playwright stuffs


# playwright vs. puppeteer  
[2020年12月現在、puppeteerとplaywright どっち選んだらいいの？ Dec 03, 2020](https://qiita.com/YusukeIwaki/items/a9dbd48b1ed4313f3815)

## 対応ブラウザ  
<img src="https://camo.qiitausercontent.com/c2563df41d6025a4be91a5e080bc728dcc4644c7/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f37343537312f39333233646633612d333637622d396133392d656231312d6132343366636663653866642e706e67" width="600" height="400">  

## PythonやC#でも使いたい？  
[microsoft/playwright-sharp](https://github.com/microsoft/playwright-sharp) 
[microsoft/playwright-python](https://github.com/microsoft/playwright) 

Browser\OS | Linux | macOS | Windows
------------------------------------ | --------------------------------------------- |--------------------------------------------- | --------------------------------------------- 
Chromium 97.0.4681.0 | ✅ | ✅ | ✅
WebKit 15.4 | ✅ | ✅ | ✅
Firefox 93.0 | ✅ | ✅ | ✅

[Documentation](https://playwright.dev/python/docs/intro) 

# Python と Playwright でブラウザを自動操作させるコードを自動生成したよ  
[Python と Playwright でブラウザを自動操作させるコードを自動生成したよ Feb 14, 2021](https://qiita.com/mainy/items/3a9de19f440991f67f34)
 
## 選定した理由 
* Python で書けること。社内で Python を使える方が多いので。pytest と連携してくれるとなおうれしい。
* Docker コンテナで動かせること。CI/CD に組み込みたい。
* 非同期動作できること。
* Windows 環境でテストコードが書きやすいこと。というか、GUI でブラウザ操作しながらテストコードを自動で作成してくれると嬉しい。
* スクリーンショットをとれること。エビデンスとしてテスト結果に使いたい。

## 環境およびインストール  
* Windows 10 Pro (2004)
* Python 3.9.1

```
# インストール
pip install playwright==1.8.0a1
playwright install

# インストールの確認
playwright --version
# Version 1.8.0-1611168053000

# もしくはこれでインストールの確認
python -m playwright --version
# Version 1.8.0-1611168053000
```

## iPhone や Android で動作を確認したい  
```
context = browser.new_context()
```

* iPhone の『iPhone 11 Pro』にできるだけ設定を合わせるにはこう、
```
context = browser.new_context(**playwright.devices["iPhone 11 Pro"])
```

* Android の『Pixel 2』にできるだけ設定を合わせるにはこう、
```
context = browser.new_context(**playwright.devices["Pixel 2"])
```

* このように分離すれば、同じテストコードでクロスモバイルデバイステストが簡単にできます。
```
def run(playwright):
    # Mobile Browser
    mobile_browser_run(playwright.chromium, "Pixel 2")
    mobile_browser_run(playwright.webkit, "iPhone 11 Pro")


def mobile_browser_run(browser_type, device_name: str):
    browser = browser_type.launch(headless=False)
    context = browser.new_context(**playwright.devices[device_name])
```

## ここまでのまとめ 
```
from playwright.sync_api import sync_playwright


def run(playwright):
    # PC Browser
    pc_browser_run(playwright.chromium)
    pc_browser_run(playwright.firefox)
    pc_browser_run(playwright.webkit)

    # Mobile Browser
    mobile_browser_run(playwright.chromium, "Pixel 2")
    mobile_browser_run(playwright.webkit, "iPhone 11 Pro")


def pc_browser_run(browser_type):
    browser = browser_type.launch(headless=False)
    context = browser.new_context(
        record_video_dir="./videos",
        record_video_size={"height": 768, "width": 1024},
    )

    # Open new page
    page = context.new_page()

    # Go to https://www.wikipedia.org/
    page.goto("https://www.wikipedia.org/")

    # Click text="日本語"
    page.click('text="日本語"')
    # assert page.url == "https://ja.wikipedia.org/wiki/メインページ"

    # Click text="最近の出来事"
    page.click('text="最近の出来事"')
    # assert page.url == "https://ja.wikipedia.org/wiki/Portal:最近の出来事"

    page.screenshot(path="./screenshot.png", full_page=True)

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


def mobile_browser_run(browser_type, device_name: str):
    browser = browser_type.launch(headless=False)
    context = browser.new_context(
        **playwright.devices[device_name],
        record_video_dir="./videos",
        record_video_size={"height": 768, "width": 1024},
    )

    # Open new page
    page = context.new_page()

    # Go to https://www.wikipedia.org/
    page.goto("https://www.wikipedia.org/")

    # Go to https://ja.m.wikipedia.org/wiki/メインページ
    page.goto("https://ja.m.wikipedia.org/wiki/メインページ")

    # Click div[id="fa_and_ga"] >> text="おまかせ表示"
    page.click('div[id="fa_and_ga"] >> text="おまかせ表示"')
    # assert page.url == "https://ja.m.wikipedia.org/wiki/0.999..."

    page.screenshot(path="./screenshot.png", full_page=True)

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
```

## 注意点      
* 最近 1.8.0a1 に大幅バージョンアップした影響で、0.x 系との互換性がありません。 特に関数名が camelCase から snake_case に変更となっていますので、バージョン 0.x 系のソースはそのままコピペしても動きません。

* 1.8.0a1 から NodeJS と同じバージョンになりベータ版扱いではなくなったみたいらしいですが、公式にその表記がないのが少し気がかりです。

* スクレイピングはサイトによっては禁止されているケースがあります。注意してください。


# Playwrightも知らないで開発してる君たちへ  
[Playwrightも知らないで開発してる君たちへ Jan 25, 2020](https://qiita.com/cc822jp/items/6f786a9ed104af1a382f)

## 比較一覧  
<img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F124296%2Fbacd1b95-2074-903b-f93c-352f28058d8d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=dd3d1e357f4d5844277df45eb4b8a273" width="500" height="300">  

# 最新自動テストツール『Playwright for Python』さわってみた  
[最新自動テストツール『Playwright for Python』さわってみた Oct 07, 2020](https://qiita.com/yaboxi_/items/266b5ce18e57aa1faca1)

## Playwright for Pythonでテストを書いてみる 
[Element Selectors](https://playwright.dev/#version=v1.4.2&path=docs%2Fselectors.md&q=)  
[Input](https://playwright.dev/#version=v1.4.2&path=docs%2Finput.md&q=)  
[Assertions](https://playwright.dev/#version=v1.4.2&path=docs%2Fassertions.md&q=)  

```
from playwright.sync_api import Page


class TestPlanisphere:
    def test_reserve_otoku(self, page: Page):
        page.goto("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0")
        page.waitForLoadState("networkidle")

        page.fill("#date", "2020/12/24")  # 宿泊日
        page.press("#date", "Tab")

        page.fill("#term", "2")  # 宿泊数

        page.fill("#head-count", "1")  # 人数

        page.check("#sightseeing")  # プラン選択

        page.fill("#username", "ベリ坊")  # 名前

        page.selectOption("#contact", "tel")  # 「電話連絡を希望」
        page.fill("#tel", "80120828828")  # 電話番号

        page.click("#submit-button")  # 予約確認ページへ遷移
        page.waitForLoadState("networkidle")

        page.screenshot(path="playwright.png")  # スクリーンショット撮影

        assert "15,000" in page.innerText("#total-bill")

        page.close()
```


#Playwright 瀏覽器自動化工具 
[Playwright 瀏覽器自動化工具，應用於網路爬蟲和測試](https://blog.jiatool.com/posts/playwright/) 

## 滑鼠 Mouse 
[滑鼠 Mouse](https://playwright.dev/python/docs/api/class-mouse)
```

```

## 鍵盤 Keyboard  
[鍵盤 Keyboard](https://playwright.dev/python/docs/api/class-keyboard) 

### An example of holding down Shift in order to select and delete some text: (Async) 
```
await page.keyboard.type("Hello World!")
await page.keyboard.press("ArrowLeft")
await page.keyboard.down("Shift")
for i in range(6):
    await page.keyboard.press("ArrowLeft")
await page.keyboard.up("Shift")
await page.keyboard.press("Backspace")
```

## An example of pressing uppercase (Async) 
```
await page.keyboard.press("Shift+KeyA")
# or
await page.keyboard.press("Shift+A")
```

## An example to trigger select-all with the keyboard (Async) 
```
# on windows and linux
await page.keyboard.press("Control+A")
# on mac_os
await page.keyboard.press("Meta+A")
```

## keyboard.down(key)​ 
```
Dispatches a keydown event.

key can specify the intended keyboardEvent.key value or a single character to generate the text for. A superset of the key values can be found here. Examples of the keys are:

F1 - F12, Digit0- Digit9, KeyA- KeyZ, Backquote, Minus, Equal, Backslash, Backspace, Tab, Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown, PageUp, ArrowRight, ArrowUp, etc.

Following modification shortcuts are also supported: Shift, Control, Alt, Meta, ShiftLeft.

Holding down Shift will type the text that corresponds to the key in the upper case.

If key is a single character, it is case-sensitive, so the values a and A will generate different respective texts.

If key is a modifier key, Shift, Meta, Control, or Alt, subsequent key presses will be sent with that modifier active. To release the modifier key, use keyboard.up(key).

After the key is pressed once, subsequent calls to keyboard.down(key) will have repeat set to true. To release the key, use keyboard.up(key).
```

## keyboard.press  
```
page = await browser.new_page()
await page.goto("https://keycode.info")
await page.keyboard.press("a")
await page.screenshot(path="a.png")
await page.keyboard.press("ArrowLeft")
await page.screenshot(path="arrow_left.png")
await page.keyboard.press("Shift+O")
await page.screenshot(path="o.png")
await browser.close()
```

## keyboard.type  
```
await page.keyboard.type("Hello") # types instantly
await page.keyboard.type("World", delay=100) # types slower, like a userawait page.keyboard.type("Hello") # types instantly
await page.keyboard.type("World", delay=100) # types slower, like a user
```




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
