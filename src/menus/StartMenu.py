from time import sleep

class StartMenu:
    def __init__(self) -> None:
        self.open()
    
    def open(self):
        print('welcome to lazy fight!')
        sleep(1)
        print('select player:')