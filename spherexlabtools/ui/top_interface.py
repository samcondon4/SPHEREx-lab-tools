# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'top_interface.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SltTop(object):
    def setupUi(self, SltTop):
        SltTop.setObjectName("SltTop")
        SltTop.resize(1020, 645)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../SPIE2022/spherex-2020logo_color_nobackground.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SltTop.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SltTop)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(SltTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.log_tab = QtWidgets.QWidget()
        self.log_tab.setObjectName("log_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.log_tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.log_tab)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.log_tab, "")
        self.threads_tab = QtWidgets.QWidget()
        self.threads_tab.setObjectName("threads_tab")
        self.tabWidget.addTab(self.threads_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SltTop)

    def retranslateUi(self, SltTop):
        _translate = QtCore.QCoreApplication.translate
        SltTop.setWindowTitle(_translate("SltTop", "SPHERExLabTools"))
        self.textBrowser.setHtml(_translate("SltTop", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_tab), _translate("SltTop", "Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.threads_tab), _translate("SltTop", "Threads"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SltTop = QtWidgets.QWidget()
    ui = Ui_SltTop()
    ui.setupUi(SltTop)
    SltTop.show()
    sys.exit(app.exec_())
