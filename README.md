## 编译命令

### conan 准备
```bash
# 检查conan profile 是否存在
conan profile detect --exist-ok 

# 安装依赖
conan install .  -pr:h=default -pr:h=./conan_profiles/require_options --build=missing -s build_type=Release
# build_type 有：Debug Release RelWithDebInfo MinSizeRel 
```

### cmake 编译
```bash
cmake --preset release
cmake --build --preset release

# 跳过测试构建（BUILD_TESTING 默认 ON）
cmake --preset release -DBUILD_TESTING=OFF
```

### 运行测试
```bash
# 需先完成对应 build_type 的 conan install 和 cmake 编译
ctest --preset release

# 失败时显示详细输出
ctest --preset release --output-on-failure
```

