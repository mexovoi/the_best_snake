import tkinter as tk
import src.variables as v

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        '''инициализация окна настроек'''
        super().__init__(parent)
        self.parent = parent
        self.geometry(f"{v.MENU_WIDTH}x{v.MENU_HEIGHT}+{v.MENU_LEFT_BOUND}+{v.MENU_UPPER_BOUND}")
        self.title("Settings")
        self.difficulty_names = {
            1: "Easy",
            2: "Medium",
            3: "Hard"
        }
        difficulty_label = tk.Label(self, text="Difficulty")
        difficulty_label.pack()

        self.difficulty_slider = tk.Scale(self, from_=1, to=3, orient=tk.HORIZONTAL, 
                                  length=v.SETTINGS_SLIDER_LENGTH,
                                  label=self.difficulty_names[1],
                                  showvalue=False)

        self.difficulty_slider.pack()
        self.difficulty_slider.set(2)
        self.difficulty_slider.config(label=self.difficulty_names[self.difficulty_slider.get()])

        def update_difficulty_label(val):
            val = int(val)
            self.difficulty_slider.config(label=self.difficulty_names[val])


        self.difficulty_slider.config(command=update_difficulty_label)
        
        colors = v.SETTINGS_COLORS_FOR_SNAKE
        
        color_label = tk.Label(self, text="Choose snake's color")
        color_label.pack()
        
        self.color_choice = tk.StringVar(value=colors[0])
        color_menu = tk.OptionMenu(self, self.color_choice, *colors)
        color_menu.pack()
        
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM)
        
        save_button = tk.Button(button_frame, text="Save", command=self.save_settings)
        save_button.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(button_frame, text="Close", command=self.on_close_button)
        close_button.pack(side=tk.RIGHT, padx=5)
        
    def on_close_button(self):
        '''закрытие окна настроек, окно parent, которое было скрыто от пользователя, становится доступно для пользователя'''
        self.destroy()
        self.parent.deiconify()

    def save_settings(self):
        '''сохранение настроек и закрытие окна настроек, окно parent, которое было скрытие от пользователя, становится доступным ему'''
        difficulty = self.difficulty_slider.get()

        color = self.color_choice.get()
        
        if difficulty == 1:
            v.SNAKE_START_SPEED = 1
            v.MAX_SNAKE_SPEED = 5
            v.MAX_START_AMOUNT_OF_WALLS = 7
            v.MAX_WALL_RANDOM_LENGTH = v.BLOCK_SIZE * 15
            v.FRAMES_BETWEEN_SPEED_BOOSTS = 360
            v.INCREASE_FRAMES_BETWEEN_SPEED_BOOSTS = 600
            v.MAX_START_AMOUNT_OF_FOOD = 20
        elif difficulty == 2:
            v.SNAKE_START_SPEED = 2
            v.MAX_SNAKE_SPEED = 9
            v.MAX_START_AMOUNT_OF_WALLS = 10
            v.MAX_WALL_RANDOM_LENGTH = v.BLOCK_SIZE * 20
            v.FRAMES_BETWEEN_SPEED_BOOSTS = 300
            v.INCREASE_FRAMES_BETWEEN_SPEED_BOOSTS = 300
            v.MAX_START_AMOUNT_OF_FOOD = 10
        elif difficulty == 3:
            v.SNAKE_START_SPEED = 4
            v.MAX_SNAKE_SPEED = 12
            v.MAX_START_AMOUNT_OF_WALLS = 20
            v.MAX_WALL_RANDOM_LENGTH = v.BLOCK_SIZE * 30
            v.FRAMES_BETWEEN_SPEED_BOOSTS = 300
            v.INCREASE_FRAMES_BETWEEN_SPEED_BOOSTS = 0
            v.MAX_START_AMOUNT_OF_FOOD = 10
        v.SNAKE_COLOR = color
        self.destroy()
        self.parent.deiconify()
