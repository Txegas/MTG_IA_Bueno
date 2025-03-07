
# Informacion téctina
Se programa todo en python usando visual studio code

# Estructura del Proyecto:

### Objetivo general:
Este simulador pretende ser muy completo. El objetivo principal es poder simular partidas contra bots para probar mazos en un entorno controlado. La implementacion de los bots será a largo plazo, el simulador debe poder crear partidas con cualquier cantidad de bots y/o jugadores reales (Las partidas son de 2 a 4 personas, cualquiera de esas personas debeberá poder ponerse en "modo bot" y jugar automaticamente) por lo que lo ideal será comenzar con un simulador solo para jugadores reales (en principio todos los jugadores jugan desde el mismo pc)

### Cartas:
Comenzaremos con un set muy reducido de cartas con mecánicas concretas para probar el funcionamiento del simulador. Con el tiempo se irán añadiendo más cartas y mecánicas por lo que todo debe ser escalable.

### Formato:
El modo de juego que el simulador debe poder manejar es únicamente commander. Es posible que en un futuro quiera añadir standard, por lo que estaría bien que fuese escalable, pero de momento solo commander.

# Componentes principales de MTG:

 - Cartas
 - Jugadores
 - Mazos
 - Turnos
 - Fases de la partida
 - Zonas de juego (campo de batalla, cementerio, exilio, zona del comandante, stack)
 - El stack y su uso (casteo de hechizos y habilidades)
 - Activacion de habilidades activables
 - Habilidades pasivas
 - State based actions

 ### CARTAS:
Creamos una clase Card para guardar la estructura general de las cartas.
Es importante tener una notacion clara para los costes de maná. Hay 7 tipos de maná en magic: rojo (R), verde (G), blanco (W), negro (B), azul (U), incoloro (C) y genérico (N). El maná genérico puede ser pagado con maná de cualquier color o incoloro.

# Instrucciones para Ejecutar el Proyecto

...     


# PSEUDOCÓDIGO DEL SIMULADOR:

...

