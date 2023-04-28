import tkinter as tk
import src.variables as v
from src.table_of_records import TableOfRecords
from src.snake_game import SnakeGame
from src.settings import SettingsWindow

def find_dict_with_name(dict_list, name):
    for d in dict_list:
        if d['name'] == name:
            return d
    return None

def validate_entry(text):
    '''проверка введенного текста в окно на валидность,
    то есть проверка не превышения максимальной длины текста v.MAX_LEN_NAME_IN_SCOREBOARD'''
    if len(text) > v.MAX_LEN_NAME_IN_SCOREBOARD:
        return False
    else:
        return True
        
class Menu:
    def __init__(self):
        '''создание окна меню игры'''
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.columnconfigure(0, weight=1)
        self.root.configure(bg="navy")
        self.root.geometry(f"{v.MENU_WIDTH}x{v.MENU_HEIGHT}+{v.MENU_LEFT_BOUND}+{v.MENU_UPPER_BOUND}")
        self.button_start = tk.Button(self.root, text='Start', width=v.BUTTONS_SIZE_X, height=v.BUTTONS_SIZE_Y, command=self.on_button_start_click)
        self.button_start.pack(pady=v.DIST_BETWEEN_BUTTONS)
        self.button_settings = tk.Button(self.root, text='Settings', width=v.BUTTONS_SIZE_X, height=v.BUTTONS_SIZE_Y, command=self.on_button_settings_click)
        self.button_settings.pack(pady=v.DIST_BETWEEN_BUTTONS)
        self.button_table_records = tk.Button(self.root, text='Table of Records', width=v.BUTTONS_SIZE_X, height=v.BUTTONS_SIZE_Y,
                                    command=self.on_button_table_records_click)
        self.button_table_records.pack(pady=v.DIST_BETWEEN_BUTTONS)
        self.button_exit = tk.Button(self.root, text='Quit game', width=v.BUTTONS_SIZE_X, height=v.BUTTONS_SIZE_Y, command=self.on_button_quit_click)
        self.button_exit.pack(pady=v.DIST_BETWEEN_BUTTONS)

        self.root.mainloop()


    def button_exit_command(self, new_window):
        '''закрытие окна и появление раннее скрытого от пользователя окна меню'''
        new_window.destroy()
        self.root.deiconify()

    def on_button_start_click(self):
        '''запуск игрового процесса SnakeGame и скрытие окна меню, после окончания игрового процесса создание окна для ввода имени для сохранения в таблице рекордов 
        и после его закрытия появление раннее скрытого от пользователя окна меню'''
        print("Game was started!")
        self.root.withdraw()
        game_snake = SnakeGame()
        new_window = tk.Toplevel(self.root)
        new_window.geometry(f"+{v.MENU_LEFT_BOUND}+{v.MENU_UPPER_BOUND}")
        text_entry = tk.Entry(new_window, width=v.AFTER_GAME_ENTRY_BUTTON_WIDTH, validate="key", validatecommand=(new_window.register(validate_entry), '%P'), invalidcommand=lambda: print("Too long name!"), textvariable=v)
        text_entry.pack()
        save_button = tk.Button(new_window, text="Enter your name", command=lambda: self.add_to_scoreboard(new_window, text_entry, game_snake.prev_score))
        save_button.pack()
        self.button_exit = tk.Button(new_window, text='Close', command=lambda: self.button_exit_command(new_window))
        self.button_exit.pack()

    def add_to_scoreboard(self, window, entry, score):
        '''добавление в таблицу рекордов результата score игрока с именем, которое введется во вход entyr окна window,
        если пользователь не вводит имя, то результат не записывается. если пользователь уже есть в таблице, то записывается максимум из его результатов'''
        text = entry.get()
        window.destroy()
        if text == '':
            self.root.deiconify()
            return
        with open('table_of_records_results.txt') as file:
            high_scores = []
            for line in file:
                words = line.split()
                name = ' '.join(words[:-1])
                result = ' '.join(words[-1:])
                high_scores.append({"name": name, "score": result})
        if find_dict_with_name(high_scores, text) == None:
            high_scores.append({"name": text, "score": score})
        else:
            find_dict_with_name(high_scores, text)["score"] = max(int(find_dict_with_name(high_scores, text)["score"]), score)
        for d in high_scores:
            d["score"] = int(d["score"])
        sorted_data = sorted(high_scores, key=lambda x: x["score"], reverse=True)
        txt_data = ''
        for d in sorted_data:
            txt_data += f'{d["name"]} {d["score"]}\n'
        with open("table_of_records_results.txt", "w") as f:
            f.write(txt_data)
        self.root.deiconify()

    def on_button_settings_click(self):
        '''открытие окна настроек игры и скрытие меню от пользователя'''
        print("Settings")
        self.root.withdraw()
        SettingsWindow(self.root)

    def on_button_table_records_click(self):
        '''открытие таблицы рекордов и скрытие меню'''
        print("This is table of records!")
        self.root.withdraw()
        TableOfRecords(self.root, "src/table_of_records_results.txt")

    def on_button_quit_click(self):
        '''закрытие меню и завершение программы'''
        print("Goodbye!")
        self.root.destroy()