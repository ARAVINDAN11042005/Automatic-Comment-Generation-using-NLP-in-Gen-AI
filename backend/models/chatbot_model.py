import re
import os
import json
from openai import OpenAI

class CodeFixerChatbot:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

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
        Fixes code using OpenAI ChatGPT if an API key is provided in OPENAI_API_KEY.
        Otherwise falls back to the robust local simulated heuristic engine.
        """
        if self.client:
            try:
                system_prompt = "You are an expert programming assistant. You fix syntax errors, bugs, and formatting issues perfectly."
                user_prompt = f"""
The user has provided a snippet of {language} code that contains syntax errors, bugs, or formatting issues.
Your task is to fix ALL errors, format it perfectly, and explain the changes you made.

Return your response strictly in the following JSON format:
{{
    "fixed_code": "the corrected code here as a single string",
    "fixes_applied": ["brief explanation 1", "brief explanation 2"]
}}

Here is the code:
{code}
"""
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={ "type": "json_object" },
                    temperature=0.2
                )
                
                result = json.loads(response.choices[0].message.content)
                return {
                    'original_code': code,
                    'fixed_code': result.get('fixed_code', code),
                    'fixes_applied': result.get('fixes_applied', ["Fixed code using ChatGPT"])
                }
            except Exception as e:
                print(f"[!] OpenAI API failed: {e}. Falling back to default heuristics.")
                return self._local_heuristic_fix(code, language)
        else:
            return self._local_heuristic_fix(code, language)

    def _local_heuristic_fix(self, code, language):
        """
        Robust heuristic fallback code fixer.
        """
        fixes = []
        
        # Check if code is crammed into a single line (typical of copy-paste loss)
        if '\n' not in code.strip() and len(code) > 50:
            code = self._auto_format(code, language)
            fixes.append("Auto-formatted single-line code into proper block structure.")
            
        fixed_code = code

        if language == 'python':
            lines = fixed_code.split('\n')
            
            # 1. Missing colons
            for i in range(len(lines)):
                line = lines[i].rstrip()
                if not line: continue
                # Check control flow statements missing colons
                if re.match(r'^\s*(def |class |if |for |while |try|except|else|elif |with ).*[^:]$', line):
                    # exclude lines ending with comma or open parens
                    if not line.endswith(',') and not line.endswith('(') and not line.endswith('\\'):
                        lines[i] = line + ':'
                        if "Added missing colon ':' to block statements." not in fixes:
                            fixes.append("Added missing colon ':' to block statements.")
                            
            # 2. Typos true, false, null -> True, False, None
            for i in range(len(lines)):
                orig = lines[i]
                lines[i] = re.sub(r'\btrue\b', 'True', lines[i])
                lines[i] = re.sub(r'\bfalse\b', 'False', lines[i])
                lines[i] = re.sub(r'\bnull\b', 'None', lines[i])
                if orig != lines[i] and "Corrected casing for True/False/None." not in fixes:
                    fixes.append("Corrected casing for True/False/None.")
                    
            # 3. print without parenthesis (Python 2 to 3)
            for i in range(len(lines)):
                orig = lines[i]
                if re.search(r'^\s*print\s+([^(].*)$', lines[i]):
                    lines[i] = re.sub(r'^(\s*print)\s+([^(].*)$', r'\1(\2)', lines[i])
                    if orig != lines[i] and "Updated print statements to use parentheses (Python 3)." not in fixes:
                        fixes.append("Updated print statements to use parentheses (Python 3).")
                        
            # 4. Assignment in conditional 'if x = 5:' -> 'if x == 5:'
            for i in range(len(lines)):
                if re.match(r'^\s*(if|elif|while)\s+', lines[i]):
                    if ' = ' in lines[i] and ' == ' not in lines[i] and '!=' not in lines[i] and '>=' not in lines[i] and '<=' not in lines[i]:
                        lines[i] = lines[i].replace(' = ', ' == ')
                        if "Fixed assignment '=' used instead of equality '==' in conditional." not in fixes:
                            fixes.append("Fixed assignment '=' used instead of equality '==' in conditional.")

            # 5. Missing `self` in methods
            for i in range(len(lines)):
                if re.match(r'^\s*def\s+\w+\(\s*\):', lines[i]):
                    lines[i] = lines[i].replace('():', '(self):')
                    if "Added 'self' parameter to empty class method definitions." not in fixes:
                        fixes.append("Added 'self' parameter to empty class method definitions.")

            # 6. Dynamic Auto-Indentation repair
            indent = 0
            for i in range(len(lines)):
                stripped = lines[i].strip()
                if not stripped: continue
                
                # Outdent blocks
                if re.match(r'^(except|else|elif|finally)', stripped):
                    indent = max(0, indent - 1)
                    
                # Fix indentation if line has NO leading spaces but we expect some
                # This corrects flat pasted code blocks automatically
                if len(lines[i]) - len(stripped) == 0 and indent > 0:
                    lines[i] = ('    ' * indent) + stripped
                    if "Dynamically fixed missing indentation blocks." not in fixes:
                        fixes.append("Dynamically fixed missing indentation blocks.")
                else:
                    # Sync indent tracker with user's actual spaces
                    actual_indent = (len(lines[i]) - len(stripped)) // 4
                    indent = max(indent, actual_indent)
                
                # Indent next lines if current line opens a block
                if stripped.endswith(':'):
                    indent += 1

            fixed_code = '\n'.join(lines)

        def fix_c_style_errors(code_str, fixes_list):
            lines = code_str.split('\n')
            for i in range(len(lines)):
                line = lines[i].strip()
                if not line: continue
                
                # Missing braces on control flow logic
                if not line.endswith('{') and not line.endswith('}') and not line.endswith(';'):
                    if re.match(r'^(if|for|while|else|catch)(\s|\()', line) or line == 'else':
                        lines[i] = lines[i] + ' {'
                        if "Added missing curly braces '{' to control statements." not in fixes_list:
                            fixes_list.append("Added missing curly braces '{' to control statements.")
                        continue
                        
                # Missing semicolons on standard expressions
                if not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                    if not re.match(r'^(if|for|while|else|catch|class|public|private|protected|import)', line):
                        if '=' in line or 'return ' in line or 'System.out' in line or 'console.' in line or '++' in line or '--' in line or 'let ' in line or 'const ' in line or 'var ' in line or 'add(' in line or "+=" in line or "-=" in line:
                            lines[i] = lines[i] + ';'
                            if "Added missing semicolons." not in fixes_list:
                                fixes_list.append("Added missing semicolons.")
                                
            return '\n'.join(lines)

        if language == 'javascript':
            # console.log typos
            if 'console.print' in fixed_code:
                fixed_code = fixed_code.replace('console.print', 'console.log')
                fixes.append("Corrected 'console.print' to 'console.log'.")
                
            fixed_code = fix_c_style_errors(fixed_code, fixes)

        elif language == 'java':
            # System.out.print typos
            if 'system.out.println' in fixed_code:
                fixed_code = fixed_code.replace('system.out.println', 'System.out.println')
                fixes.append("Capitalized 'System' in System.out.println.")
            if 'System.out.printLn' in fixed_code:
                fixed_code = fixed_code.replace('System.out.printLn', 'System.out.println')
                fixes.append("Fixed capitalization of 'println'.")
                
            fixed_code = fix_c_style_errors(fixed_code, fixes)

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
