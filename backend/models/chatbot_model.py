import re


class CodeFixerChatbot:
    """
    Fully offline Code Fixer Chatbot.
    All language knowledge is embedded locally — no internet or API required.
    Supports comprehensive error detection and repair for Python, JavaScript, and Java.
    Returns a structured 5-step analysis: Problem, Cause, Fixed Code, Changes, Pro-Tip.
    """

    def __init__(self):
        # ── Common typo dictionaries for each language ──────────────────────

        self.python_typos = {
            'pritn': 'print', 'pirnt': 'print', 'prnt': 'print', 'prit': 'print',
            'retrun': 'return', 'reutrn': 'return', 'retrn': 'return', 'retunr': 'return',
            'improt': 'import', 'imoprt': 'import', 'ipmort': 'import',
            'fromt': 'from', 'form': 'from',
            'dfe': 'def', 'edf': 'def', 'defi': 'def',
            'calss': 'class', 'classs': 'class', 'clas': 'class',
            'whlie': 'while', 'whle': 'while', 'wihle': 'while',
            'esle': 'else', 'elese': 'else', 'els': 'else',
            'elfi': 'elif', 'elseif': 'elif', 'else if': 'elif',
            'breack': 'break', 'braek': 'break',
            'contniue': 'continue', 'contiue': 'continue',
            'ture': 'True', 'treu': 'True', 'Ture': 'True',
            'flase': 'False', 'fasle': 'False', 'Flase': 'False',
            'noen': 'None', 'NOne': 'None',
            'lne': 'len', 'rnage': 'range', 'rnge': 'range',
            'appned': 'append', 'apend': 'append',
            'lsit': 'list', 'dcit': 'dict', 'tupe': 'tuple',
            'execpt': 'except', 'exept': 'except', 'excpet': 'except',
            'finaly': 'finally', 'finnaly': 'finally',
            'rasie': 'raise', 'riase': 'raise',
            'yeild': 'yield', 'yeld': 'yield',
            'glboal': 'global', 'gloabl': 'global',
            'lamda': 'lambda', 'labmda': 'lambda',
            'assrt': 'assert', 'asert': 'assert',
        }

        self.javascript_typos = {
            'fucntion': 'function', 'funtion': 'function', 'fucntion': 'function',
            'funciton': 'function', 'funcion': 'function',
            'cosnt': 'const', 'conts': 'const', 'cnst': 'const',
            'lte': 'let', 'elt': 'let',
            'vra': 'var', 'avr': 'var',
            'retrun': 'return', 'reutrn': 'return', 'retrn': 'return',
            'consoel': 'console', 'conosle': 'console',
            'doucment': 'document', 'docuemnt': 'document',
            'widnow': 'window', 'winodw': 'window',
            'ture': 'true', 'treu': 'true',
            'flase': 'false', 'fasle': 'false',
            'nul': 'null', 'nulol': 'null',
            'undefiend': 'undefined', 'udnefined': 'undefined',
            'asncy': 'async', 'asyc': 'async', 'asnyc': 'async',
            'awiat': 'await', 'aaiwt': 'await',
            'reqiure': 'require', 'reuqire': 'require',
            'exoprt': 'export', 'exprot': 'export',
            'improt': 'import', 'imoprt': 'import',
            'elseif': 'else if',
            'lenght': 'length', 'legnth': 'length',
            'thenm': 'then', 'cahtc': 'catch',
        }

        self.java_typos = {
            'pubilc': 'public', 'pubic': 'public', 'publc': 'public',
            'priavte': 'private', 'privte': 'private',
            'proected': 'protected', 'protectd': 'protected',
            'statci': 'static', 'staic': 'static',
            'viod': 'void', 'voiid': 'void',
            'Stirng': 'String', 'Strign': 'String', 'Sting': 'String',
            'Integre': 'Integer', 'Intger': 'Integer',
            'Booelan': 'Boolean', 'Booelean': 'Boolean',
            'Systme': 'System', 'Sysetm': 'System', 'Ssytem': 'System',
            'retrun': 'return', 'reutrn': 'return', 'retrn': 'return',
            'calss': 'class', 'classs': 'class',
            'extneds': 'extends', 'extnds': 'extends',
            'implments': 'implements', 'implemnts': 'implements',
            'thwros': 'throws', 'throows': 'throws',
            'catchh': 'catch', 'cahtc': 'catch',
            'finaly': 'finally', 'finnaly': 'finally',
            'ture': 'true', 'treu': 'true',
            'flase': 'false', 'fasle': 'false',
            'nwe': 'new', 'enw': 'new',
            'lenght': 'length', 'legnth': 'length',
            'arraylist': 'ArrayList', 'hashmap': 'HashMap',
            'Scaner': 'Scanner', 'Scannner': 'Scanner',
            'pritnln': 'println', 'printlnn': 'println',
        }

        # ── Python tips dictionary ──────────────────────────────────────────
        self.python_tips = [
            "Use a linter like pylint or flake8 to catch errors before running.",
            "Python uses indentation (4 spaces) instead of curly braces — be consistent.",
            "Always use '==' for comparison and '=' for assignment.",
            "Remember: Python keywords like True, False, None are case-sensitive.",
            "Use f-strings (f'Hello {name}') for cleaner string formatting.",
            "Missing colons at the end of if/for/while/def/class is the #1 Python error.",
            "Use 'try/except' blocks to handle errors gracefully.",
            "Always close parentheses, brackets, and quotes in matching pairs.",
            "Use list comprehensions for cleaner, more Pythonic code.",
            "Check your indentation — mixing tabs and spaces causes errors.",
        ]

        self.javascript_tips = [
            "Use 'const' for values that don't change, 'let' for ones that do.",
            "Always use '===' instead of '==' for strict equality comparison.",
            "Don't forget semicolons at the end of statements.",
            "Arrow functions (=>) are a cleaner way to write short functions.",
            "Use template literals (`Hello ${name}`) instead of string concatenation.",
            "Always handle Promise rejections with .catch() or try/catch.",
            "Use 'console.log()' for debugging — but remove them before production.",
            "Remember: JavaScript is case-sensitive — 'getElementById' not 'getElementByID'.",
            "Async/await makes asynchronous code much easier to read and debug.",
            "Check for null/undefined before accessing object properties.",
        ]

        self.java_tips = [
            "Every statement in Java must end with a semicolon.",
            "Java is strongly typed — always declare variable types explicitly.",
            "Use 'equals()' for String comparison, not '=='.",
            "The main method signature must be exactly: public static void main(String[] args).",
            "Always capitalize class names and use camelCase for method names.",
            "Remember to import java.util.* when using ArrayList, HashMap, etc.",
            "Use try-catch blocks for checked exceptions — Java enforces this.",
            "Every '{' must have a matching '}' — use an IDE to auto-format.",
            "Use 'System.out.println()' — note the lowercase 'l' in println.",
            "Avoid NullPointerException by always checking for null before use.",
        ]

    # ══════════════════════════════════════════════════════════════════════
    #  PUBLIC API   — the single entry point
    # ══════════════════════════════════════════════════════════════════════

    def fix_code(self, code, language):
        """
        Fix code using the comprehensive local heuristic engine.
        Fully offline — no internet or API required.
        Returns a structured 5-step analysis dict.
        """
        return self._local_heuristic_fix(code, language)

    # ══════════════════════════════════════════════════════════════════════
    #  AUTO-FORMAT — single-line / cramped code cleanup
    # ══════════════════════════════════════════════════════════════════════

    def _auto_format(self, code, language):
        if language == 'python':
            code = re.sub(r'(?<!^)(def |class |if |for |while |try:|except:|else:|elif )', r'\n\1', code)
            return code

        # C-style (JS / Java) brace formatting
        code = re.sub(r'\{\s*', ' {\n', code)
        code = re.sub(r'\s*}', '\n}', code)

        parts = re.split(r'(for\s*\([^)]+\))', code)
        for i in range(len(parts)):
            if not parts[i].strip().startswith('for'):
                parts[i] = re.sub(r';\s*', ';\n', parts[i])
        code = "".join(parts)

        lines = code.split('\n')
        formatted = []
        indent = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('}'):
                indent = max(0, indent - 1)
            formatted.append(('    ' * indent) + line)
            if line.endswith('{'):
                indent += 1
        return '\n'.join(formatted)

    # ══════════════════════════════════════════════════════════════════════
    #  TYPO FIXER — language-aware keyword correction
    # ══════════════════════════════════════════════════════════════════════

    def _fix_typos(self, code, language):
        typo_dict = {
            'python': self.python_typos,
            'javascript': self.javascript_typos,
            'java': self.java_typos,
        }.get(language, {})

        fixes = []
        for typo, correct in typo_dict.items():
            pattern = r'\b' + re.escape(typo) + r'\b'
            if re.search(pattern, code):
                code = re.sub(pattern, correct, code)
                fixes.append(f"Corrected typo '{typo}' → '{correct}'.")
        return code, fixes

    # ══════════════════════════════════════════════════════════════════════
    #  PYTHON FIXER — comprehensive Python error repair
    # ══════════════════════════════════════════════════════════════════════

    def _fix_python(self, code):
        fixes = []
        lines = code.split('\n')

        # 1. Missing/incorrect colons on block statements
        for i in range(len(lines)):
            line = lines[i].rstrip()
            if not line.strip():
                continue
            if re.match(r'^\s*(def |class |if |for |while |try|except|else|elif |with )', line):
                if re.search(r'[;,.\- ]+$', line) and not line.endswith(':'):
                    line = re.sub(r'[;,.\- ]+$', ':', line)
                    lines[i] = line
                    if "Replaced incorrect trailing punctuation with colon ':'." not in fixes:
                        fixes.append("Replaced incorrect trailing punctuation with colon ':'.")
                elif not line.endswith(':') and not line.endswith('(') and not line.endswith('\\'):
                    lines[i] = line + ':'
                    if "Added missing colon ':' to block statement." not in fixes:
                        fixes.append("Added missing colon ':' to block statement.")

        # 2. Remove rogue semicolons
        for i in range(len(lines)):
            line = lines[i].rstrip()
            if line.endswith(';') and not re.match(r'^\s*(for|while|if|def|class)', line):
                lines[i] = line[:-1]
                if "Removed unnecessary semicolons from Python code." not in fixes:
                    fixes.append("Removed unnecessary semicolons from Python code.")

        # 3. Fix Python boolean/None casing
        for i in range(len(lines)):
            orig = lines[i]
            lines[i] = re.sub(r'\btrue\b', 'True', lines[i])
            lines[i] = re.sub(r'\bfalse\b', 'False', lines[i])
            lines[i] = re.sub(r'\bnull\b', 'None', lines[i])
            if orig != lines[i] and "Corrected casing for True/False/None." not in fixes:
                fixes.append("Corrected casing for True/False/None.")

        # 4. print without parentheses (Python 2 → 3)
        for i in range(len(lines)):
            orig = lines[i]
            if re.search(r'^\s*print\s+([^(].*)$', lines[i]):
                lines[i] = re.sub(r'^(\s*print)\s+([^(].*)$', r'\1(\2)', lines[i])
                if orig != lines[i] and "Updated print to use parentheses (Python 3)." not in fixes:
                    fixes.append("Updated print to use parentheses (Python 3).")

        # 5. Assignment in conditional
        for i in range(len(lines)):
            if re.match(r'^\s*(if|elif|while)\s+', lines[i]):
                if ' = ' in lines[i] and ' == ' not in lines[i] and '!=' not in lines[i] and '>=' not in lines[i] and '<=' not in lines[i]:
                    lines[i] = lines[i].replace(' = ', ' == ')
                    if "Fixed '=' used instead of '==' in conditional." not in fixes:
                        fixes.append("Fixed '=' used instead of '==' in conditional.")

        # 6. Missing = in simple assignments like `sum 0` → `sum = 0`
        for i in range(len(lines)):
            if re.match(r'^\s*[a-zA-Z_]\w*\s+([\d.\-]+|["\'].*?["\']|\[.*?\]|\{.*?\})\s*$', lines[i]):
                lines[i] = re.sub(r'^(\s*[a-zA-Z_]\w*)\s+([\d.\-]+|["\'].*?["\']|\[.*?\]|\{.*?\})\s*$', r'\1 = \2', lines[i])
                if "Added missing '=' in variable assignment." not in fixes:
                    fixes.append("Added missing '=' in variable assignment.")

        # 7. Unmatched parentheses
        for i in range(len(lines)):
            open_p = lines[i].count('(')
            close_p = lines[i].count(')')
            if open_p > close_p:
                lines[i] = lines[i] + (')' * (open_p - close_p))
                if "Added missing closing parenthesis ')'." not in fixes:
                    fixes.append("Added missing closing parenthesis ')'.")
            elif close_p > open_p:
                diff = close_p - open_p
                lines[i] = lines[i].replace(')', '', diff) if diff == 1 else lines[i]

        # 8. Unmatched brackets
        for i in range(len(lines)):
            open_b = lines[i].count('[')
            close_b = lines[i].count(']')
            if open_b > close_b:
                lines[i] = lines[i] + (']' * (open_b - close_b))
                if "Added missing closing bracket ']'." not in fixes:
                    fixes.append("Added missing closing bracket ']'.")

        # 9. Missing self in class methods
        for i in range(len(lines)):
            if re.match(r'^\s*def\s+\w+\(\s*\):', lines[i]):
                lines[i] = lines[i].replace('():', '(self):')
                if "Added 'self' to class method definition." not in fixes:
                    fixes.append("Added 'self' to class method definition.")

        # 10. f-string missing 'f' prefix
        for i in range(len(lines)):
            # Detect strings with {var} that aren't f-strings
            if re.search(r"[^f]['\"].*\{[a-zA-Z_]\w*\}.*['\"]", lines[i]):
                orig = lines[i]
                lines[i] = re.sub(r"(?<!=\s)(['\"])(.*\{[a-zA-Z_]\w*\}.*)\1", r"f\1\2\1", lines[i])
                if orig != lines[i] and "Added missing 'f' prefix for f-string." not in fixes:
                    fixes.append("Added missing 'f' prefix for f-string.")

        # 11. Dynamic auto-indentation repair
        indent = 0
        for i in range(len(lines)):
            stripped = lines[i].strip()
            if not stripped:
                continue
            if re.match(r'^(except|else|elif|finally)', stripped):
                indent = max(0, indent - 1)
            if len(lines[i]) - len(stripped) == 0 and indent > 0:
                lines[i] = ('    ' * indent) + stripped
                if "Fixed missing indentation." not in fixes:
                    fixes.append("Fixed missing indentation.")
            else:
                actual_indent = (len(lines[i]) - len(stripped)) // 4
                indent = max(indent, actual_indent)
            if stripped.endswith(':'):
                indent += 1

        return '\n'.join(lines), fixes

    # ══════════════════════════════════════════════════════════════════════
    #  JAVASCRIPT FIXER — comprehensive JS error repair
    # ══════════════════════════════════════════════════════════════════════

    def _fix_javascript(self, code):
        fixes = []
        lines = code.split('\n')

        # 1. console.log typos
        if 'console.print' in code:
            code = code.replace('console.print', 'console.log')
            fixes.append("Corrected 'console.print' to 'console.log'.")
            lines = code.split('\n')

        # 2. Missing semicolons on statements
        for i in range(len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            if not line.endswith(';') and not line.endswith('{') and not line.endswith('}') and not line.endswith(','):
                if not re.match(r'^(if|for|while|else|catch|class|function|switch|case|default|\/\/|\/\*|\*)', line):
                    if '=' in line or 'return ' in line or 'console.' in line or \
                       'let ' in line or 'const ' in line or 'var ' in line or \
                       '++' in line or '--' in line or '+=' in line or '-=' in line or \
                       'throw ' in line or 'break' == line or 'continue' == line:
                        lines[i] = lines[i].rstrip() + ';'
                        if "Added missing semicolons." not in fixes:
                            fixes.append("Added missing semicolons.")

        # 3. Missing braces on control flow
        for i in range(len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            if not line.endswith('{') and not line.endswith('}') and not line.endswith(';'):
                if re.match(r'^(if|for|while|else|catch)(\s|\()', line) or line == 'else':
                    lines[i] = lines[i].rstrip() + ' {'
                    if "Added missing curly braces to control statements." not in fixes:
                        fixes.append("Added missing curly braces to control statements.")

        # 4. Arrow function syntax: `const fn = (x) = >` → `const fn = (x) =>`
        for i in range(len(lines)):
            orig = lines[i]
            lines[i] = re.sub(r'=\s+>', '=>', lines[i])
            if orig != lines[i] and "Fixed arrow function syntax '= >' → '=>'." not in fixes:
                fixes.append("Fixed arrow function syntax '= >' → '=>'.")

        # 5. Template literal: using regular quotes with ${} → backticks
        for i in range(len(lines)):
            orig = lines[i]
            if re.search(r'["\'].*\$\{.*\}.*["\']', lines[i]):
                lines[i] = re.sub(r'["\'](.+?\$\{.+?\}.+?)["\']', r'`\1`', lines[i])
                if orig != lines[i] and "Changed string to template literal with backticks for ${} expressions." not in fixes:
                    fixes.append("Changed string to template literal with backticks for ${} expressions.")

        # 6. Unmatched braces
        total_open = code.count('{')
        total_close = code.count('}')
        if total_open > total_close:
            lines.append('}' * (total_open - total_close))
            if "Added missing closing braces '}'." not in fixes:
                fixes.append("Added missing closing braces '}'.")

        # 7. Unmatched parentheses
        for i in range(len(lines)):
            op = lines[i].count('(')
            cl = lines[i].count(')')
            if op > cl:
                lines[i] = lines[i] + (')' * (op - cl))
                if "Added missing closing parenthesis ')'." not in fixes:
                    fixes.append("Added missing closing parenthesis ')'.")

        return '\n'.join(lines), fixes

    # ══════════════════════════════════════════════════════════════════════
    #  JAVA FIXER — comprehensive Java error repair
    # ══════════════════════════════════════════════════════════════════════

    def _fix_java(self, code):
        fixes = []
        lines = code.split('\n')

        # 1. System.out.println typos
        if 'system.out.println' in code:
            code = code.replace('system.out.println', 'System.out.println')
            fixes.append("Capitalized 'System' in System.out.println.")
            lines = code.split('\n')
        if 'System.out.printLn' in code:
            code = code.replace('System.out.printLn', 'System.out.println')
            fixes.append("Fixed capitalization of 'println'.")
            lines = code.split('\n')

        # 2. Missing semicolons on statements
        for i in range(len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            if not line.endswith(';') and not line.endswith('{') and not line.endswith('}') and not line.endswith(','):
                if not re.match(r'^(if|for|while|else|catch|class|public|private|protected|import|package|interface|switch|case|default|\/\/|\/\*|\*|@)', line):
                    if '=' in line or 'return ' in line or 'System.out' in line or \
                       '++' in line or '--' in line or '+=' in line or '-=' in line or \
                       'throw ' in line or 'break' == line or 'continue' == line or \
                       re.match(r'^\s*\w+\.\w+\(', line) or re.match(r'^\s*new\s+', line):
                        lines[i] = lines[i].rstrip() + ';'
                        if "Added missing semicolons." not in fixes:
                            fixes.append("Added missing semicolons.")

        # 3. Missing braces on control flow
        for i in range(len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            if not line.endswith('{') and not line.endswith('}') and not line.endswith(';'):
                if re.match(r'^(if|for|while|else|catch)(\s|\()', line) or line == 'else':
                    lines[i] = lines[i].rstrip() + ' {'
                    if "Added missing curly braces to control statements." not in fixes:
                        fixes.append("Added missing curly braces to control statements.")

        # 4. Missing 'new' keyword for object instantiation
        for i in range(len(lines)):
            orig = lines[i]
            # Pattern: Type var = Type(args); but missing 'new'
            match = re.search(r'=\s*([A-Z]\w+)\s*\(', lines[i])
            if match and 'new ' not in lines[i] and 'static ' not in lines[i]:
                cls_name = match.group(1)
                if cls_name not in ('String', 'Integer', 'Double', 'Float', 'Boolean', 'Character', 'Math', 'System'):
                    lines[i] = lines[i].replace(f'= {cls_name}(', f'= new {cls_name}(')
                    if orig != lines[i] and "Added missing 'new' keyword for object creation." not in fixes:
                        fixes.append("Added missing 'new' keyword for object creation.")

        # 5. main method signature check
        for i in range(len(lines)):
            # Fix common wrong main signatures
            if 'static void main' in lines[i] and 'public' not in lines[i]:
                lines[i] = lines[i].replace('static void main', 'public static void main')
                if "Added 'public' to main method." not in fixes:
                    fixes.append("Added 'public' to main method.")
            if 'public static main' in lines[i] and 'void' not in lines[i]:
                lines[i] = lines[i].replace('public static main', 'public static void main')
                if "Added 'void' return type to main method." not in fixes:
                    fixes.append("Added 'void' return type to main method.")

        # 6. Unmatched braces
        total_open = '\n'.join(lines).count('{')
        total_close = '\n'.join(lines).count('}')
        if total_open > total_close:
            lines.append('}' * (total_open - total_close))
            if "Added missing closing braces '}'." not in fixes:
                fixes.append("Added missing closing braces '}'.")

        # 7. Unmatched parentheses
        for i in range(len(lines)):
            op = lines[i].count('(')
            cl = lines[i].count(')')
            if op > cl:
                lines[i] = lines[i] + (')' * (op - cl))
                if "Added missing closing parenthesis ')'." not in fixes:
                    fixes.append("Added missing closing parenthesis ')'.")

        return '\n'.join(lines), fixes

    # ══════════════════════════════════════════════════════════════════════
    #  MAIN ENGINE — orchestrates all fixes + generates 5-step response
    # ══════════════════════════════════════════════════════════════════════

    def _local_heuristic_fix(self, code, language):
        """
        Comprehensive offline code fixer.
        Applies typo correction, language-specific fixes, and formatting.
        Returns a structured 5-step response.
        """
        all_fixes = []

        # ── Step 0: Auto-format if crammed into one line ──
        if '\n' not in code.strip() and len(code) > 50:
            code = self._auto_format(code, language)
            all_fixes.append("Auto-formatted single-line code into proper block structure.")

        # ── Step 1: Fix typos ──
        code, typo_fixes = self._fix_typos(code, language)
        all_fixes.extend(typo_fixes)

        # ── Step 2: Language-specific fixes ──
        if language == 'python':
            code, lang_fixes = self._fix_python(code)
            all_fixes.extend(lang_fixes)
        elif language == 'javascript':
            code, lang_fixes = self._fix_javascript(code)
            all_fixes.extend(lang_fixes)
        elif language == 'java':
            code, lang_fixes = self._fix_java(code)
            all_fixes.extend(lang_fixes)

        # ── Fallback if no issues found ──
        if not all_fixes:
            if code.strip():
                all_fixes.append("Code looks syntactically correct. No errors found.")
            else:
                all_fixes.append("No code provided to fix.")

        # ── Build structured 5-step response ──
        fixed_code = code.strip()

        # Generate a smart problem description
        if len(all_fixes) == 1 and 'correct' in all_fixes[0].lower():
            problem = "No syntax or logic errors were detected in your code."
            cause = "The code appears to be well-written with correct syntax."
        else:
            problem = f"Found {len(all_fixes)} issue(s): " + '; '.join(all_fixes[:2])
            if len(all_fixes) > 2:
                problem += f" (and {len(all_fixes) - 2} more)"
            cause = self._generate_cause(all_fixes, language)

        # Pick a relevant tip
        import random
        import hashlib
        seed = int(hashlib.md5(code.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        tips = {
            'python': self.python_tips,
            'javascript': self.javascript_tips,
            'java': self.java_tips,
        }.get(language, self.python_tips)
        tip = random.choice(tips)

        return {
            'original_code': code,
            'problem': problem,
            'cause': cause,
            'fixed_code': fixed_code,
            'changes': all_fixes,
            'tip': tip,
        }

    def _generate_cause(self, fixes, language):
        """Generate a human-readable cause from the list of fixes applied."""
        causes = []
        for fix in fixes[:3]:
            fix_lower = fix.lower()
            if 'colon' in fix_lower:
                causes.append("block statements require a colon at the end in Python")
            elif 'semicolon' in fix_lower and language == 'python':
                causes.append("Python doesn't use semicolons to end statements")
            elif 'semicolon' in fix_lower:
                causes.append(f"{language.capitalize()} requires semicolons at the end of statements")
            elif 'typo' in fix_lower:
                causes.append("a keyword was mistyped")
            elif 'parenthes' in fix_lower:
                causes.append("there were unmatched parentheses")
            elif 'brace' in fix_lower:
                causes.append("curly braces were missing or unmatched")
            elif 'indent' in fix_lower:
                causes.append("Python uses indentation to define code blocks")
            elif 'self' in fix_lower:
                causes.append("class methods in Python need 'self' as the first parameter")
            elif 'print' in fix_lower and 'python' in language:
                causes.append("Python 3 requires print() with parentheses")
            elif 'true' in fix_lower or 'false' in fix_lower or 'none' in fix_lower:
                causes.append("Python booleans and None are case-sensitive")
            elif '==' in fix_lower:
                causes.append("'=' is assignment while '==' is comparison")
            elif 'arrow' in fix_lower:
                causes.append("arrow function syntax requires '=>' without spaces")
            elif 'template' in fix_lower:
                causes.append("template literals require backticks instead of quotes")
            elif 'new' in fix_lower:
                causes.append("Java requires 'new' keyword to create object instances")
            elif 'main' in fix_lower:
                causes.append("Java main method requires the exact signature: public static void main")
            elif 'format' in fix_lower:
                causes.append("the code was not properly formatted with line breaks")
            else:
                causes.append("there were syntax issues in the code")

        if not causes:
            return "The code had some minor formatting issues."

        # Deduplicate
        seen = set()
        unique = []
        for c in causes:
            if c not in seen:
                seen.add(c)
                unique.append(c)

        if len(unique) == 1:
            return f"This happened because {unique[0]}."
        return "This happened because " + ", ".join(unique[:-1]) + f", and {unique[-1]}."
