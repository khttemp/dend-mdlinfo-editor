from importPy.decrypt import *
from importPy.tkinterClass import *

decryptFile = None
frame = None

def openFile():
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("MDLINFO", "MDLINFO*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのMDLINFOではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            del decryptFile
            decryptFile = None
            filename = os.path.basename(file_path)
            v_fileName.set(filename)
            
            decryptFile = MdlDecrypt(file_path)
            if not decryptFile.open():
                decryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return

            deleteWidget()
            createWidget()
            viewData(decryptFile.allInfoList)
            copyAnotherBtn['state'] = 'normal'
        except Exception as e:
            print(e)
            mb.showerror(title="エラー", message=errorMsg)

def deleteWidget():
    global mdlInfoLf

    children = mdlInfoLf.winfo_children()
    for child in children:
        child.destroy()

    v_select.set("")

def createWidget():
    global mdlInfoLf
    global frame

    btnList = [getMdlDetailBtn, getMdlImageBtn, getSmfDetailBtn, getBinOrFlagBtn, deleteMdlInfoBtn]

    frame = Scrollbarframe(mdlInfoLf, v_select, btnList)

    col_tuple = ("番号", "smf", "イメージ数", "smf要素数", "binファイル", "フラグ")
    frame.tree['columns'] = col_tuple

    frame.tree.column("#0",width=0, stretch=False)
    frame.tree.column("番号", anchor=CENTER, width=60, stretch=False)
    frame.tree.column("smf", anchor=CENTER)
    frame.tree.column("イメージ数", anchor=CENTER, width=60, stretch=False)
    frame.tree.column("smf要素数", anchor=CENTER, width=80, stretch=False)
    frame.tree.column("binファイル",anchor=CENTER)
    frame.tree.column("フラグ", anchor=CENTER, width=60, stretch=False)

    frame.tree.heading("番号", text="番号",anchor=CENTER)
    frame.tree.heading("smf", text="smf",anchor=CENTER)
    frame.tree.heading("イメージ数", text="イメージ数",anchor=CENTER)
    frame.tree.heading("smf要素数", text="smf要素数",anchor=CENTER)
    frame.tree.heading("binファイル", text="binファイル", anchor=CENTER)
    frame.tree.heading("フラグ", text="フラグ", anchor=CENTER)

    frame.tree["displaycolumns"] = col_tuple

def viewData(allInfoList):
    index = 0
    for mdlInfo in allInfoList:
        binName = "-"
        if mdlInfo["binInfo"][0]:
            binName = mdlInfo["binInfo"][0]
        data = (index+1, mdlInfo["smfName"])
        data += (len(mdlInfo["imgList"]),)
        data += (len(mdlInfo["smfDetailList"]),)
        data += (binName, mdlInfo["binInfo"][1])
        frame.tree.insert(parent='', index='end', iid=index ,values=data)
        index += 1

def getMdlDetailBtn():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])-1
    TreeViewDialog(root, "モデルの詳細情報", num, decryptFile)

def getMdlImage():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])-1
    ImageDialog(root, "モデルのイメージ情報", num, decryptFile)

    decryptFile = decryptFile.reload()
    for i in frame.tree.get_children():
        frame.tree.delete(i)
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)

def getSmfDetail():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])-1
    SmfDetailDialog(root, "smf要素情報", num, decryptFile)

    decryptFile = decryptFile.reload()
    for i in frame.tree.get_children():
        frame.tree.delete(i)
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)

def getBinOrFlag():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])-1
    BinFileOrFlagEditDialog(root, "バイナリファイルとフラグ情報", num, decryptFile)

    decryptFile = decryptFile.reload()
    for i in frame.tree.get_children():
        frame.tree.delete(i)
    viewData(decryptFile.allInfoList)
    frame.tree.selection_set(num)

