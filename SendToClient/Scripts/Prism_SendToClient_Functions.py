# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2021 Richard Frangenberg
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.
####################################################
# Plugin author: Elise Vidal
# Contact: evidal@artfx.fr
# Beta Testeur: Simon 'ca marche pas' Tarsiguel

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from dataclasses import dataclass
from PrismUtils.Decorators import err_catcher_plugin as err_catcher

import os
from distutils.dir_util import copy_tree
import shutil
import datetime
import re
from SetName import SetName
import subprocess


class Prism_SendToClient_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True

    def onProjectBrowserShow(self, *args):
        self.core.plugins.monkeyPatch(
            self.core.pb.mediaBrowser.rclList,
            self.rclList, self, force=True
            )

    def format_toClient_media_name(self, path):
        data = self.core.pb.mediaBrowser.getCurrentIdentifier()
        try:
            asset_name = data['asset_path']
        except:
            asset_name = data['shot']
        # asset_name = 'debug'
        task = data['displayName']
        task = task.split(' ')[0]
        version = self.core.pb.mediaBrowser.getCurrentVersion()['version']
        version = version.split(' ')[0]
        formatted_toClient_media_name = asset_name + '_' + task + '_' + version
        return formatted_toClient_media_name

    def open_explorer(self, path):
        path = path.replace('/', '\\')
        cmd = 'explorer ' + path
        subprocess.Popen(cmd)

    def get_toClient_folder(self):
        data = self.core.pb.mediaBrowser.getCurrentIdentifier()
        project_path = data['project_path']
        project_dirs = os.listdir(project_path)
        for dir in project_dirs:
            if 'toclient' in dir.lower():
                toClient_folder = os.path.join(project_path, dir)
        toClient_folder_full = toClient_folder + '\\'

        return toClient_folder_full

    def get_toClient_media_folder(self):
        date = datetime.datetime.now()
        date = date.strftime('%y%m%d')
        toClient_media_folder = date + '_'
        return toClient_media_folder

    def copy_files(self, src, dst):
        src = src.replace('/', '\\')
        dst = dst.replace('/', '\\')
        copy_tree(src, dst)

    def rename_files(self, src, name):
        for file in os.listdir(src):
            file_ext = file.split('.', 1)[1]
            new_media_name = name + '.' + file_ext
            new_path = os.path.join(src, new_media_name)
            old_path = os.path.join(src, file)
            os.replace(old_path, new_path)

    def get_existing_folders(self, search_dir):
        existing_folders = []
        for dir in os.listdir(search_dir):
            if os.path.isdir(os.path.join(search_dir, dir)):
                existing_folders.append(dir)
        return existing_folders

    def copyToClient(self, path):
        media_folder = path
        placeholder_media_name = self.format_toClient_media_name(path)

        toClient_folder = self.get_toClient_folder()

        # GET MEDIA NAME FROM USER INPUT
        dlg = SetName()
        dlg.e_mediaName.setText(placeholder_media_name)
        existing_folders = self.get_existing_folders(toClient_folder)
        placeholder_media_folder = self.get_toClient_media_folder()
        existing_folders.append(placeholder_media_folder)
        dlg.c_mediaFolders.addItems(existing_folders)
        dlg.b_explorer.clicked.connect(
            lambda: self.open_explorer(toClient_folder)
            )
        result = dlg.exec_()
        if result == 0:
            return

        # RETRIEVE AND FORMAT USER INPUT
        toClient_media_folder = dlg.c_mediaFolders.currentText()
        toClient_media_folder = re.sub(
            r"[^a-zA-Z0-9]", "_", toClient_media_folder
            )
        toClient_media_path = os.path.join(
            toClient_folder, toClient_media_folder
            )
        toClient_media_name = dlg.e_mediaName.text()
        toClient_media_name = re.sub(r"[^a-zA-Z0-9]", "_", toClient_media_name)

        self.copy_files(media_folder, toClient_media_path)
        self.rename_files(toClient_media_path, toClient_media_name)

    def rclList(self,  pos, lw, mediaPlayback=None):
        cpos = QCursor.pos()
        if mediaPlayback is None:
            mediaPlayback = self.core.pb.mediaBrowser.mediaPlaybacks["shots"]

        if lw == self.core.pb.mediaBrowser.cb_layer:

            item = None
            identifier = self.core.pb.mediaBrowser.getCurrentIdentifier()
            if identifier["mediaType"] != "3drenders":
                return

            data = self.core.pb.mediaBrowser.getCurrentAOV()
            if data:
                path = data["path"]
            else:
                version = self.core.pb.mediaBrowser.getCurrentVersion()
                if not version:
                    return

                path = self.core.mediaProducts.getAovPathFromVersion(version)

        else:
            item = lw.itemAt(pos)
            if item is not None:
                itemName = item.text()
            else:
                itemName = ""

            entity = self.core.pb.mediaBrowser.getCurrentEntity()
            if not entity:
                return False

            if lw == self.core.pb.mediaBrowser.lw_task:
                if itemName:
                    path = item.data(Qt.UserRole)["path"]
                else:
                    path = self.core.mediaProducts.getIdentifierPathFromEntity(
                        entity
                        )
            elif lw == self.core.pb.mediaBrowser.lw_version:
                if itemName:
                    data = item.data(Qt.UserRole)
                    path = data["path"]
                else:
                    identifier =\
                        self.core.pb.mediaBrowser.getCurrentIdentifier()
                    if not identifier:

                        return

                    path = self.core.mediaProducts.\
                        getVersionPathFromIdentifier(identifier)

        rcmenu = QMenu(self.core.pb.mediaBrowser)

        add = QAction("Add current to compare", self.core.pb.mediaBrowser)
        add.triggered.connect(self.core.pb.mediaBrowser.addCompare)
        version = self.core.pb.mediaBrowser.getCurrentVersion()
        if self.core.pb.mediaBrowser.rv and (
                (version and len(mediaPlayback["seq"]) > 0) or
                len(self.core.pb.mediaBrowser.lw_task.selectedItems()) > 1 or
                len(self.core.pb.mediaBrowser.lw_version.selectedItems()) > 1
        ):
            rcmenu.addAction(add)

        if lw == self.core.pb.mediaBrowser.lw_task:
            refresh = self.core.pb.mediaBrowser.updateTasks
            if entity.get("type") in ["asset", "shot"]:
                depAct = QAction(
                    "Create Identifier...",
                    self.core.pb.mediaBrowser
                    )
                depAct.triggered.connect(
                    self.core.pb.mediaBrowser.createIdentifierDlg
                    )
                rcmenu.addAction(depAct)

                exAct = QAction(
                    "Add external media",
                    self.core.pb.mediaBrowser
                    )
                exAct.triggered.connect(
                    self.core.pb.mediaBrowser.createExternalTask
                    )
                rcmenu.addAction(exAct)

        elif lw == self.core.pb.mediaBrowser.lw_version:

            refresh = self.core.pb.mediaBrowser.updateVersions
            identifier = self.core.pb.mediaBrowser.getCurrentIdentifier()
            if identifier:

                depAct = QAction(
                    "Create Version...",
                    self.core.pb.mediaBrowser
                    )
                depAct.triggered.connect(
                    self.core.pb.mediaBrowser.createVersionDlg
                    )
                rcmenu.addAction(depAct)

            if identifier["mediaType"] == "externalMedia":
                nvAct = QAction(
                    "Create new external version",
                    self.core.pb.mediaBrowser
                    )
                nvAct.triggered.connect(
                    self.core.pb.mediaBrowser.newExternalVersion
                    )
                rcmenu.addAction(nvAct)

            if item:
                infAct = QAction("Edit comment...", self.core.pb.mediaBrowser)
                infAct.triggered.connect(
                    lambda: self.core.pb.mediaBrowser.editComment(path)
                    )
                rcmenu.addAction(infAct)

                infAct = QAction(
                    "Show version info",
                    self.core.pb.mediaBrowser
                    )
                infAct.triggered.connect(
                    lambda: self.core.pb.mediaBrowser.showVersionInfoForItem(
                        item
                        )
                    )
                rcmenu.addAction(infAct)

                depAct = QAction(
                    "Show dependencies",
                    self.core.pb.mediaBrowser
                    )
                depAct.triggered.connect(
                    lambda: self.core.pb.mediaBrowser.showDependencies(data)
                    )
                rcmenu.addAction(depAct)

                useMaster = self.core.mediaProducts.getUseMaster()
                if useMaster:
                    if itemName.startswith("master"):
                        masterAct = QAction(
                            "Delete master", self.core.pb.mediaBrowser
                            )
                        masterAct.triggered.connect(
                            lambda: self.core.mediaProducts.
                            deleteMasterVersion(data["path"])
                        )
                        masterAct.triggered.connect(
                            self.core.pb.mediaBrowser.updateVersions
                            )
                        rcmenu.addAction(masterAct)
                    else:
                        masterAct = QAction(
                            "Set as master", self.core.pb.mediaBrowser
                            )
                        masterAct.triggered.connect(
                            lambda: self.core.pb.mediaBrowser.setMaster(data)
                            )
                        rcmenu.addAction(masterAct)

                        masterAct = QAction(
                            "Add to master", self.core.pb.mediaBrowser
                            )
                        masterAct.triggered.connect(
                            lambda: self.core.pb.mediaBrowser.addMaster(data)
                            )
                        rcmenu.addAction(masterAct)

                if os.path.exists(path):
                    # PLUGIN MONKEYPATCH
                    sendToAct = QAction(
                        "Copy to 'Send to Client'",
                        self.core.pb.mediaBrowser
                        )
                    sendToAct.triggered.connect(
                        lambda: self.copyToClient(path)
                        )
                    rcmenu.addAction(sendToAct)

        elif lw == self.core.pb.mediaBrowser.cb_layer:
            depAct = QAction("Create AOV...", self.core.pb.mediaBrowser)
            depAct.triggered.connect(self.core.pb.mediaBrowser.createAovDlg)
            rcmenu.addAction(depAct)
            refresh = self.core.pb.mediaBrowser.updateLayers

        act_refresh = QAction("Refresh", self.core.pb.mediaBrowser)
        act_refresh.triggered.connect(lambda: refresh(restoreSelection=True))
        rcmenu.addAction(act_refresh)

        if os.path.exists(path):
            opAct = QAction("Open in Explorer", self.core.pb.mediaBrowser)
            opAct.triggered.connect(lambda: self.core.openFolder(path))
            rcmenu.addAction(opAct)

            copAct = QAction("Copy", self.core.pb.mediaBrowser)
            copAct.triggered.connect(
                lambda: self.core.copyToClipboard(path, file=True)
                )
            rcmenu.addAction(copAct)

        if lw == self.core.pb.mediaBrowser.lw_version:
            copAct = QAction(
                "Copy path for next version",
                self.core.pb.mediaBrowser
                )
            copAct.triggered.connect(
                self.core.pb.mediaBrowser.prepareNewVersion
                )
            rcmenu.addAction(copAct)

        if lw == self.core.pb.mediaBrowser.lw_version and itemName.endswith(
            " (local)"
        ):
            glbAct = QAction("Move to global", self.core.pb.mediaBrowser)
            glbAct.triggered.connect(
                lambda: self.core.pb.mediaBrowser.copyToGlobal(path)
                )
            rcmenu.addAction(glbAct)

        if rcmenu.isEmpty():
            return False

        rcmenu.exec_(cpos)
