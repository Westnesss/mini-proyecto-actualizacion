from scr.ProgramMonitor import ProgramMonitor

class Menu:
    def __init__(self):
        self.PROGRAM_MONITOR = ProgramMonitor()

    def show_menu(self):
        print("1. Agregar programa a la lista de monitoreo")
        print("2. Eliminar programa de la lista de monitoreo")
        print("3. Mostrar lista de programas en monitoreo")
        print("4. Iniciar monitoreo")
        print("5. Dejar de monitorear")
        print("6. Salir")

    def add_program_to_monitor_list(self):
        program_name = input("Ingrese el nombre del programa: ")
        self.PROGRAM_MONITOR.PROGRAMS_TO_LOG.append(program_name)

    def remove_program_from_monitor_list(self):
        program_name = input("Ingrese el nombre del programa a eliminar: ")
        if program_name in self.PROGRAM_MONITOR.PROGRAMS_TO_LOG:
            self.PROGRAM_MONITOR.PROGRAMS_TO_LOG.remove(program_name)
            print(f"{program_name} eliminado de la lista de monitoreo.")
        else:
            print(f"{program_name} no se encontró en la lista de monitoreo.")

    def show_monitoring_list(self):
        print("Lista de programas en monitoreo:")
        for program in self.PROGRAM_MONITOR.PROGRAMS_TO_LOG:
            print(f"- {program}")

    def start_monitoring(self):
        self.PROGRAM_MONITOR.start_monitoring()

    def stop_monitoring(self):
        print("Deteniendo el monitoreo...")
        exit()

    def execute_option(self, option):
        if option == "1":
            self.add_program_to_monitor_list()
        elif option == "2":
            self.remove_program_from_monitor_list()
        elif option == "3":
            self.show_monitoring_list()
        elif option == "4":
            self.start_monitoring()
        elif option == "5":
            self.stop_monitoring()
        elif option == "6":
            print("Saliendo del programa...")
            exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")
