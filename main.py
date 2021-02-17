import os

class Log:

    def __init__(self):
        self.arqs = []
        self.callid = []
        self.bilhetes = []
        self.bilhetes_escolhidos = []
        self.call = ""        
        self.separadow = ""
        self.f = ''
    
    def ArquivoFinal(self):
        self.separadow = open(input("Digite o nome do arquivo final sem extensão: ") + '.log', 'w')
        
    
    def DirecionaFolder(self):
        #self.Folder(str(input("Digite a pasta: ")))
        os.chdir(input("Digite a pasta: "))

    def listArqs(self):
        self.arqs = os.listdir()

    def busca(self):
        self.call = input("Digite o numero: ")


    def criaListaCallid(self,linha):
        if linha.find("Call-ID: ") >= 0:
            callidstr = linha[9:linha.find("@")]
            if callidstr not in self.callid:
                self.callid.append(callidstr)

    def openFile(self):
        for a in self.arqs:
            if a.find("rm_") < 0:
                continue
            with open(a, 'r', encoding='utf-8', errors='ignore') as file:
                self.f = file.readlines()
            file.close()
            self.preencheBilhetes()
            self.preencheBilhetesEscolhidos()

    def preencheBilhetes(self):
        achado = False
        kall = 0
        sip = False
        count = -1

        for linha in self.f:
            if linha.find('CCPSIPMessageInterceptor') > 1:
                kall = len(self.bilhetes)+1
                sip = True
                #fw.write("\n")
                #fw.write(linha)
                self.bilhetes.append("\n")
                self.bilhetes.append(linha)
                achado = False
            else:
                if sip == True and linha.find('2021-') < 0:
                    if len(linha) > 2:
                        count = count + 1
                        #fw.write(linha)
                        self.bilhetes.append(linha)
                        self.criaListaCallid(linha)
                        if linha.find(self.call) > 1 and achado is False:
                            self.bilhetes_escolhidos.append(kall)
                            achado = True
                else:
                    sip = False
                    achado = False
        
    def preencheBilhetesEscolhidos(self):
        for linhab in self.bilhetes_escolhidos:
            acabou = False
            count = linhab
            while acabou is not True:
                if len(str(self.bilhetes[count])) < 3:
                    acabou = True
                    self.separadow.write("\n")
                else:
                    self.separadow.write(self.bilhetes[count])
                    count = count + 1


    def mostraBilhetes(self):
        print("Quantidade de pacotes: " + str(len(self.bilhetes_escolhidos)))
        for b in self.bilhetes_escolhidos:
            print(b)



if __name__ == '__main__':
    log = Log()
    log.DirecionaFolder()
    log.ArquivoFinal()
    log.listArqs()
    log.busca()
    log.openFile()