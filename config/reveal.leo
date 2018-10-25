<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20180904144300.1"><vh>@settings</vh>
<v t="leo.20180904144300.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20180904144300.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20180904144325.1" a="E"><vh>編輯 reveal</vh>
<v t="leo.20180904144325.2" a="E"><vh>@path ./../reveal</vh>
<v t="leo.20180904144325.3" a="E"><vh>@clean index.html</vh>
<v t="leo.20180904144325.4" a="E"><vh>html</vh>
<v t="leo.20180904144325.5"><vh>head</vh></v>
<v t="leo.20180904144325.6" a="E"><vh>body</vh>
<v t="leo.20180904144325.7" a="E"><vh>reveal div</vh>
<v t="leo.20180904144325.8" a="E"><vh>slides div</vh>
<v t="leo.20180904144325.9"><vh>封面投影片</vh>
<v t="leo.20180904144325.10"><vh>封面投影片內容</vh></v>
</v>
<v t="leo.20180904181252.1"><vh>9月10日</vh>
<v t="leo.20180904181252.2"><vh>2018 Fal l上課模式</vh></v>
</v>
<v t="leo.20180904182228.1" a="E"><vh>9月10日之一</vh>
<v t="leo.20180904182228.2"><vh>2018 Fal l上課模式</vh></v>
</v>
<v t="leo.20181001094259.1"><vh>10月1日</vh>
<v t="leo.20181001094259.2"><vh>2018 Fal l上課模式</vh></v>
</v>
<v t="leo.20181022071449.1" a="E"><vh>10月22日</vh>
<v t="leo.20181022071449.2"><vh>如何更加精確並注重細節</vh></v>
</v>
<v t="leo.20180904144325.11" a="E"><vh>快捷鍵</vh>
<v t="leo.20180904144325.12"><vh>投影片快捷鍵</vh></v>
</v>
<v t="leo.20180904144325.13" a="E"><vh>各式內容引用範例</vh>
<v t="leo.20180904144325.14" a="E"><vh>導入數學符號與方程式</vh>
<v t="leo.20180904144325.15"><vh>LaTeX 格式方程式</vh></v>
</v>
<v t="leo.20180904144325.16" a="E"><vh>導入縮排程式碼</vh>
<v t="leo.20180904144325.17"><vh>引用程式碼</vh></v>
</v>
<v t="leo.20180904144325.18" a="E"><vh>導入影片</vh>
<v t="leo.20180904144325.19"><vh>iframe 導入影片</vh></v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20180904144300.1"></t>
<t tx="leo.20180904144300.2">QSplitter::handle {
    background-color: #CAE1FF; /* lightSteelBlue1 */
}

QStackedWidget {
    /* background-color:lightpink; */
    border-color: red;
    padding: 0px;
    /* border-width: 0px; */
    /* background-color: yellow; */
}

QSplitter {
    border-color: white;
    background-color: white;
    border-style: solid;
}

QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 22px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20180904144300.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20180904144325.1"></t>
<t tx="leo.20180904144325.10">## 2018Fall 電腦輔助設計實習

### 虎科大機械設計工程系

