export const redirectToAppBase = () => {
    const {origin, pathname, search} = window.location
    window.location.replace(`${origin}${pathname}${search}`)
}
