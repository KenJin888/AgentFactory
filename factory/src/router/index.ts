import {createRouter, createWebHashHistory, type RouteRecordRaw, RouterView} from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../components/Layout.vue'
import Agent from '../views/Agent.vue'
import MySpace from '../views/MySpace.vue'
import ChatPage from '../views/ChatPage.vue'
import Profile from '../views/Profile.vue'
import {useUserStore} from '@/stores/user'
import {usePermissionStore} from '@/stores/permission'

const AGENT_ENTRY_STORAGE_KEY = 'agent_entry_id'
const CATCH_ALL_ROUTE_PATH = '/:pathMatch(.*)*'


const resolveAgentId = (value: unknown): string => {
  const raw = String(value ?? '').trim()
  const agentId = Number(raw)
  if (!Number.isInteger(agentId) || agentId <= 0) {
    return ''
  }
  return String(agentId)
}

export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      hidden: true,
      hideInTags: true
    }
  },
  {
    path: '/agent/:agentid',
    name: 'AgentEntry',
    component: ChatPage,
    meta: {
      requiresAuth: true,
      isAgentEntry: true,
      hidden: true,
      hideInTags: true
    }
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'MySpace',
        component: MySpace,
        meta: {
          title: '我的空间',
          icon: 'compass',
          affix: true,
          // keepAlive: true
        }
      },
      {
        path: 'agent-square',
        name: 'AgentSquare',
        component: Agent,
        meta: {
          title: '智能体广场',
          icon: 'layout-grid'
        }
      },
      {
        path: 'chat/:conversationId',
        name: 'ChatPage',
        component: ChatPage,
        meta: {
          title: '会话',
          icon: 'message-square',
          keepAlive: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: {
          title: '个人中心',
          icon: 'user'
        }
      },
      {
        path: 'help',
        name: 'Help',
        component: () => import('../views/Help.vue'),
        meta: {
          title: '帮助中心',
          icon: 'help-circle'
        }
      }
    ]
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('../views/error/404.vue'),
    meta: {
      hidden: true,
      hideInTags: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: (to) => ({
      path: '/404',
      query: {
        path: to.fullPath
      }
    })
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: constantRoutes
})

let tokenProcessed = false

const ensureDynamicRoutes = async () => {
  const permissionStore = usePermissionStore()
  if (permissionStore.isRouteGenerated) {
    return
  }
  const dynamicRoutes = await permissionStore.generateRoutes()
  dynamicRoutes.forEach((route) => {
    if (typeof route.name === 'string' && !router.hasRoute(route.name)) {
      router.addRoute(route)
    }
  })
}

const isNotFoundMatch = (fullPath: string) => {
  const resolved = router.resolve(fullPath)
  return resolved.matched.length === 0 || resolved.matched.some((record) => {
    if (record.path === CATCH_ALL_ROUTE_PATH) {
      return true
    }
    return record.name === 'NotFound'
  })
}

// 路由守卫
router.beforeEach(async (to, _from, next) => {
  const userStore = useUserStore();
  const permissionStore = usePermissionStore();
  const isAgentEntryRoute = to.name === 'AgentEntry'
  const toAgentId = resolveAgentId(to.params.agentid)

  // Check for auto-login token in URL
  const tokenFromUrl = to.query._xtoken as string
  if (tokenFromUrl && !tokenProcessed) {
    try {
      // Set the token temporarily
      userStore.setTokens(tokenFromUrl, '', true)
      // remove '_xtoken' from URL and proceed
      const query = { ...to.query }
      delete query._xtoken
      const userInfo=await userStore.loadUser(true)
      if (userInfo) {
        tokenProcessed = true

        if (isAgentEntryRoute && toAgentId) {
          sessionStorage.setItem(AGENT_ENTRY_STORAGE_KEY, toAgentId)
        }

        if (to.path === '/login') {
          const redirectPath = typeof to.query.redirect === 'string' && to.query.redirect.startsWith('/')
            ? to.query.redirect
            : '/'
          next({ path: redirectPath, replace: true })
        } else {
          next({ path: to.path, query, replace: true })
        }
        return
      } else {
        await userStore.loginOut()
      }
    } catch (error) {
      console.error('Auto-login failed:', error)
      await userStore.loginOut()
    }
  }

  const token = userStore.token;
  if (token && (to.path === '/login' || to.path === '/mobile/login')) {
    next({ path: to.path.startsWith('/mobile') ? '/mobile' : '/', replace: true })
    return
  }
  if (to.meta.requiresAuth && !token) {
    permissionStore.resetRouter()
    const isMobile = to.path.startsWith('/mobile')
    next({
      path: isMobile ? '/mobile/login' : '/login',
      query: {
        redirect: to.fullPath
      }
    })
    return
  }

  if (token && !permissionStore.isRouteGenerated) {
    await userStore.loadUser()
    await ensureDynamicRoutes()

    const redirectedPath = typeof to.query.path === 'string' ? to.query.path : ''
    const originalTarget = to.path === '/404' && redirectedPath.startsWith('/')
      ? redirectedPath
      : to.fullPath

    if (!isNotFoundMatch(originalTarget)) {
      const resolvedTarget = router.resolve(originalTarget)
      next({
        path: resolvedTarget.path,
        query: resolvedTarget.query,
        hash: resolvedTarget.hash,
        replace: true
      })
      return
    }
  }

  if (!to.meta.requiresAuth) {
    next()
    return
  }

  if (isAgentEntryRoute) {
    if (!toAgentId) {
      next('/')
      return
    }
    sessionStorage.setItem(AGENT_ENTRY_STORAGE_KEY, toAgentId)
  } else {
    const lockedAgentId = sessionStorage.getItem(AGENT_ENTRY_STORAGE_KEY)
    if (lockedAgentId) {
      next(`/agent/${lockedAgentId}`)
      return
    }
  }

  if (!permissionStore.isRouteGenerated) {
    await userStore.loadUser()
    await ensureDynamicRoutes()
    next({ ...to, replace: true })
    return
  }
  if (to.matched.length === 0) {
    next('/')
    return
  }
  userStore.loadUser();
  next()
})

export default router
