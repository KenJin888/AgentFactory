/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_ENV: string;
  readonly VITE_APP_TITLE: string;
  readonly VITE_API_BASE_URL: string;
  readonly VITE_APP_BASE_API: string;
  readonly VITE_APP_PORT: string;
  readonly VITE_TIMEOUT: string;
  readonly VITE_SAAS_SECRET_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
