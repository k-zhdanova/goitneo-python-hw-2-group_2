from exceptions.main import main as run_exceptions_app
from classes.main import main as run_classes_app

def main():
    try:
        print("Which verion of app do you want to test? \n (1) App with exceptions and decorator \n (2) App written with classes \n (q) Quit \n")
        action = input()
        if action == '1':
            run_exceptions_app()
        elif action == '2':
            run_classes_app()
        elif action == 'q':
            print("\nGood bye!")
            return
        else:
            print('\033[91mI don\'t understand that command\033[0m')
    except KeyboardInterrupt:
        print("\nGood bye!")
        return

if __name__ == "__main__":
    main()