&lt;small&gt;
Created by [KMOLab](http://lab.kmol.info/)
&lt;/small&gt;

[電腦輔助設計實習網誌](./../blog/index.html)


</t>
<t tx="leo.20180904144325.11">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20180904144325.12"># 投影片快捷鍵

* 利用箭頭上下前後換頁
* 按 f 鍵進入全螢幕模式 (full screen)
* 按 s 鍵可以顯示投影片筆記 (show)
* 按 o 鍵可以切換單張或全域檢視 (overview)
* 按 b 或 . 鍵可以切換螢幕黑屏 (black)
* 按 Esc 可以退出全螢幕或全域檢視 (Escape)

</t>
<t tx="leo.20180904144325.13">&lt;section&gt;
@others
&lt;/section&gt;

</t>
<t tx="leo.20180904144325.14">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
&lt;!-- 請注意, @others 不可以內縮 --&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;



						
</t>
<t tx="leo.20180904144325.15"># 數學符號與方程式

Inline math equations go in like so: $\omega = d\phi / dt$. Display
math should get its own line and be put in in double-dollarsigns:

$$I = \int \rho R^{3} dV$$
</t>
<t tx="leo.20180904144325.16">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
&lt;!-- 請注意, @others 不可以內縮 --&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;



						
</t>
<t tx="leo.20180904144325.17">## 利用 Markdown 寫投影片
以下利用 Markdown 格式展示 Python 程式碼:
```
@language python
# use threading and subprocess to threading the make process
import os
import subprocess
import threading

def domake():
    
    path = "../exposed/api/exposed"
    ubuntu = "../Ubuntu"
    
    # create obj path
    
    if not os.path.exists(path+"/../obj"):
        os.makedirs(path+"/../obj")
    
    subprocess.call(["make", "clean"], cwd=path)
    subprocess.call("make", cwd=path)
    subprocess.call(["cp", "{libslvs.so, _slvs.so, slvs.py}", ubuntu], cwd=path)
    subprocess.call(["python3", "circle_ex.py"], cwd=path+"/"+ubuntu)
    
make = threading.Thread(target=domake)
make.start()
```
</t>
<t tx="leo.20180904144325.18">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20180904144325.19">## 使用 iframe 導入影片

### 導入影片 template

&lt;iframe src="https://player.vimeo.com/video/183950627" width="640" height="492" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen&gt;&lt;/iframe&gt;
</t>
<t tx="leo.20180904144325.2"></t>
<t tx="leo.20180904144325.3">@language xml
@tabwidth -4
@others

</t>
<t tx="leo.20180904144325.4">&lt;!doctype html&gt;
&lt;html lang="en"&gt;
@others
&lt;/html&gt;
</t>
<t tx="leo.20180904144325.5">&lt;head&gt;
    &lt;meta charset="utf-8"&gt;
&lt;title&gt;
2018 Fall 機械設計工程系電腦輔助設計實習
&lt;/title&gt;
    &lt;meta name="description" content="A framework for easily creating beautiful presentations using HTML"&gt;
    &lt;meta name="author" content="Hakim El Hattab"&gt;
    
    &lt;meta name="apple-mobile-web-app-capable" content="yes"&gt;
    &lt;meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"&gt;
    
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"&gt;
    
    &lt;link rel="stylesheet" href="css/reveal.css"&gt;
    &lt;link rel="stylesheet" href="css/theme/black.css" id="theme"&gt;
    
    &lt;!-- Theme used for syntax highlighting of code --&gt;
    &lt;link rel="stylesheet" href="lib/css/zenburn.css"&gt;
    &lt;link rel="icon" href="favicon.ico" type="image/x-icon" /&gt;

    &lt;!-- Printing and PDF exports --&gt;
    &lt;script&gt;
        var link = document.createElement( 'link' );
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = window.location.search.match( /print-pdf/gi ) ? 'css/print/pdf.css' : 'css/print/paper.css';
        document.getElementsByTagName( 'head' )[0].appendChild( link );
    &lt;/script&gt;

    &lt;!--[if lt IE 9]&gt;
    &lt;script src="lib/js/html5shiv.js"&gt;&lt;/script&gt;
    &lt;![endif]--&gt;
&lt;/head&gt;

</t>
<t tx="leo.20180904144325.6">&lt;body&gt;
@others
&lt;script src="lib/js/head.min.js"&gt;&lt;/script&gt;
&lt;script src="js/reveal.js"&gt;&lt;/script&gt;
&lt;script&gt;
        // More info https://github.com/hakimel/reveal.js#configuration
        Reveal.initialize({
            controls: true,
            progress: true,
            history: true,
            center: true,

            transition: 'slide', // none/fade/slide/convex/concave/zoom

            // More info https://github.com/hakimel/reveal.js#dependencies
            dependencies: [
                { src: 'lib/js/classList.js', condition: function() { return !document.body.classList; } },
                { src: 'plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                { src: 'plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
                { src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
                { src: 'plugin/zoom-js/zoom.js', async: true },
                { src: 'plugin/notes/notes.js', async: true },
                { src: 'plugin/math/math.js', async: true }
            ]
        });
&lt;/script&gt;
&lt;/body&gt;

</t>
<t tx="leo.20180904144325.7">&lt;div class="reveal"&gt;
@others
&lt;/div&gt;

</t>
<t tx="leo.20180904144325.8">&lt;!-- Any section element inside of this container is displayed as a slide --&gt;
&lt;div class="slides"&gt;
@others
&lt;/div&gt;

</t>
<t tx="leo.20180904144325.9">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20180904181252.1">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20180904181252.2"># 2018 Fall CADP

* 指定 OnShape 12 週課程教材
* 各學員依序自行掌握進度
* 將實際操作影片上傳 Youtube
* 自製教學手冊放入 CMSimfly
* 自製簡報放入 Reveal.js
* 學習流程與心得放入 Pelican 網誌
* 第十週之後, 六人一組執行期末專案

</t>
<t tx="leo.20180904182228.1">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20180904182228.2"># 2018 Fall CADP (續)

* Github 與 Youtube 將完整紀錄學員進度
* 學習成績將以自評互評與倉儲內容為準
* 期末專案可以採 OnShape 或其他 CAD 繪圖
* 動態系統模擬將採 V-rep 進行
* 驅動與控制將使用 Arduino 與直流或伺服馬達
* 本課程為協同產品設計實習的先導課程

</t>
<t tx="leo.20181001094259.1">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20181001094259.2"># 2018 Fall CADP Week4

* 指定 OnShape 12 週課程教材
* 各學員依序自行掌握進度
* 將實際操作影片上傳 Youtube
* 自製教學手冊放入 CMSimfly
* 自製簡報放入 Reveal.js
* 學習流程與心得放入 Pelican 網誌
* 第十週之後, 六人一組執行期末專案

</t>
<t tx="leo.20181022071449.1">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
@others
    &lt;/script&gt;
&lt;/section&gt;


						
</t>
<t tx="leo.20181022071449.2"># 保持精確與注重細節

* 如何保持精確?
* 為何要注重細節?
* 自我練習再練習
* 確認再確認
* 團隊協同

</t>
</tnodes>
</leo_file>
