"""
    Toolbar giving access to experimental MXS -> Python translation
"""
#pylint: disable= import-error, invalid-name, too-few-public-methods
from qtpy.QtWidgets import (QApplication, QWidget, QDockWidget,
        QVBoxLayout, QLabel, QTextEdit, QStyle, QToolBar, QCommonStyle)
from qtpy.QtGui import (QSyntaxHighlighter, QTextCharFormat,
        QFont, Qt, QBrush, QColor, QKeyEvent)
from qtpy import QtCore
from qtpy.QtCore import QMimeData, QEvent
from pygments.lexers.python import PythonLexer
from pygments.token import Token
from mxs2py import topy
from qtmax import GetQMaxMainWindow

def makeFormat(weight, color):
    """Create a format from a font weight and color"""
    f = QTextCharFormat()
    f.setFontWeight(weight)
    f.setForeground(color)
    return f

# Color scheme for the syntax highlighted QTextEdit

COMMENT_FORMAT=makeFormat(QFont.Normal, QBrush(QColor(0xd8, 0x98, 0x68)))
OPERATOR_FORMAT=makeFormat(QFont.Bold, QBrush(QColor(0x66, 0x87, 0x99)))
KEYWORD_FORMAT=makeFormat(QFont.Normal, QBrush(QColor(0x8b,0xe5,0x7a)))
LITERAL_FORMAT=makeFormat(QFont.Normal, QBrush(QColor(0xcf,0x6a,0xa0)))
IDENTIFIER_FORMAT=makeFormat(QFont.Normal, QBrush(QColor(220, 220, 220)))
BUILTIN_FORMAT=makeFormat(QFont.Normal, QBrush(QColor(200, 100, 150)))
DEFAULT_FORMAT = makeFormat(QFont.Normal, QBrush(QColor(220, 0, 0)))

COLOR_SCHEME = {
    Token.Text: IDENTIFIER_FORMAT,
    Token.Text.Whitespace: IDENTIFIER_FORMAT,
    Token.Error: IDENTIFIER_FORMAT,
    Token.Other: IDENTIFIER_FORMAT,
    Token.Keyword: KEYWORD_FORMAT,
    Token.Keyword.Namespace: KEYWORD_FORMAT,
    Token.Keyword.Constant: LITERAL_FORMAT,
    Token.Name: IDENTIFIER_FORMAT,
    Token.Name.Function: IDENTIFIER_FORMAT,
    Token.Name.Builtin: BUILTIN_FORMAT,
    Token.Name.Builtin.Pseudo: BUILTIN_FORMAT,
    Token.Name.Namespace: LITERAL_FORMAT,
    Token.Literal: LITERAL_FORMAT,
    Token.Literal.String: LITERAL_FORMAT,
    Token.Literal.String.Double: LITERAL_FORMAT,
    Token.Literal.String.Single: LITERAL_FORMAT,
    Token.Literal.Number: LITERAL_FORMAT,
    Token.Literal.Number.Integer: LITERAL_FORMAT,
    Token.Literal.Number.Float: LITERAL_FORMAT,
    Token.Operator: OPERATOR_FORMAT,
    Token.Operator.Word: OPERATOR_FORMAT,
    Token.Punctuation: OPERATOR_FORMAT,
    Token.Comment: COMMENT_FORMAT,
    Token.Comment.Single: COMMENT_FORMAT,
    Token.Generic: IDENTIFIER_FORMAT
}

class GenericHighlighter(QSyntaxHighlighter):
    """Initialize a syntax highlighter"""
    def highlightBlock(self, text):
        """higlight a block of text"""
        results = self.lexer.get_tokens_unprocessed(text)
        for index, tokentype,value in results:
            style = COLOR_SCHEME[tokentype] if tokentype in COLOR_SCHEME else DEFAULT_FORMAT
            if tokentype not in COLOR_SCHEME:
                print(tokentype)
            self.setFormat(index, len(value),style)

class PythonHighlighter(GenericHighlighter):
    """Intialize a python syntax highlighter"""
    lexer = PythonLexer()

class CustomEditor(QTextEdit):
    """Custom editor for showing python code and
    converting mxs code to python when dropped or pasted."""
    def insertFromMimeData(self, source):
        """Insert code from mime data"""
        if source.hasText():
            # get the text
            snippet = source.text()
            # try to convert it to python
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                (output, err) = topy(snippet)
                pysnippet = output + "\n"
                source = QMimeData()
                source.setText(pysnippet)
                if err:
                    print(err)
            except Exception as e: #pylint: disable=broad-exception-caught
                print(e)
            QApplication.restoreOverrideCursor()
        super().insertFromMimeData(source)

    def keyPressEvent (self, event):
        """Simulate a tab"""
        if event.key() == Qt.Key_Tab:
            event = QKeyEvent (QEvent.KeyPress, Qt.Key_Space,
                Qt.KeyboardModifiers(event.nativeModifiers()),
                "    ")
        super().keyPressEvent(event)

class ScriptEditor(QWidget):
    """
    Custom dialog attached to the 3ds Max main window
    Message label and action push button to create a cylinder in the 3ds Max scene graph
    """
    def __init__(self, parent=None):
        """Initialize the script editor"""
        super().__init__(parent)
        self.init_ui()
    def init_ui(self):
        """ Prepare Qt UI layout for custom dialog """
        main_layout = QVBoxLayout()
        # Add some explanation of what to do
        main_layout.addWidget(QLabel("Drop or Paste MXS Snippets to get them translated to Python"))
        # Add a toolbar
        toolbar = QToolBar()

        def clear_it():
            """Clear editor contents"""
            self.pyEdit.clear()
        def run_it():
            """Run editor contents"""
            exec(self.pyEdit.toPlainText()) #pylint: disable=exec-used
        main_layout.addWidget(toolbar)
        self.common_style=QCommonStyle()
        print(self.common_style)
        self.runAction = toolbar.addAction(
                self.common_style.standardIcon(QStyle.SP_ArrowRight), "Run Snippet", run_it)
        self.clearAction = toolbar.addAction(
                self.common_style.standardIcon(QStyle.SP_DialogCancelButton), "Clear", clear_it)

        self.pyEdit=CustomEditor()
        self.pyEdit.setStyleSheet("background-color: #333333;")
        def enable_text_actions():
            empty = self.pyEdit.document().isEmpty()
            self.runAction.setEnabled(not empty)
            self.clearAction.setEnabled(not empty)
        self.pyEdit.textChanged.connect(enable_text_actions)

        main_layout.addWidget(self.pyEdit)
        self.setLayout(main_layout)
        # syntax highlighting
        self.pyHighlighter = PythonHighlighter(self.pyEdit.document())
        enable_text_actions()

def new_editor(tabto=None, floating=False, dockingarea=QtCore.Qt.RightDockWidgetArea):
    """Create an editor dock widget."""
    main_window = GetQMaxMainWindow()
    # create and setup a console
    recorder = ScriptEditor()
    dock_widget = QDockWidget(main_window)
    dock_widget.setWidget(recorder)
    dock_widget.setObjectName("py_editor")
    dock_widget.setWindowTitle("Experimental MXS -> Python Translator")
    main_window.addDockWidget(dockingarea, dock_widget)
    if not tabto is None:
        tabw = main_window.findChild(QWidget, tabto)
        main_window.tabifyDockWidget(tabw, dock_widget)
    dock_widget.setFloating(floating)
    dock_widget.show()
    return recorder

if __name__ == "__main__":
    theEditor = new_editor()
