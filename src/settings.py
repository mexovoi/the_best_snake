import tkinter as tk
import src.variables as v

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        '''инициализация окна настроек'''
        super().__init__(parent)
        self.parent = parent
        self.geometry(f"{v.menu_width}x{v.menu_height}+{v.menu_left_bound}+{v.menu_upper_bound}")
        self.title("Settings")
        self.difficulty_names = {
            1: "Easy",
            2: "Medium",
            3: "Hard"
        }
        difficulty_label = tk.Label(self, text="Difficulty")
        difficulty_label.pack()

        self.difficulty_slider = tk.Scale(self, from_=1, to=3, orient=tk.HORIZONTAL, 
                                  length=v.settings_slider_length,
                                  label=self.difficulty_names[1],
                                  showvalue=False)

        self.difficulty_slider.pack()
        self.difficulty_slider.set(2)
        self.difficulty_slider.config(label=self.difficulty_names[self.difficulty_slider.get()])

        def update_difficulty_label(val):
            val = int(val)
            self.difficulty_slider.config(label=self.difficulty_names[val])


        self.difficulty_slider.config(command=update_difficulty_label)
        
        colors = v.settings_colors_for_snake
        
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
            v.snake_start_speed = 1
            v.max_snake_speed = 5
            v.max_start_amount_of_walls = 7
            v.max_wall_random_length = v.block_size * 15
            v.frames_between_speed_boosts = 360
            v.increase_frames_between_speed_boosts = 600
            v.max_start_amount_of_food = 20
        elif difficulty == 2:
            v.snake_start_speed = 2
            v.max_snake_speed = 9
            v.max_start_amount_of_walls = 10
            v.max_wall_random_length = v.block_size * 20
            v.frames_between_speed_boosts = 300
            v.increase_frames_between_speed_boosts = 300
            v.max_start_amount_of_food = 10
        elif difficulty == 3:
            v.snake_start_speed = 4
            v.max_snake_speed = 12
            v.max_start_amount_of_walls = 20
            v.max_wall_random_length = v.block_size * 30
            v.frames_between_speed_boosts = 300
            v.increase_frames_between_speed_boosts = 0
            v.max_start_amount_of_food = 10
        v.snake_color = color
        self.destroy()
        self.parent.deiconify()
