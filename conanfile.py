#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools

class SingleApplicationConan(ConanFile):
    name = "SingleApplication"
    version = "3.0.19"
    license = "The MIT License (MIT)"
    url = "https://github.com/itay-grudev/SingleApplication"
    description = "Replacement of QtSingleApplication for Qt5 with support for instance communication"
    settings = "os", "arch", "compiler", "build_type", "os_build", "arch_build"
    options = {"BaseClass": ["QCoreApplication", "QGuiApplication", "QApplication"]}
    default_options = "BaseClass=QCoreApplication", "Qt:openssl=True"
    requires = [("Qt/5.12.4@tereius/stable", "private")]
    generators = "cmake"

    def source(self):
        tools.download("https://github.com/itay-grudev/SingleApplication/archive/v%s.zip" % self.version, "single_app_src.zip")
        tools.unzip("single_app_src.zip")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["QAPPLICATION_CLASS"] = self.options.BaseClass
        cmake.configure(source_folder=("SingleApplication-%s" % self.version))
        cmake.build()
        
    def package(self):
        self.copy("*.h", src=os.path.join(self.source_folder, "SingleApplication-%s" % self.version), dst="include")
        self.copy("*.lib", src=self.build_folder, keep_path=False, dst="lib")
        self.copy("*.a", src=self.build_folder, keep_path=False, dst="lib")