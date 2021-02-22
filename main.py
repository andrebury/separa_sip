import os
from separa_sip import *

import tkinter as tk
from tkinter import Listbox, messagebox
from tkinter.filedialog import askdirectory,askopenfilenames, asksaveasfilename

class Application:
    def __init__(self, master_window=None):
        master_window = tk.Tk()
        menubar = tk.Menu(master_window)
        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.openFiles)
        self.filemenu.add_command(label="Save", command=self.salvaResult)
        self.filemenu.add_command(label="Close", command=self.limpar)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master_window.quit)
        menubar.add_cascade(label="File", menu=self.filemenu)
        master_window.config(menu=menubar)

        master_window.title("SeparaSip")
        self.files = []
        self.log = Log()
        self.listofarqs = []
        self.index = 0
        self.fonte = ("Verdana", "8")

        self.containerCabecalho = tk.Frame(master_window)
        self.containerCabecalho.grid( row=0,padx=10, pady=10,sticky=tk.E+tk.W)

        self.containerSelecao = tk.Frame(self.containerCabecalho)
        self.containerSelecao.grid( row=0,column=0,padx=10, pady=10)

        self.containerInterface = tk.Frame(self.containerCabecalho)
        self.containerInterface.grid(row=0,column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        self.containerTxtBUSCA = tk.Frame(self.containerInterface)
        self.containerTxtBUSCA.grid( sticky=tk.E+tk.W+tk.N+tk.S,padx=10, pady=10)

        self.containerTxtBUSCA_1 = tk.Frame(self.containerTxtBUSCA)
        self.containerTxtBUSCA_1.grid( sticky=tk.E+tk.W+tk.N+tk.S,)

        self.containerTxtBUSCA_2 = tk.Frame(self.containerTxtBUSCA)
        self.containerTxtBUSCA_2.grid( sticky=tk.E+tk.W+tk.N+tk.S,)

        self.containerbtnBUSCA = tk.Frame(self.containerTxtBUSCA)
        self.containerbtnBUSCA.grid( sticky=tk.E+tk.W+tk.N+tk.S,pady=2)

        self.containerListBoxTextArea = tk.Frame(master_window)
        self.containerListBoxTextArea.grid(sticky=tk.E+tk.W+tk.N+tk.S,padx=10, pady=10)

        master_window.columnconfigure(0, weight=1)
        master_window.rowconfigure(1, weight=1)

        self.containerListBoxTextArea.rowconfigure(0, weight=1)
        self.containerListBoxTextArea.columnconfigure(0, weight=1)


        self.listboxCall = tk.Listbox(self.containerSelecao, width=60, height=10, selectmode=tk.SINGLE)
        self.listboxCall.bind("<Double-Button-1>", self.curseletCall)
        self.scrollbarCall = tk.Scrollbar(self.containerSelecao, orient="vertical")

        self.lblBUSCA = tk.Label(self.containerTxtBUSCA_1, text="BUSCAR:", font=self.fonte, width=8)
        self.lblBUSCA.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)

        self.txtBUSCA = tk.Entry(self.containerTxtBUSCA_2,width=30,font=self.fonte)
        self.txtBUSCA.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.btnBUSCA = tk.Button(self.containerbtnBUSCA,text="BUSCAR",width=15,font=self.fonte,command=self.buscaCall)
        self.btnBUSCA.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.listbox = tk.Listbox(self.containerListBoxTextArea,selectmode=tk.EXTENDED)
        self.listbox.bind("<Double-Button-1>", self.curselet)
        self.scrollbar = tk.Scrollbar(self.containerListBoxTextArea, orient="vertical")

        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.listbox.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self.scrollbar.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        self.listboxCall.pack(side=tk.LEFT)
        self.listboxCall.config(yscrollcommand=self.scrollbarCall.set)

        self.scrollbarCall.config(command=self.listboxCall.yview)
        self.scrollbarCall.pack(side=tk.LEFT, fill="y",expand=True)

        master_window.mainloop()

    def limpar(self):
        self.listbox.delete (0,self.listbox.size())
        self.listboxCall.delete (0,self.listbox.size())

    def destacaTexto(self):
        tamanho_lista = 0
        for linha in self.log.resultadoFinal:
            self.listbox.insert(tamanho_lista,linha)
            if "RM - SIP Message " in linha:
                self.listbox.itemconfig(tamanho_lista)
            elif self.log.call in linha:
                self.listbox.itemconfig(tamanho_lista, bg = "green")
            else:
                self.listbox.itemconfig(tamanho_lista, bg = "white")
            tamanho_lista += 1

    def curselet(self, event):
        widget = event.widget
        selection = widget.curselection()
        self.index = selection[0]

    def mostraConteudoPacote(self,chamada):
        self.listbox.delete(0,self.listbox.size())
        self.log.resultadoFinal = []
        bilhete = Pacote()
        for bilhete in self.log.bilhetes:
            if bilhete.id == chamada:
                for linha in bilhete.conteudo:
                    self.listbox.insert(self.listbox.size(),str(linha).replace("\n",""))
                self.listbox.insert(self.listbox.size(),"\n")
            bilhete = Pacote()


    def curseletCall(self, event):
        widget = event.widget
        selection = widget.curselection()
        chamada = self.listboxCall.get(selection[0])
        self.mostraConteudoPacote(chamada)


    def buscaCall(self):
        count = 0
        callBusca = self.txtBUSCA.get()
        self.mostraConteudoPacote(callBusca)

    def openFiles(self):
        self.files = askopenfilenames()
        #self.log.arqs = self.files
        #self.log.call = self.txtBUSCA.get()
        for a in self.files:
            with open(a, 'r', encoding='utf-8', errors='ignore') as file:
                self.log.f = file.readlines()
                for linha in range(0,30):
                    if self.log.f[linha].find("CFGGVPResourceMgr") > 0:
                        self.log.appType = "RM"
                for linha in range(0,30):
                    if self.log.f[linha].find("TServer") > 0:
                        self.log.appType = "SIPServer"
            file.close()
            self.log.preencheBilhetes(self.log.f)
        # for linha in self.f:
        #     self.listbox.insert(self.listbox.size(),str(linha).replace("\n",""))
        
        for id in self.log.callid:
            self.listboxCall.insert(self.listbox.size(),str(id).replace("\n",""))
        # pass
        # self.log.openFile()
        

        # for linha in self.log.resultadoFinal:
        #     self.listbox.insert(self.listbox.size(),str(linha).replace("\n",""))
   
    
    def salvaResult(self):
        savefilename = asksaveasfilename(
                defaultextension='.log', filetypes=[("log files", '*.log')],
                initialdir=os.path.dirname(self.files[0]),
                title="Escolha o nome do arquivo")
        if len(savefilename) > 1:
            self.log.arquivofinal = savefilename
            self.log.defineArqFinal()
            try:
                for linha in self.log.resultadoFinal:
                    self.log.separadow.write(linha)
                messagebox.showinfo(message="Arquivo Salvo com Sucesso")
            except:    
                messagebox.showerror(message="Problemas para salvar no arquivo informado")
        else:
            messagebox.showwarning(message="Favor colocar o nome do arquivo final")

if __name__ == "__main__":
    root = Application()
