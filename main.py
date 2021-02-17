import os
from tkinter.filedialog import askdirectory
from separa_sip import *
from tkinter import *
from tkinter import messagebox


class Application:
    def __init__(self, master=None):
        self.log = Log()
        self.listofarqs = []
        self.index = 0
        self.fonte = ("Verdana", "8")

        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["pady"] = 10
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 5
        self.container3.pack()

        self.container4 = Frame(master)
        self.container4["padx"] = 10
        self.container4["pady"] = 10
        self.container4.pack()

        self.container5 = Frame(master)
        self.container5["padx"] = 20
        self.container5["pady"] = 5
        self.container5.pack()

        self.container6 = Frame(self.container5)
        self.container6["padx"] = 10
        self.container6["pady"] = 10
        self.container6.pack()

        self.container7 = Frame(self.container5)
        self.container7["padx"] = 10
        self.container7["pady"] = 10
        self.container7.pack()

        self.titulo = Label(self.container1, text="Separa Sip",font=("Calibri", "9", "bold")).pack()

        self.lblarquivofinal = Label(self.container2, text="Arquivo Final:", font=self.fonte, width=12)
        

        self.txtarquivofinal = Entry(self.container2,width=30,font=self.fonte)
        

        self.lblANI = Label(self.container3, text="ANI:", font=self.fonte, width=10).pack(side=LEFT)

        self.txtANI = Entry(self.container3,width=30,font=self.fonte)
        self.txtANI.pack(side=RIGHT)

        self.btnCarrega = Button(self.container4, text="Carrega", font=self.fonte, width=12,command=self.directorychooser)
        self.btnCarrega.pack(side=LEFT)
        self.btnSalva = Button(self.container4, text="Salva", font=self.fonte, width=12,command=self.salvaResult)
        
        self.listbox = Listbox(self.container5, width=200, height=50, selectmode=SINGLE)
        self.listbox.bind("<Double-Button-1>", self.curselet)
        self.scrollbar = Scrollbar(self.container5, orient="vertical")


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


    def directorychooser(self):
        # askdirectory é um método do Tkinter que abre uma janela para escolher o diretorio
        directory = askdirectory()
        os.chdir(directory)
        self.listbox.pack(side=LEFT)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set) 
        self.log.arqs = os.listdir(directory)
        self.log.call = self.txtANI.get()
        tamanho_lista = 0
        self.log.openFile()
        
        for linha in self.log.resultadoFinal:
            self.listbox.insert(tamanho_lista,linha)
            tamanho_lista = tamanho_lista + 1
        self.btnSalva.pack(side=RIGHT)
        self.lblarquivofinal.pack(side=LEFT)
        self.txtarquivofinal.pack(side=RIGHT)
        
    def salvaResult(self):        
        if len(self.txtarquivofinal.get()) > 1:
            self.log.arquivofinal = self.txtarquivofinal.get()
            self.log.defineArqFinal()
            try:
                for linha in self.log.resultadoFinal:
                    self.log.separadow.write(linha)
                messagebox.showinfo(message="Arquivo Salvo com Sucesso")
            except:    
                messagebox.showerror(message="Problemas para salvar no arquivo informado")
                print(sys.exc_info()[0])
        else:
            messagebox.showwarning(message="Favor colocar o nome do arquivo final")

root = Tk()
Application(root)
root.mainloop()