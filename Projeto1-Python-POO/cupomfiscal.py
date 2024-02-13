import os
import pickle
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

class CupomFiscal():
  def __init__(self, itensCupom, nroCupom):
    self.__itensCupom = itensCupom
    self.__nroCupom = nroCupom

  @property
  def itensCupom(self):
    return self.__itensCupom

  @property
  def nroCupom(self):
    return self.__nroCupom


class ProdutoContabilizado():
  def __init__(self, produto, nroRepeticoes):
    self.__produto = produto
    self.__nroRepeticoes = nroRepeticoes

  @property
  def produto(self):
    return self.__produto

  @property
  def nroRepeticoes(self):
    return self.__nroRepeticoes

class LimiteCriaCupomFiscal(tk.Toplevel):
  def __init__(self, controle, listaCodItens):

    tk.Toplevel.__init__(self)
    self.geometry('250x100')
    self.title("Cria cupom")
    self.controle = controle
    self.frameNro = tk.Frame(self)
    self.frameNro.pack()
    self.frameEscolheItem = tk.Frame(self)
    self.frameEscolheItem.pack()
    self.frameButton = tk.Frame(self)
    self.frameButton.pack()
  
  
    self.labelNro = tk.Label(self.frameNro, text="Número do cupom fiscal: ")
    self.labelNro.pack(side="left")
    self.inputNro = tk.Entry(self.frameNro, width=20)
    self.inputNro.pack(side="left")

  
    self.labelEscolheItem = tk.Label(self.frameEscolheItem, text="Escolha o produto: ")
    self.labelEscolheItem.pack(side="left")
    self.escolhaCombo = tk.StringVar()
    self.combobox = ttk.Combobox(self.frameEscolheItem, width = 15, textvariable = self.escolhaCombo)
    self.combobox.pack(side="left")
    self.combobox['values'] = listaCodItens


    self.buttonAdiciona = tk.Button(self.frameButton, text="Adicionar produto")
    self.buttonAdiciona.pack(side="left")
    self.buttonAdiciona.bind("<Button>", controle.adicionaHandler)
  
    self.buttonCria = tk.Button(self.frameButton, text="Fecha cupom")
    self.buttonCria.pack(side="left")
    self.buttonCria.bind("<Button>", controle.criaHandler)

    self.buttonFecha = tk.Button(self.frameButton, text="Concluído")
    self.buttonFecha.pack(side="left")
    self.buttonFecha.bind("<Button>", controle.fechaHandler)

class LimiteConsultaCupom(tk.Toplevel):
  def __init__(self, controle, listaCupom):

    tk.Toplevel.__init__(self)
    self.geometry('250x100')
    self.title("Consulta cupom")
    self.controle = controle
    self.frameNro = tk.Frame(self)
    self.frameNro.pack()
    self.frameButton = tk.Frame(self)
    self.frameButton.pack()

 
    self.labelNro = tk.Label(self.frameNro, text="Número do cupom fiscal: ")
    self.labelNro.pack(side="left")
    self.escolhaCombo = tk.StringVar()
    self.combobox = ttk.Combobox(self.frameNro, width = 15, textvariable = self.escolhaCombo)
    self.combobox.pack(side="left")
    self.combobox['values'] = listaCupom


    self.buttonConsulta = tk.Button(self.frameButton, text="Consultar cupom")
    self.buttonConsulta.pack(side="left")
    self.buttonConsulta.bind("<Button>", controle.consultaHandler)
  
    self.buttonFecha = tk.Button(self.frameButton, text="Concluído")      
    self.buttonFecha.pack(side="left")
    self.buttonFecha.bind("<Button>", controle.fechaConsulHandler)

class CtrlCupom():

  def __init__(self, controlePrincipal):
    self.ctrlPrincipal = controlePrincipal

    if not os.path.isfile("cupom.pickle"):
      self.listaCupons =  []
    else:
      with open("cupom.pickle", "rb") as f:
        self.listaCupons = pickle.load(f)

  def salvaCupons(self):
    if len(self.listaCupons) != 0:
      with open("cupom.pickle", "wb") as f:
        pickle.dump(self.listaCupons, f)

  def criaCupom(self):
    self.listaProdutoAdd = []
    self.limiteCria = LimiteCriaCupomFiscal(self, self.ctrlPrincipal.ctrlProduto.listaDescProdutos)

  def criaHandler(self, event):
    nroCupom = self.limiteCria.inputNro.get()
    cupom = CupomFiscal(nroCupom, self.listaProdutoAdd)
    for cup in self.listaCupons:
      if cup.nroCupom == nroCupom:
        return messagebox.showerror('Atenção', 'Cupom já cadastrado')
    self.listaCupons.append(cupom)
    messagebox.showinfo('Sucesso', 'Cupom cadastrado')
    self.limiteCria.destroy()

  def adicionaHandler(self, event):
    nroCupom = self.limiteCria.inputNro.get()
    produtoSel = self.limiteCria.escolhaCombo.get()
    listaProdutos = []
    listaProdutos = self.ctrlPrincipal.ctrlProduto.addProdutos()
    for cup in self.listaCupons:
      if cup.nroCupom == nroCupom:
        return messagebox.showerror('Atenção', 'Cupom já cadastrado')
    for produto in listaProdutos:
      if produto.descricao == produtoSel:
        self.listaProdutoAdd.append(produto)
        return messagebox.showinfo('Sucesso', 'Produto adicionado')

  def fechaHandler(self, event):
    self.limiteCria.destroy()

  def consultaCupom(self):
    listaCup = []
    for cupom in self.listaCupons:
      listaCup.append(cupom.nroCupom)
    self.limiteConsul = LimiteConsultaCupom(self, listaCup)

  def consultaHandler(self, event):
    nroCupom = self.limiteConsul.escolhaCombo.get()
    msg = ''
    total = 0 
    dentro = False 
    self.produtosContabilizados = []
    for cupons in self.listaCupons:
      if nroCupom is not None and nroCupom == cupons.nroCupom:
        msg = 'O número do cupom é ' + nroCupom + '\n'
        for itens in cupons.itensCupom:
          repeticoes = cupons.itensCupom.count(itens)
          for i in self.produtosContabilizados:
            if itens.codigo == i.produto.codigo:
              dentro = True
          if dentro is False:
            self.produtosContabilizados.append(ProdutoContabilizado(itens, repeticoes))
          dentro = False
        for prod in self.produtosContabilizados:
          msg += str(prod.nroRepeticoes) + 'x ' + prod.produto.codigo + ' -- ' + prod.produto.descricao + ' -- ' + 'R$' + prod.produto.valor + '\n'
          total += (float(prod.produto.valor)*prod.nroRepeticoes)
        msg += 'O valor total é R$' + str(total)
    if msg == '':
      messagebox.showerror('Aviso!', 'Cupom não encontrado')
    else:
      messagebox.showinfo('Sucesso', msg)

  def fechaConsulHandler(self, event):
    self.limiteConsul.destroy()
