import Image from "next/image";
import { ThemeToggle } from "@/components/theme-toggle"


export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
             <ThemeToggle></ThemeToggle>

      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
            <div>
        trade: foundamental and quantative analyse
        choose, trade, backtest, AI Agent + Machine Learning
      </div>
      <div>
        predict: tredency , future
      </div>
      <div>
        digitHuman: entertaiment, communication, growing
      </div>
   
    
      </main>
    </div>
  );
}
