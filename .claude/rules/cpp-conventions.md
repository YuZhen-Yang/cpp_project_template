---
paths:
  - "**/*.cpp"
  - "**/*.h"
  - "**/*.hpp"
  - "**/*.cc"
  - "**/*.cxx"
---

# C++ 编码规范

> 以项目根目录 `.clang-tidy` 为最终权威，本规范从中提炼关键要求。遇到规范不明确时，以 `.clang-tidy` 的 `CheckOptions` 为准。

---

## 1. 命名规范

基于 `readability-identifier-naming` 配置：

| 类型 | 规则 | 示例 |
|------|------|------|
| 类 / 结构体 | PascalCase | `AudioBuffer`, `DataProcessor` |
| 私有 / 保护成员变量 | `m` 前缀 + CamelCase | `mSampleRate`, `mIsConnected` |
| 公有成员变量 | snake_case | `sample_rate`, `frame_count` |
| 函数 / 方法 | camelBack | `startAcquisition()`, `sendFrame()` |
| 局部变量 / 参数 | snake_case | `buffer_size`, `input_data` |
| 常量 / 枚举值 | `k` 前缀 + CamelCase | `kMaxRetry`, `kDefaultTimeout` |
| 命名空间 | snake_case | `audio_engine`, `net_utils` |
| 类型别名（using / typedef） | PascalCase | `SampleBuffer`, `CallbackFn` |

---

## 2. 现代 C++ 要求

基于 `modernize-*` checks：

- 使用 `nullptr`，禁止 `NULL` 或 `0` 表示空指针（`modernize-use-nullptr`）
- 虚函数重写必须加 `override`，禁止省略（`modernize-use-override`）
- 成员变量在声明处就地初始化，而非在构造函数体内赋值（`modernize-use-default-member-init`）
- 使用 `using` 定义类型别名，禁止 `typedef`（`modernize-use-using`）

```cpp
// 正确
class Processor {
public:
    void process() override;
private:
    int mCount{0};          // 就地初始化
    std::string* mPtr{nullptr};  // nullptr
};

using DataCallback = std::function<void(int)>;  // using 而非 typedef
```

---

## 3. 控制语句必须加 `{}`

基于 `readability-braces-around-statements`：

- `if`、`else`、`for`、`while`、`do while` 的语句体**必须**使用 `{}` 包裹，即使只有单行。

```cpp
// 正确
if (ready) {
    process();
}

for (auto const& item : items) {
    sum += item.value;
}

// 错误：缺少 {}
if (ready)
    process();

for (auto const& item : items)
    sum += item.value;
```

---

## 4. 禁止事项

基于 `google-*` 和 `bugprone-*` checks：

- 禁止使用 `NULL`（用 `nullptr`）
- 禁止隐式类型转换构造函数（单参数构造函数须加 `explicit`）
- 禁止在头文件中使用 `using namespace`
- 禁止对 `std::endl` 的滥用（用 `'\n'` 替代，避免不必要的 flush）
- 避免易混淆的相邻同类型参数（`bugprone-easily-swappable-parameters` 已豁免，但仍需注意可读性）

---

## 5. 性能要求

基于 `performance-*` checks：

- 按值传入后仅用于初始化时，优先使用移动语义
- 避免不必要的拷贝，优先使用 `const` 引用传参
- 容器遍历优先使用范围 for 而非下标

---

## 6. `const` 位置风格

优先使用 **east const**（`const` 放类型右侧），配合 `auto` 时写作 `auto const&`：

```cpp
// 正确：east const 风格
auto const& name = getName();
auto const  value = compute();
int  const  kMaxSize = 256;

// 范围 for 优先写法
for (auto const& item : items) { ... }

// 错误：west const（禁止）
const auto& name = getName();
const int   kMaxSize = 256;
```

- 规则统一：`const` 始终位于它所修饰类型的**右侧**。
- 指针场景同理：`int* const p`（指针本身不可变）、`int const* p`（指向内容不可变）。

---

## 7. 兜底声明

本规范从 `.clang-tidy` 提炼，若遇到未覆盖的情况，**直接读取项目根目录的 `.clang-tidy` 文件**，以其 `Checks` 和 `CheckOptions` 字段为最终判断依据。