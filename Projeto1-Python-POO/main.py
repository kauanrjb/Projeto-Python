#Kauan Rajab

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import cupomfiscal
import produto as prod

class LimitePrincipal():
    def __init__(self, root, controle):
        self.controle = controle
        self.root = root
        self.root.geometry('300x250')
        self.menubar = tk.Menu(self.root)
        self.produtoMenu = tk.Menu(self.menubar)
        self.cupomMenu = tk.Menu(self.menubar)
        self.sairMenu = tk.Menu(self.menubar)
        

        self.produtoMenu.add_command(label="Cadastrar", \
                    command=self.controle.insereProduto)
        self.produtoMenu.add_command(label="Consultar", \
                    command=self.controle.consultaProduto)
        self.menubar.add_cascade(label="Produto", \
                    menu=self.produtoMenu)


        self.cupomMenu.add_command(label="Criar", \
                    command=self.controle.criaCupom)
        self.cupomMenu.add_command(label="Consultar", \
                    command=self.controle.consultaCupom)
        self.menubar.add_cascade(label="Cupom", \
                    menu=self.cupomMenu)     


        self.sairMenu.add_command(label="Sair e Salvar", \
                    command=self.controle.salvaDados)
        self.menubar.add_cascade(label="Sair", \
                    menu=self.sairMenu)   

        self.root.config(menu=self.menubar)

class ControlePrincipal():       
    def __init__(self):
        self.root = tk.Tk()
        self.ctrlCupom = cupomfiscal.CtrlCupom(self)
        self.ctrlProduto = prod.CtrlProduto()

        self.limite = LimitePrincipal(self.root, self) 

        self.root.title("Trabalho 14")

        self.root.mainloop()
       
    def criaCupom(self):
        self.ctrlCupom.criaCupom()

    def consultaCupom(self):
        self.ctrlCupom.consultaCupom()

    def insereProduto(self):
        self.ctrlProduto.insereProduto()

    def consultaProduto(self):
        self.ctrlProduto.consultaProduto()

    def salvaDados(self):
        self.ctrlCupom.salvaCupons()
        self.ctrlProduto.salvaProdutos()
        self.root.destroy()

if __name__ == '__main__':
    c = ControlePrincipal()
