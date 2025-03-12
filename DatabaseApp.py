from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QPushButton, QComboBox,
                             QLineEdit, QLabel, QHBoxLayout, QHeaderView, QAbstractItemView, QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
import sys

from PyQt5.QtWidgets import QHeaderView, QStyleOptionButton, QStyle
from PyQt5.QtCore import Qt

class CheckableHeader(QHeaderView,QTableView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.is_checked_list = []
        self.check_rects = []  # تعریف لیست برای نگهداری موقعیت چک‌باکس‌ها

    from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QHeaderView, QStyle,
                                 QStyleOptionButton, QMessageBox)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QBrush, QColor
    from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
    import sys

    class CheckableHeader(QHeaderView):
        def __init__(self, orientation, parent=None):
            super().__init__(orientation, parent)
            self.setSectionsClickable(True)
            self.is_checked_list = []
            self.check_rects = []

        def update_checked_list(self):
            count = self.count()
            self.is_checked_list = [False] * count
            self.check_rects = [None] * count

        def paintSection(self, painter, rect, logicalIndex):
            super().paintSection(painter, rect, logicalIndex)

            option = QStyleOptionButton()
            option.state = QStyle.State_Enabled | (
                QStyle.State_On if self.is_checked_list[logicalIndex] else QStyle.State_Off)

            checkbox_size = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, option, self)
            checkbox_rect = checkbox_size
            checkbox_rect.moveCenter(rect.center())
            self.check_rects[logicalIndex] = checkbox_rect

            option.rect = checkbox_rect
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

        def mousePressEvent(self, event):
            try:
                for i, rect in enumerate(self.check_rects):
                    if rect and rect.contains(event.pos()):
                        if i < len(self.is_checked_list):
                            self.is_checked_list[i] = not self.is_checked_list[i]
                            self.updateSection(i)
                        break
                super().mousePressEvent(event)
            except Exception as e:
                self.show_error_message(f"Error occurred: {e}")

        def is_checked(self, index):
            return self.is_checked_list[index]



