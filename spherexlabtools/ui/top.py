""" This module provides the class SltTop, which provides the main SPHERExLabTools gui interface.
"""
from PyQt5 import QtCore, QtGui, QtWidgets


# - QtDesigner auto generated object - #
class TopQT(object):
    def setupUi(self, SltTop):
        SltTop.setObjectName("SltTop")
        SltTop.resize(1020, 645)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../SPIE2022/spherex-2020logo_color_nobackground.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SltTop.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SltTop)
        self.gridLayout.setObjectName("gridLayout")
        self.Tab_log_threads = QtWidgets.QTabWidget(SltTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tab_log_threads.sizePolicy().hasHeightForWidth())
        self.Tab_log_threads.setSizePolicy(sizePolicy)
        self.Tab_log_threads.setObjectName("Tab_log_threads")
        self.log_tab = QtWidgets.QWidget()
        self.log_tab.setObjectName("log_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.log_tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.logBrowser = QtWidgets.QTextBrowser(self.log_tab)
        self.logBrowser.setObjectName("logBrowser")
        self.gridLayout_3.addWidget(self.logBrowser, 0, 0, 1, 1)
        self.Tab_log_threads.addTab(self.log_tab, "")
        self.threads_tab = QtWidgets.QWidget()
        self.threads_tab.setObjectName("threads_tab")
        self.Tab_log_threads.addTab(self.threads_tab, "")
        self.gridLayout.addWidget(self.Tab_log_threads, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(SltTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.top_horizontal_layout = QtWidgets.QHBoxLayout()
        self.top_horizontal_layout.setObjectName("top_horizontal_layout")
        self.gridLayout_2.addLayout(self.top_horizontal_layout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(SltTop)
        self.Tab_log_threads.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SltTop)

    def retranslateUi(self, SltTop):
        _translate = QtCore.QCoreApplication.translate
        SltTop.setWindowTitle(_translate("SltTop", "SPHERExLabTools"))
        self.logBrowser.setHtml(_translate("SltTop", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                     "p, li { white-space: pre-wrap; }\n"
                                                     "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#00007f;\"># ---------------- SPHERExLabTools v1.0------------------- #</span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                                     .....                                     </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                                              ........                          </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                      /                              </span><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#ffff00;\">..</span><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                         </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                  /////                                       (                 </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">               ///                                               (              </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">            ///           #################                        ((           </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">          //            #### ############### ####                    ((         </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">         /             ###################### ### ###                 ((        </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">       /               ############################## ###              (((      </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">      /                 ### ### ##################### ## ##             (((     </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                         ###(##%&amp;######################*## ##,           (((    </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                         &amp;##&amp;&amp; #&amp;&amp;&amp;### //////##################           ((    </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">      #                  /&amp;&amp;(&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp; ////*############# ######                </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">   ###                  //%&amp;&amp;&amp;%&amp;&amp;&amp;&amp;&amp; &amp;&amp;&amp;&amp;&amp;&amp; ############ ########               </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">   ###                 ////&amp;&amp;&amp;&amp;&amp;&amp;&amp;/&amp;&amp;&amp;&amp;&amp;&amp;,&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;###### ####                </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">   ##                    .//&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp; &amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;   &amp;&amp;########              #  </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">   ##                       /&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;  &amp;&amp;&amp;########                   #  </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">   ##                       *&amp; &amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;                         #  </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">    #                     &amp;&amp;////&amp;&amp;%&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;&amp;//////                        #   </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">    ##                     &amp;///&amp;&amp;&amp;&amp;//&amp;&amp;&amp;&amp;&amp;////////////                     ##   </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">     #                    &amp;&amp;&amp;&amp;&amp;&amp;(&amp;////&amp;&amp;&amp;///////////////                  ##    </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">      #                     &amp;&amp;&amp;&amp;&amp; &amp;&amp;&amp;&amp;&amp;&amp; /////////////                  ###     </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">       #                         &amp;&amp;*        /////////                  ###      </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                                              //////                 ###        </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                                                 /                                      </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                           ##                                                   </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                            #######                  #                          </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,BitstreamVeraSansMono,CourierNew,Courier,monospace\'; font-size:6pt; color:#000000;\">                                      #####  </span></p>\n"
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#00007f;\"># -------------------------------------------------------------------- #</span></p></body></html>"))
        self.Tab_log_threads.setTabText(self.Tab_log_threads.indexOf(self.log_tab), _translate("SltTop", "Log"))
        self.Tab_log_threads.setTabText(self.Tab_log_threads.indexOf(self.threads_tab), _translate("SltTop", "Threads"))


# - top ui wrapper - #
class TopUI(TopQT, QtCore.QObject):

    ui_log_signal = QtCore.pyqtSignal(object, name="UI Log Signal")

    def __init__(self, top_widget):
        super().__init__()
        self.setupUi(top_widget)
        self.ver_scrollbar = self.logBrowser.verticalScrollBar()
        self.hor_scrollbar = self.logBrowser.horizontalScrollBar()
        self.ui_log_signal.connect(self.log)

    def log(self, msg):
        """ This method allows logging of formatted log messaged created by the logging package to the log
        interface.

        :param msg: String message to write to the log window.
        """
        self.logBrowser.append(msg)
        scroll = self.ver_scrollbar.maximum() - self.ver_scrollbar.value() <= 10
        if scroll:
            self.ver_scrollbar.setValue(self.ver_scrollbar.maximum())
            self.hor_scrollbar.setValue(0)

