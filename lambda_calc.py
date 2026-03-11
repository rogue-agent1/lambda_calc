#!/usr/bin/env python3
"""Lambda calculus reducer."""
import sys
class Var:
    def __init__(self,n): self.n=n
    def __repr__(self): return self.n
class Lam:
    def __init__(self,p,b): self.p,self.b=p,b
    def __repr__(self): return f"(λ{self.p}.{self.b})"
class App:
    def __init__(self,f,a): self.f,self.a=f,a
    def __repr__(self): return f"({self.f} {self.a})"
def subst(expr,name,val):
    if isinstance(expr,Var): return val if expr.n==name else expr
    if isinstance(expr,Lam): return expr if expr.p==name else Lam(expr.p,subst(expr.b,name,val))
    if isinstance(expr,App): return App(subst(expr.f,name,val),subst(expr.a,name,val))
def reduce(expr,depth=0):
    if depth>100: return expr
    if isinstance(expr,App):
        f=reduce(expr.f,depth+1)
        if isinstance(f,Lam): return reduce(subst(f.b,f.p,expr.a),depth+1)
        return App(f,reduce(expr.a,depth+1))
    if isinstance(expr,Lam): return Lam(expr.p,reduce(expr.b,depth+1))
    return expr
# Church numerals demo
zero=Lam('f',Lam('x',Var('x')))
succ=Lam('n',Lam('f',Lam('x',App(Var('f'),App(App(Var('n'),Var('f')),Var('x'))))))
one=reduce(App(succ,zero))
two=reduce(App(succ,one))
print(f"0 = {zero}")
print(f"1 = {one}")
print(f"2 = {two}")
print(f"succ(2) = {reduce(App(succ,two))}")
