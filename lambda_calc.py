#!/usr/bin/env python3
"""lambda_calc — Lambda calculus interpreter with Church encodings. Zero deps."""

class Var:
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name
    def __eq__(self, o): return isinstance(o, Var) and o.name == self.name

class Lam:
    def __init__(self, param, body): self.param, self.body = param, body
    def __repr__(self): return f"(λ{self.param}.{self.body})"

class App:
    def __init__(self, fn, arg): self.fn, self.arg = fn, arg
    def __repr__(self): return f"({self.fn} {self.arg})"

def subst(expr, name, value):
    if isinstance(expr, Var):
        return value if expr.name == name else expr
    if isinstance(expr, Lam):
        if expr.param == name: return expr
        return Lam(expr.param, subst(expr.body, name, value))
    if isinstance(expr, App):
        return App(subst(expr.fn, name, value), subst(expr.arg, name, value))

def beta_reduce(expr, max_steps=100):
    for _ in range(max_steps):
        reduced = _step(expr)
        if reduced is None: return expr
        expr = reduced
    return expr

def _step(expr):
    if isinstance(expr, App):
        if isinstance(expr.fn, Lam):
            return subst(expr.fn.body, expr.fn.param, expr.arg)
        fn_step = _step(expr.fn)
        if fn_step: return App(fn_step, expr.arg)
        arg_step = _step(expr.arg)
        if arg_step: return App(expr.fn, arg_step)
    if isinstance(expr, Lam):
        body_step = _step(expr.body)
        if body_step: return Lam(expr.param, body_step)
    return None

# Church encodings
def church(n):
    body = Var("x")
    for _ in range(n):
        body = App(Var("f"), body)
    return Lam("f", Lam("x", body))

def unchurch(expr):
    expr = beta_reduce(expr)
    count = [0]
    def counter(_): count[0] += 1; return count[0]
    # Manual evaluation
    body = expr
    n = 0
    while isinstance(body, Lam): body = body.body
    while isinstance(body, App): n += 1; body = body.arg
    return n

SUCC = Lam("n", Lam("f", Lam("x", App(Var("f"), App(App(Var("n"), Var("f")), Var("x"))))))
PLUS = Lam("m", Lam("n", Lam("f", Lam("x", App(App(Var("m"), Var("f")), App(App(Var("n"), Var("f")), Var("x")))))))
MULT = Lam("m", Lam("n", Lam("f", App(Var("m"), App(Var("n"), Var("f"))))))
TRUE = Lam("a", Lam("b", Var("a")))
FALSE = Lam("a", Lam("b", Var("b")))
AND = Lam("p", Lam("q", App(App(Var("p"), Var("q")), Var("p"))))

def main():
    print("Lambda Calculus Interpreter:\n")
    # Identity
    I = Lam("x", Var("x"))
    print(f"  I = {I}")
    print(f"  I 42 = {beta_reduce(App(I, Var('42')))}")

    # Church numerals
    two = church(2)
    three = church(3)
    print(f"\n  2 = {two}")
    print(f"  3 = {three}")
    five = beta_reduce(App(App(PLUS, two), three))
    print(f"  2+3 = {five}")
    print(f"  unchurch(2) = {unchurch(two)}")
    print(f"  unchurch(3) = {unchurch(three)}")
    succ2 = beta_reduce(App(SUCC, two))
    print(f"  succ(2) = unchurch={unchurch(succ2)}")

    # Boolean logic
    print(f"\n  TRUE = {TRUE}")
    print(f"  FALSE = {FALSE}")
    result = beta_reduce(App(App(AND, TRUE), FALSE))
    print(f"  TRUE AND FALSE = {result}")

if __name__ == "__main__":
    main()
