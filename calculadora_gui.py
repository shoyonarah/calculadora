"""
Calculadora Científica (interface gráfica)
==========================================

Uma calculadora com interface gráfica em Tkinter, com visual e funções
parecidos com a calculadora científica do Google.

Recursos:
  - Operações básicas: + - x /
  - Potência (x^y), raiz quadrada, fatorial (x!), porcentagem
  - Funções: sin, cos, tan (e inversas com "Inv"), ln, log, EXP
  - Constantes: π e e
  - Modo Rad/Deg para as funções trigonométricas
  - Parênteses, "Ans" (último resultado) e preview do resultado ao vivo
  - Teclado: digite os números/operadores, Enter = igual, Backspace apaga,
    Esc limpa tudo

Não precisa instalar nada (Tkinter já vem com o Python). Para rodar:

    python calculadora_gui.py

Autor: shoyonarah (Jailson Junior)
"""

import tkinter as tk
import math
import re

# ----------------------------------------------------------------------
# Paleta de cores (inspirada na calculadora do Google, tema escuro)
# ----------------------------------------------------------------------
BG        = "#202124"   # fundo da janela / display
EXPR_FG   = "#9aa0a6"   # texto da expressão (cinza)
RESULT_FG = "#e8eaed"   # resultado (branco)
SCI_BG    = "#2b2c2f"   # botões científicos
SCI_FG    = "#9aa0a6"
NUM_BG    = "#3c4043"   # números
NUM_FG    = "#e8eaed"
OP_FG     = "#8ab4f8"   # operadores (azul)
AC_FG     = "#f28b82"   # botão AC (vermelho)
EQ_BG     = "#8ab4f8"   # igual (azul preenchido)
EQ_FG     = "#202124"


