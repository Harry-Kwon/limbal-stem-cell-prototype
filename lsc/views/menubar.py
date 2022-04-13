from PySide2.QtWidgets import QMenuBar, QAction, QFileDialog
from lsc.models import state, grade_regions
import json, os

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        # file
        file_menu = self.addMenu("File")

        open_action = QAction("Open", file_menu)
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("Save Grades", file_menu)
        save_action.triggered.connect(self.save_grades)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
    
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        file_path, _ = file_dialog.getOpenFileName()

        state.load_image(file_path)
        print(f"loaded file {state.current_file}")
    
    def save_grades(self):
        dir = os.path.dirname(state.current_file)
        basename = os.path.basename(state.current_file).split(".")[0]

        dir = QFileDialog.getExistingDirectory(self, dir=dir)
        
        grades = {}
        grades["grades"] = [g.score for g in grade_regions]
        for i in range(len(grade_regions)):
            g = grade_regions[i]
            grades[i] = {
                "grade": g.score,
                "angle": [g.min_angle, g.max_angle],
                "radius": [g.min_radius, g.max_angle]
            }
            with open(os.path.join(dir, f"{basename}_grades.json"), "w+") as f:
                json.dump(grades, f, indent=4)