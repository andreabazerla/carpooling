from replit import clear
from Generator import Generator

clear()

instance_generated = False

menu_options = {
    1: 'Generate new instance',
    2: 'Show instance data',
    3: 'Print total distance',
    0: 'Exit',
} 

menu_options_show_instance = {
    1: 'Show distance histogram',
    2: 'Show angle histogram',
    3: 'Show polar coordinates',
    4: 'Show cartesian coordinates',
    5: 'Print total distance',
    6: 'Show graph',
    7: 'Show map',
    0: '<- Back',
}

def print_menu():
    print('Menu\n')
    
    for key in menu_options.keys():
        if (key == 2 or key == 3) and instance_generated == False:
            continue
        print(str(key) + ')', menu_options[key])
    print()

def generate_instance():
    global instance_generated, generator, drivers_coordinates, passengers_coordinates, ORIGIN, upp
    clear()
    
    print('Insert instance data\n')

    origin_latitude = float(input('Latitude of origin (44.83436): ') or 44.83436)
    origin_longitude = float(input('Longitude of origin (11.59934): ') or 11.59934)

    ORIGIN = (origin_latitude, origin_longitude)

    students_number = int(input('Insert students number (100): ') or 100)
    drivers_percentage = float(input('Insert drivers percentage (12): ') or 12)
    mean = float(input('Insert students distribution mean (1000): ') or 1000)
    sd = float(input('Insert students distribution standard deviation (5000): ') or 5000)
    low = float(input('Insert students truncated distribution lower limit (1000): ') or 1000)
    upp = float(input('Insert students truncated distribution upper limit (10000): ') or 10000)

    generator = Generator(ORIGIN, students_number, drivers_percentage, mean, sd, low, upp)

    students_coordinates = generator.get_students_coordinates()

    drivers_coordinates = generator.get_drivers_coordinates(students_coordinates)
    passengers_coordinates = generator.get_passengers_coordinates(students_coordinates)

    instance_generated = True

def print_menu_show_instance():
    print('Show instance\n')
    
    for key in menu_options_show_instance.keys():
        print(str(key) + ')', menu_options_show_instance[key])
    print()

def show_instance():
    clear()

clear()

print('Operative Research - University of Ferrara, Italy - .A. 2020/21\n')
print('Andrea Bazerla - 151792')
print('Taoufik Souidi - 124485')
print()

if __name__=='__main__':
    while(True):
        print_menu()
        
        menu_option = ''
        
        try:
            menu_option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a valid number...')

        if menu_option == 1:
            generate_instance()
            clear()

            print('Instance created :)\n')
            continue
        if menu_option == 2:
            if instance_generated == True:
                output = False
                while(True):
                    if output == False:
                        clear()
                    output = False
                    
                    print_menu_show_instance()
                    
                    menu_show_instance_option = ''
                    
                    try:
                        menu_show_instance_option = int(input('Enter your choice: '))
                    except:
                        print('Wrong input. Please enter a valid number...')

                    if menu_show_instance_option == 1:
                        generator.show_distances_distribution()
                    elif menu_show_instance_option == 2:
                        generator.show_angles_distribution()
                    elif menu_show_instance_option == 3:
                        generator.show_polar_coordinates()
                    elif menu_show_instance_option == 4:
                        generator.show_cartesian_coordinates()
                    elif menu_show_instance_option == 5:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        clear()
                        print('Total distance:', str(generator.get_total_distance(G)/1000) + 'km\n')
                        output = True
                    elif menu_show_instance_option == 6:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        generator.show_graph(G)
                    elif menu_show_instance_option == 7:
                        generator.show_map(ORIGIN, upp, drivers_coordinates, passengers_coordinates)
                    elif menu_show_instance_option == 0:
                        clear()
                        break
                    else:
                        clear()
                        print('Invalid option. Please enter a valid number...\n')
            else:
                clear()
                print('Invalid option. Please enter a valid number...\n')
                continue

        if menu_option == 3:
            origin_coordinates = generator.get_origin_coordinates()
            G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
            clear()
            print('Total distance:', str(generator.get_total_distance(G)/1000) + 'km\n')
            output = True
        elif menu_option == 0:
            clear()
            exit()
        else:
            clear()
            print('Invalid option. Please enter a valid number...\n')