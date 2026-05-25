"use client"

import { usePathname } from "next/navigation"
import {ThemeProvider as NextThemesProvider} from "next-themes"

export  function ThemeProvider({children, ...props} :
     React.ComponentProps<typeof NextThemesProvider>) {
        const pathname = usePathname();
        return (
            <NextThemesProvider {...props}
            forcedTheme={pathname === "/" ? "dark" : "light"}
            defaultTheme="light"
            enableSystem={true}
            attribute="class">
                {children}
            </NextThemesProvider>   
        )
     }