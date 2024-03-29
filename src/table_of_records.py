import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import src.variables as v

class TableOfRecords(tk.Toplevel):
    def __init__(self, parent, file_path):
        '''инициализация таблицы рекордов как Toplevel parent, передача файла file_path, где хранятся результаты игроков для таблицы рекордов'''
        super().__init__(parent)
        self.parent = parent
        self.title("Table Window")
        self.geometry(f"{v.table_of_records_width}x{v.table_of_records_hight}+{v.table_of_records_left_bound}+{v.table_of_records_upper_bound}")

        table = ttk.Treeview(self, columns=("place", "name", "score"), show="headings")
        style = ttk.Style()
        style.configure("Treeview.Heading", background="gray", foreground=v.table_of_records_header_color)
        style.configure("Treeview.Cell", font=(v.table_of_records_font, v.table_of_records_text_size))
        style.configure("Treeview", background=v.table_of_records_background_color, foreground=v.table_of_records_text_color, rowheight=v.table_of_records_text_size * 2)

        style.configure("Treeview.Heading", font=(v.table_of_records_header_font, v.table_of_records_header_size))
        table.heading("place", text="Place")
        table.column("place", anchor="center")
        table.heading("name", text="Name")
        table.column("name", anchor="center")
        table.heading("score", text="Score")
        table.column("score", anchor="center")
        with open(file_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                last_space_index = line.rfind(" ")
                if last_space_index == -1:
                    place, name, score = i+1, line, ""
                else:
                    place, name, score = i+1, line[:last_space_index], line[last_space_index+1:]
                table.insert("", "end", values=(place, name, score), tags=("Treeview.Cell",))
        table.tag_configure("Treeview.Cell", font=(v.table_of_records_font, v.table_of_records_text_size))
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def delete_selected_row():
            '''удаление выбранного пользователем ряда таблицы рекордов'''
            selected_item = table.selection()[0]
            values = table.item(selected_item)["values"]
            if values[0] != "1":
                confirm = messagebox.askyesno("Delete row", "Are you sure you want to delete the selected row?")
                if confirm:
                    table.delete(selected_item)
                    with open(file_path, "w") as f:
                        for j, line in enumerate(lines):
                            if j == int(values[0]) - 1:
                                continue
                            f.write(line)
        
        def close_table_button():
            '''закрытие таблицы рекордов и появление окна меню parent'''
            self.parent.deiconify()
            self.destroy()

        delete_button = ttk.Button(self, text="Delete selected row", command=delete_selected_row)
        close_button = ttk.Button(self, text="Close", command=close_table_button)
        close_button.pack(side="bottom")
        delete_button.pack(side="bottom")
        table.pack(fill="both", expand=True, side="top")

        self.mainloop()