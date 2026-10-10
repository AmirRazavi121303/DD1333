
import importlib.util

# Läser in ditt befintliga program utan att starta terminalmenyn
spec = importlib.util.spec_from_file_location(
    "patiens_program", "184.py"
)

program = importlib.util.module_from_spec(spec)
spec.loader.exec_module(program)

# Startar GUI-klassen som ligger i 184.py
program.GUI()