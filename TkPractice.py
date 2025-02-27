import re #正規表現ライブラリ
from tkinter import *
import tkinter as tk
#from tkinter import ttk
import tkinter.font as tkfont
import textwrap


#===================================
flagArr = []
charaArr= []
itemArr = []
pageArr = []

mode = 0
#modeは、1ならChara、2ならpageを読み込んでいるという意味

item_page="page" #今表示しているものは、ページ("page")かもちもの("item")か
#===================================

temp_pageArr = {"title": "" ,  "img": "", "description":[] , "selection": []}

page_num = -1 #ページ番号。BTAPでいうところのmov関数などの制御に使おうかと。
#ページタイトルの時に１つ増やすので、実際の運用は0以上の整数となる。

root = Tk()
root.title("Tk習作")
root.geometry("650x450")
#root.resizable(width=False, height=False)

#=======================================
# フォント
Default_font = tkfont.Font(
    root,
    family="",
    size=16
)

Bold_font = tkfont.Font(
    root,
    family="",
    size=16,
    weight="bold"
)
#    family="Yu Ghotic",
UI_large_font = tkfont.Font(
    root,
    family="",
    size=17
)

Title_font = tkfont.Font(root, family="Yu Gothic Bold", size=20)

#==============================
menubar= tk.Menu(root)
root.config(menu=menubar)

#フォントメニュー～～～～～～～～～～～～～
fontmenu=tk.Menu(menubar, tearoff=1)
#①フォントサイズ
fontmenu.add_command(label="文字を大きくする",command=lambda:change_font_size(1))
fontmenu.add_command(label="文字を小さくする",command=lambda:change_font_size(-1))
fontmenu.add_separator()
#②フォント
fontmenu.add_command(label="MS UI Ghotic",command=lambda:change_font("MS UI Ghotic"))
fontmenu.add_command(label="BIZ UDゴシック",command=lambda:change_font("BIZ UDゴシック"))
fontmenu.add_command(label="BIZ UD明朝 Medium",command=lambda:change_font("BIZ UD明朝 Medium"))
fontmenu.add_command(label="Times",command=lambda:change_font("Times New Roman"))
fontmenu.add_command(label="游明朝",command=lambda:change_font("游明朝"))
fontmenu.add_command(label="Yu Gothic UI Semilight", command=lambda:change_font("Yu Gothic UI Semilight"))
fontmenu.add_command(label="メイリオ", command=lambda:change_font("メイリオ"))

#以下の2つは、半ばジョーク枠
fontmenu.add_command(label="HGS教科書体",command=lambda:change_font("HGS教科書体"))
fontmenu.add_command(label="HGS創英角ﾎﾟｯﾌﾟ体",command=lambda:change_font("HGS創英角ﾎﾟｯﾌﾟ体"))

menubar.add_cascade(label="フォント", menu=fontmenu)

#フォントを変える
def change_font(fontname):
    Default_font["family"]=  fontname
    Bold_font["family"]=  fontname
    UI_large_font["family"]=  fontname
    Title_font["family"]=  fontname
    
#フォントサイズを d だけ増やす
def change_font_size(d):
    Default_font["size"]+=d
    Bold_font["size"]+=d
    UI_large_font["size"]+=d
    Title_font["size"]+=d
#左側~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#左側（タイトル、描写）のウィジェットをまとめるフレーム
pageF = tk.Frame(root, width=400, pady=10,padx=10)
pageF.propagate(False) #フレームサイズが変更されないようにする

############
#タイトル 
titleV = tk.StringVar()
titleV.set("デフォルトのタイトル")
titleM = tk.Message(pageF, justify="center", width=380,textvariable=titleV,font=Title_font)

############
#描写内容が入る配列 
msgArr = []


#右側~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#右側（画像、選択肢）のウィジェットをまとめるフレーム
subF = tk.Frame(root, width=206,pady=15,padx=10, bg="#c0c0c0")
subF.propagate(False) #フレームサイズが変更されないようにする

############
#画像表示用 
# イメージ作成
# イメージの配置がよくわからん。実際に表示されるのはshow_page内での再処理を経てから
canvas = tk.Canvas(subF, bg="black", height=198, width=198, relief=tk.RIDGE, borderwidth="3")
img = PhotoImage(file="source/images/white.png", height=95, width=95)
canvas.create_image(105,105,image=img)

############
#選択リストLと、そのスクロールバーS、選択ボタンB 
#リストの中の選択肢を管理する変数selectV。中にはリストなどを入れる
selectV = tk.StringVar()
selectF = tk.Frame(subF)

