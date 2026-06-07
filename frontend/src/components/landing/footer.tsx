import { useMemo } from "react";
import { BarChart3 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useI18n } from "@/core/i18n/hooks";


export type FooterProps = {
  className?: string;
};

export function Footer({ className }: FooterProps) {
  const year = useMemo(() => new Date().getFullYear(), []);
  const { locale, t, changeLocale } = useI18n();
  

  return (
    <footer
      className={cn(
        "container-md mx-auto mt-10 flex flex-col items-center justify-center px-4",
        className
      )}
    >
      <hr className="m-0 h-px w-full border-none bg-gradient-to-r from-transparent via-border/60 to-transparent" />
      
      <div className="text-muted-foreground container flex h-12 flex-col items-center justify-center text-sm">
        <p className="flex items-center gap-2 text-center font-medium opacity-80">
          <BarChart3 className="w-4 h-4" />
            {t.footer.title}
        </p>
      </div>
      
      <div className="text-muted-foreground/60 container mb-8 flex flex-col items-center justify-center gap-1 text-xs">
        <p>{t.footer.license}</p>
        <p>{t.footer.description.replace("{year}", year.toString())}</p>
      </div>
    </footer>
  );
}

