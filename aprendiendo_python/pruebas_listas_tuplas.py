# ESTRUCTURAS DE DATOS

# Listas
# (son dinamicas -> podemos hacerles cambios en tiempo de ejecución, como agregar o eliminar elementos, no tienen una longitud fija)

lista = ['a', 8, "hola", 3.14] #podemos tener distintos tipos de datos almacenados, no hace falta que sean todos del mismo.
print(lista)

nombres = ["juan", "lucas", "sebastian"]
print(nombres)
print(nombres[0]) #para acceder a un elemento concreto.
print(nombres[0].upper()) #tambien podemos usar metodos de strings, cada posicion es como una variable.
print(nombres[-1]) #para acceder al ultimo elemento de la lista.
print(nombres[-2]) #para acceder al anteultimo elemento de la lsta,..., y así. :o

nombres[0] = "roberto" #modificar un elemento de la lista.
print(nombres)
nombres.append("nicolas") #agregar un elemento al final de la lista.
print(nombres)
nombres.insert(0, "carlos") #insertar un elemento en cierta posicion de la lista (hace un 'shift'/corrimiento de los demás).
print(nombres)
del nombres[1] #eliminar un elemento de cierta posicion de la lista.
print(nombres)
aux = nombres.pop() #elimino y retorno el ultimo elemento de la lista (como el 'pop' de las pilas/stacks)
print(nombres)
print(aux)
aux = nombres.pop(0) #elimino y retorno el elemento de cierta posicion de la lista
print(nombres)
print(aux)
nombres.remove("sebastian") #elimino el elemento de la lista cuyo valor es el especificado (solo la primera ocurrencia).
print(nombres)

autos = ['bmw', 'audi', 'toyota', 'subaru']
print(autos)
autos.sort() #ordenar una lista alfabeticamente (es irreversible, no podremos volver al orden original de la lista).
print(autos)
autos.sort(reverse=True) #ordenar una lista alfabeticamente pero en sentido inverso.
print(autos)
print(sorted(autos)) #funcion que devuelve la lista ordenada, pero sin modificarla.
print(autos)
autos.reverse() #le "da la vuelta" a la lista (es permanente, salvo que volvamos a hacer 'reverse')
print(autos)
print(len(autos)) #funcion que devuelve la cantidad de elementos de la lista.

numeros = [1,2,3,4,5]
print(max(numeros)) #maximo de la lista.
print(min(numeros)) #minimo de la lista.
print(sum(numeros)) #suma de los elementos de la lista.

# ---

#COPIAR LISTAS (se copian sus valores, no alguna 'referencia')
lista1 = [1, 2, 3]
lista2 = lista1[:] #esto es un 'slice'
print(lista1)
print(lista2)
lista1.append(10)
lista2.append(20)
print(lista1)
print(lista2)
#para que ambas referencias sean las mismas, y los cambios hechos e una se vean en la otra (ya que apunta a la misma lista)
#se hace una asigancion comun "lista2 = lista1"

# ---

#Listas CONSTANTES ('Tuples')
# se definen como las listas, pero con parentesis. Sus elementos no pueden ser modificados.
#"Python refers to values that cannot change as immutable, and an immutable list is called a tuple."
lista_constante = (1, 2, 3)
print(lista_constante)
print(lista_constante[0])
#lista_constante[0] = 7
print(min(lista_constante))
#lo que sí podemos es redefinir completamente la tupla.
lista_constante = ('a', 'b', 'c', 'd')
print(lista_constante)