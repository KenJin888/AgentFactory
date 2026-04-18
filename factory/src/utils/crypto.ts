import CryptoJS from 'crypto-js';

const SAAS_SECRET_KEY = import.meta.env.VITE_SAAS_SECRET_KEY || 'a2946e69b8'; // 仅用于前端混淆

export const encrypt = (text: string): string => {
  if (!text) return '';
  try {
    return CryptoJS.AES.encrypt(text, SAAS_SECRET_KEY).toString();
  } catch (e) {
    console.error('Encryption failed', e);
    return text;
  }
};

export const decrypt = (ciphertext: string): string => {
  if (!ciphertext) return '';
  try {
    const bytes = CryptoJS.AES.decrypt(ciphertext, SAAS_SECRET_KEY);
    const originalText = bytes.toString(CryptoJS.enc.Utf8);
    // 如果解密结果为空字符串但密文不为空，可能是解密失败（例如密钥不对或非密文），或者是空字符串加密后的结果（但我们上面处理了空字符串）
    // 这里简单处理：如果解密出内容则返回，否则返回原文本（兼容未加密的情况）
    return originalText || ciphertext;
  } catch (e) {
    // 解密失败，假定是明文
    return ciphertext;
  }
};
