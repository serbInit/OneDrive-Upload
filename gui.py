from PySide6 import QtCore, QtWidgets, QtGui
import sys
import high_level
import os

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.filelist = []
        passw, accept = QtWidgets.QInputDialog.getText(self, "Password", "")
        if not accept:
            exit()
        
        self.key = high_level.key_from_password(passw)

        self.list = QtWidgets.QListWidget()

        self.info = QtWidgets.QLabel("Test")
        self.upload_button = QtWidgets.QPushButton("Upload")
        self.download_button = QtWidgets.QPushButton("Download")

        self.left_side = QtWidgets.QVBoxLayout()
        self.right_side = QtWidgets.QVBoxLayout()

        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.addLayout(self.left_side)
        self.layout.addLayout(self.right_side)

        self.left_side.addWidget(self.list)
        self.right_side.addWidget(self.info)
        self.right_side.addWidget(self.upload_button)
        self.right_side.addWidget(self.download_button)

        self.update_filelist()

        self.upload_button.clicked.connect(self.uploadFile)
        self.download_button.clicked.connect(self.saveFile)


    def fetch_filelist(self):
        try:
            high_level.download_file("file_index_table", self.key)
        except high_level.pyfile.DoesntExistException:
            os.system("echo '#' > file_index_table")
            high_level.upload_file("file_index_table", self.key)
            os.remove("file_index_table")
            os.remove("file_index_table.jfe")
            high_level.download_file("file_index_table", self.key)
        except high_level.fernet.InvalidToken:
            x = QtWidgets.QMessageBox()
            x.setText("Wrong Password")
            x.exec()
        f = open("downloads/file_index_table.decrypted")
        raw = f.read()
        f.close()
        os.remove("downloads/file_index_table.decrypted")
        liste = []
        raw = raw.removesuffix("\n")
        for line in raw.split("\n"):
            if line.startswith("#") or line.startswith("\n") or line.startswith(" "):
                continue
            if len(line.split("#.öüä.#")) == 2:
                liste.append(line.split("#.öüä.#"))
        return liste

    def update_filelist(self):
        files = self.fetch_filelist()
        print(files)
        self.list.clear()

        for name, passw in files:
            item = QtWidgets.QListWidgetItem(name)
            item.passw = passw
            self.list.addItem(item)

    def uploadFile(self):
        path, selector = QtWidgets.QFileDialog.getOpenFileName(self, "based", "")
        passw, accept = QtWidgets.QInputDialog.getText(self, "Password", "")
        if not accept:
            return
        key = high_level.key_from_password(passw)
        high_level.upload_file(path, key)
        self.addEntry(os.path.basename(path), passw)
        os.remove(path + ".jfe")
        self.update_filelist()

    def addEntry(self, name, passw):
        high_level.download_file("file_index_table", self.key)
        os.rename("downloads/file_index_table.decrypted", "downloads/file_index_table")
        f = open("downloads/file_index_table")
        data = f.read()
        new_data = ""
        f.close()
        if name in data:
            for line in data.split("\n"):
                if line.startswith(name):
                    new_data += f"{name},{passw}\n"
                else:
                    new_data += line + "\n"
        else:
            new_data = data
            new_data += f"\n{name},{passw}"

        f = open("downloads/file_index_table", "w")
        f.write(new_data)
        f.close()
        high_level.upload_file("downloads/file_index_table", self.key)
        os.remove("downloads/file_index_table")
        os.remove("downloads/file_index_table.jfe")

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

