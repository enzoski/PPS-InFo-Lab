"""
Programa para testear el contenido del código fuente del parser de ext2.

Dado un archivo .py con un código fuente que sepamos que es correcto,
lo compararemos con otro archivo .py que contenga el código fuente a testear.

De esta manera evito tener que revisar a ojo linea por linea el código para
comprobar que todo quedó igual entre ambos archivos luego de haber trasladado
los cambios hechos en uno al otro (por ejemplo entre mi repo y haruspex).
"""

import filecmp # para comparar los archivos
from colorama import init, Fore # para colorear el texto de salida
# https://pypi.org/project/colorama/

# ---------------------------------------------------------------
# + SETEAR LA RUTA DE LOS ARCHIVOS A COMPARAR SEGUN CORRESPONDA +
# ---------------------------------------------------------------

CODIGOS_FUENTE_A_TESTEAR = [
    "./repo haruspex/haruspex/ext2/directory_entry.py",
    "./repo haruspex/haruspex/ext2/group_descriptor.py",
    "./repo haruspex/haruspex/ext2/inode.py",
    "./repo haruspex/haruspex/ext2/superblock.py"
]

CODIGOS_FUENTE_CORRECTOS = [
    "./repo mio/directory_entry.py",
    "./repo mio/group_descriptor.py",
    "./repo mio/inode.py",
    "./repo mio/superblock.py",
]

# ---------------------------------------------------------------
# +                           TESTING                           +
# ---------------------------------------------------------------

# Método de comparación 1:
def __metodo_1(file_name_1, file_name_2):
    resultado = filecmp.cmp(file_name_1, file_name_2)
    color = Fore.GREEN if resultado else Fore.RED
    return f"[Método1] arch1 == arch2 ? : {color}{resultado}{Fore.RESET}"


# Método de comparación 2:
def __metodo_2(file_name_1, file_name_2):
    with open(file_name_1, "r") as f1:
        arch1 = f1.read()
    with open(file_name_2, "r") as f2:
        arch2 = f2.read()
    resultado = arch1==arch2
    color = Fore.GREEN if resultado else Fore.RED
    return f"[Método2] arch1 == arch2 ? : {color}{resultado}{Fore.RESET}"

# En caso de que los archivos que comparemos tengan el mismo contenido,
# ambos métodos darán 'True', caso contrario ambos darán 'False', ya que
# ambos métodos hacen lo mismo, pero con otra implementación.
def testear(files_to_test, correct_files):
    print(f"\nTesteando los {Fore.YELLOW}CÓDIGOS FUENTE{Fore.RESET} del parser de ext2...")
    for file_path_1, file_path_2 in zip(files_to_test, correct_files):
        resultado_1 = __metodo_1(file_path_1, file_path_2)
        resultado_2 = __metodo_2(file_path_1, file_path_2)
        print(f"\n\t{Fore.CYAN}{file_path_1}{Fore.RESET} VS {Fore.BLUE}{file_path_2}{Fore.RESET} (el correcto)")
        print(f"\t{resultado_1}")
        print(f"\t{resultado_2}")


# ---------------------------------------------------------------
# +                            MAIN                             +
# ---------------------------------------------------------------

init() # para que funcione el modulo de colores
testear(CODIGOS_FUENTE_A_TESTEAR, CODIGOS_FUENTE_CORRECTOS)
print()

