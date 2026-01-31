
# sahadia_c.py
# SAHADIA C (SCL) - v0.2
# Compiler / Transpiler for SAHADIA LANGUAGE v1.1

def normalize_expr(expr):
    return (expr.replace("plus", "+")
                .replace("minus", "-")
                .replace("fois", "*")
                .replace("divided", "/")
                .replace("power", "**"))

def normalize_condition(cond):
    return (cond.replace("above", ">")
                .replace("greater", ">")
                .replace("below", "<")
                .replace("less", "<")
                .replace("same", "==")
                .replace("equal", "==")
                .replace("different", "!=")
                .replace("not", "!="))

def compile_sahadia(source, target="python"):
    lines = source.split("\n")
    output = []
    indent = 0

    for raw in lines:
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        # BEGIN / END
        if line == "BeginSoul":
            continue

        if line.startswith("End"):
            indent -= 1
            continue

        prefix = "    " * indent

        # SOUL / SAY
        if line.startswith("Soul") or line.startswith("Say"):
            text = line.split('"')[1]
            if target == "python":
                output.append(f'{prefix}print("{text}")')
            elif target == "js":
                output.append(f'{prefix}console.log("{text}");')

        # ASK
        elif line.startswith("Ask"):
            parts = line.split('"')
            question = parts[1]
            var = parts[-1].strip().split()[-1]
            if target == "python":
                output.append(f'{prefix}{var} = input("{question} ")')
            elif target == "js":
                output.append(f'{prefix}let {var} = prompt("{question}");')

        # REMEMBER
        elif line.startswith("Remember"):
            if "Count" in line:
                name = line.split()[1]
                expr = line.split("Count")[1]
                expr = normalize_expr(expr)
                output.append(f'{prefix}{name} = {expr}')
            else:
                parts = line.split()
                name = parts[1]
                value = parts[3]
                output.append(f'{prefix}{name} = {value}')

        # COUNT (direct print)
        elif line.startswith("Count"):
            expr = normalize_expr(line.replace("Count", ""))
            output.append(f'{prefix}print({expr})')

        # IF
        elif line.startswith("IfSoul"):
            cond = normalize_condition(line.replace("IfSoul", ""))
            output.append(f'{prefix}if {cond}:')
            indent += 1

        # ELSE
        elif line.startswith("ElseSoul"):
            indent -= 1
            prefix = "    " * indent
            output.append(f'{prefix}else:')
            indent += 1

        # REPEAT
        elif line.startswith("RepeatSoul"):
            times = line.split()[1]
            output.append(f'{prefix}for _ in range({times}):')
            indent += 1

    return "\n".join(output)
