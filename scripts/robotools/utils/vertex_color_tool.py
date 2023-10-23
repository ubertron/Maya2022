import pymel.core as pm

from PySide2.QtWidgets import QLabel, QSizePolicy
from robotools.widgets.maya_widgets import MayaWidget, ColorPickerButton, \
    SwatchMultiButton
from robotools.widgets.generic_widget import GenericWidget
from functools import partial

class VertexColorTool(MayaWidget):
    _name = 'Vertex Color Tool'
    button_size = 24

    def __init__(self):
        super(VertexColorTool, self).__init__(self._name)
        self.swatch_button = ColorPickerButton('Apply Vertex Color', self.button_size,
                                               self.apply_vertex_color_clicked)
        self.add_widget(self.swatch_button)
        self.add_button('Apply Random Vertex Color',
                        self.apply_random_vertex_color_clicked)
        self.add_button('Remove Vertex Color',
                        self.remove_vertex_color_clicked)
        self.add_button('Select Faces By Vertex Color',
                        self.select_by_vertex_color_clicked)
        self.selection_label = QLabel()
        self.selection_label.setWordWrap(True)
        self.selection_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.add_widget(self.selection_label)
        self.button_widget = GenericWidget()
        self.button_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.add_widget(self.button_widget)
        self.setMinimumWidth(328)
        self.script_job_id = None
        self.current_nodes = None
        self.enable_script_job()
        self.refresh_ui()

    def enable_script_job(self):
        self.script_job_id = pm.scriptJob(event=['SelectionChanged', self.refresh_ui])

    def disable_script_job(self):
        pm.scriptJob(kill=self.script_job_id)

    def refresh_ui(self):
        self.current_nodes = self.current_transforms
        transform_names = [x.name() for x in self.current_transforms]
        selection = ', '.join(transform_names) if transform_names else 'None'
        self.selection_label.setText(f"Selection: {selection}")
        self.button_widget.clear_layout()
        for x in self.parsed_vertex_colors:
            print(f'Parsed vertex color: {x}, {type(x)}')
            button = SwatchMultiButton(self.button_size, x)
            button.add_button('Select', partial(self.select_vertex_color, x))
            button.add_button('Remove', self.test_event)
            self.button_widget.add_widget(button)
        self.button_widget.setVisible(len(self.vertex_colors) > 0)
        self.button_widget.updateGeometry()
        self.resize(self.width(), self.sizeHint().height())
        self.adjustSize()

    def apply_vertex_color_clicked(self):
        ad_vertex_colors.apply_vertex_color([x/255 for x in self.swatch_button.color])

    @staticmethod
    def remove_vertex_color_clicked():
        ad_vertex_colors.remove_vertex_color()

    @staticmethod
    def test_event():
        print('Test')

    @property
    def current_transforms(self):
        return ad_node.get_transforms()

    @staticmethod
    def apply_random_vertex_color_clicked():
        ad_vertex_colors.apply_vertex_color()

    @staticmethod
    def apply_vertex_color(color):
        ad_vertex_colors.apply_vertex_color(color)

    def select_vertex_color(self, color):
        self.disable_script_job()
        ad_vertex_colors.select_faces_by_vertex_color(color)
        self.enable_script_job()

    def select_by_vertex_color_clicked(self):
        self.disable_script_job()
        ad_vertex_colors.select_faces_by_selected_vertex_colors()
        self.enable_script_job()

    @property
    def vertex_colors(self):
        vertex_colors = []
        for x in self.current_transforms:
            vertex_colors.extend(ad_vertex_colors.get_face_vertex_color_dict(x).keys())
        return list(set(vertex_colors))

    @property
    def parsed_vertex_colors(self):
        return [self.parse_vertex_color(x) for x in self.vertex_colors]

    @staticmethod
    def parse_vertex_color(str_color):
        return [float(x) for x in str_color[1: -1].split(', ')]

    def closeEvent(self, event):
        if pm.scriptJob(exists=self.script_job_id):
            pm.scriptJob(kill=self.script_job_id)
        event.accept()
