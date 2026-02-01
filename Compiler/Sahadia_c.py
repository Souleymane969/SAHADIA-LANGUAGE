from compiler.lexer import SahadiaLexer
from compiler.parser import SahadiaParser
from compiler.soul_bridge import SoulBridge

def compile_sahadia(source_code: str) -> str:
    tokens = SahadiaLexer(source_code).tokenize()
    ast = SahadiaParser(tokens).parse()
    python_code = SoulBridge().generate(ast)
    return python_code


if __name__ == "__main__":
    with open("examples/hello_sahadia.sl", "r", encoding="utf-8") as f:
        source = f.read()

    output = compile_sahadia(source)
    print(output)
