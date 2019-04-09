import sys, os

# Main definition - constants
from src.agroldETL import getAllValuesOfAllAttributesOfADataset, createDataFrameFromFilterAndResponseValues, serverConnection

menu_actions = {}


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system("cls" if os.name == "nt" else "clear")

    print("Welcome,\n")
    print("Please choose the menu you want to start:")
    print("1. To retreive all data")
    print("2. To retreive filter data")
    print("\n0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    os.system("cls" if os.name == "nt" else "clear")
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    print("Menu --> To retreive all data !\n")
    dataset = input('Enter your database name eg:athaliana_eg_gene : ')
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    print("Menu --> To retreive filter data !\n")
    server = serverConnection(verbose=True)
    print('Example of databse name : athaliana_eg_gene\n')
    dataset = input('Enter your database name : ')
    print('\n\n')
    print('Example of liste for filters : ensembl_gene_id external_gene_name description chromosome_name start_position end_position')
    filter = input('Enter your list of filter : ')
    filter = filter.split()
    print('\n\n')
    resp, filt = getAllValuesOfAllAttributesOfADataset(server, dataset, filter=filter)
    createDataFrameFromFilterAndResponseValues(filt, resp, fileName='dataset')
    print('###########################################################################################################')
    print(resp)
    print('###########################################################################################################')
    print(filt)
    print('###########################################################################################################')
    print("9. Back")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
'''
if __name__ == "__main__":
    # Launch main menu
    main_menu()
'''