#selectFのなかに、LとSを横並びで入れる
selectL = tk.Listbox(selectF, justify="center", listvariable=selectV, height=4,width=15,relief=tk.RIDGE,borderwidth="5",font=Default_font, selectmode="BROWSE")
selectS = tk.Scrollbar(selectF, orient=VERTICAL, width=15)
selectS["command"]=selectL.yview


selectB = tk.Button(subF, justify="center", text='決定', command=lambda:eval_selection(selectL.curselection()[0]),font=UI_large_font)


#1回リストが選択されたら、selectBボタンをアクティブにする。
def listbox_select(event):
    if len(selectL.curselection())>0:   #何か選択されている場合、
        selectB["state"] = "normal"
            #注意！リストに何も入っていない状態でクリックされた場合でも、<<ListboxSelect>>イベントが発生してしまう。
            #そのため、ボタンを押しても何も選択されていないのでエラーが起こる。
            #これをふせぐために、リストの選択数が0でないときだけ、ボタンをアクティブにする。

#ダブルクリックされたら、selectBボタンを押さなくても直で実行する
def listbox_double_clicked(event):
    if len(selectL.curselection())>0:
        eval_selection(selectL.curselection()[0])
        
            
selectL.bind("<<ListboxSelect>>", listbox_select)
selectL.bind("<Double-Button-1>", listbox_double_clicked)
    
#selectBボタンでエンターキーを押されても、listbox_double_clickedと同等の処理を行う。commandプロパティは、クリック時しか動かないので。
selectB.bind("<Return>", listbox_double_clicked)


############
#もちものを開く、閉じる
itemB = tk.Button(subF, justify="center", text='もちものを見る', bg="#E0E0E0",command=lambda:switch_item_page(),font=UI_large_font)

def Enter_key_switch_item_page(event):
    switch_item_page()
    
#itemBボタンでエンターキーを押されても、switch_item_page()と同等の処理を行う。commandプロパティは、クリック時しか動かないので。
itemB.bind("<Return>", Enter_key_switch_item_page)



#============================================================= 
#ファイルを読み込んで、データを配列に落とし込む。

#ファイル読み込み
f = open('source/script.txt', 'r', encoding='UTF-8')  

#読み込んで各行を配列にする。
story_data = f.readlines()
f.close()

#走査
for i in range(len(story_data)):
    line = story_data[i].rstrip('\n')   #読み込んだあとの各行には、改行コードが入っていることがあるので除去する

        # キャラクターを記載する際は、
        #  ・ 番号は0からはじめ、改行するごとに1ずつ増やさねばならない
        # という仕様を設ける。
        # どうせそうするのだから、「番号>」の部分は要らないのでは無いかとも思うが、
        # 後から参照するときに、このキャラは何番だっけ…と迷わないための、お行儀の良いインデックスに。と暫定的に思う
    
    #コメントはすっとばす
    if re.match(r'//', line):
        continue
    
    #フラグかどうか
    REflag = re.match(r'f:(.*)', line)
    if REflag:
        flag_max = int(REflag.group(1))
        for i in range(flag_max):
            flagArr.append(False)
            
    #アイテムかどうか
    item_list = re.match(r'[0-9]*!(.*)!(.*)', line)  
    if item_list:
        itemArr.append([False, item_list.group(1), item_list.group(2)])
        continue
    
    #ページのタイトルかどうか
    REtitle =  re.match(r"^#(.*)", line)
    if REtitle:
        temp_pageArr = {"title": REtitle.group(1), "description":[] , "selection": []}
        mode=2  #次からの行は、ページの描写部であることを示す
        page_num+=1 #ページ番号を一つ増やす。
        continue
        
    #ページの画像かどうか 
    REimg =  re.match(r"^C:(.*)", line)
    if REimg:
        temp_pageArr["img"] = REimg.group(1)
        continue   
        
    #ページの選択肢かどうか
    REselection =  re.match(r"^%(.*)%(.*)", line)
    if REselection:
        temp_pageArr["selection"].append([REselection.group(1), REselection.group(2)]) #←あとでこの構造を変えるが、暫定的にこうする
        continue
    
    #ページの終わりかどうか
    REend_of_page =  re.match(r"^(.*?)E$", line)
    if REend_of_page:
        mode=0 #ページの読み取り終了
        pageArr.append(temp_pageArr)
        continue

    #ページのタイトルでも選択肢でも終わりでもなく、描写部の場合は
    if mode==2: 
        adjusted_line = ["n", line] #下のところでフィルターして、特に問題なければこれが入る
        
        
        REdecoration_talk = re.match(r"b/([0-9]+)>(.*)", line)
        if REdecoration_talk:
            adjusted_line = ["bt", REdecoration_talk.group(1), REdecoration_talk.group(2)]
        else:
            REdecoration = re.match(r"b/(.*)", line)
            if REdecoration:
                adjusted_line = ["bold", REdecoration.group(1)]
            
            REtalk= re.match(r"([0-9]+)>(.*)", line)
            if REtalk:
                adjusted_line = ["talk", REtalk.group(1), REtalk.group(2)]
            
        
        temp_pageArr["description"].append(adjusted_line)
        continue
   
