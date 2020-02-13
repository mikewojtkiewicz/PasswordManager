from config.config import Config
from data.include import Methods


def main():
    config = Config()
    config.GetKey()
    cmd = Methods()
    # master_key = True
    master_key = config.master_password()
    while master_key:
        run_script = True
        while run_script:
            menu_input = input("> ")
            if menu_input.lower() == 'm' or menu_input.lower() == 'menu' or menu_input.lower() == 'help':
                print("*** Password Manager Menu ***")
                print("[(m)enu / (g)et / (s)earch / show (all) / (a)dd / (u)pdate / (d)elete / (gen)erate password / (q)uit]")
            elif menu_input.lower() == 'q':
                master_key = False
                run_script = False
            elif menu_input.lower() == 's':
                cmd.search_password()
            elif menu_input.lower() == 'a':
                cmd.store_password()
            elif menu_input.lower() == 'all':
                cmd.list_names()
            elif menu_input.lower() == 'u':
                cmd.update_password()
            elif menu_input.lower() == 'd':
                cmd.remove_password()
            elif menu_input.lower() == 'g':
                cmd.get_password()
            elif menu_input.lower() == 'gen':
                cmd.password_generator()
            else:
                print("Invalid Command!")


main()

