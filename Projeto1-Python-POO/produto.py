import os
import pickle
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Produto():
  def __init__(self, codigo, valor, descricao):

    self.__codigo = codigo
    self.__valor = valor
    self.__descricao = descricao 
    
  @property
  def codigo(self):
    return self.__codigo

  @property
  def valor(self):
    return self.__valor

  @property
  def descricao(self):
    return self.__descricao


class LimiteCadastrarProduto(tk.Toplevel):
  def __init__(self, controle):

    tk.Toplevel.__init__(self)
    self.geometry('250x100')
    self.title("Cadastra produto")
    self.controle = controle

    self.frameCodigo = tk.Frame(self)
    self.frameCodigo.pack()
    self.frameDescricao = tk.Frame(self)
    self.frameDescricao.pack()
    self.frameValor = tk.Frame(self)
    self.frameValor.pack()
    self.frameButton = tk.Frame(self)
    self.frameButton.pack()
  
    self.labelCodigo = tk.Label(self.frameCodigo, text="Código do produto: ")
    self.labelCodigo.pack(side="left")
    self.inputCodigo = tk.Entry(self.frameCodigo, width=20)
    self.inputCodigo.pack(side="left")

    self.labelDescricao = tk.Label(self.frameDescricao, text="Descrição do produto: ")
    self.labelDescricao.pack(side="left")
    self.inputDescricao = tk.Entry(self.frameDescricao, width=20)
    self.inputDescricao.pack(side="left")
           
    self.labelValor = tk.Label(self.frameValor, text="Valor do produto: ")
    self.labelValor.pack(side="left")
    self.inputValor = tk.Entry(self.frameValor, width=20)
    self.inputValor.pack(side="left")

    self.buttonCadastro = tk.Button(self.frameButton, text="Cadastrar")
    self.buttonCadastro.pack(side="left")
    self.buttonCadastro.bind("<Button>", controle.cadastraHandler)
  
    self.buttonLimpa = tk.Button(self.frameButton, text="Limpa")      
    self.buttonLimpa.pack(side="left")
    self.buttonLimpa.bind("<Button>", controle.limpaHandler)

    self.buttonFecha = tk.Button(self.frameButton, text="Concluído")
    self.buttonFecha.pack(side="left")
    self.buttonFecha.bind("<Button>", controle.fechaHandler)

class LimiteConsultaProduto(tk.Toplevel):
  def __init__(self, controle, listaProd):

    tk.Toplevel.__init__(self)
    self.geometry('250x100')
    self.title("Consulta produto")
    self.controle = controle

    self.frameCodigo = tk.Frame(self)
    self.frameButton = tk.Frame(self)
    self.frameCodigo.pack()
    self.frameButton.pack()
  
    self.labelCodigo = tk.Label(self.frameCodigo, text="Insira o código: ")
    self.labelCodigo.pack(side="left")
    self.escolhaCombo = tk.StringVar()
    self.combobox = ttk.Combobox(self.frameCodigo, width = 15, textvariable = self.escolhaCombo)
    self.combobox.pack(side="left")
    self.combobox['values'] = listaProd

    self.buttonConsulta = tk.Button(self.frameButton, text="Consultar")
    self.buttonConsulta.pack(side="left")
    self.buttonConsulta.bind("<Button>", controle.consultaHandler)

    self.buttonFecha = tk.Button(self.frameButton, text="Concluído")
    self.buttonFecha.pack(side="left")
    self.buttonFecha.bind("<Button>", controle.fechaConsultaHandler)

class CtrlProduto():
  def __init__(self):
    if not os.path.isfile("produto.pickle"):
      self.listaProdutos =  []
    else:
      with open("produto.pickle", "rb") as f:
        self.listaProdutos = pickle.load(f)

  def salvaProdutos(self):
    if len(self.listaProdutos) != 0:
      with open("produto.pickle","wb") as f:
        pickle.dump(self.listaProdutos, f)

  def insereProduto(self):
    self.limiteCad = LimiteCadastrarProduto(self)

  @property
  def listaDescProdutos(self):
    listaDescProdutos = []
    for produto in self.listaProdutos:
      listaDescProdutos.append(produto.descricao)
    return listaDescProdutos

  def addProdutos(self):
    listaProdutos = []
    for produto in self.listaProdutos:
      listaProdutos.append(produto)
    return listaProdutos

  def cadastraHandler(self, event):
    codigo = self.limiteCad.inputCodigo.get()
    descricao = self.limiteCad.inputDescricao.get()
    valor = self.limiteCad.inputValor.get()
    produto = Produto(codigo, descricao, valor)
    for prod in self.listaProdutos:
      if prod.codigo == codigo:
        self.limpaHandler(event)
        return messagebox.showerror("Já Cadastrado", 'Produto já está cadastrado!')
    self.listaProdutos.append(produto)
    messagebox.showinfo("Cadastrado", 'Produto cadastrado!')
    self.limpaHandler(event)

  def limpaHandler(self, event):
    self.limiteCad.inputCodigo.delete(0, len(self.limiteCad.inputCodigo.get()))
    self.limiteCad.inputDescricao.delete(0, len(self.limiteCad.inputDescricao.get()))
    self.limiteCad.inputValor.delete(0, len(self.limiteCad.inputValor.get()))

  def fechaHandler(self, event):
    self.limiteCad.destroy()
  
  def consultaProduto(self):
    listaProd = []
    for produto in self.listaProdutos:
      listaProd.append(produto.codigo)
    self.limiteConsul = LimiteConsultaProduto(self, listaProd)

  def consultaHandler(self, event):
    codigo = self.limiteConsul.escolhaCombo.get()
    msg = ""
    for produto in self.listaProdutos:
      if codigo is not None and codigo == produto.codigo:
        msg = produto.descricao + ' -- ' + 'R$' + produto.valor + '\n'
    messagebox.showinfo('Dados do produtos', msg)

  def fechaConsultaHandler(self, event):
    self.limiteConsul.destroy()