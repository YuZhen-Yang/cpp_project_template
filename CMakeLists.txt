cmake_minimum_required(VERSION 3.29)
project(TODO_ProjectName VERSION 0.1.0 LANGUAGES CXX)

option(BUILD_TESTING "Build the testing tree." ON)

add_executable(HelloWorld src/main.cpp)

# --------------------------------------------------------------------------
# Google Test（依赖由 conanfile.py 的 test_requires 提供，
# 需先 conan install 生成 toolchain 后再 cmake configure）
# --------------------------------------------------------------------------
if(BUILD_TESTING)
    enable_testing()
    find_package(GTest REQUIRED)

    add_executable(HelloTest test/hello_test.cpp)

    # 链接GTest::Main 提供main函数 提供main函数,链接GTest::GTest
    target_link_libraries(HelloTest PRIVATE GTest::Main)  

    include(GoogleTest)
    gtest_discover_tests(HelloTest)
endif()

# --------------------------------------------------------------------------
# clangd: keep compile_commands.json at source root,服务于clangd 插件正确索引
# --------------------------------------------------------------------------
if(CMAKE_EXPORT_COMPILE_COMMANDS AND 
   CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR) # 根项目的时候才执行
    add_custom_target(copy_compile_commands ALL
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_BINARY_DIR}/compile_commands.json
            ${CMAKE_SOURCE_DIR}/compile_commands.json
        DEPENDS HelloWorld
        COMMENT "Copying compile_commands.json to source root"
        )
endif()


