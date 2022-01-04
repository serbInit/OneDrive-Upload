from PySide6 import QtCore, QtWidgets, QtGui
import sys
import high_level
import os

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.filelist = []
        self.key = high_level.key_from_password("gigachad")

        self.list = QtWidgets.QListWidget()

        self.info = QtWidgets.QLabel("Test")
        self.download_button = QtWidgets.QPushButton("Download")

        self.left_side = QtWidgets.QVBoxLayout()
        self.right_side = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.addLayout(self.left_side)
        self.layout.addLayout(self.right_side)

        self.left_side.addWidget(self.list)
        self.right_side.addWidget(self.info)
        self.right_side.addWidget(self.download_button)

        self.update_filelist()

        self.download_button.clicked.connect(self.saveFile)


    def fetch_filelist(self):
        high_level.download_file("file_index_table", self.key)
        f = open("downloads/file_index_table.decrypted")
        raw = f.read()
        f.close()
        os.remove("downloads/file_index_table.decrypted")
        liste = []
        raw = raw.removesuffix("\n")
        for line in raw.split("\n"):
            if line.startswith("#"):
                continue
            liste.append(line.split(","))
        return liste

    def update_filelist(self):
        files = self.fetch_filelist()
        print(files)
        self.list.clear()

        for name, passw in files:
            item = QtWidgets.QListWidgetItem(name)
            item.passw = passw
            self.list.addItem(item)

    def saveFile(self):
        file_name = self.list.currentItem().text()
        path, selector = QtWidgets.QFileDialog.getSaveFileName(self, "based", "")
        key = high_level.key_from_password(self.list.currentItem().passw)
        high_level.download_file(file_name, key)
        os.rename(f"downloads/{file_name}.decrypted", path)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
