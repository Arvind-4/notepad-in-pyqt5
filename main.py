from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import uuid

l = []
for i in range(1, 289):
    l.append(i)
fontSizeList = l
imageExtensions = ['.jpg', '.png', '.bmp']
htmlExtensions = ['.htm', '.html']


def hexuuid():
    return uuid.uuid4().hex


def splitText(p):
    return os.path.splitext(p)[1].lower()


class TextEdit(QTextEdit):
    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

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
        self.editor.selectionChanged.connect(self.updateFormat)

        font = QFont('Times', 14)
        self.editor.setFont(font)

        self.editor.setFontPointSize(14)

        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        fileToolbar = QToolBar('File')
        fileToolbar.setIconSize(QSize(30, 30))
        self.addToolBar(fileToolbar)
        fileMenu = self.menuBar().addMenu('File')

        openFileAction = QAction(QIcon('Images/Open.png'), 'Open File...', self)
        openFileAction.setStatusTip('Open File')
        openFileAction.setShortcut(QKeySequence.Open)
        openFileAction.triggered.connect(self.fileOpen)
        fileMenu.addAction(openFileAction)
        fileToolbar.addAction(openFileAction)

        saveFileAction = QAction(QIcon('Images/Save.png'), 'Save...', self)
        saveFileAction.setStatusTip('Save')
        saveFileAction.setShortcut(QKeySequence.Save)
        saveFileAction.triggered.connect(self.fileSave)
        fileMenu.addAction(saveFileAction)
        fileToolbar.addAction(saveFileAction)

        saveAsFileAction = QAction(QIcon('Images/SaveAs.png'), 'Save As...', self)
        saveAsFileAction.setStatusTip('Save As')
        saveAsFileAction.setShortcut('ctrl+shift+S')
        saveAsFileAction.triggered.connect(self.fileSaveAs)
        fileMenu.addAction(saveAsFileAction)
        fileToolbar.addAction(saveAsFileAction)

        printFileAction = QAction(QIcon('Images/Print.png'), 'Print...', self)
        printFileAction.setStatusTip('Print')
        printFileAction.setShortcut(QKeySequence.Print)
        printFileAction.triggered.connect(self.filePrint)
        fileMenu.addAction(printFileAction)
        fileToolbar.addAction(printFileAction)

        exitFileAction = QAction(QIcon('Images/Close.png'), 'Close...', self)
        exitFileAction.setStatusTip('Close')
        exitFileAction.setShortcut(QKeySequence.Close)
        exitFileAction.triggered.connect(lambda: exit(0))
        fileMenu.addAction(exitFileAction)
        fileToolbar.addAction(exitFileAction)

        editToolBar = QToolBar('Edit')
        editToolBar.setIconSize(QSize(30, 30))
        self.addToolBar(editToolBar)
        editMenu = self.menuBar().addMenu('Edit')

        undoEditAction = QAction(QIcon('Images/Undo.png'), 'Undo...', self)
        undoEditAction.setStatusTip('Undo')
        undoEditAction.setShortcut(QKeySequence.Undo)
        undoEditAction.triggered.connect(self.editor.undo)
        editMenu.addAction(undoEditAction)
        editToolBar.addAction(undoEditAction)

        redoEditAction = QAction(QIcon('Images/Redo.png'), 'Redo...', self)
        redoEditAction.setStatusTip('Redo')
        redoEditAction.setShortcut(QKeySequence.Redo)
        redoEditAction.triggered.connect(self.editor.redo)
        editMenu.addAction(redoEditAction)
        editToolBar.addAction(redoEditAction)

        editMenu.addSeparator()

        cutEditAction = QAction(QIcon('Images/Cut.png'), 'Cut...', self)
        cutEditAction.setStatusTip('Cut')
        cutEditAction.setShortcut(QKeySequence.Cut)
        cutEditAction.triggered.connect(self.editor.cut)
        editMenu.addAction(cutEditAction)
        editToolBar.addAction(cutEditAction)

        copyEditAction = QAction(QIcon('Images/Copy.png'), 'Copy...', self)
        copyEditAction.setStatusTip('Copy')
        copyEditAction.setShortcut(QKeySequence.Copy)
        copyEditAction.triggered.connect(self.editor.copy)
        editMenu.addAction(copyEditAction)
        editToolBar.addAction(copyEditAction)

        pasteEditAction = QAction(QIcon('Images/Paste.png'), 'Paste...', self)
        pasteEditAction.setStatusTip('Paste')
        pasteEditAction.setShortcut(QKeySequence.Paste)
        pasteEditAction.triggered.connect(self.editor.paste)
        editMenu.addAction(pasteEditAction)
        editToolBar.addAction(pasteEditAction)

        selectAllEditAction = QAction(QIcon('Images/SelectAll.png'), 'Select All...', self)
        selectAllEditAction.setStatusTip('Select All')
        selectAllEditAction.setShortcut(QKeySequence.SelectAll)
        selectAllEditAction.triggered.connect(self.editor.selectAll)
        editMenu.addAction(selectAllEditAction)
        editToolBar.addAction(selectAllEditAction)

        cleartAllEditAction = QAction(QIcon('Images/Clear.png'), 'Clear All...', self)
        cleartAllEditAction.setStatusTip('Clear All')
        cleartAllEditAction.setShortcut('ctrl+i')
        cleartAllEditAction.triggered.connect(lambda: self.editor.setText(''))
        editMenu.addAction(cleartAllEditAction)
        editToolBar.addAction(cleartAllEditAction)

        editMenu.addSeparator()

        wrapEditAction = QAction(QIcon('Images/WrapText.png'), 'Wrap Text...', self)
        wrapEditAction.setStatusTip('Wrap Text')
        wrapEditAction.setCheckable(True)
        wrapEditAction.setChecked(True)
        wrapEditAction.triggered.connect(self.toggleWrap)
        editMenu.addAction(wrapEditAction)
        editToolBar.addAction(wrapEditAction)

        formatToolBar = QToolBar('Format')
        formatToolBar.setIconSize(QSize(30, 30))
        self.addToolBar(formatToolBar)
        formatMenu = self.menuBar().addMenu('Format')

        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        formatToolBar.addWidget(self.fonts)

        self.fontSize = QComboBox()
        self.fontSize.addItems([str(s) for s in fontSizeList])
        self.fontSize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)))
        formatToolBar.addWidget(self.fontSize)

        self.boldAction = QAction(QIcon('Images/Bold.png'), 'Bold', self)
        self.boldAction.setStatusTip('Bold')
        self.boldAction.setShortcut(QKeySequence.Bold)
        self.boldAction.setCheckable(True)
        self.boldAction.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        formatToolBar.addAction(self.boldAction)
        formatMenu.addAction(self.boldAction)

        self.italicAction = QAction(QIcon('Images/Italic.png'), 'Italic', self)
        self.italicAction.setStatusTip('Italic')
        self.italicAction.setShortcut(QKeySequence.Italic)
        self.italicAction.setCheckable(True)
        self.italicAction.toggled.connect(self.editor.setFontItalic)
        formatToolBar.addAction(self.italicAction)
        formatMenu.addAction(self.italicAction)

        self.underLineAction = QAction(QIcon('Images/Underline.png'), 'Underline', self)
        self.underLineAction.setStatusTip('Underline')
        self.underLineAction.setShortcut(QKeySequence.Underline)
        self.underLineAction.setCheckable(True)
        self.underLineAction.toggled.connect(self.editor.setFontUnderline)
        formatToolBar.addAction(self.underLineAction)
        formatMenu.addAction(self.underLineAction)

        formatMenu.addSeparator()

        self.alignLeftAction = QAction(QIcon('Images/AlignLeft.png'), 'Align Left', self)
        self.alignLeftAction.setStatusTip('Align Left')
        self.alignLeftAction.setCheckable(True)
        self.alignLeftAction.toggled.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        formatToolBar.addAction(self.alignLeftAction)
        formatMenu.addAction(self.alignLeftAction)

        self.alignCenterAction = QAction(QIcon('Images/AlignCenter.png'), 'Align Center', self)
        self.alignCenterAction.setStatusTip('Align Center')
        self.alignCenterAction.setCheckable(True)
        self.alignCenterAction.toggled.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        formatToolBar.addAction(self.alignCenterAction)
        formatMenu.addAction(self.alignCenterAction)

        self.alignRightAction = QAction(QIcon('Images/AlignRight.png'), 'Align Right', self)
        self.alignRightAction.setStatusTip('Align Right')
        self.alignRightAction.setCheckable(True)
        self.alignRightAction.toggled.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        formatToolBar.addAction(self.alignRightAction)
        formatMenu.addAction(self.alignRightAction)

        self.alignJustifyAction = QAction(QIcon('Images/AlignJustify.png'), 'Align Justify', self)
        self.alignJustifyAction.setStatusTip('Align Justify')
        self.alignJustifyAction.setCheckable(True)
        self.alignJustifyAction.toggled.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
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

        self.updateFormat()
        self.updateTitle()

    def blockSignals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def updateFormat(self):
        self.blockSignals(self._formatAction, True)
        self.fonts.setCurrentFont(self.editor.currentFont())
        self.fontSize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italicAction.setChecked(self.editor.fontItalic())
        self.underLineAction.setChecked(self.editor.fontUnderline())
        self.boldAction.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignLeftAction.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignCenterAction.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignRightAction.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignJustifyAction.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.blockSignals(self._formatAction, False)

    def dialogCritcal(self, s):
        dialog = QMessageBox()
        dialog.setText(s)
        dialog.setIcon(QMessageBox.Critical)
        dialog.show()

    def fileOpen(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', '',
                                              'Text Documents (*.txt)')

        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            self.dialogCritcal(str(e))

        else:
            self.path = path
            self.editor.setText(text)
            self.updateTitle()

    def fileSave(self):
        if self.path is None:
            return self.fileSaveAs()

        text = self.editor.toHtml() if splitText(self.path) in htmlExtensions else self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialogCritcal(str(e))

    def fileSaveAs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                              "Text documents (*.txt)")
        if not path:
            return
        text = self.editor.toHtml() if splitText(path) in htmlExtensions else self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialogCritcal(str(e))

        else:
            self.path = path
            self.updateTitle()

    def filePrint(self):
        dialog = QPrintDialog()
        if dialog.exec():
            self.editor.print_(dialog.printer())

    def updateTitle(self):
        path = self.path
        self.setWindowTitle('%s -Notepad by Arvind' % (os.path.basename(path) if path else '*Untitled'))

    def toggleWrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.resize(1100, 700)
    window.setWindowIcon(QIcon('Images/Logo.png'))
    window.show()
    app.exec()


if __name__ == '__main__':
    main()