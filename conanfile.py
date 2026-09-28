from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeConfigDeps, CMake, cmake_layout
from conan.tools.files import load
from conan.errors import ConanInvalidConfiguration
import os
import re


class TODOProjectNameConanFile(ConanFile):
    name = "todo_project_name"  # 需要小写
    description = "......"

    settings = "os", "compiler", "build_type", "arch"

    # options
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }

    # exports_sources = (
    #     "CMakeLists.txt",
    #     "cmake/*",
    #     "src/*",
    #     "include/*",
    #     "resource/*",
    # )

    def set_version(self):
        # 根据CMakeLists.txt 中 Project 的Version 来确定
        cmake_content = load(self, "CMakeLists.txt")
        match = re.search(r"project\([^)]*VERSION\s+([0-9.]+)", cmake_content)
        if not match:
            raise Exception("Failed to parse project version number from CMakeLists.txt")
        self.version = match.group(1)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    # def requirements(self):
    #     self.requires("qt/[~5.15]", transitive_headers=True)
    #     self.requires("boost/1.90.0", transitive_headers=True)

    def build_requirements(self):
        self.test_requires("gtest/1.18.0")


    # def package_id(self):
    #     self.info.requires["boost"].full_mode()

    # def validate(self):
    #     if not self.dependencies["qt"].options.shared:
    #         raise ConanInvalidConfiguration("todo_project_name requires qt:shared=True")
    #     if not self.dependencies["boost"].options.header_only:
    #         raise ConanInvalidConfiguration("todo_project_name requires boost:header_only=True")

    def layout(self):
        cmake_layout(self)
        # 根据build_type 类型 放置 build 和 generator  文件
        build_type = str(self.settings.build_type)
        self.folders.generators = os.path.join("build", build_type, "generator")
        self.folders.build = os.path.join("build", build_type)

    def generate(self):
        tc = CMakeToolchain(self, generator="Ninja")
        tc.user_presets_path = False  # 禁止生成 CMakeUserPresets.json
        tc.generate()
        deps = CMakeConfigDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # def package(self):
    #     cmake = CMake(self)
    #     cmake.install()

    # def package_info(self):
    #     self.cpp_info.builddirs = ["lib/cmake/XXX"]  # 安装目录下，XXXConfig.cmake 的路径
    #     self.cpp_info.set_property("cmake_find_mode", "none")
    #     self.cpp_info.set_property("cmake_file_name", "XXX")  # 该名称会影响find_package
    #     self.cpp_info.requires = [
    #         "qt::qtCore",
    #         "boost::headers",
    #     ]
