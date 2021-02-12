import struct

filename = "datos.txt"

with open(filename, "rb") as f:
    raw_data_1 = f.read(1) #cuando abrimos un archivo en modo 'binario', le podemos especificar al 'read' cuantos bytes leer.
    raw_data_2 = f.read(3) #en cada read, el offset se va moviendo (puntero a las posiciones de los bytes).


print(raw_data_1) #el read (en modo binario) nos devuelve un string de bytes de la forma b'datos'
print(raw_data_2) #(solo que python nos lo muestra decodificado como chars ascii, pero realmente son bytes, 1s y 0s)
print(f"{raw_data_2[0]} {raw_data_2[1]} {raw_data_2[2]}")

print(type(raw_data_1))
print(type(raw_data_1[0]))

with open(filename, "rb") as f:
    raw_data_3 = f.read() #y así leemos el archivo entero.

print(raw_data_3)
print(raw_data_3.decode('utf-8')) #y asi convertimos los bytes en un string como tal (la 'decodificacion' es la traduccion de los binarios
# a algo legible por nosotros, a demas de la codificacion utf-8, tambien está utf-16, unicode, latin1, etc...)
print("")

# ------------------------------------------------------------------------------

filename = "datos_2.txt"

with open(filename, "rb") as f:
    raw_data_4 = f.read() #el read siempre devuelve bytestrings

print(raw_data_4)
print(raw_data_4[0]) #por eso aca nos muestra el ascii del '9'
#(realmente como el archivo es de texto, al escribir el 9 lo codifica como ascii (char), no como un número como tal; veremos el binario del 57)
#(para leer realmente el 9 binario, tendriamos que escribir en el archivo lo siguiente: f.write(struct.pack("<B", 9) )

#lo mismo si 'desempaquetamos' los bytes uno a uno. (serian los bytes 00111001 y 00110111) [importante respetar los 8 bits]
print(struct.unpack("<BB", raw_data_4))
#pero si desempaquetamos los 2 bytes como si fueran una unidad, obviamente cambia el binario. (ahora sería 0011011100111001)
print(struct.unpack("<H", raw_data_4))
#y si cambiamos el little-endian (<) por el big-endian (>), tambien cambia el binario (sería leer de izq a der: 0011100100110111)
print(struct.unpack(">H", raw_data_4))

#el unpack por defecto devuelve la representacion decimal de los binarios dentro de una tupla
#pero si hacemos una asignacion de multiple variables, las asigna una por una directamente con los numeros decimales.

decimal_1, decimal_2 = struct.unpack("<BB", raw_data_4)

print(decimal_1, decimal_2)

# ------------------------------------------------------------------------------
