from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout


class VBoxLayout(QVBoxLayout):
    def __init__(self, margin=2):
        super(VBoxLayout, self).__init__()
        self.setContentsMargins(margin, margin, margin, margin)
        self.setMargin(margin)
        self.setSpacing(margin)


class HBoxLayout(QHBoxLayout):
    def __init__(self, margin=2):
        super(HBoxLayout, self).__init__()
        self.setContentsMargins(margin, margin, margin, margin)
        self.setMargin(margin)
        self.setSpacing(margin)
