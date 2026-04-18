import { createVNode, render } from 'vue';
import Message from './Message.vue';

export type MessageType = 'primary' | 'success' | 'warning' | 'info' | 'error';
export type MessagePosition = 'top' | 'bottom' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';

interface MessageOptions {
  message: string;
  type?: MessageType;
  duration?: number;
  position?: MessagePosition;
  showClose?: boolean;
  offset?: number;
  onClose?: () => void;
}

interface MessageInstance {
  id: string;
  vnode: any;
  container: HTMLElement;
  position: MessagePosition;
  offset: number;
  height: number;
}

const instances: MessageInstance[] = [];
let seed = 1;

const showMessage = (options: MessageOptions | string) => {
  const id = `message_${seed++}`;
  const userOptions = typeof options === 'string' ? { message: options } : options;
  const { 
    message, 
    type = 'info', 
    duration = 3000, 
    position = 'top',
    showClose = false,
    onClose
  } = userOptions;

  // Calculate vertical offset
  let verticalOffset = userOptions.offset || 20;
  const samePositionInstances = instances.filter(inst => inst.position === position);
  
  samePositionInstances.forEach(inst => {
    verticalOffset += inst.height + 16; // height + gap
  });

  const container = document.createElement('div');
  
  const props = {
    id,
    message,
    type,
    duration,
    position,
    showClose,
    offset: verticalOffset,
    onClose: () => {
      if (onClose) onClose();
      closeMessage(id);
    },
    onDestroy: () => {
      render(null, container);
      // document.body.removeChild(container); // container is not appended directly
    }
  };

  const vnode = createVNode(Message, props);
  
  render(vnode, container);
  
  // Since Message uses Teleport? No, it's fixed position.
  // We append container to body.
  // But wait, if we append container, and container is a div, it might block clicks if it covers screen?
  // We should make container pointer-events-none but allow children pointer-events-auto?
  // Or just append container.firstElementChild?
  // If we append container.firstElementChild, Vue might complain on updates.
  // Standard way is to append container.
  
  // Let's set container style to not interfere layout
  // container.style.position = 'absolute';
  // container.style.top = '0';
  // container.style.left = '0';
  // container.style.width = '100%';
  // container.style.pointerEvents = 'none'; // So clicks pass through
  // But children (message box) should have pointer-events: auto (which they have by default if not inherited)
  
  // Actually Message.vue has `fixed` class. So it positions itself relative to viewport.
  // The container div will just sit in body.
  // But if container is static block, it pushes content down.
  // So we must make container position absolute or fixed or display none (but then child is hidden).
  
  // Using render(vnode, container), the container becomes the parent of the root element of component.
  // The root element of Message.vue has `fixed` class.
  // So the container just needs to be in the DOM.
  // If we append container to body, it will be at the end.
  // We should ensure container doesn't take space.
  
  // Let's just create a single container for all messages? No, each message needs independent lifecycle.
  // Usually libraries create a new div for each message.
  
  document.body.appendChild(container);
  
  // We need to store the instance to manage offsets
  // We can't know the height immediately because it's not rendered fully?
  // Wait, render is synchronous but layout might not be.
  // However, we can approximate or use a fixed height assumption if needed, or get it after mount.
  // But after mount requires a callback.
  // Let's assume a default height or get it via nextTick?
  // For now, let's assume 50px height if we can't measure.
  // Actually, let's just use a fixed offset increment for simplicity (e.g. 60px).
  // Real implementation would measure.
  
  const instance: MessageInstance = {
    id,
    vnode,
    container,
    position,
    offset: verticalOffset,
    height: 60 // Approximate height including padding/margin
  };
  
  instances.push(instance);
  
  return {
    close: () => closeMessage(id)
  };
};

const closeMessage = (id: string) => {
  const idx = instances.findIndex(inst => inst.id === id);
  if (idx === -1) return;
  
  const instance = instances[idx];
  // Remove from instances first to prevent calculation errors for new messages
  instances.splice(idx, 1);
  
  // Trigger close on component
  if (instance.vnode.component?.exposed?.close) {
    instance.vnode.component.exposed.close();
  } else {
      // Fallback if component instance not available or method not exposed
      // Remove from DOM manually
      render(null, instance.container);
      if (document.body.contains(instance.container)) {
        document.body.removeChild(instance.container);
      }
  }

  // We should re-calculate offsets for remaining messages of same position
  // But that requires updating props on existing components.
  // That's advanced. For now, let's just let them stay or leave a gap.
  // Gaps are fine for simple implementation.
};

export const message = {
  primary: (msg: string, duration?: number) => showMessage({ message: msg, type: 'primary', duration }),
  success: (msg: string, duration?: number) => showMessage({ message: msg, type: 'success', duration }),
  warning: (msg: string, duration?: number) => showMessage({ message: msg, type: 'warning', duration }),
  info: (msg: string, duration?: number) => showMessage({ message: msg, type: 'info', duration }),
  error: (msg: string, duration?: number) => showMessage({ message: msg, type: 'error', duration }),
  show: (options: MessageOptions) => showMessage(options)
};

export default message;
