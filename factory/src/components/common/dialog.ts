import { createVNode, render } from 'vue';
import ConfirmDialog from './ConfirmDialog.vue';

export interface DialogOptions {
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
  type?: 'primary' | 'danger';
}

const showDialog = (options: DialogOptions): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Create a container for the component mounting
    const container = document.createElement('div');
    // Hide the container as it's just a placeholder for the component instance
    // The actual content is Teleported to body
    container.style.display = 'none';
    document.body.appendChild(container);

    let isResolved = false;

    const cleanup = () => {
      render(null, container);
      if (document.body.contains(container)) {
        document.body.removeChild(container);
      }
    };

    const props = {
      ...options,
      visible: true,
      'onUpdate:visible': (val: boolean) => {
        if (!val) {
          // If the dialog is closed and not yet resolved (confirmed), treat as cancel
          if (!isResolved) {
            isResolved = true;
            reject(new Error('Cancel'));
          }
          // Destroy the component instance after a short delay
          setTimeout(cleanup, 100);
        }
      },
      onConfirm: () => {
        if (!isResolved) {
          isResolved = true;
          resolve();
        }
      },
      onCancel: () => {
        if (!isResolved) {
          isResolved = true;
          reject(new Error('Cancel'));
        }
      }
    };

    const vnode = createVNode(ConfirmDialog, props);
    render(vnode, container);
  });
};

export const dialog = {
  show: showDialog,
  // Helper for simple confirmation
  confirm: (message: string, title?: string, options?: Omit<DialogOptions, 'message' | 'title'>) => 
    showDialog({ message, title, ...options })
};

export default dialog;
