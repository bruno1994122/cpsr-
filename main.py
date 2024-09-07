import re
import os
import importlib.util
import sys

class PSRInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.imported_modules = {}

    def execute_file(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                self.execute(line.strip())
        self.print_variables()

    def execute(self, command):
        command = command.strip()

        # Comando para definir variáveis
        if re.match(r'^[\w]+\s*=\s*.+$', command):
            var_name, value = map(str.strip, command.split('=', 1))
            self.variables[var_name] = self.evaluate(value)
        
        # Comando para condicional If
        elif command.startswith('if'):
            condition_body = command[3:].strip()
            condition, body = condition_body.split(':', 1)
            if self.evaluate(condition.strip()):
                self.execute(body.strip())
        
        # Comando para input
        elif command.startswith('input'):
            _, var_name = command.split(' ', 1)
            self.variables[var_name] = input(f'Enter value for {var_name}: ')
        
        # Comando screentext
        elif command.startswith('screentext'):
            _, text = command.split(' ', 1)
            self.show_text(self.evaluate(text.strip()))
        
        # Definição de funções
        elif command.startswith('def'):
            func_def = command[4:]
            func_name, params_body = func_def.split('(', 1)
            params_body, body = params_body.split(')', 1)
            func_name = func_name.strip()
            params = [p.strip() for p in params_body.split(',') if p.strip()]
            body = body.strip()
            self.functions[func_name] = (params, body)
        
        # Chamada de funções
        elif command.startswith('call'):
            _, func_call = command.split(' ', 1)
            func_name, args_body = func_call.split('(', 1)
            args_body = args_body.rstrip(')')
            args = [a.strip() for a in args_body.split(',') if a.strip()]
            func_name = func_name.strip()
            if func_name in self.functions:
                params, body = self.functions[func_name]
                local_vars = dict(zip(params, args))
                self.variables.update(local_vars)
                self.execute(body)
            elif func_name in self.imported_modules:
                func = self.imported_modules[func_name]
                func()
            else:
                print(f"Função '{func_name}' não encontrada.")
        
        # Definição de classes e métodos
        elif command.startswith('Class'):
            class_def = command[6:]
            class_name, methods_body = class_def.split('{', 1)
            methods_body = methods_body.rstrip('}')
            class_name = class_name.strip()
            methods = methods_body.split('\n')
            self.classes[class_name] = methods
        
        # Comando para detectar teclas (simulação)
        elif command.startswith('detect.phone'):
            # Simulação de detecção de teclas
            pass
        
        # Comando para teste
        elif command.startswith('test'):
            test_body = command[5:]
            try:
                exec(test_body)
            except Exception as e:
                print(f"Erro: {e}")

        # Importação de funções
        elif command.startswith('import'):
            _, file_path, func_name = command.split(' ', 2)
            self.import_function(file_path, func_name)

    def evaluate(self, expression):
        # Avalia expressões simples e variáveis
        expression = expression.strip()
        if expression in self.variables:
            return self.variables[expression]
        try:
            return eval(expression)
        except Exception as e:
            print(f"Erro na avaliação: {e}")
            return None

    def show_text(self, text):
        # Exibe o texto na tela
        print(text)

    def print_variables(self):
        # Exibe as variáveis atuais
        for var, value in self.variables.items():
            print(f"{var} = {value}")

    def import_function(self, file_path, function_name):
        # Importa uma função de um arquivo .py
        if not os.path.isfile(file_path):
            print(f"Arquivo '{file_path}' não encontrado.")
            return
        
        spec = importlib.util.spec_from_file_location("module", file_path)
        if spec is None:
            print(f"Não foi possível carregar o módulo do arquivo '{file_path}'.")
            return

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"Erro ao importar o módulo '{file_path}': {e}")
            return

        if hasattr(module, function_name):
            self.imported_modules[function_name] = getattr(module, function_name)
            print(f"Função '{function_name}' importada de '{file_path}'")
        else:
            print(f"Função '{function_name}' não encontrada no arquivo '{file_path}'")

# Exemplo de uso
interpreter = PSRInterpreter()
interpreter.execute_file('exemplo.psr')
