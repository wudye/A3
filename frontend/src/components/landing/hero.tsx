"use client";


import { ChevronRightIcon } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { FlickeringGrid } from "@/components/ui/flickering-grid";
import Galaxy from "@/components/ui/galaxy";
import { WordRotate } from "@/components/ui/word-rotate";
import { cn } from "@/lib/utils";
import { useI18n } from "@/core/i18n/hooks";




export function Hero({ className }: { className?: string }) {
  const {t} = useI18n();
  return (
    <div
      className={cn(
        "flex size-full flex-col items-center justify-center",
        className,
      )}
    >
        <div style={{ width: '100%', height: '650px', position: 'absolute', top:0 , backgroundColor:"black"}}>
            <Galaxy
                mouseRepulsion
                mouseInteraction
                density={1}
                glowIntensity={0.3}
                saturation={0}
                hueShift={140}
                twinkleIntensity={0.3}
                rotationSpeed={0.1}
                repulsionStrength={2}
                autoCenterRepulsion={0}
                starSpeed={0.5}
                speed={1}
            >
            </Galaxy>
            <FlickeringGrid
                className="absolute inset-0 z-0 translate-y-8 mask-[url(/images/cc.svg)] mask-size-[34vw] mask-center mask-no-repeat md:mask-size-[50vh] pointer-events-none"
                squareSize={4}
                gridGap={4}
                color={"white"}
                maxOpacity={0.3}
                flickerChance={0.25}
            />
       
         </div>

        <div className="container-md relative z-10 flex h-screen flex-col items-center justify-center">
            <h1 className="flex items-center gap-2 text-4xl font-bold md:text-6xl">
            <WordRotate
                className="bg-gradient-to-r from-yellow-200 via-yellow-400 to-amber-500 bg-clip-text text-transparent"

                words={t.hero.content}
            />{" "}
            </h1>
       
            <p className="text-muted-foreground ml-5 mr-5  mt-8  text-center text-2xl text-shadow-sm">
                {t.hero.description}
            </p>
            <Link href="/workspace">
            <Button className="size-lg mt-8 scale-108" size="lg">
                <span className="text-md">{t.hero.versionInfo}</span>

                <ChevronRightIcon className="size-4" />
            </Button>
            </Link>
            <p className="text-muted-foreground mt-4 text-center text-sm opacity-80">
                    planed sandboxes, memories, tools, skills and subagents
            </p>
        </div>
    </div>
  );
}
