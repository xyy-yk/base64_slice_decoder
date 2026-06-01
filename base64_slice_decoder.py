#!/usr/bin/env python3
"""
Base64 Slice Decoder - 通用 Base64 截断还原工具
适用于 CTF 中 Base64 多层编码 + 固定盐 + slice/substr 截断场景

依赖：Python 3.7+
"""

import base64
import itertools

# ==================== 配置区 ====================
# 残缺的 Base64 字符串（slice / substr 之后拿到的结果）
CHOPPED = "FM016RTJ4SDdqSw=="

# 固定前缀（正向拼接时加在待编码字符串前面的固定字符串）
# 如果没有固定前缀，请设置为 b""
PREFIX_SIGNATURE = b""

# 固定后缀（正向拼接时加在待编码字符串后面的固定字符串）
# 如果没有固定后缀，请设置为 b""
SUFFIX_SIGNATURE = b"xH7jK"

# 被截断的前缀字符个数（例如 slice(3) 就是 3，substr(2) 就是 2）
MISSING_LENGTH = 3

# Base64 字符集（标准 Base64，通常不需要改）
BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# 中间层 Base64 解码后，允许的字符集（默认字母数字，可根据题目调整）
# 例如：题目密码是 hex 就可以设为 '0123456789abcdefABCDEF'
# 如果不限制，请设为空字符串 ""
ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
# ==================== 配置区结束 ====================


def try_prefix(prefix_candidate: str):
    """尝试用候选前缀补全残缺串，并校验头尾固定字符串及中间层合法性"""
    full = prefix_candidate + CHOPPED
    missing_padding = (4 - len(full) % 4) % 4
    full += '=' * missing_padding

    try:
        decoded = base64.b64decode(full, validate=True)
    except Exception:
        return None

    # 检查固定前缀/后缀
    if PREFIX_SIGNATURE and not decoded.startswith(PREFIX_SIGNATURE):
        return None
    if SUFFIX_SIGNATURE and not decoded.endswith(SUFFIX_SIGNATURE):
        return None

    inner_bytes = decoded
    if PREFIX_SIGNATURE:
        inner_bytes = inner_bytes[len(PREFIX_SIGNATURE):]
    if SUFFIX_SIGNATURE:
        inner_bytes = inner_bytes[:-len(SUFFIX_SIGNATURE)]

    try:
        inner_b64 = inner_bytes.decode('ascii')
    except UnicodeDecodeError:
        return None

    # 第一关：中间层自身必须能 Base64 解码
    try:
        test_decode = base64.b64decode(inner_b64, validate=True)
    except Exception:
        return None

    # 第二关：解码结果必须全部为 ASCII 字符（严格模式，不允许忽略非 ASCII 字节）
    if not test_decode.isascii():
        return None

    # 第三关（可选）：解码后的 ASCII 字符串必须在白名单内
    if ALLOWED_CHARS:
        decoded_str = test_decode.decode('ascii')
        if not all(c in ALLOWED_CHARS for c in decoded_str):
            return None

    return inner_b64


def main():
    print("[*] 开始爆破缺失前缀...")
    for comb in itertools.product(BASE64_CHARS, repeat=MISSING_LENGTH):
        prefix = ''.join(comb)
        result = try_prefix(prefix)
        if result:
            print(f"[+] 缺失的前缀: {prefix}")
            print(f"[+] 完整 Base64: {prefix + CHOPPED}")
            print(f"[+] 剥离头尾后的中间层 Base64: {result}")

            # 尝试继续解码中间层（如果中间层本身也是 Base64）
            try:
                next_level = base64.b64decode(result).decode()
                print(f"[+] 中间层解码: {next_level}")
            except Exception:
                print("[!] 中间层解码失败，可能需要继续逆向（如反转、再次爆破等）")
            return

    print("[-] 未找到合法前缀，请检查：")
    print("    1. CHOPPED 字符串是否抄错（0/O、l/1 容易混淆）")
    print("    2. PREFIX / SUFFIX 的大小写是否正确")
    print("    3. MISSING_LENGTH 设置是否正确")


if __name__ == "__main__":
    main()
