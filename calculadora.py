"""
Calculadora de terminal
=======================

Um utilitário simples de linha de comando que faz operações
matemáticas básicas e algumas extras. Roda em qualquer máquina
com Python 3 instalado:

    python calculadora.py

Autor: shoyonarah (Jailson Junior)
"""

import math


def ler_numero(mensagem):
    """Pede um número ao usuário e só retorna quando ele digitar algo válido."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            return float(entrada)
        except ValueError:
            print("  ! Valor inválido. Digite um número (ex: 12 ou 3.5).")


def formatar(resultado):
    """Mostra 7 sem casas decimais quando o número é inteiro (7 em vez de 7.0)."""
    if isinstance(resultado, float) and resultado.is_integer():
        return str(int(resultado))
    return str(round(resultado, 8))


def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("Não dá para dividir por zero.")
    return a / b


def potencia(a, b):
    return a ** b


def raiz_quadrada(a):
    if a < 0:
        raise ValueError("Não existe raiz quadrada real de número negativo.")
    return math.sqrt(a)


def porcentagem(valor, percentual):
    """Calcula 'percentual'% de 'valor'. Ex: 20% de 150 = 30."""
    return valor * percentual / 100


MENU = """
====================================
        CALCULADORA EM PYTHON
====================================
  1) Somar           (+)
  2) Subtrair        (-)
  3) Multiplicar     (x)
  4) Dividir         (/)
  5) Potência        (a^b)
  6) Raiz quadrada   (V)
  7) Porcentagem     (%)
  0) Sair
====================================
"""


def main():
    print("Bem-vindo(a) à calculadora! 🧮")

    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até a próxima! 👋")
            break

        try:
            if opcao == "1":
                a, b = ler_numero("Primeiro número: "), ler_numero("Segundo número: ")
                print(f"\n>> {formatar(a)} + {formatar(b)} = {formatar(somar(a, b))}")

            elif opcao == "2":
                a, b = ler_numero("Primeiro número: "), ler_numero("Segundo número: ")
                print(f"\n>> {formatar(a)} - {formatar(b)} = {formatar(subtrair(a, b))}")

            elif opcao == "3":
                a, b = ler_numero("Primeiro número: "), ler_numero("Segundo número: ")
                print(f"\n>> {formatar(a)} x {formatar(b)} = {formatar(multiplicar(a, b))}")

            elif opcao == "4":
                a, b = ler_numero("Dividendo: "), ler_numero("Divisor: ")
                print(f"\n>> {formatar(a)} / {formatar(b)} = {formatar(dividir(a, b))}")

            elif opcao == "5":
                a, b = ler_numero("Base: "), ler_numero("Expoente: ")
                print(f"\n>> {formatar(a)} ^ {formatar(b)} = {formatar(potencia(a, b))}")

            elif opcao == "6":
                a = ler_numero("Número: ")
                print(f"\n>> raiz de {formatar(a)} = {formatar(raiz_quadrada(a))}")

            elif opcao == "7":
                valor = ler_numero("Valor total: ")
                pct = ler_numero("Quantos %? ")
                print(f"\n>> {formatar(pct)}% de {formatar(valor)} = {formatar(porcentagem(valor, pct))}")

            else:
                print("Opção inválida. Escolha um número do menu.")

        except (ZeroDivisionError, ValueError) as erro:
            print(f"\n  ! Erro: {erro}")


if __name__ == "__main__":
    main()
