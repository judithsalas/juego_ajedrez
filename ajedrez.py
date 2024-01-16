class Ajedrez:
    def __init__(self, jugador):
        # Inicialización de la clase Ajedrez con el nombre del jugador
        self.jugador = jugador
        # Creación de un tablero vacío de 8x8
        self.tablero = [['' for _ in range(8)] for _ in range(8)]
        # Inicialización del tablero con las piezas de ajedrez
        self.iniciar_tablero()
        # Lista para almacenar los movimientos realizados
        self.movimientos = []
        # Guardar la partida inicial en un archivo
        self.guardar_partida()

    def iniciar_tablero(self):
        # Inicialización del tablero con las piezas de ajedrez en sus posiciones iniciales
        self.tablero[0] = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
        self.tablero[1] = ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"]
        for i in range(2, 6):
            self.tablero[i] = [' ' for _ in range(8)]
        self.tablero[6] = ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"]
        self.tablero[7] = ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]

    def guardar_partida(self):
        # Guardar el estado actual del tablero en un archivo
        with open(f"{self.jugador}_ajedrez.txt", "a") as archivo:
            for fila in self.tablero:
                archivo.write("\t".join(map(str, fila)) + "\n")
            archivo.write("\n")

    def mostrar_tablero(self):
        # Mostrar el tablero en la consola
        columna_letras = "abcdefgh"
        print("    " + "   ".join(columna_letras))
        for i, fila in enumerate(self.tablero[::-1], 1):
            print(f"{9 - i}  {' '.join(fila)}")

    def mover_ficha(self, start, end):
        # Mover una ficha en el tablero y guardar el movimiento
        start = (ord(start[0]) - ord('a'), int(start[1]) - 1) if len(start) == 2 else (ord(start[0]) - ord('a'), int(start[1:]) - 1)
        end = (ord(end[0]) - ord('a'), int(end[1]) - 1)
        if start == end:
            print("\nNo se ha cambiado de posicion")
            return
        if self.tablero[start[1]][start[0]] == ' ':
            print("\nNo se puede retroceder")
            return
        if self.tablero[end[1]][end[0]] != ' ':
            print("\nYa hay una ficha en esa posicion")
            return
        self.tablero[end[1]][end[0]] = self.tablero[start[1]][start[0]]
        self.tablero[start[1]][start[0]] = ' '
        self.guardar_movimiento(start, end)
    
    def enroque(self, tipo):
        # Realizar el enroque (corto o largo) y guardar el movimiento
        if tipo == 'corto':
            self.tablero[0][6] = self.tablero[0][4]
            self.tablero[0][5] = self.tablero[0][7] = ' '
            self.guardar_movimiento((0, 4), (0, 6))
        elif tipo == 'largo':
            self.tablero[0][2] = self.tablero[0][4]
            self.tablero[0][3] = self.tablero[0][0] = ' '
            self.guardar_movimiento((0, 4), (0, 2))
        else:
            print("\nTipo de enroque no valido. Utilice 'corto' o 'largo'.")

    def guardar_movimiento(self, start, end):
        # Guardar el movimiento en el archivo y en la lista de movimientos
        with open(f"{self.jugador}_ajedrez.txt", "a") as archivo:
            archivo.write("\nTablero despues del movimiento:\n")
            for fila in self.tablero:
                archivo.write('\t'.join(map(str, fila)) + '\n')
            archivo.write(f"{self.convertir_notacion(start)} -> {self.convertir_notacion(end)}\n")
        self.movimientos.append((start, end))

    def consultar_jugada(self, mover_numero):
        # Consultar el estado del tablero después de un número específico de movimientos
        if 1 <= mover_numero <= len(self.movimientos):
            self.iniciar_tablero()
            for i in range(mover_numero):
                start, end = self.movimientos[i]
                self.mover_ficha(start, end)
            return self.tablero
        else:
            print("\nNo se puede introducir ese numero")
            return None

    def convertir_notacion(self, posicion):
        # Convertir la posición del tablero a notación alfanumérica
        columna = chr(posicion[0] + ord('a'))
        fila = str(posicion[1] + 1)
        return f"{columna}{fila}"


def jugar_ajedrez(jugador):
    # Crear una instancia de la clase Ajedrez y comenzar el juego
    juego_ajedrez = Ajedrez(jugador)
    juego_ajedrez.mostrar_tablero()
    mover_numero = 0

    while True:
        # Solicitar entrada del usuario para mover una ficha o salir
        start = input("\nIntroduce la posicion de la ficha que deseas mover (o 'salir' para finalizar el juego): ").lower()

        if start == 'salir':
            # Permitir al usuario revisar movimientos pasados antes de salir
            revisit = input("\nDesea volver a ver una de las jugadas realizadas? (s/n): ").lower()
            if revisit == 's':
                movimiento_consultar = int(input("Introduzca el número de jugada que quiere consultar: "))
                estado_tablero = juego_ajedrez.consultar_jugada(movimiento_consultar)
                if estado_tablero:
                    print("\nTablero después del movimiento {}:".format(movimiento_consultar))
                    for fila in estado_tablero:
                        print(fila)
                else:
                    print("\nNo se han consultado movimientos")
            break

        # Solicitar posición de destino y mover la ficha
        end = input("Introduce la posición donde te gustaría mover la pieza: ").lower()
        mover_numero += 1
        juego_ajedrez.mover_ficha(start, end)
        juego_ajedrez.mostrar_tablero()
        
        if start == 'enroque':
            tipo_enroque = input("¿Enroque corto o largo? ").lower()
            juego_ajedrez.enroque(tipo_enroque)
            juego_ajedrez.mostrar_tablero()


if __name__ == "__main__":
    # Iniciar el juego de ajedrez con el nombre del jugador
    jugador = input("Cual es el nombre de la partida (insertar nombre de jugador)?: ")
    jugar_ajedrez(jugador)
