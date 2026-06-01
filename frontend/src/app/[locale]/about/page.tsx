import { useI18n } from '@/components/I18nProviderClient';

export default function AboutPage() {
  const { t, locale } = useI18n();

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-50">
      <div className="max-w-2xl mx-auto px-6 text-center">
        <h1 className="text-5xl font-bold mb-6">{t('common.about')}</h1>
        
        <div className={`inline-block px-4 py-2 rounded-full text-sm font-bold mb-8 ${
          locale === 'zh' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
        }`}>
          {locale === 'zh' ? '当前语言：中文' : 'Current Language: English'}
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 border">
          <h2 className="text-2xl font-semibold mb-4">{t('nav.title')}</h2>
          <p className="text-gray-600 leading-relaxed">{t('nav.subtitle')}</p>
        </div>

        <div className="mt-8 grid grid-cols-2 gap-4">
          <div className="p-4 bg-white rounded-lg border">
            <h3 className="font-bold">{t('common.home')}</h3>
          </div>
          <div className="p-4 bg-white rounded-lg border">
            <h3 className="font-bold">{t('common.login')}</h3>
          </div>
          <div className="p-4 bg-white rounded-lg border">
            <h3 className="font-bold">{t('common.logout')}</h3>
          </div>
          <div className="p-4 bg-white rounded-lg border">
            <h3 className="font-bold">{t('welcome.title')}</h3>
          </div>
        </div>
      </div>
    </div>
  );
}
