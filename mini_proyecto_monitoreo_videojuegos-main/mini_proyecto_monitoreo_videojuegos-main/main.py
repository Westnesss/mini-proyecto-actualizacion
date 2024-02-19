from scr.Menu import Menu
from scr.ProgramMonitor import ProgramMonitor

def main():
    menu = Menu()

    while True:
        menu.show_menu()
        option = input("Seleccione una opción: ")
        menu.execute_option(option)

if __name__ == "__main__":
    target_location = (-0.2295, -78.5243)  # Ejemplo de ubicación de destino (Quito, Ecuador)
    program_monitor = ProgramMonitor(target_location)
    program_monitor.start_monitoring()
    main()