def copyAnother():
    global decryptFile
    file_path = fd.askopenfilename(filetypes=[("MDLINFO", "MDLINFO*.BIN")])

    errorMsg = "予想外のエラーが出ました。\n電車でDのMDLINFOではない、またはファイルが壊れた可能性があります。"
    if file_path:
        try:
            tempDecryptFile = MdlDecrypt(file_path)
            if not tempDecryptFile.open():
                tempDecryptFile.printError()
                mb.showerror(title="エラー", message=errorMsg)
                return
            
            result = CopyMdlDialog(root, "コピー", tempDecryptFile)
            if result.dirtyFlag:
                copyByteArr = result.copyByteArr
                del tempDecryptFile
                tempDecryptFile = None

                if not decryptFile.copy(copyByteArr):
                    self.decryptFile.printError()
                    mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                    return
                mb.showinfo(title="成功", message="コピーしました")
                
                decryptFile = decryptFile.reload()
                for i in frame.tree.get_children():
                    frame.tree.delete(i)
                viewData(decryptFile.allInfoList)
            
        except Exception as e:
            print(e)
            mb.showerror(title="エラー", message=errorMsg)

def deleteMdlInfo():
    global frame
    global decryptFile
    selectId = int(frame.tree.selection()[0])
    selectItem = frame.tree.set(selectId)
    num = int(selectItem["番号"])-1

    warnMsg = "{0}番のモデル情報を削除しますか？".format(num+1)
    result = mb.askokcancel(message=warnMsg, icon="warning")
    if result:
        if not decryptFile.delete(num):
            decryptFile.printError()
            mb.showerror(title="エラー", message="予想外のエラーが発生しました")
        mb.showinfo(title="成功", message="モデル要素情報を修正しました")

        decryptFile = decryptFile.reload()
        for i in frame.tree.get_children():
            frame.tree.delete(i)
        viewData(decryptFile.allInfoList)

        num -= 1
        if num >= 0:
            frame.tree.selection_set(num)

root = Tk()
root.title("電車でD MDLINFO 改造 1.0.0")
root.geometry("960x640")

menubar = Menu(root)
menubar.add_cascade(label='ファイルを開く', command= lambda: openFile())
root.config(menu=menubar)

v_fileName = StringVar()
fileNameEt = ttk.Entry(root, textvariable=v_fileName, font=("",14), width=20, state="readonly", justify="center")
fileNameEt.place(relx=0.053, rely=0.03)

selectLb = ttk.Label(text="選択した行番号：", font=("",14))
selectLb.place(relx=0.05, rely=0.11)

v_select = StringVar()
selectEt = ttk.Entry(root, textvariable=v_select, font=("",14), width=5, state="readonly", justify="center")
selectEt.place(relx=0.22, rely=0.11)

mdlInfoLf = ttk.LabelFrame(root, text="MDLINFO内容")
mdlInfoLf.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.70)

getMdlDetailBtn = ttk.Button(root, text="選択したモデルの詳細情報", width=25, state="disabled", command=getMdlDetailBtn)
getMdlDetailBtn.place(relx=0.32, rely=0.03)

getMdlImageBtn = ttk.Button(root, text="選択したモデルのイメージ情報", width=25, state="disabled", command=getMdlImage)
getMdlImageBtn.place(relx=0.55, rely=0.03)

getSmfDetailBtn = ttk.Button(root, text="選択したモデルのsmf要素情報", width=25, state="disabled", command=getSmfDetail)
getSmfDetailBtn.place(relx=0.78, rely=0.03)

getBinOrFlagBtn = ttk.Button(root, text="binファイル、フラグ修正", width=25, state="disabled", command=getBinOrFlag)
getBinOrFlagBtn.place(relx=0.32, rely=0.11)

copyAnotherBtn = ttk.Button(root, text="別のMDLINFOからコピーする", width=25, state="disabled", command=copyAnother)
copyAnotherBtn.place(relx=0.55, rely=0.11)

deleteMdlInfoBtn = ttk.Button(root, text="選択したモデル情報を削除する", width=25, state="disabled", command=deleteMdlInfo)
deleteMdlInfoBtn.place(relx=0.78, rely=0.11)

root.mainloop()
