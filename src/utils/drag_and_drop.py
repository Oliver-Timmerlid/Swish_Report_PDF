from tkinterdnd2 import TkinterDnD

class DragAndDrop:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.setup_drag_and_drop()

    def setup_drag_and_drop(self):
        self.master.drop_target_register('DND_Files')
        self.master.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        file_path = event.data.strip('{}')  # Remove curly braces around the file path
        if file_path.endswith('.csv'):
            self.callback(file_path)
        else:
            print("Please drop a valid CSV file.")