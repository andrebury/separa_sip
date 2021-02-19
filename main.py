import os
from separa_sip import *

import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory,askopenfilenames, asksaveasfilename



class Application:
    def __init__(self, master=None):
        master_window = tk.Tk()
        master_window.title("SeparaSip")
        self.files = []
        self.log = Log()
        self.listofarqs = []
        self.index = 0
        self.fonte = ("Verdana", "8")

        self.containerCabecalho = tk.Frame(master_window)
        self.containerCabecalho.grid( row=0,padx=10, pady=10,sticky=tk.E+tk.W)


        # self.containerSelecao = tk.Frame(self.containerCabecalho)
        # self.containerSelecao.grid( row=0,column=0,padx=10, pady=10)

        self.containerInterface = tk.Frame(self.containerCabecalho)
        self.containerInterface.grid( row=0,column=1,padx=10, pady=10)

        self.containerTxtANI = tk.Frame(self.containerInterface)
        self.containerTxtANI.grid( row=0,column=0,padx=10, pady=10)

        self.containerTxtANI_1 = tk.Frame(self.containerTxtANI)
        self.containerTxtANI_1.grid( row=0,column=0)

        self.containerTxtANI_2 = tk.Frame(self.containerTxtANI)
        self.containerTxtANI_2.grid( row=0,column=1)

        self.containerBtn = tk.Frame(self.containerInterface)
        self.containerBtn.grid( row=2,column=0,padx=10, pady=10)

        self.containerListBoxTextArea = tk.Frame(master_window)
        self.containerListBoxTextArea.grid(sticky=tk.E+tk.W+tk.N+tk.S,padx=10, pady=10)


        master_window.columnconfigure(0, weight=1)
        master_window.rowconfigure(1, weight=1)

        self.containerListBoxTextArea.rowconfigure(0, weight=1)
        self.containerListBoxTextArea.columnconfigure(0, weight=1)




        # self.listboxCall = tk.Listbox(self.containerSelecao, width=20, height=10, selectmode=tk.SINGLE)
        # self.listboxCall.bind("<Double-Button-1>", self.curseletCall)
        # self.scrollbarCall = tk.Scrollbar(self.containerSelecao, orient="vertical")

        

        self.lblANI = tk.Label(self.containerTxtANI_1, text="ANI:", font=self.fonte, width=15)
        self.lblANI.pack(side=tk.RIGHT)
        self.txtANI = tk.Entry(self.containerTxtANI_2,width=30,font=self.fonte)
        self.txtANI.pack(side=tk.LEFT)

    
  

        self.btnCarrega = tk.Button(self.containerBtn, text="Carrega", font=self.fonte, width=12,command=self.directorychooser)
        self.btnCarrega.pack(side=tk.BOTTOM)
        self.btnSalva = tk.Button(self.containerBtn, text="Salva", font=self.fonte, width=12,command=self.salvaResult)
        
        self.listbox = tk.Listbox(self.containerListBoxTextArea,selectmode=tk.EXTENDED)
        self.listbox.bind("<Double-Button-1>", self.curselet)
        self.scrollbar = tk.Scrollbar(self.containerListBoxTextArea, orient="vertical")


        # self.listbox.pack(side=tk.LEFT,expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        # self.scrollbar.pack(side=tk.RIGHT, fill="y",expand=True)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.listbox.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self.scrollbar.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        # self.listboxCall.pack(side=tk.LEFT)
        # self.scrollbarCall.config(command=self.listboxCall.yview)
        # self.scrollbarCall.pack(side=tk.LEFT, fill="y",expand=True)
        # self.listboxCall.config(yscrollcommand=self.scrollbarCall.set)
        master_window.mainloop()


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
    
    def curseletCall(self, event):
        pass


    def directorychooser(self):
        if len(self.txtANI.get()) > 0:
            # askdirectory é um método do Tkinter que abre uma janela para escolher o diretorio
            self.files = askopenfilenames()
            self.log.arqs = self.files
            self.log.call = self.txtANI.get()
            tamanho_lista = 0
            self.log.openFile()
            
            for linha in self.log.resultadoFinal:
                self.listbox.insert(tamanho_lista,str(linha).replace("\n",""))
                tamanho_lista = tamanho_lista + 1
            self.btnSalva.pack(side=tk.RIGHT)
        else:
            messagebox.showwarning(message="Favor colocar o nome do ANI para busca!")
        
    def salvaResult(self):
        savefilename = asksaveasfilename(
                defaultextension='.log', filetypes=[("log files", '*.log')],
                initialdir=os.path.dirname(self.files[0]),
                title="Escolha o nome do arquivo")
        if len(savefilename) > 1:
            self.log.arquivofinal = savefilename#self.txtarquivofinal.get()
            self.log.defineArqFinal()
            try:
                for linha in self.log.resultadoFinal:
                    self.log.separadow.write(linha)
                messagebox.showinfo(message="Arquivo Salvo com Sucesso")
            except:    
                messagebox.showerror(message="Problemas para salvar no arquivo informado")
        else:
            messagebox.showwarning(message="Favor colocar o nome do arquivo final")

root = Application()

#Application(root)
#root.mainloop()