# 選択肢について
# リストボックスに表示する文字列はリストとかタプルとかでなければならない。
# そのため、構造を変更する。
# [[選択肢名, 選択後関数], ... ] --> [[選択名, ...] , [選択後関数, ...]]

for j in pageArr:
    temp_selection = j["selection"]
    if(len(temp_selection) > 0):
        selection_nameArr = []
        selection_funcArr = []
        for k in temp_selection:
            selection_nameArr.append(k[0])
            selection_funcArr.append(k[1])

        temp_selection = [selection_nameArr, selection_funcArr]
    j["selection"] = temp_selection
    
#######################################    
#アイテムを表示する。 show_pageと対。
def show_item():     
    titleV.set("～ もちもの ～")
    
    global msgArr
    
    for i in msgArr:
        for j in i:
            j.destroy()
    msgArr=[]
    
    
    #何もアイテムを持っていないなら、その旨を表示する。持っているなら、それぞれ表示する。
    #その判定のための変数。初期値はFalse。
    if_hav_any_item = False
    
    #走査して、何かあればそれを表示できるようにし、if_hav_any_itemはTrueにする
    for i in itemArr:
        if i[0]:
            if_hav_any_item=True
            
            tempF = tk.Frame(pageF)
            temp_itemArr = [tempF]
            
            item_name=f"★ {i[1]} ★"
            
            temp_itemArr.append(tk.Message(tempF, justify="center", text=item_name, width=380, font=Default_font))
            temp_itemArr.append(tk.Message(tempF, justify="center", text=i[2], width=380, font=Default_font))
            temp_itemArr.append(tk.Message(tempF, justify="center", text="", width=380, font=Default_font))
            
            msgArr.append(temp_itemArr)
            
    #何もアイテムを持っていないなら、その旨を表示する。
    if not(if_hav_any_item):
        tempF = tk.Frame(pageF)
        temp_itemArr = [tempF]
        
        temp_itemArr.append(tk.Message(tempF, justify="center", text="今は何も持っていません", width=380, font=Default_font))
        
        msgArr.append(temp_itemArr)
        
        
    for j in msgArr:
        for k in j:
            k.pack(side="top", fill="x", anchor=tk.CENTER)
    
    #画像は真っ白にしておく
    global img
    img = PhotoImage(file="source/images/white.png", height=200, width=200)
    canvas.create_image(105,105,image=img)

    ###選択肢###
    selectB["state"] = "disabled" #最初、ボタンは押せないようにする。リストから選択後"normal"になって使えるようになる
    selectV.set([])
    

#########################################


#ページの内容を表示する。show_itemと対。
def show_page(): 
    now_page=pageArr[page_num]

    ###タイトル###
    hoge = now_page["title"]
    titleV.set(hoge)

    ###描写###
    global msgArr
    
    for i in msgArr:
        for j in i:
            j.destroy()
    msgArr=[]
            
    
    
    for now_desc in now_page["description"]:
        tempF = tk.Frame(pageF)
        temp_descArr = [tempF]
        
        if now_desc[0]=="bold": #太字
            temp_descArr.append(tk.Message(tempF, justify="left", text=now_desc[1], width=380,font=Bold_font))

        else:          
            temp_descArr.append(tk.Message(tempF, justify="left", text=now_desc[1], width=380,font=Default_font))
        
        msgArr.append(temp_descArr)
    
    for i in msgArr:
    
        #0要素目のFrameは上詰めで、1要素目のMessageは左詰めで詰めていく。
        i[0].pack(side="top", fill="x")
        
        if len(i) == 2:
            i[1].pack(side="left", fill="x", anchor="nw")
    
    ###絵###
    global img
    img_src= "source/images/" + now_page["img"] + ".png"
    img = PhotoImage(file=img_src, width=200,height=200)
    canvas.create_image(5,4,image=img, anchor="nw")
    
    
    ###選択肢###
    selectB["state"] = "disabled" #最初、ボタンは押せないようにする。リストから選択後"normal"になって使えるようになる
    
    
    if len(now_page["selection"])==0:
        selectV.set([])   
    else:
        selectV.set(now_page["selection"][0])   
        selectL.select_clear(0, tk.END) #これがないと、一番上の項目がもともと選択されている状態になる。
        if len(now_page["selection"][0])>selectL["height"]:
            #gridにて配置
            selectS.grid(row=0, column=1, sticky=(N, S))
        else:
            selectS.grid_remove()


