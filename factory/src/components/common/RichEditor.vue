<template>
  <div class="border border-slate-200 rounded-xl overflow-hidden">
    <!-- 工具栏 -->
    <Toolbar
      :editor="editorRef"
      mode="default"
      :default-config="toolbarConfig"
      class="border-b border-slate-200"
    />
    <!-- 编辑器 -->
    <Editor
      v-model="modelValue"
      :style="{ minHeight: height, overflowY: 'hidden' }"
      :default-config="editorConfig"
      mode="default"
      @on-created="handleCreated"
      @on-change="handleChange"
    />
  </div>
</template>

<script setup lang="ts">
import "@wangeditor-next/editor/dist/css/style.css";
import { Toolbar, Editor } from "@wangeditor-next/editor-for-vue";
import { IToolbarConfig, IEditorConfig } from "@wangeditor-next/editor";
import { ref, shallowRef, onBeforeUnmount } from "vue";
import { api } from "@/services/api";

// 上传图片回调函数类型
type InsertFnType = (_url: string, _alt: string, _href: string) => void;

const props = defineProps({
  height: {
    type: String,
    default: "300px",
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  autoFocus: {
    type: Boolean,
    default: false,
  },
  scroll: {
    type: Boolean,
    default: true,
  },
  placeholder: {
    type: String,
    default: "请输入内容...",
  },
});

// 双向绑定
const modelValue = defineModel<string>("modelValue", {
  default: "",
});

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef();

// 工具栏配置
const toolbarConfig = ref<Partial<IToolbarConfig>>({
  // 可以在这里自定义工具栏
  excludeKeys: [],
});

// 编辑器配置
const editorConfig = ref<Partial<IEditorConfig>>({
  placeholder: props.placeholder,
  readOnly: props.readonly,
  autoFocus: props.autoFocus,
  scroll: props.scroll,
  MENU_CONF: {
    uploadImage: {
      async customUpload(file: File, insertFn: InsertFnType) {
        try {
          // 创建 FormData
          const formData = new FormData();
          formData.append("file", file);
          
          // 调用上传接口
          const res = await api.file.upload(formData);
          
          if (res?.data?.file_url) {
            // 插入图片
            insertFn(res.data.file_url, file.name, res.data.file_url);
          } else {
            console.error("Upload failed: no file_url in response");
          }
        } catch (error) {
          console.error("Image upload failed:", error);
        }
      },
    } as any,
  },
});

// 记录 editor 实例
const handleCreated = (editor: any) => {
  editorRef.value = editor;
};

// 处理内容变化
const handleChange = (editor: any) => {
  editorRef.value = editor;
  // 获取 HTML 内容
  if (editorRef.value) {
    const html = editorRef.value.getHtml();
    modelValue.value = html;
  }
};

// 组件销毁时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor == null) return;
  editor.destroy();
});
</script>

<style scoped>
/* 自定义编辑器样式 */
:deep(.w-e-text-container) {
  background-color: #f8fafc;
}

:deep(.w-e-toolbar) {
  background-color: #fff;
}

:deep(.w-e-bar-item) {
  color: #475569;
}

:deep(.w-e-bar-item-active) {
  color: #3b82f6;
  background-color: #eff6ff;
}
</style>
