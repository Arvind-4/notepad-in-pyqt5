import os
import sys

from PyQt5.QtCore import QMimeData, QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QImage, QKeySequence, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QComboBox,
    QFileDialog,
    QFontComboBox,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.config import ICON_DIR, MIN_HEIGHT, MIN_WIDTH, htmlExtensions, imageExtensions
from app.utils import fontList, hexuuid, splitText


class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source: QMimeData) -> bool:
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source: QMimeData) -> None:
        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():
            for u in source.urls():
                fileExt = splitText(str(u.toLocalFile()))
                if u.isLocalFile() and fileExt in imageExtensions:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())
                else:
                    break

            else:
                return

        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.editor = TextEdit()
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)

        font = QFont("Times", 14)
        self.editor.setFont(font)

        self.editor.setFontPointSize(14)

        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        fileToolbar = QToolBar("File")
        fileToolbar.setIconSize(QSize(30, 30))
        self.addToolBar(fileToolbar)
        fileMenu = self.menuBar().addMenu("File")

        openFileAction = QAction(
            QIcon(str(ICON_DIR / "Open.png")), "Open File...", self
        )
        openFileAction.setStatusTip("Open File")
        openFileAction.setShortcut(QKeySequence.Open)
        openFileAction.triggered.connect(self.file_open)
        fileMenu.addAction(openFileAction)
        fileToolbar.addAction(openFileAction)

        saveFileAction = QAction(QIcon(str(ICON_DIR / "Save.png")), "Save...", self)
        saveFileAction.setStatusTip("Save")
        saveFileAction.setShortcut(QKeySequence.Save)
        saveFileAction.triggered.connect(self.file_save)
        fileMenu.addAction(saveFileAction)
        fileToolbar.addAction(saveFileAction)

        saveAsFileAction = QAction(
            QIcon(str(ICON_DIR / "SaveAs.png")), "Save As...", self
        )
        saveAsFileAction.setStatusTip("Save As")
        saveAsFileAction.setShortcut("ctrl+shift+S")
        saveAsFileAction.triggered.connect(self.file_save_as)
        fileMenu.addAction(saveAsFileAction)
        fileToolbar.addAction(saveAsFileAction)

        printFileAction = QAction(QIcon(str(ICON_DIR / "Print.png")), "Print...", self)
        printFileAction.setStatusTip("Print")
        printFileAction.setShortcut(QKeySequence.Print)
        printFileAction.triggered.connect(self.file_print)
        fileMenu.addAction(printFileAction)
        fileToolbar.addAction(printFileAction)

        exitFileAction = QAction(QIcon(str(ICON_DIR / "Close.png")), "Close...", self)
        exitFileAction.setStatusTip("Close")
        exitFileAction.setShortcut(QKeySequence.Close)
        exitFileAction.triggered.connect(lambda: exit(0))
        fileMenu.addAction(exitFileAction)
        fileToolbar.addAction(exitFileAction)

        editToolBar = QToolBar("Edit")
        editToolBar.setIconSize(QSize(30, 30))
        self.addToolBar(editToolBar)
        editMenu = self.menuBar().addMenu("Edit")

        undoEditAction = QAction(QIcon(str(ICON_DIR / "Undo.png")), "Undo...", self)
        undoEditAction.setStatusTip("Undo")
        undoEditAction.setShortcut(QKeySequence.Undo)
        undoEditAction.triggered.connect(self.editor.undo)
        editMenu.addAction(undoEditAction)
        editToolBar.addAction(undoEditAction)

        redoEditAction = QAction(QIcon(str(ICON_DIR / "Redo.png")), "Redo...", self)
        redoEditAction.setStatusTip("Redo")
        redoEditAction.setShortcut(QKeySequence.Redo)
        redoEditAction.triggered.connect(self.editor.redo)
        editMenu.addAction(redoEditAction)
        editToolBar.addAction(redoEditAction)

        editMenu.addSeparator()

        cutEditAction = QAction(QIcon(str(ICON_DIR / "Cut.png")), "Cut...", self)
        cutEditAction.setStatusTip("Cut")
        cutEditAction.setShortcut(QKeySequence.Cut)
        cutEditAction.triggered.connect(self.editor.cut)
        editMenu.addAction(cutEditAction)
        editToolBar.addAction(cutEditAction)

        copyEditAction = QAction(QIcon(str(ICON_DIR / "Copy.png")), "Copy...", self)
        copyEditAction.setStatusTip("Copy")
        copyEditAction.setShortcut(QKeySequence.Copy)
        copyEditAction.triggered.connect(self.editor.copy)
        editMenu.addAction(copyEditAction)
        editToolBar.addAction(copyEditAction)

        pasteEditAction = QAction(QIcon(str(ICON_DIR / "Paste.png")), "Paste...", self)
        pasteEditAction.setStatusTip("Paste")
        pasteEditAction.setShortcut(QKeySequence.Paste)
        pasteEditAction.triggered.connect(self.editor.paste)
        editMenu.addAction(pasteEditAction)
        editToolBar.addAction(pasteEditAction)

        selectAllEditAction = QAction(
            QIcon(str(ICON_DIR / "SelectAll.png")), "Select All...", self
        )
        selectAllEditAction.setStatusTip("Select All")
        selectAllEditAction.setShortcut(QKeySequence.SelectAll)
        selectAllEditAction.triggered.connect(self.editor.selectAll)
        editMenu.addAction(selectAllEditAction)
        editToolBar.addAction(selectAllEditAction)

        cleartAllEditAction = QAction(
            QIcon(str(ICON_DIR / "Clear.png")), "Clear All...", self
        )
        cleartAllEditAction.setStatusTip("Clear All")
        cleartAllEditAction.setShortcut("ctrl+i")
        cleartAllEditAction.triggered.connect(lambda: self.editor.setText(""))
        editMenu.addAction(cleartAllEditAction)
        editToolBar.addAction(cleartAllEditAction)

        editMenu.addSeparator()

        wrapEditAction = QAction(
            QIcon(str(ICON_DIR / "WrapText.png")), "Wrap Text...", self
        )
        wrapEditAction.setStatusTip("Wrap Text")
        wrapEditAction.setCheckable(True)
        wrapEditAction.setChecked(True)
        wrapEditAction.triggered.connect(self.toggle_wrap)
        editMenu.addAction(wrapEditAction)
        editToolBar.addAction(wrapEditAction)

        formatToolBar = QToolBar("Format")
        formatToolBar.setIconSize(QSize(30, 30))
        self.addToolBar(formatToolBar)
        formatMenu = self.menuBar().addMenu("Format")

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        formatToolBar.addWidget(self.fonts)

        self.fontSize = QComboBox()
        self.fontSize.addItems(fontList())

        self.fontSize.currentIndexChanged[str].connect(
            lambda s: self.editor.setFontPointSize(float(s))
        )
        self.fontSize.setStyleSheet("QComboBox { combobox-popup: 0; }")
        formatToolBar.addWidget(self.fontSize)

        self.boldAction = QAction(QIcon(str(ICON_DIR / "Bold.png")), "Bold", self)
        self.boldAction.setStatusTip("Bold")
        self.boldAction.setShortcut(QKeySequence.Bold)
        self.boldAction.setCheckable(True)
        self.boldAction.toggled.connect(
            lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal)
        )
        formatToolBar.addAction(self.boldAction)
        formatMenu.addAction(self.boldAction)

        self.italicAction = QAction(QIcon(str(ICON_DIR / "Italic.png")), "Italic", self)
        self.italicAction.setStatusTip("Italic")
        self.italicAction.setShortcut(QKeySequence.Italic)
        self.italicAction.setCheckable(True)
        self.italicAction.toggled.connect(self.editor.setFontItalic)
        formatToolBar.addAction(self.italicAction)
        formatMenu.addAction(self.italicAction)

        self.underLineAction = QAction(
            QIcon(str(ICON_DIR / "Underline.png")), "Underline", self
        )
        self.underLineAction.setStatusTip("Underline")
        self.underLineAction.setShortcut(QKeySequence.Underline)
        self.underLineAction.setCheckable(True)
        self.underLineAction.toggled.connect(self.editor.setFontUnderline)
        formatToolBar.addAction(self.underLineAction)
        formatMenu.addAction(self.underLineAction)

        formatMenu.addSeparator()

        self.alignLeftAction = QAction(
            QIcon(str(ICON_DIR / "AlignLeft.png")), "Align Left", self
        )
        self.alignLeftAction.setStatusTip("Align Left")
        self.alignLeftAction.setCheckable(True)
        self.alignLeftAction.toggled.connect(
            lambda: self.editor.setAlignment(Qt.AlignLeft)
        )
        formatToolBar.addAction(self.alignLeftAction)
        formatMenu.addAction(self.alignLeftAction)

        self.alignCenterAction = QAction(
            QIcon(str(ICON_DIR / "AlignCenter.png")), "Align Center", self
        )
        self.alignCenterAction.setStatusTip("Align Center")
        self.alignCenterAction.setCheckable(True)
        self.alignCenterAction.toggled.connect(
            lambda: self.editor.setAlignment(Qt.AlignCenter)
        )
        formatToolBar.addAction(self.alignCenterAction)
        formatMenu.addAction(self.alignCenterAction)

        self.alignRightAction = QAction(
            QIcon(str(ICON_DIR / "AlignRight.png")), "Align Right", self
        )
        self.alignRightAction.setStatusTip("Align Right")
        self.alignRightAction.setCheckable(True)
        self.alignRightAction.toggled.connect(
            lambda: self.editor.setAlignment(Qt.AlignRight)
        )
        formatToolBar.addAction(self.alignRightAction)
        formatMenu.addAction(self.alignRightAction)

        self.alignJustifyAction = QAction(
            QIcon(str(ICON_DIR / "AlignJustify.png")), "Align Justify", self
        )
        self.alignJustifyAction.setStatusTip("Align Justify")
        self.alignJustifyAction.setCheckable(True)
        self.alignJustifyAction.toggled.connect(
            lambda: self.editor.setAlignment(Qt.AlignJustify)
        )
        formatToolBar.addAction(self.alignJustifyAction)
        formatMenu.addAction(self.alignJustifyAction)

        formatGroup = QActionGroup(self)
        formatGroup.setExclusive(True)
        formatGroup.addAction(self.alignLeftAction)
        formatGroup.addAction(self.alignCenterAction)
        formatGroup.addAction(self.alignRightAction)
        formatGroup.addAction(self.alignJustifyAction)

        formatMenu.addSeparator()

        self._formatAction = [
            self.fonts,
            self.fontSize,
            self.boldAction,
            self.italicAction,
            self.underLineAction,
        ]

        self.update_format()
        self.update_title()

    def block_signal(self, objects: list, b: bool) -> None:
        for o in objects:
            o.blockSignals(b)

    def update_format(self) -> None:
        self.block_signal(self._formatAction, True)
        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontSize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italicAction.setChecked(self.editor.fontItalic())
        self.underLineAction.setChecked(self.editor.fontUnderline())
        self.boldAction.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignLeftAction.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignCenterAction.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignRightAction.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignJustifyAction.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signal(self._formatAction, False)

    def dialog_critical(self, s: str) -> None:
        dialog = QMessageBox()
        dialog.setText(s)
        dialog.setIcon(QMessageBox.Critical)
        dialog.show()

    def file_open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Documents (*.txt)"
        )

        try:
            with open(path, "rU") as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.editor.setText(text)
            self.update_title()

    def file_save(self) -> None:
        if self.path is None:
            return self.file_save_as()

        text = (
            self.editor.toHtml()
            if splitText(self.path) in htmlExtensions
            else self.editor.toPlainText()
        )
        try:
            with open(self.path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_save_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text documents (*.txt)"
        )
        if not path:
            return
        text = (
            self.editor.toHtml()
            if splitText(path) in htmlExtensions
            else self.editor.toPlainText()
        )
        try:
            with open(path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self) -> None:
        dialog = QPrintDialog()
        if dialog.exec():
            self.editor.print_(dialog.printer())

    def update_title(self) -> None:
        path = self.path
        self.setWindowTitle(
            "%s -Notepad by Arvind" % (os.path.basename(path) if path else "*Untitled")
        )

    def toggle_wrap(self) -> None:
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.resize(MIN_WIDTH, MIN_HEIGHT)
    window.setWindowIcon(QIcon(str(ICON_DIR / "Logo.png")))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
