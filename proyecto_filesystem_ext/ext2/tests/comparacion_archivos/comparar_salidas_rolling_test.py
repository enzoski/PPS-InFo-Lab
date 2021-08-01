"""
Programa para testear las salidas de consola obtenidas al ejecutar
los rolling test del parser de ext2.

Dado un archivo .txt con una salida de un rolling test que sepamos
que es correcta (debido a un previo testeo 'manual'), lo compararemos
con otro archivo .txt que contenga la salida del rolling test a testear.

De esta manera evito tener que revisar a ojo linea por linea de la salida
de un rolling test para comprobar que todo sigue como corresponde luego de
hacer algún cambio en el código.
"""

import filecmp # para comparar los archivos
from colorama import init, Fore # para colorear el texto de salida
# https://pypi.org/project/colorama/

# ---------------------------------------------------------------
# + SETEAR LA RUTA DE LOS ARCHIVOS A COMPARAR SEGUN CORRESPONDA +
# ---------------------------------------------------------------

SALIDA_CORRECTA_RT1 = "test_output_rt1.txt"
SALIDA_CORRECTA_RT2 = "test_output_rt2.txt"

SALIDAS_RT1_A_TESTEAR = [
    "./repo mio/salida1_mio.txt",
    "./repo haruspex/salida1_haruspex.txt"
]

SALIDAS_RT2_A_TESTEAR = [
    "./repo mio/salida2_mio.txt",
    "./repo haruspex/salida2_haruspex.txt"
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
def testear(files_to_test, correct_file, rtest_num):
    print(f"\nTesteando la salida del {Fore.YELLOW}ROLLING TEST {rtest_num}{Fore.RESET}...")
    for file_path in files_to_test:
        resultado_1 = __metodo_1(file_path, correct_file)
        resultado_2 = __metodo_2(file_path, correct_file)
        file_name = file_path.split('/')[-1]
        print(f"\n\t{Fore.CYAN}{file_name}{Fore.RESET} VS Salida Correcta del RT{rtest_num}")
        print(f"\t{resultado_1}")
        print(f"\t{resultado_2}")


# ---------------------------------------------------------------
# +                            MAIN                             +
# ---------------------------------------------------------------

init() # para que funcione el modulo de colores
testear(SALIDAS_RT1_A_TESTEAR, SALIDA_CORRECTA_RT1, rtest_num=1)
testear(SALIDAS_RT2_A_TESTEAR, SALIDA_CORRECTA_RT2, rtest_num=2)
print()

