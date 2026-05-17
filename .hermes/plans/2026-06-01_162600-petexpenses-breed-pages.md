# Breed Pages for petexpenses.com

Goal: Создать 20 страниц под породы собак в `/breeds/` для покрытия семантических пустот.

## Текущее состояние

- **Проект:** `/Users/aleksejs/Desktop/dog-cost-tool/`
- **Деплой:** CF Pages (git push → auto-deploy)
- **Архитектура:** Мульти-страничный статик (index.html + about/compare/contact/privacy/terms/sources + blog/ с 3 постами)
- **Данные:** 51 порода собак + 22 кошки в `PET_DATA` (inline JS в index.html)
- **Стиль блога:** blog/understanding-pet-costs.html — шаблон для breed-страниц (nav `site-nav`, footer `site-footer`, контейнер `article-wrap`)
- **Монетизация:** CJ Raw Paws (dog + cat), пустой "Partner #2" для insurance
- **Аналитика:** PostHog EU

## Что нужно сделать

### Batch 1: топ-20 пород собак (приоритет)

Очерёдность (по объёму запросов + популярности):

1. French Bulldog (multi=1.7, size=small, coat=short, health=Breathing & spine issues)
2. Labrador Retriever (multi=1.2, size=large, coat=short, health=Hip dysplasia & obesity)
3. Golden Retriever (multi=1.25, size=large, coat=long, health=High cancer risk)
4. German Shepherd (multi=1.3, size=large, coat=long, health=Hip dysplasia common)
5. Bulldog (multi=1.8, size=medium, coat=short, health=Very high lifetime vet costs)
6. Poodle (multi=1.1, size=medium, coat=wire, health=Addison's disease risk)
7. Beagle (multi=1.2, size=small, coat=short, health=Obesity & epilepsy risk)
8. Rottweiler (multi=1.35, size=large, coat=short, health=Hip & high cancer rate)
9. Dachshund (multi=1.3, size=small, coat=short, health=High risk of back (IVDD) problems)
10. Siberian Husky (multi=1.1, size=medium, coat=long, health=Eye & hip issues)
11. Pomeranian (multi=1.1, size=small, coat=long, health=Dental & luxating patella)
12. Great Dane (multi=1.4, size=giant, coat=short, health=Bloat; lifespan 7–10 yrs)
13. Chihuahua (multi=1.1, size=small, coat=short, health=Dental issues common)
14. Yorkshire Terrier (multi=1.15, size=small, coat=long, health=Dental & tracheal)
15. Boxer (multi=1.4, size=large, coat=short, health=Heart issues & cancer rate)
16. Shih Tzu (multi=1.2, size=small, coat=long, health=Brachycephalic; lots of grooming)
17. Boston Terrier (multi=1.4, size=small, coat=short, health=Eye & joint issues)
18. Corgi (Pembroke) — slug: corgi-pembroke (multi=1.2, size=small, coat=long, health=Back & hip; obesity)
19. Australian Shepherd (multi=1.15, size=medium, coat=long, health=MDR1 mutation; epilepsy)
20. Bernese Mountain Dog (multi=1.5, size=large, coat=long, health=Short lifespan ~7–8 yrs)

**Start with Batch 1a: top 10** — затем остальные 10.

### Процесс создания одной breed-страницы

**Шаг 1:** Создать `.html` файл из шаблона blog-поста, заменив:
- `<title>` — уникальное под породу
- `<meta name="description">` — уникальное, 150-160 chars
- Breadcrumb JSON-LD — Home → Breeds → Breed Name
- FAQPage JSON-LD — 2 вопроса специфичных для породы
- OG meta tags
- H1 — "How Much Does a [Breed] Cost Per Year? (2026 Guide)"
- Hero-блок с cost stats
- Cost breakdown таблица
- Health factors секция
- Savings tips секция
- FAQ секция
- Similar breeds (3-5 ссылок)
- Affiliate CTA блок (Raw Paws + insurance)
- Calculator CTA блок (ссылка на `/?breed=...&weight=...&age=adult`)

**Шаг 2:** Заменить inline CSS на CSS из blog-шаблона (CSS vars одинаковые по всему сайту)

**Шаг 3:** Заменить nav на `site-nav` из blog-шаблона

**Шаг 4:** Заменить footer на `site-footer` из blog-шаблона

**Шаг 5:** Добавить PostHog analytics (такой же сниппет как в blog)

### Обновление инфраструктуры

**Sitemap:** Добавить 20 URL в `/breeds/` с priority=0.85 для топ-10, 0.75 для остальных.

**Homepage (index.html):** Добавить секцию "Popular Dog Breeds" со ссылками на топ-10 breed-страниц после FAQ.

**Internal links:** Каждая breed-страница ссылается на 3-5 похожих пород + /compare + /sources.

**Insurance affiliate fix:** "Partner #2" в offers — пустой ctaLink. Залить реальную партнёрскую ссылку или заменить на информационный блок.

### Проверка качества (Reviewer)

По чеклисту из навыка `petexpenses-reviewer`:
- Уникальный title/meta на каждой странице
- Все ссылки root-relative
- Нет dead href="#" (кроме #calculator/#faq/#sources)
- JS без ошибок (апострофы экранированы)
- Файлы называются {slug}.html

### Деплой

Git commit → push → CF Pages auto-deploy.
Проверить curl'ом первые 5 страниц.

### SMM план

После деплоя — по расписанию из навыка `petexpenses-smm`:
- Reddit r/dogs, r/FrenchBulldog и т.д.
- Pinterest infographics
- Quora answers
- X/Twitter threads

## Файлы

**Новые:**
- `breeds/french-bulldog-cost.html`
- `breeds/labrador-retriever-cost.html`
- `breeds/golden-retriever-cost.html`
- `breeds/german-shepherd-cost.html`
- `breeds/bulldog-cost.html`
- `breeds/poodle-cost.html`
- `breeds/beagle-cost.html`
- `breeds/rottweiler-cost.html`
- `breeds/dachshund-cost.html`
- `breeds/siberian-husky-cost.html`
- ... и т.д. до 20

**Изменяемые:**
- `sitemap.xml` — добавить 20 URL
- `index.html` — добавить "Popular Breeds" секцию

## Риски

1. **Content-каннибализация** — /compare уже сравнивает породы. Breed-страницы не должны дублировать контент, а углублять.
2. **Апострофы в JS** — `pet's`, `bulldog's` ломают single-quoted JS строки. Проверять каждый файл.
3. **Ссылки в /breeds/** — все root-relative (`href="/compare"`), иначе сломаются.
4. **Partner #2** — пустой ctaLink. Пока не заменён на реального партнёра, не убирать offer-card, но ссылка ведёт на /sources или /blog/pet-insurance-worth-it.
5. **Размер index.html** — 86KB уже. Добавление секции популярных пород не должно сильно увеличить.

## Timeline

| Этап | Время |
|------|-------|
| Создание шаблона + генератор | ~30 min |
| Batch 1a: 10 страниц (DeepSeek) | ~20 min |
| Обновление sitemap + homepage | ~10 min |
| QA review | ~10 min |
| Deploy + проверка | ~5 min |
| **Total** | **~75 min** |
