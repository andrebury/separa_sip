import os
#os.chdir(os.path("C:\\Users\\abury\\Documents\\Evidências\\Empresas\\Cielo\\nice_12-06-2017\\bad_call_rm1\\"))
os.chdir(input("Digite a pasta: "))
arqs = os.listdir()
print(os.getcwd())
sip = False
callid = []
callidstr = ''
#fw = open('teste.log', 'w')
bilhetes = []
bilhetes_escolhidos = []
call = input("Digite o numero: ")
kall = 0
achou = False
achado = False
separadoFileName = input("Digite o nome do arquivo final sem extensão: ")
separadow = open(separadoFileName + '.log', 'w')

def criaListaCallid(linha):
    if linha.find("Call-ID: ") >= 0:
        callidstr = linha[9:linha.find("@")]
        if callidstr not in callid:
            callid.append(callidstr)
print(arqs)
count = -1
for a in arqs:
    if a.find("rm_") < 0:
        continue
    with open(a, 'r', encoding='utf-8', errors='ignore') as file:
        f = file.readlines()
    file.close()
    for linha in f:
        if linha.find('CCPSIPMessageInterceptor') > 1:
            kall = len(bilhetes)+1
            sip = True
            #fw.write("\n")
            #fw.write(linha)
            bilhetes.append("\n")
            bilhetes.append(linha)
            achado = False
        else:
            if sip == True and linha.find('2017-') < 0:
                if len(linha) > 2:
                    count = count + 1
                    #fw.write(linha)
                    bilhetes.append(linha)
                    criaListaCallid(linha)
                    if linha.find(call) > 1 and achado is False:
                        bilhetes_escolhidos.append(kall)
                        achado = True
            else:
                sip = False
                achado = False

    for linhab in bilhetes_escolhidos:
        acabou = False
        count = linhab
        while acabou is not True:
            if len(str(bilhetes[count])) < 3:
                acabou = True
                separadow.write("\n")
            else:
                separadow.write(bilhetes[count])
                count = count + 1
    bilhetes = []
#fw.close()
print("Quantidade de pacotes: " + str(len(bilhetes_escolhidos)))
separadow.close()

