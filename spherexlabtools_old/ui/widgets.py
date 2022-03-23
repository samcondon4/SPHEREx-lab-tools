from PyQt5.QtWidgets import QListWidgetItem


class QListWidgetItemCustom(QListWidgetItem):
    def __init__(self):
        super().__init__(type=QListWidgetItem.UserType)
        self.user_data = None

    def set_user_data(self, user_data):
        self.user_data = user_data


