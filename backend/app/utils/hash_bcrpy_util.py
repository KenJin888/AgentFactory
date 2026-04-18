import base64
import hashlib
import os
from typing import Any

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from itsdangerous import URLSafeSerializer
from passlib.context import CryptContext

from app.config.setting import settings
from app.core.logger import log

# 密码加密配置
PwdContext = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # 设置加密轮数,增加安全性
)


class PwdUtil:
    """
    密码工具类,提供密码加密和验证功能
    """

    @classmethod
    def verify_password(cls, plain_password: str, password_hash: str) -> bool:
        """
        校验密码是否匹配

        参数:
        - plain_password (str): 明文密码。
        - password_hash (str): 加密后的密码哈希值。

        返回:
        - bool: 密码是否匹配。
        """
        return PwdContext.verify(plain_password, password_hash)

    @classmethod
    def set_password_hash(cls, password: str) -> str:
        """
        对密码进行加密

        参数:
        - password (str): 明文密码。

        返回:
        - str: 加密后的密码哈希值。
        """
        return PwdContext.hash(password)

    @classmethod
    def check_password_strength(cls, password: str) -> str | None:
        """
        检查密码强度

        参数:
        - password (str): 明文密码。

        返回:
        - str | None: 如果密码强度不够返回提示信息,否则返回None。
        """
        if len(password) < 6:
            return "密码长度至少6位"
        if not any(c.isupper() for c in password):
            return "密码需要包含大写字母"
        if not any(c.islower() for c in password):
            return "密码需要包含小写字母"
        if not any(c.isdigit() for c in password):
            return "密码需要包含数字"
        return None


class AesEncryption:
    def __init__(self, key=None, mode: int = None, iv=None, block_size: int = 16):
        if not key:
            self.key = bytes(settings.SSO_KEY, encoding='utf-8')
        else:
            self.key = bytes(key, encoding='utf-8') if isinstance(key, str) else key
        self.mode = mode if mode is not None else AES.MODE_ECB
        self.aes = AES.new(self.key, self.mode, iv) if iv else AES.new(self.key, self.mode)
        self.block_size = block_size

    def encrypt(self, text: str or bytes):
        if isinstance(text, str):
            text = text.encode('utf-8')  # 明文必须编码成字节流数据，即数据类型为bytes
        text = self.aes.encrypt(pad(text, self.block_size, 'pkcs7'))  # 明文进行加密，返回加密后的字节流数据
        return str(base64.b64encode(base64.b64encode(text)), encoding='utf-8')  # 将加密后得到的字节流数据进行base64编码并再转换为unicode类型

    def decrypt(self, text: str or bytes):
        text = base64.b64decode(base64.b64decode(text))  # 对密文进行base64解码
        de_text = unpad(self.aes.decrypt(text), self.block_size, 'pkcs7')  # 密文进行解密，返回明文的bytes
        return str(de_text, encoding='utf-8')  # 将解密后得到的bytes型数据转换为str型，并去除末尾的填充


class AESCipher:
    """AES 加密器"""

    def __init__(self, key: bytes | str) -> None:
        """
        初始化 AES 加密器。

        参数:
        - key (bytes | str): 密钥，16/24/32 bytes 或 16 进制字符串。

        返回:
        - None
        """
        self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

    def encrypt(self, plaintext: bytes | str) -> bytes:
        """
        AES 加密。

        参数:
        - plaintext (bytes | str): 加密前的明文。

        返回:
        - bytes: 加密后的密文（前16字节为随机IV）。
        """
        if not isinstance(plaintext, bytes):
            plaintext = str(plaintext).encode("utf-8")
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(cipher.algorithm.block_size).padder()  # type: ignore
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes | str) -> str:
        """
        AES 解密。

        参数:
        - ciphertext (bytes | str): 解密前的密文，bytes 或 16 进制字符串。

        返回:
        - str: 解密后的明文。
        """
        ciphertext = ciphertext if isinstance(ciphertext, bytes) else bytes.fromhex(ciphertext)
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()  # type: ignore
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode("utf-8")


class Md5Cipher:
    """MD5 加密器"""

    @staticmethod
    def encrypt(plaintext: bytes | str) -> str:
        """
        MD5 加密。

        参数:
        - plaintext (bytes | str): 加密前的明文。

        返回:
        - str: MD5 十六进制摘要。
        """
        md5 = hashlib.md5()
        if not isinstance(plaintext, bytes):
            plaintext = str(plaintext).encode("utf-8")
        md5.update(plaintext)
        return md5.hexdigest()


class ItsDCipher:
    """ItsDangerous 加密器"""

    def __init__(self, key: bytes | str) -> None:
        """
        初始化 ItsDangerous 加密器。

        参数:
        - key (bytes | str): 密钥，16/24/32 bytes 或 16 进制字符串。

        返回:
        - None
        """
        self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

    def encrypt(self, plaintext: Any) -> str:
        """
        ItsDangerous 加密。

        参数:
        - plaintext (Any): 加密前的明文。

        返回:
        - str: 加密后的密文（URL安全）。

        异常:
        - Exception: 加密失败时使用 MD5 作为降级，错误已记录。
        """
        serializer = URLSafeSerializer(self.key)
        try:
            ciphertext = serializer.dumps(plaintext)
        except Exception as e:
            log.error(f"ItsDangerous encrypt failed: {e}")
            ciphertext = Md5Cipher.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext: str) -> Any:
        """
        ItsDangerous 解密。

        参数:
        - ciphertext (str): 解密前的密文。

        返回:
        - Any: 解密后的明文；失败时返回原密文。

        异常:
        - Exception: 解密失败时记录错误并返回原密文。
        """
        serializer = URLSafeSerializer(self.key)
        try:
            plaintext = serializer.loads(ciphertext)
        except Exception as e:
            log.error(f"ItsDangerous decrypt failed: {e}")
            plaintext = ciphertext
        return plaintext
