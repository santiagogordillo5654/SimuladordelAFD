class ProcesadorFarmacologicoAFD:
    def __init__(self):
        self.estado_inicial = 'q0'
        # q9 es el único estado de aceptación según el documento
        self.estados_aceptacion = {'q9'}

        # Mapeo d e la función de tr ansición δ(q, a) basada en la tabla del avance
        self.transiciones = {
            'q0': {'A': 'q1', 'B': 'q1'},
            'q1': {'A': 'q2', 'B': 'q2'},
            'q2': {'-': 'q3'},
            'q3': {'1': 'q4', '2': 'q4'},
            'q4': {'1': 'q5', '2': 'q5', 'M': 'q6'},
            'q5': {'M': 'q6'},
            'q6': {'-': 'q7'},
            'q7': {'1': 'q8', '2': 'q8'},
            'q8': {'H': 'q9'},
            'q9': {}, # Cualquier entrada adicional estando en q9 va a q_err
        }

    def simular(self, cadena):
        estado_actual = self.estado_inicial
        traza = [f"Inicio en: {estado_actual}"]

        for simbolo in cadena:
            # Si el estado actual tiene transiciones y el símbolo es válido para ese estado
            if estado_actual in self.transiciones and simbolo in self.transiciones[estado_actual]:
                estado_siguiente = self.transiciones[estado_actual][simbolo]
            else:
                # Todo símbolo no listado va al sumidero
                estado_siguiente = 'q_err'

            traza.append(f"Lee '{simbolo}' -> {estado_siguiente}")
            estado_actual = estado_siguiente

            # Optimización: Si cae en estado de error, de ahí no puede salir
            if estado_actual == 'q_err':
                # Consumimos el resto de la cadena marcando q_err
                restante = cadena[cadena.index(simbolo)+1:]
                for s in restante:
                    traza.append(f"Lee '{s}' -> q_err")
                break

        # Verificación final
        if estado_actual in self.estados_aceptacion:
            return "ACEPTADA", traza
        else:
            return "RECHAZADA", traza

def ejecutar_bateria_pruebas():
    procesador = ProcesadorFarmacologicoAFD()

    print("\n" + "="*50)
    print(" BATERÍA DE PRUEBAS AUTOMATIZADA")
    print("="*50)

    # 5 Casos exitosos (cadenas válidas)
    casos_validos = [
        "AA-1M-2H",   # Dosis 1 dígito
        "AB-12M-1H",  # Dosis 2 dígitos
        "BB-2M-2H",   # Dosis 1 dígito, medicamentos BB
        "BA-21M-1H",  # Dosis 2 dígitos, medicamentos BA
        "AA-22M-2H"   # Dosis 2 dígitos, todos 2
    ]


    # 5 Casos con fallas esperadas (cadenas inválidas)
    casos_invalidos = [
        "A-1M-2H",    # Código muy cortoo
        "AB-12-2H",   # Falta la unidad M
        "AB-1M-2",    # Falta la unidad H
        "AB1M2H",     # Faltan guiones
        "CC-1M-2H",   # Caracteres de medicamento inválidos
        "AA-123M-1H"  # Dosis con demasiados dígitos
    ]

    print("\n--- CASOS VÁLIDOS ESPERADOS ---")
    for cadena in casos_validos:
        resultado, _ = procesador.simular(cadena)
        print(f"Cadena: {cadena.ljust(12)} | Resultado: {resultado}")

    print("\n--- CASOS INVÁLIDOS ESPERADOS ---")
    for cadena in casos_invalidos:
        resultado, _ = procesador.simular(cadena)
        print(f"Cadena: {cadena.ljust(12)} | Resultado: {resultado}")


def menu_interactivo():
    procesador = ProcesadorFarmacologicoAFD()

    while True:
        print("\n" + "="*50)
        print(" SIMULADOR DE RECETAS MÉDICAS (AFD)")
        print("="*50)
        print("1. Ingresar cadena manualmente")
        print("2. Ejecutar batería de pruebas")
        print("3. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            cadena = input("\nIngrese la receta a validar (Ej: AB-12M-1H): ")
            resultado, traza = procesador.simular(cadena)

            print("\n--- TRAZA DE ESTADOS ---")
            for paso in traza:
                print(paso)

            print("-" * 25)
            print(f"RESULTADO FINAL: {resultado}")
            print("-" * 25)

        elif opcion == '2':
            ejecutar_bateria_pruebas()
        elif opcion == '3':
            print("\nSaliendo del simulador...")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_interactivo()