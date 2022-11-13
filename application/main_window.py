# -*- coding: utf-8 -*-
import os
from glob import glob
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel


# Form implementation generated from reading ui file 'Bulk Image Tagger qt5.ui'
#
# Created by: PyQt5 UI code generator 5.14.1

def get_folder(folder):
    glob_pattern = sorted(glob(os.path.join(folder, '*')), key=os.path.getctime)
    out = []
    for i in range(len(glob_pattern)):
        if os.path.splitext(os.path.basename(glob_pattern[i]))[-1] in ['.jpg', '.jpeg', '.png']:
            out.append(glob_pattern[i])
    return out


def resizeAndPad(img, size, padColor=0):
    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw:  # shrinking image
        interp = cv2.INTER_AREA
    else:  # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w / h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1:  # horizontal image
        new_w = sw
        new_h = np.round(new_w / aspect).astype(int)
        pad_vert = (sh - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1:  # vertical image
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = (sw - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else:  # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)):  # color image but only one color provided
        padColor = [padColor] * 3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.folder_contents = None
        self.folder_contents_i = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(632, 447)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(10, 11, 611, 311))
        # self.graphicsView.setObjectName("graphicsView")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 330, 611, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.write_txtbox)
        self.lineEdit.setEnabled(False)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 370, 181, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setEnabled(False)

        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(530, 370, 89, 25))
        self.save_button.setObjectName("save_button")
        self.save_button.clicked.connect(self.write_txtbox)
        self.save_button.setEnabled(False)

        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(400, 370, 31, 25))
        self.next_button.setObjectName("next_button")
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setEnabled(False)

        self.last_button = QtWidgets.QPushButton(self.centralwidget)
        self.last_button.setGeometry(QtCore.QRect(360, 370, 31, 25))
        self.last_button.setObjectName("last_button")
        self.last_button.clicked.connect(self.prev_image)
        self.last_button.setEnabled(False)

        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setGeometry(QtCore.QRect(440, 370, 89, 25))
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_image)
        self.delete_button.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.close)

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.write_txtbox)

        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionNext.triggered.connect(self.prev_image)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.folder_open)

        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.actionNext.triggered.connect(self.next_image)

        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionDelete.triggered.connect(self.delete_image)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNext)
        self.menuFile.addAction(self.actionNext)
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 30, 611, 311))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bulk Image Tagger"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter prompt here"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Premade Prompts"))
        self.comboBox.setItemText(1, _translate("MainWindow", "example1"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.next_button.setText(_translate("MainWindow", "→"))
        self.last_button.setText(_translate("MainWindow", "←"))
        self.delete_button.setText(_translate("MainWindow", "Delete"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionNext.setText(_translate("MainWindow", "Previous"))
        self.actionNext.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionOpen.setText(_translate("MainWindow", "Open Folder"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionNext.setText(_translate("MainWindow", "&Next"))
        self.actionNext.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionDelete.setText(_translate("MainWindow", "&Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Ctrl+D"))

    def folder_open(self):
        self.user_dir = QFileDialog.getExistingDirectory(
            self, "Open Directory",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        self.folder_contents = get_folder(self.user_dir)
        self.folder_contents_i = 0
        self.last_button.setEnabled(False)
        if len(self.folder_contents) > 0:
            self.load_image(self.folder_contents[self.folder_contents_i])
            self.enable(True)
        else:
            self.statusBar.showMessage('No images found!')

    def load_image(self, image_path):
        self.lineEdit.clear()
        if os.path.isfile(image_path):
            im = cv2.imread(image_path)  # square image
            im_resize = resizeAndPad(im, (311, 311), 311)
            is_success, im_buf_arr = cv2.imencode(".png", im_resize)
            im = Image.open(BytesIO(im_buf_arr.tobytes()))
            im.tobytes('raw', 'RGB')
            qim = ImageQt(im)
            pixmap = QPixmap.fromImage(qim)
            self.label.setPixmap(pixmap)
            self.label.show()
            self.statusBar.showMessage(os.path.split(self.folder_contents[self.folder_contents_i])[-1])

    def next_image(self):
        if self.folder_contents is not None:
            if self.folder_contents_i + 1 < len(self.folder_contents):
                self.folder_contents_i += 1
                self.load_image(self.folder_contents[self.folder_contents_i])
            else:
                self.next_button.setEnabled(False)
            if self.folder_contents_i - 1 < len(self.folder_contents):
                self.last_button.setEnabled(True)

    def prev_image(self):
        if self.folder_contents is not None:
            if self.folder_contents_i - 1 >= 0:
                self.folder_contents_i -= 1
                self.load_image(self.folder_contents[self.folder_contents_i])
            elif self.folder_contents_i - 1 < len(self.folder_contents):
                self.last_button.setEnabled(False)
            if self.folder_contents_i + 1 < len(self.folder_contents):
                self.next_button.setEnabled(True)

    def write_txtbox(self):
        if self.folder_contents is not None:
            textbox_content = self.lineEdit.text()
            if len(textbox_content) > 0:
                f = open(f'{self.folder_contents[self.folder_contents_i]}.txt', 'w')
                f.write(textbox_content)
                f.close()
                self.lineEdit.clear()
                self.next_image()

    def delete_image(self):
        if self.folder_contents is not None and len(self.folder_contents) > 0:
            self.label.hide()
            try:
                os.remove(self.folder_contents[self.folder_contents_i])
            except:
                print(self.folder_contents, self.folder_contents_i)
            if os.path.exists(f'{self.folder_contents[self.folder_contents_i]}.txt'):
                os.remove(f'{self.folder_contents[self.folder_contents_i]}.txt')
            self.statusBar.showMessage(f'Deleted {os.path.split(self.folder_contents[self.folder_contents_i])[-1]}')
            del self.folder_contents[self.folder_contents_i]
            self.folder_contents_i -= 1
            if len(self.folder_contents) > 0:
                self.next_image()
            else:
                self.enable(False)

    def enable(self, action):
        self.save_button.setEnabled(action)
        self.next_button.setEnabled(action)
        self.last_button.setEnabled(action)
        self.delete_button.setEnabled(action)
        self.lineEdit.setEnabled(action)
        self.comboBox.setEnabled(action)
