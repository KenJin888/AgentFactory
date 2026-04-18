import type { App } from 'vue'
import { hasPerm, hasRole } from '@/directives/permission'

export const setupDirectives = (app: App) => {
  app.directive('hasPerm', hasPerm)
  app.directive('hasRole', hasRole)
}

