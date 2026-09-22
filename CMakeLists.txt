cmake_minimum_required(VERSION 3.29)
project(TODO_ProjectName VERSION 0.1.0 LANGUAGES CXX)

add_executable(HelloWorld src/main.cpp)


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