##############################################
#選択結果を実行する
def eval_selection(i):
    selectionArr = pageArr[page_num]["selection"][1][i].split(";")
    
    def inner_eval_selection(arr):
        for s in arr:
            #ページ移動 (m数字)-----------------------
            REmov = re.match(r"m([0-9]*)", s)
            
            if REmov:
                global page_num
                page_num = int(REmov.group(1))
                continue
                
            #アイテムゲット(g数字）----------------------
            REget = re.match(r"g([0-9]*)", s)
            
            if REget:
                itemArr[int(REget.group(1))][0]=True
                continue
                
            #アイテムロスト(L数字）---------------------
            RElost = re.match(r"L([0-9]*)", s)
            
            if RElost:
                itemArr[int(RElost.group(1))][0]=False
                continue
    
            #もしアイテムを持っているなら-------------------
            REifhave = re.match(r"ifi([0-9]*)(.*?)<(.*)><(.*)>", s)
            #ifi [アイテム番号] [区切り文字] < [True節] >< [False節] >
            #各節の中を普通にセミコロンで区切ると、もうあらかじめsplitされてしまって原型がなくなってしまう。
            #そのため、セミコロン以外の文字で区切る。
            #例：ifi1x<L1xm5><m6> =もしアイテム1を持っていたら、アイテム1を捨ててページ5へ。さもなくばページ6へ。
            if REifhave:
                item_number = REifhave.group(1)
                split_tag = REifhave.group(2)
                true_node= REifhave.group(3)
                false_node = REifhave.group(4)
                if itemArr[int(item_number)][0]:
                    inner_eval_selection(true_node.split(split_tag))
                else:
                    inner_eval_selection(false_node.split(split_tag))
                continue
            
            
            #フラグを立てる(on数字）-------------------
            REonflag = re.match(r"on([0-9]*)", s)
            if REonflag:
                flagArr[int(REonflag.group(1))] = True
                continue
                
            #フラグをおろす(off数字）-------------------
            REoffflag = re.match(r"off([0-9]*)", s)
            if REoffflag:
                flagArr[int(REoffflag.group(1))] = False
                continue
            
            #もしアフラグが立っているなら-------------------
            REifflag = re.match(r"iff([0-9]*)(.*?)<(.*)><(.*)>", s)
            #ifiのフラグ版
            #ifi [フラグ番号] [区切り文字] < [True節] >< [False節] >
            if REifflag:
                flag_number = REifflag.group(1)
                split_tag = REifflag.group(2)
                true_node= REifflag.group(3)
                false_node = REifflag.group(4)
                if flagArr[int(flag_number)]:
                    inner_eval_selection(true_node.split(split_tag))
                else:
                    inner_eval_selection(false_node.split(split_tag))
                continue
            
    inner_eval_selection(selectionArr)
        
    show_page()


#ここからが表示の本番！
page_num = 0    #今いるページ番号

###################################

#もちもののボタン(itemB)を押したときの反応について
def switch_item_page():
    global item_page
    if item_page=="page":    #今、ページを開いているなら、持ち物を開くようにする
        item_page = "item"
        itemB["text"] = "もちものを閉じる"
        itemB["bg"]="#F0C0C0"
        show_item()
    else:
        item_page = "page"
        itemB["text"] = "もちものを見る"
        itemB["bg"]="#E0E0E0"
        show_page()
    
#################################
# 関数は以上     
        
        
        
pageF.pack(side="left", fill="both", expand=1)
subF.pack(side="left", fill="both", expand=1)
titleM.pack()

canvas.pack(side="top")
selectF.pack()

#スクロールバーselectSがちゃんと動くように、gridでないといけない。
#おなじFrame内のselectLもgridで配置する。
selectL.grid(row=0, column=0)


selectB.pack(side="top")
itemB.pack(side="bottom")

show_page()

root.mainloop()