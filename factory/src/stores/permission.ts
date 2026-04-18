import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { Component } from 'vue'
import type { RouteRecordRaw } from 'vue-router'
import router, { constantRoutes } from '@/router'
import { useUserStore } from '@/stores/user'
import type { MenuTable } from '@/services/fastApi/module_system/menu'

type ViewModule = { default: Component }

const modules = import.meta.glob<ViewModule>('../views/**/*.vue')
const Layout = () => import('@/components/Layout.vue')
const ExternalLink = () => import('@/views/ExternalLink.vue')

// 菜单类型枚举
const MenuTypeEnum = {
  CATALOG: 1,  // 目录
  MENU: 2,     // 菜单
  BUTTON: 3,   // 按钮
  EXTLINK: 4   // 外链
}

interface Meta {
  alwaysShow?: boolean
  hidden?: boolean
  icon?: string
  keepAlive?: boolean
  title?: string
  order?: number
  params?: { key: string; value: string }[]
  affix?: boolean
  externalUrl?: string
  menuType?: number
}

interface RouteVO {
  children: RouteVO[]
  component?: string | (() => Promise<Component>)
  meta?: Meta
  name?: string
  path?: string
  redirect?: string
}

const generator = (routers: MenuTable[]): RouteVO[] => {
  return routers.map((item) => {
    // 外链类型：route_path 是内部路由路径，component_path 是外链目标地址
    // 其他类型：使用原始逻辑
    const isExtLink = item.type === MenuTypeEnum.EXTLINK
    
    const currentRouter: RouteVO = {
      children: [],
      path: item.route_path,
      name: item.route_name,
      component: isExtLink ? undefined : item.component_path,
      redirect: item.redirect,
      meta: {
        title: item.title,
        icon: item.icon || undefined,
        keepAlive: item.keep_alive,
        hidden: item.hidden,
        order: item.order,
        alwaysShow: item.always_show,
        params: item.params,
        affix: item.affix,
        // 外链类型保存外链目标地址（从 component_path 读取）
        externalUrl: isExtLink ? item.component_path : undefined,
        menuType: item.type,
      },
    };
    if (item.children && item.children.length > 0) {
      currentRouter.children = item.children ? generator(item.children) : [];
    }
    return currentRouter;
  });
};

/**
 * 转换后端路由数据为Vue Router配置
 * 处理组件路径映射和Layout层级嵌套
 */
const transformRoutes = (routes: RouteVO[], isTopLevel: boolean = true): RouteRecordRaw[] => {
  return routes.map((route) => {
    // 创建路由对象，保留所有路由属性
    const normalizedRoute = { ...route } as RouteRecordRaw;

    // 处理组件路径映射
    // normalizedRoute.component = !normalizedRoute.component
    //   ? Layout
    //   : modules[`../../views/${normalizedRoute.component}.vue`] ||
    //     modules["../../views/error/404.vue"];

    // 关键优化：
    // 1. 顶级路由（一级目录）使用Layout组件，确保菜单和navbar能正常显示
    // 2. 二级及以上的父路由不使用Layout组件，只作为路由容器，避免Layout嵌套
    // 3. 叶子路由使用实际组件
    // 4. 递归处理子路由，实现无限层级菜单
    if (normalizedRoute.children && normalizedRoute.children.length > 0) {
      // normalizedRoute.children = transformRoutes(route.children);

      // 非叶子路由
      if (isTopLevel) {
        // 顶级路由（一级目录），使用Layout组件
        normalizedRoute.component = Layout;
      } else {
        // 二级及以上的父路由，不使用Layout组件，只作为路由容器
        normalizedRoute.component = undefined;
      }
      // 递归处理子路由，标记为非顶级路由
      normalizedRoute.children = transformRoutes(route.children, false);
    } else {
      // 叶子路由，使用实际组件
      const menuType = (normalizedRoute.meta as any)?.menuType
      const externalUrl = (normalizedRoute.meta as any)?.externalUrl
      
      if (menuType === MenuTypeEnum.EXTLINK) {
        // 外链类型使用 ExternalLink 组件，并将外链地址作为 props
        normalizedRoute.component = ExternalLink
        // 使用 props 传递外链地址
        normalizedRoute.props = { src: externalUrl || '' }
      } else if (normalizedRoute.component) {
        normalizedRoute.component = modules[`../views/${normalizedRoute.component}.vue`] ||
          modules["../views/error/404.vue"]
      } else {
        normalizedRoute.component = modules["../views/error/404.vue"]
      }
    }

    return normalizedRoute;
  });
};


const collectRouteNames = (items: RouteRecordRaw[], names: string[]) => {
  items.forEach((item) => {
    if (typeof item.name === 'string') {
      names.push(item.name)
    }
    if (Array.isArray(item.children) && item.children.length > 0) {
      collectRouteNames(item.children, names)
    }
  })
}

export const usePermissionStore = defineStore('permission', () => {
  const routes = ref<RouteRecordRaw[]>([...constantRoutes])
  const dynamicRoutes = ref<RouteRecordRaw[]>([])
  const mixLayoutSideMenus = ref<RouteRecordRaw[]>([])
  const isRouteGenerated = ref(false)
  const dynamicRouteNames = ref<string[]>([])

  const generateRoutes = async (): Promise<RouteRecordRaw[]> => {
    const userStore = useUserStore()
    if (!userStore.hasGetRoute) {
      await userStore.loadUser(true)
    }
    const generatedRoutes = transformRoutes(generator(userStore.routeList || []))
    dynamicRoutes.value = generatedRoutes
    routes.value = [...constantRoutes, ...generatedRoutes]
    const nextNames: string[] = []
    collectRouteNames(generatedRoutes, nextNames)
    dynamicRouteNames.value = Array.from(new Set(nextNames))
    isRouteGenerated.value = true
    return generatedRoutes
  }

  const setMixLayoutSideMenus = (parentPath: string) => {
    const parentMenu = routes.value.find((item) => item.path === parentPath)
    mixLayoutSideMenus.value = parentMenu?.children || []
  }

  const resetRouter = () => {
    dynamicRouteNames.value.forEach((name) => {
      if (router.hasRoute(name)) {
        router.removeRoute(name)
      }
    })
    routes.value = [...constantRoutes]
    dynamicRoutes.value = []
    mixLayoutSideMenus.value = []
    dynamicRouteNames.value = []
    isRouteGenerated.value = false
  }

  return {
    routes,
    dynamicRoutes,
    mixLayoutSideMenus,
    isRouteGenerated,
    generateRoutes,
    setMixLayoutSideMenus,
    resetRouter
  }
})
