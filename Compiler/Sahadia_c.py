# sahadia_c.py
# SAHADIA C (SCL) - v0.1

def compile_sahadia(source, target="python"):
    lines = source.split("\n")
    output = []

    for line in lines:
        line = line.strip()

        if line.startswith("Soul") or line.startswith("Say"):
            text = line.split('"')[1]
            if target == "python":
                output.append(f'print("{text}")')
            elif target == "js":
                output.append(f'console.log("{text}");')
            elif target == "html":
                output.append(f'<p>{text}</p>')

        elif line.startswith("Remember"):
            parts = line.split()
            name = parts[1]
            value = parts[3]
            if target == "python":
                output.append(f'{name} = {value}')
            elif target == "js":
                output.append(f'let {name} = {value};')

        elif line.startswith("Count"):
            expr = line.replace("Count", "")
            expr = expr.replace("plus", "+") \
                       .replace("minus", "-") \
                       .replace("fois", "*") \
                       .replace("divided", "/")
            if target == "python":
                output.append(f'print({expr})')
            elif target == "js":
                output.append(f'console.log({expr});')

    return "\n".join(output)
