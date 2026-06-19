# 🧮 Calculadora em Python

Calculadora feita em Python puro (sem bibliotecas externas), em duas versões:

1. **`calculadora.py`** — versão de terminal (linha de comando)
2. **`calculadora_gui.py`** — versão gráfica científica, com visual parecido com a calculadora do Google

---

## 1. Versão de terminal — `calculadora.py`

Menu simples no terminal com as operações: somar, subtrair, multiplicar, dividir, potência, raiz quadrada e porcentagem. Valida o que o usuário digita (se digitar letra no lugar de número, avisa e pede de novo).

Para rodar:

```bash
python calculadora.py
```

---

## 2. Versão gráfica — `calculadora_gui.py`

Uma calculadora **científica** com interface gráfica (Tkinter), no estilo da calculadora do Google.

Funcionalidades:

- Operações básicas: `+  −  ×  ÷`
- Potência (`xʸ`), raiz quadrada (`√`), fatorial (`x!`) e porcentagem (`%`)
- Funções: `sin`, `cos`, `tan` (e as inversas com o botão **Inv**), `ln`, `log` e `EXP`
- Constantes `π` e `e`
- Modo **Rad / Deg** para as funções trigonométricas
- Parênteses, **Ans** (último resultado) e **preview do resultado ao vivo** enquanto você digita
- Suporte ao teclado: digite números e operadores, **Enter** = igual, **Backspace** apaga, **Esc** limpa tudo

Para rodar:

```bash
python calculadora_gui.py
```

> O Tkinter já vem junto com o Python, então não precisa instalar nada.

---

Feito por [shoyonarah](https://github.com/shoyonarah) 🐱
