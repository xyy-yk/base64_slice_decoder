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
