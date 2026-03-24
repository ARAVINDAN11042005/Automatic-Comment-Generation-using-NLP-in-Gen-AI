import re

class CodeFixerChatbot:
    def __init__(self):
        pass

    def _auto_format(self, code, language):
        if language == 'python':
            # Python is whitespace dependent; do basic splitting on common keywords if crammed
            code = re.sub(r'(?<!^)(def |class |if |for |while |try:|except:|else:|elif )', r'\n\1', code)
            return code
            
        # For JS and Java, perform curly-brace formatting
        # 1. Ensure basic spacing
        code = re.sub(r'{\s*', ' {\n', code)
        code = re.sub(r'\s*}', '\n}', code)
        
        # safely handle semicolons outside 'for' loops
        parts = re.split(r'(for\s*\([^)]+\))', code)
        for i in range(len(parts)):
            if not parts[i].strip().startswith('for'):
                parts[i] = re.sub(r';\s*', ';\n', parts[i])
        code = "".join(parts)

        # 2. Fix indentation
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

    def fix_code(self, code, language):
        """
        Simulates an intelligent code-fixing AI by resolving common syntax errors.
        """
        fixes = []
        
        # Check if code is crammed into a single line (typical of copy-paste loss)
        if '\n' not in code.strip() and len(code) > 50:
            code = self._auto_format(code, language)
            fixes.append("Auto-formatted single-line code into proper block structure.")
            
        fixed_code = code

        if language == 'python':
            # Missing colons in def, if, for, while, elif, else
            if re.search(r'(def\s+\w+\([^)]*\))\s*\n', fixed_code):
                fixed_code = re.sub(r'(def\s+\w+\([^)]*\))\s*\n', r'\1:\n', fixed_code)
                fixes.append("Added missing colon after function definition.")
            
            if re.search(r'(if|elif|while|for\s+.*\s+in\s+.*)[^:]\s*\n', fixed_code):
                fixed_code = re.sub(r'((?:if|elif|while|for\s+.*\s+in\s+.*)[^:])\s*\n', r'\1:\n', fixed_code)
                fixes.append("Added missing colons in control flow statements.")
                
            # print without parenthesis (Python 2 to 3)
            if re.search(r'print\s+["\']', fixed_code):
                fixed_code = re.sub(r'print\s+(["\'].*?["\'])', r'print(\1)', fixed_code)
                fixes.append("Updated print statements to use parentheses (Python 3 syntax).")

            # Basic indentation fix (very simplified)
            lines = fixed_code.split('\n')
            for i in range(1, len(lines)):
                if lines[i-1].strip().endswith(':'):
                    if lines[i].strip() and not lines[i].startswith(' ') and not lines[i].startswith('\t'):
                        lines[i] = '    ' + lines[i]
                        if "Fixed missing indentation." not in fixes:
                            fixes.append("Fixed missing indentation.")
            fixed_code = '\n'.join(lines)

        elif language == 'javascript':
            # console.log typos
            if 'console.print' in fixed_code:
                fixed_code = fixed_code.replace('console.print', 'console.log')
                fixes.append("Corrected 'console.print' to 'console.log'.")
                
            # Missing semicolons on basic lines (lazy simulation)
            lines = fixed_code.split('\n')
            for i in range(len(lines)):
                line = lines[i].strip()
                if line and not line.endswith(';') and not line.endswith('{') and not line.endswith('}') and not line.endswith(','):
                    if '=' in line or 'let ' in line or 'const ' in line or 'console.log' in line or 'return ' in line:
                        lines[i] = lines[i] + ';'
                        if "Added missing semicolons." not in fixes:
                            fixes.append("Added missing semicolons.")
            fixed_code = '\n'.join(lines)

        elif language == 'java':
            # System.out.print typos
            if 'system.out.println' in fixed_code:
                fixed_code = fixed_code.replace('system.out.println', 'System.out.println')
                fixes.append("Capitalized 'System' in System.out.println.")
            if 'System.out.printLn' in fixed_code:
                fixed_code = fixed_code.replace('System.out.printLn', 'System.out.println')
                fixes.append("Fixed capitalization of 'println'.")
                
            # Missing semicolons
            lines = fixed_code.split('\n')
            for i in range(len(lines)):
                line = lines[i].strip()
                if line and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                    if 'System.out' in line or 'return ' in line or '=' in line or '++' in line or 'add(' in line:
                        lines[i] = lines[i] + ';'
                        if "Added missing semicolons." not in fixes:
                            fixes.append("Added missing semicolons.")
            fixed_code = '\n'.join(lines)

        if not fixes:
            if code.strip():
                fixes.append("Code looks syntactically correct. No major stylistic errors found.")
            else:
                fixes.append("No code provided to fix.")
                
        # Always format cleanly
        fixed_code = fixed_code.strip()

        return {
            'original_code': code,
            'fixed_code': fixed_code,
            'fixes_applied': fixes
        }
