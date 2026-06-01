# Base64 Slice Decoder

CTF 利器：一键还原被 `slice()` / `substr()` 截断的 Base64 加盐编码。

## 它能干什么？

当你遇到类似这样的 JavaScript 加密逻辑时：

```javascript
let encoded = btoa(input);
encoded = btoa(encoded + 'xH7jK').slice(3);
encoded = btoa(encoded.split('').reverse().join(''));
encoded = btoa('aB3' + encoded + 'qW9').substr(2);
if (btoa(encoded) === 'SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU=') { ... }
```
这个脚本可以逆向爆破出原始密码，一层层剥开洋葱皮。

快速开始
1.安装 Python 3.7 或更高版本。
2.克隆仓库：
  git clone https://github.com/你的用户名/Base64-Slice-Decoder.git
  cd Base64-Slice-Decoder
3.修改 base64_slice_decoder.py 顶部 配置区 的变量：
  CHOPPED：截断后拿到的残缺 Base64 字符串。
  PREFIX_SIGNATURE：正向拼接的固定前缀（没有就写 b""）。
  SUFFIX_SIGNATURE：正向拼接的固定后缀（没有就写 b""）。
  MISSING_LENGTH：被截掉的前缀字符数。
  ALLOWED_CHARS：（可选）中间层解码结果允许的字符集。
4.运行：
  python3 base64_slice_decoder.py
