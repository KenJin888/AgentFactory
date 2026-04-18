<template>
  <transition name="message-fade" @after-leave="handleAfterLeave">
    <div
      v-show="visible"
      :class="[
        'fixed z-[9999] flex items-center px-4 py-3 rounded-lg shadow-lg border transition-all duration-300 min-w-[300px]',
        positionClass,
        typeClass
      ]"
      :style="style"
      role="alert"
    >
      <component :is="iconComponent" class="w-5 h-5 mr-3 flex-shrink-0" />
      <span class="text-sm font-medium flex-1 break-words">{{ message }}</span>
      <button v-if="showClose" @click="close" class="ml-4 hover:opacity-70 transition-opacity focus:outline-none">
        <XIcon class="w-4 h-4" />
      </button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { 
  CheckCircle, 
  AlertTriangle, 
  Info, 
  XCircle, 
  X as XIcon,
  Bell
} from 'lucide-vue-next';

const props = withDefaults(defineProps<{
  id: string;
  message: string;
  type?: 'primary' | 'success' | 'warning' | 'info' | 'error';
  position?: 'top' | 'bottom' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  duration?: number;
  showClose?: boolean;
  offset?: number;
  onClose?: () => void;
  onDestroy?: () => void;
}>(), {
  type: 'info',
  position: 'top',
  duration: 3000,
  showClose: false,
  offset: 20
});

const visible = ref(false);
let timer: any = null;

const iconComponent = computed(() => {
  switch (props.type) {
    case 'success': return CheckCircle;
    case 'warning': return AlertTriangle;
    case 'error': return XCircle;
    case 'info': return Info;
    case 'primary': return Bell; // Using Bell for Primary
    default: return Info;
  }
});

const typeClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bg-green-50 border-green-200 text-green-800';
    case 'warning': return 'bg-yellow-50 border-yellow-200 text-yellow-800';
    case 'error': return 'bg-red-50 border-red-200 text-red-800';
    case 'info': return 'bg-blue-50 border-blue-200 text-blue-800';
    case 'primary': return 'bg-indigo-50 border-indigo-200 text-indigo-800';
    default: return 'bg-gray-50 border-gray-200 text-gray-800';
  }
});

const positionClass = computed(() => {
  switch (props.position) {
    case 'top': return 'left-1/2 -translate-x-1/2';
    case 'bottom': return 'left-1/2 -translate-x-1/2';
    case 'top-left': return 'left-4';
    case 'top-right': return 'right-4';
    case 'bottom-left': return 'left-4';
    case 'bottom-right': return 'right-4';
    default: return 'left-1/2 -translate-x-1/2';
  }
});

const style = computed(() => {
  const styleObj: Record<string, string> = {};
  if (props.position.includes('top')) {
    styleObj.top = `${props.offset}px`;
  } else {
    styleObj.bottom = `${props.offset}px`;
  }
  return styleObj;
});

const startTimer = () => {
  if (props.duration > 0) {
    timer = setTimeout(() => {
      close();
    }, props.duration);
  }
};

const close = () => {
  visible.value = false;
  if (props.onClose) {
    props.onClose();
  }
};

const handleAfterLeave = () => {
  if (props.onDestroy) {
    props.onDestroy();
  }
};

onMounted(() => {
  visible.value = true;
  startTimer();
});

onUnmounted(() => {
  if (timer) clearTimeout(timer);
});

defineExpose({ close });
</script>

<style scoped>
.message-fade-enter-active,
.message-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-fade-enter-from,
.message-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* For bottom positions, slide up from bottom */
.message-fade-enter-from.bottom, 
.message-fade-leave-to.bottom {
    transform: translateY(20px);
}
</style>