def lighten(hex_color, amount=18):
    """Clareia uma cor (usado no efeito hover dos botões)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = min(255, r + amount), min(255, g + amount), min(255, b + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


class Calculadora:
    def __init__(self, root):
        self.root = root
        self.tokens = []          # lista de tokens {disp, code, kind}
        self.ans = 0              # último resultado
        self.deg_mode = True      # Deg por padrão (igual ao Google)
        self.inv = False          # modo inverso (Inv)
        self.just_eval = False    # acabou de apertar "="

        root.title("Calculadora")
        root.configure(bg=BG)
        root.geometry("380x600")
        root.minsize(320, 520)

        self._build_display()
        self._build_buttons()
        self.set_mode(True)       # destaca "Deg"

        root.bind("<Key>", self.on_key)

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _build_display(self):
        self.expr_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="0")

        disp = tk.Frame(self.root, bg=BG)
        disp.pack(fill="x", padx=20, pady=(22, 8))

        tk.Label(disp, textvariable=self.expr_var, anchor="e", bg=BG,
                 fg=EXPR_FG, font=("Segoe UI", 15)).pack(fill="x")
        tk.Label(disp, textvariable=self.result_var, anchor="e", bg=BG,
                 fg=RESULT_FG, font=("Segoe UI", 32, "bold")).pack(fill="x", pady=(4, 0))

    def _mk(self, parent, text, r, c, cat, cmd, hover=True):
        colors = {
            "sci": (SCI_BG, SCI_FG),
            "num": (NUM_BG, NUM_FG),
            "op":  (NUM_BG, OP_FG),
            "ac":  (NUM_BG, AC_FG),
            "eq":  (EQ_BG, EQ_FG),
        }
        bg, fg = colors[cat]
        font = ("Segoe UI", 13) if cat == "sci" else ("Segoe UI", 17)
        b = tk.Button(parent, text=text, bg=bg, fg=fg, font=font, bd=0,
                      relief="flat", command=cmd, cursor="hand2",
                      activebackground=lighten(bg), activeforeground=fg)
        b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
        if hover:
            hb = lighten(bg)
            b.bind("<Enter>", lambda e, w=b, col=hb: w.config(bg=col))
            b.bind("<Leave>", lambda e, w=b, col=bg: w.config(bg=col))
        return b

    def _build_buttons(self):
        grid = tk.Frame(self.root, bg=BG)
        grid.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        for i in range(5):
            grid.rowconfigure(i, weight=1)
        for j in range(7):
            grid.columnconfigure(j, weight=1)

        m = lambda *a, **k: self._mk(grid, *a, **k)

        # ---- Linha 0 ----
        self.btn_rad = m("Rad", 0, 0, "sci", lambda: self.set_mode(False))
        self.btn_deg = m("Deg", 0, 1, "sci", lambda: self.set_mode(True))
        m("x!", 0, 2, "sci", lambda: self.add_token("!", "!", "post"))
        m("(", 0, 3, "sci", lambda: self.add_token("(", "(", "open"))
        m(")", 0, 4, "sci", lambda: self.add_token(")", ")", "close"))
        m("%", 0, 5, "op", lambda: self.add_token("%", "/100", "op"))
        m("AC", 0, 6, "ac", self.clear)

        # ---- Linha 1 ----
        self.btn_inv = m("Inv", 1, 0, "sci", self.toggle_inv, hover=False)
        self.btn_sin = m("sin", 1, 1, "sci", self.on_sin)
        self.btn_ln = m("ln", 1, 2, "sci", self.on_ln)
        m("7", 1, 3, "num", lambda: self.press_digit("7"))
        m("8", 1, 4, "num", lambda: self.press_digit("8"))
        m("9", 1, 5, "num", lambda: self.press_digit("9"))
        m("÷", 1, 6, "op", lambda: self.press_op("÷", "/"))

        # ---- Linha 2 ----
        m("π", 2, 0, "sci", lambda: self.add_token("π", "pi", "const"))
        self.btn_cos = m("cos", 2, 1, "sci", self.on_cos)
        self.btn_log = m("log", 2, 2, "sci", self.on_log)
        m("4", 2, 3, "num", lambda: self.press_digit("4"))
        m("5", 2, 4, "num", lambda: self.press_digit("5"))
        m("6", 2, 5, "num", lambda: self.press_digit("6"))
        m("×", 2, 6, "op", lambda: self.press_op("×", "*"))

        # ---- Linha 3 ----
        m("e", 3, 0, "sci", lambda: self.add_token("e", "e", "const"))
        self.btn_tan = m("tan", 3, 1, "sci", self.on_tan)
        self.btn_sqrt = m("√", 3, 2, "sci", self.on_sqrt)
        m("1", 3, 3, "num", lambda: self.press_digit("1"))
        m("2", 3, 4, "num", lambda: self.press_digit("2"))
        m("3", 3, 5, "num", lambda: self.press_digit("3"))
        m("−", 3, 6, "op", lambda: self.press_op("−", "-"))

        # ---- Linha 4 ----
        m("Ans", 4, 0, "sci", self.press_ans)
        m("EXP", 4, 1, "sci", lambda: self.add_token("×10^", "*10**", "op"))
        m("xʸ", 4, 2, "sci", lambda: self.press_op("^", "**"))
        m("0", 4, 3, "num", lambda: self.press_digit("0"))
        m(".", 4, 4, "num", self.press_dot)
        m("=", 4, 5, "eq", self.equals)
        m("+", 4, 6, "op", lambda: self.press_op("+", "+"))

    # ------------------------------------------------------------------
    # Lógica de entrada (tokens)
    # ------------------------------------------------------------------
    def add_token(self, disp, code, kind):
        if self.just_eval:
            # ao começar um novo valor depois de "=", recomeça do zero
            if kind in ("num", "const", "func", "open"):
                self.tokens = []
            self.just_eval = False

        prev = self.tokens[-1] if self.tokens else None

        # dígitos seguidos formam um único número
        if kind == "num" and prev and prev["kind"] == "num":
            prev["disp"] += disp
            prev["code"] += code
            self.update()
            return

        # multiplicação implícita: 2π -> 2×π, )( -> )×(, 2sin( -> 2×sin( ...
        if prev:
            need = False
            if kind in ("open", "func", "const", "num") and prev["kind"] in ("const", "close", "post"):
                need = True
            if kind in ("open", "func", "const") and prev["kind"] == "num":
                need = True
            if need:
                self.tokens.append({"disp": "×", "code": "*", "kind": "op"})

        self.tokens.append({"disp": disp, "code": code, "kind": kind})
        self.update()

    def press_digit(self, d):
        self.add_token(d, d, "num")

    def press_dot(self):
        if self.just_eval:
            self.tokens = []
            self.just_eval = False
        prev = self.tokens[-1] if self.tokens else None
        if prev and prev["kind"] == "num" and "." not in prev["code"]:
            prev["disp"] += "."
            prev["code"] += "."
        elif not prev or prev["kind"] != "num":
            self.tokens.append({"disp": "0.", "code": "0.", "kind": "num"})
        self.update()

    def press_op(self, disp, code):
        if self.just_eval:
            # continua a conta a partir do último resultado
            self.tokens = [{"disp": self.fmt(self.ans), "code": repr(self.ans), "kind": "num"}]
            self.just_eval = False
        # troca o operador se o último token já for um operador
        if self.tokens and self.tokens[-1]["kind"] == "op":
            self.tokens.pop()
        if not self.tokens:
            return  # não começa com operador
        self.tokens.append({"disp": disp, "code": code, "kind": "op"})
        self.update()

    def press_ans(self):
        self.add_token("Ans", repr(self.ans), "const")

    # ---- funções científicas (respeitam o modo Inv) ----
    def on_sin(self):
        self.add_token("sin⁻¹(", "asin(", "func") if self.inv else self.add_token("sin(", "sin(", "func")

    def on_cos(self):
        self.add_token("cos⁻¹(", "acos(", "func") if self.inv else self.add_token("cos(", "cos(", "func")

    def on_tan(self):
        self.add_token("tan⁻¹(", "atan(", "func") if self.inv else self.add_token("tan(", "tan(", "func")

    def on_ln(self):
        self.add_token("e^(", "e**(", "func") if self.inv else self.add_token("ln(", "log(", "func")

    def on_log(self):
        self.add_token("10^(", "10**(", "func") if self.inv else self.add_token("log(", "log10(", "func")

    def on_sqrt(self):
        if self.inv:
            self.add_token("²", "**2", "op")    # inverso da raiz = x²
        else:
            self.add_token("√(", "sqrt(", "func")

    def toggle_inv(self):
        self.inv = not self.inv
        self.btn_inv.config(bg=(OP_FG if self.inv else SCI_BG),
                            fg=(EQ_FG if self.inv else SCI_FG))
        pairs = [(self.btn_sin, "sin", "sin⁻¹"), (self.btn_cos, "cos", "cos⁻¹"),
                 (self.btn_tan, "tan", "tan⁻¹"), (self.btn_ln, "ln", "eˣ"),
                 (self.btn_log, "log", "10ˣ"), (self.btn_sqrt, "√", "x²")]
        for b, normal, inv in pairs:
            b.config(text=(inv if self.inv else normal))

    def set_mode(self, deg):
        self.deg_mode = deg
        self.btn_deg.config(fg=(OP_FG if deg else SCI_FG))
        self.btn_rad.config(fg=(OP_FG if not deg else SCI_FG))
        self.update()

    def backspace(self):
        if self.just_eval:
            self.clear()
            return
        if not self.tokens:
            return
        t = self.tokens[-1]
        if t["kind"] == "num" and len(t["code"]) > 1:
            t["disp"] = t["disp"][:-1]
            t["code"] = t["code"][:-1]
        else:
            self.tokens.pop()
        self.update()

    def clear(self):
        self.tokens = []
        self.just_eval = False
        self.expr_var.set("")
        self.result_var.set("0")

    # ------------------------------------------------------------------
    # Avaliação da expressão
    # ------------------------------------------------------------------
    def code_str(self):
        return "".join(t["code"] for t in self.tokens)

    def display_str(self):
        return "".join(t["disp"] for t in self.tokens)

    def _balance(self, code):
        """Fecha parênteses que ficaram abertos (para o preview)."""
        diff = code.count("(") - code.count(")")
        return code + ")" * diff if diff > 0 else code

    def evaluate(self, code):
        code = self._balance(code)
        code = re.sub(r"(\d+\.?\d*)!", r"fact(\1)", code)   # 5! -> fact(5)

        deg = self.deg_mode
        to_rad = (lambda a: math.radians(a)) if deg else (lambda a: a)
        from_rad = (lambda a: math.degrees(a)) if deg else (lambda a: a)

        ns = {
            "sin": lambda x: math.sin(to_rad(x)),
            "cos": lambda x: math.cos(to_rad(x)),
            "tan": lambda x: math.tan(to_rad(x)),
            "asin": lambda x: from_rad(math.asin(x)),
            "acos": lambda x: from_rad(math.acos(x)),
            "atan": lambda x: from_rad(math.atan(x)),
            "sqrt": math.sqrt,
            "log": math.log,        # ln (logaritmo natural)
            "log10": math.log10,    # log base 10
            "fact": lambda x: math.factorial(int(round(x))),
            "pi": math.pi,
            "e": math.e,
        }
        return eval(code, {"__builtins__": {}}, ns)

    def fmt(self, v):
        """Formata o resultado de forma amigável."""
        if isinstance(v, complex):
            return "Erro"
        if v != v:                       # NaN
            return "Erro"
        if v in (float("inf"), float("-inf")):
            return "∞"
        if isinstance(v, float) and v.is_integer() and abs(v) < 1e16:
            return str(int(v))
        return f"{v:.10g}"

    def update(self):
        """Atualiza a expressão e mostra o preview do resultado ao vivo."""
        self.expr_var.set(self.display_str())
        code = self.code_str()
        if not code.strip():
            self.result_var.set("0")
            return
        try:
            self.result_var.set(self.fmt(self.evaluate(code)))
        except Exception:
            self.result_var.set("")     # expressão ainda incompleta

    def equals(self):
        code = self.code_str()
        if not code.strip():
            return
        try:
            val = self.evaluate(code)
        except Exception:
            self.result_var.set("Erro")
            return
        self.ans = val
        self.expr_var.set(self.display_str() + " =")
        self.result_var.set(self.fmt(val))
        self.just_eval = True

    # ------------------------------------------------------------------
    # Teclado
    # ------------------------------------------------------------------
    def on_key(self, event):
        c, k = event.char, event.keysym
        if c in "0123456789":
            self.press_digit(c)
        elif c == ".":
            self.press_dot()
        elif c == "+":
            self.press_op("+", "+")
        elif c == "-":
            self.press_op("−", "-")
        elif c == "*":
            self.press_op("×", "*")
        elif c == "/":
            self.press_op("÷", "/")
        elif c == "^":
            self.press_op("^", "**")
        elif c == "%":
            self.add_token("%", "/100", "op")
        elif c == "(":
            self.add_token("(", "(", "open")
        elif c == ")":
            self.add_token(")", ")", "close")
        elif c == "!":
            self.add_token("!", "!", "post")
        elif k in ("Return", "KP_Enter") or c == "=":
            self.equals()
        elif k == "BackSpace":
            self.backspace()
        elif k == "Escape":
            self.clear()


def main():
    root = tk.Tk()
    Calculadora(root)
    root.mainloop()


if __name__ == "__main__":
    main()