class DatabaseApp(QMainWindow):
    def __init__(self):
        try:

            super().__init__()

            self.setWindowTitle('PersonalInfo Table Viewer')
            self.setGeometry(200, 200, 800, 600)
            # Initialize selected_column to -1
            self.selected_column = -1
            self.create_ui()
            print("uuuuu")
            # Connect header click event
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def create_ui(self):
        try:

            # Layout
            layout = QVBoxLayout()

            # Table View
            self.table_view = QTableView()

            layout.addWidget(self.table_view)

            # ComboBox for selecting filter column (header names)
            self.column_combo = QComboBox()
            layout.addWidget(self.column_combo)

            # Filter input for value based on selected column
            self.filter_input = QLineEdit()
            self.filter_input.setPlaceholderText("Enter search value...")
            layout.addWidget(self.filter_input)

            # Search button
            self.search_button = QPushButton("Search")
            layout.addWidget(self.search_button)
            self.search_button.clicked.connect(self.filter_data)

            # Row selection combo box
            self.rows_per_page_combo = QComboBox(self)
            self.rows_per_page_combo.addItems(["10", "20", "50", "100"])
            self.rows_per_page_combo.currentIndexChanged.connect(self.change_page_size)

            layout.addWidget(self.rows_per_page_combo)

            # Pagination buttons
            pagination_layout = QHBoxLayout()
            self.prev_button = QPushButton("Previous Page")
            self.next_button = QPushButton("Next Page")
            self.page_label = QLabel("Page: 1")
            pagination_layout.addWidget(self.prev_button)
            pagination_layout.addWidget(self.page_label)
            pagination_layout.addWidget(self.next_button)
            layout.addLayout(pagination_layout)

            self.prev_button.clicked.connect(self.previous_page)
            self.next_button.clicked.connect(self.next_page)

            # Main widget and layout setup
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

            # Set up database
            self.db = QSqlDatabase.addDatabase('QODBC')
            connection_string = ('DRIVER={SQL Server};'
                                 'SERVER=192.168.10.1;'
                                 'DATABASE=HS;'
                                 'UID=sa;'
                                 'PWD=*ab123456789'
                                 )
            self.db.setDatabaseName(connection_string)

            if not self.db.open():
                print("Unable to connect to database")
                if not self.db.open():
                    QMessageBox.critical(self, "Database Error", "Unable to connect to the database.")
                    return
                print("ccccc")
                sys.exit(1)

            # Model to manage table data
            self.model = QSqlQueryModel()

            # Page state
            self.page_size = 10
            self.current_page = 0
            self.total_rows = self.get_total_row_count()
            self.update_table_view()

            self.table_view.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.table_view.viewport().update()

            # Connect header click event
            # Load header names into combo box
            self.header = CheckableHeader(Qt.Horizontal, self.table_view)
            self.table_view.setHorizontalHeader(self.header)


            self.load_header_names()
            print("ffff")
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def add_checkbox_to_header(self, index):
        try:
            # Create a widget to hold the checkbox and add it to the header
            widget = QWidget()
            layout = QHBoxLayout(widget)
            checkbox = QCheckBox(self)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setSectionResizeMode(index, QHeaderView.Stretch)
            self.checkboxes.append(checkbox)
            self.setSectionResizeMode(index, QHeaderView.Fixed)
            self.setStretchLastSection(True)
            model_index = self.parent().model().index(0, index)  # سطر و ستون مورد نظر را مشخص کنید
            self.parent().setIndexWidget(model_index, widget)
        except Exception as e:
           self.show_error_message(f"Error occurred: {e}")

    def load_header_names(self):
        try:

            """
            Load the header names from the model into the QComboBox for filtering.
            """
            query = "SELECT * FROM PersonalInfo WHERE 1=0"  # Load only headers
            self.model.setQuery(query)
            self.column_combo.clear()

            for col in range(self.model.columnCount()):
                header = self.model.headerData(col, Qt.Horizontal)
                self.column_combo.addItem(header)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def toggle_column_visibility(self):
        try:
            # این متد وضعیت چک‌باکس‌ها را بررسی می‌کند و بر اساس آن نمایش یا پنهان کردن ستون‌ها را انجام می‌دهد.
            for index, checkbox in enumerate(self.header.checkboxes):
                if checkbox.isChecked():
                    self.table_view.setColumnHidden(index, False)
                else:
                    self.table_view.setColumnHidden(index, True)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def toggle_columns(self):
        try:
            # Show or hide columns based on the checkboxes in the header
            for index in range(self.model.columnCount()):
                if self.header.is_checked(index):
                    self.table_view.setColumnHidden(index, False)
                else:
                    self.table_view.setColumnHidden(index, True)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def get_total_row_count(self):
        try:
            query = "SELECT COUNT(*) FROM PersonalInfo"
            model = QSqlQueryModel()
            model.setQuery(query)
            return model.record(0).value(0)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def filter_data(self):
        selected_column = self.column_combo.currentText()
        filter_value = self.filter_input.text()

        # اگر فیلد انتخاب‌شده عددی باشد
        if selected_column in ["Age", "Salary"]:
            filter_expression = f"{selected_column} = {filter_value}"
        else:
            filter_expression = f"{selected_column} LIKE '%{filter_value}%'"

        self.update_table_view(filter_expression)

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def change_page_size(self):
        try:
            selected_value = int(self.rows_per_page_combo.currentText())
            self.page_size = selected_value
            self.current_page = 0  # Reset to the first page
            self.update_table_view()
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def highlight_column(self, column_index, color):
        try:
            for row in range(self.table_view.model().rowCount()):
                index = self.table_view.model().index(row, column_index)
                self.table_view.model().setData(index, QBrush(color), role=Qt.BackgroundRole)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def header_clicked(self, logicalIndex):
        try:
            # Highlight the entire column
            self.selected_column = logicalIndex
            self.highlight_column(self.selected_column, QColor('lightgreen'))

            # Refresh the view to apply changes
            self.table_view.viewport().update()

        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def update_table_view(self, filter_expression=None):
        try:
            offset = self.current_page * self.page_size
            # استفاده از ROW_NUMBER() برای صفحه‌بندی
            query = f"""
            SELECT * FROM (
                SELECT *, ROW_NUMBER() OVER (ORDER BY ID) AS RowNum
                FROM PersonalInfo
                {'WHERE ' + filter_expression if filter_expression else ''}
            ) AS RowConstrainedResult
            WHERE RowNum > {offset} AND RowNum <= {offset + self.page_size}
            ORDER BY RowNum
            """

            self.model.setQuery(query)
            self.table_view.setModel(self.model)
            self.page_label.setText(f"Page: {self.current_page + 1}")

            # Set the default selection mode to row selection
            self.table_view.setSelectionBehavior(QTableView.SelectRows)
            self.table_view.setSelectionMode(QTableView.SingleSelection)

            # Clear previous column highlight
            if self.selected_column != -1:
                for row in range(self.table_view.model().rowCount()):
                    index = self.table_view.model().index(row, self.selected_column)
                    self.table_view.model().setData(index, QBrush(QColor('white')), role=Qt.BackgroundRole)

        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def next_page(self):
        if (self.current_page + 1) * self.page_size < self.total_rows:
            self.current_page += 1
            self.update_table_view()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table_view()

    def selection_changed(self, selected, deselected):
        try:
            # Highlight selected rows
            for index in selected.indexes():
                self.table_view.model().setData(index, QBrush(QColor('lightblue')), role=Qt.BackgroundRole)

            # Remove highlight from deselected rows
            for index in deselected.indexes():
                self.table_view.model().setData(index, QBrush(QColor('white')), role=Qt.BackgroundRole)
        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

    def header_clicked(self, logicalIndex):

        try:
            # Highlight the entire column
            self.selected_column = logicalIndex
            for row in range(self.table_view.model().rowCount()):
                index = self.table_view.model().index(row, self.selected_column)
                self.table_view.model().setData(index, QBrush(QColor('lightgreen')), role=Qt.BackgroundRole)

            # Refresh the view to apply changes
            self.table_view.viewport().update()

        except Exception as e:
            self.show_error_message(f"Error occurred: {e}")

            def apply_color_to_column(self, column_index, color):
                """Apply a color to all cells in a specific column."""
                try:
                    for row in range(self.table_view.model().rowCount()):
                        index = self.table_view.model().index(row, column_index)
                        self.table_view.model().setData(index, QBrush(color), role=Qt.BackgroundRole)
                except Exception as e:
                    self.show_error_message(f"Error occurred: {e}")

            def header_clicked(self, logicalIndex):
                try:
                    # Highlight the entire column
                    self.selected_column = logicalIndex
                    self.apply_color_to_column(self.selected_column, QColor('lightgreen'))

                    # Refresh the view to apply changes
                    self.table_view.viewport().update()

                except Exception as e:
                    self.show_error_message(f"Error occurred: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = DatabaseApp()
        window.show()
        try:
            app.exec_()
        except Exception as e:
            print(f"Application Error: {e}")
    except Exception as e:
        print(f"Initialization Error: {e}")

