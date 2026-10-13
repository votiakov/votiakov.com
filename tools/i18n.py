#!/usr/bin/env python3
"""Build site/pl/index.html and site/ua/index.html from the English site/index.html.

English is the source. Each entry below is (English, Polish, Ukrainian). The script
fails if an English string is missing from site/index.html, so after editing the
English page, update the matching entry here and run:  python3 tools/i18n.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "site"

PAIRS = [
    # head
    ('<html lang="en">', '<html lang="pl">', '<html lang="uk">'),
    ('<title>Andrii Votiakov · Lead engineer, former CTO, web data at scale</title>',
     '<title>Andrii Votiakov · Lead engineer, były CTO, dane z internetu</title>',
     '<title>Andrii Votiakov · Lead engineer, колишній CTO, вебдані</title>'),
    ('content="Andrii Votiakov, lead engineer and former CTO in Łódź, Poland. Founding engineer twice, CTO of an award-winning insurer, builder of Cartpie and Fabla. Cloud bills cut by up to 90%."',
     'content="Andrii Votiakov, lead engineer i były CTO z Łodzi. Dwukrotnie founding engineer, CTO nagradzanego ubezpieczyciela, twórca Cartpie i Fabli. Rachunki za chmurę niższe nawet o 90%."',
     'content="Andrii Votiakov, lead engineer і колишній CTO з Лодзі. Двічі founding engineer, CTO нагородженого страховика, автор Cartpie та Fabla. Рахунки за хмару менші до 90%."'),
    ('<link rel="canonical" href="https://votiakov.com/">', '<link rel="canonical" href="https://votiakov.com/pl/">', '<link rel="canonical" href="https://votiakov.com/ua/">'),
    ('<meta property="og:locale" content="en_GB">\n<meta property="og:locale:alternate" content="pl_PL">\n<meta property="og:locale:alternate" content="uk_UA">',
     '<meta property="og:locale" content="pl_PL">\n<meta property="og:locale:alternate" content="en_GB">\n<meta property="og:locale:alternate" content="uk_UA">',
     '<meta property="og:locale" content="uk_UA">\n<meta property="og:locale:alternate" content="en_GB">\n<meta property="og:locale:alternate" content="pl_PL">'),
    ('content="Andrii Votiakov · I scrape the web at scale, build software products and cut cloud bills"',
     'content="Andrii Votiakov · Zbieram dane z internetu na dużą skalę, tworzę produkty software\'owe i tnę rachunki za chmurę"',
     'content="Andrii Votiakov · Збираю дані з інтернету у великому масштабі, створюю програмні продукти та скорочую рахунки за хмару"'),
    ('content="Lead engineer and former CTO in Łódź, Poland. Products, case studies and how I work."',
     'content="Lead engineer i były CTO z Łodzi. Produkty, projekty i sposób pracy."',
     'content="Lead engineer і колишній CTO з Лодзі. Продукти, проєкти та підхід до роботи."'),
    ('<meta property="og:url" content="https://votiakov.com/">', '<meta property="og:url" content="https://votiakov.com/pl/">', '<meta property="og:url" content="https://votiakov.com/ua/">'),
    ('"url": "https://votiakov.com/",', '"url": "https://votiakov.com/pl/",', '"url": "https://votiakov.com/ua/",'),

    # nav
    ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Przejdź do treści</a>', '<a class="skip" href="#main">Перейти до змісту</a>'),
    ('<a class="brand" href="/" aria-label="Andrii Votiakov, home">', '<a class="brand" href="/pl/" aria-label="Andrii Votiakov, strona główna">', '<a class="brand" href="/ua/" aria-label="Andrii Votiakov, головна">'),
    ('title="Open to new work"', 'title="Otwarty na nową pracę"', 'title="Відкритий до нової роботи"'),
    ('<nav aria-label="Main">', '<nav aria-label="Menu główne">', '<nav aria-label="Головне меню">'),
    ('<a href="#built">Built</a>', '<a href="#built">Produkty</a>', '<a href="#built">Продукти</a>'),
    ('<a href="#work">Work</a>', '<a href="#work">Firmy</a>', '<a href="#work">Компанії</a>'),
    ('<a href="#approach">Approach</a>', '<a href="#approach">Podejście</a>', '<a href="#approach">Підхід</a>'),
    ('<a href="#now">Now</a>', '<a href="#now">Teraz</a>', '<a href="#now">Зараз</a>'),
    ('<a class="cta" href="#contact">Contact</a>', '<a class="cta" href="#contact">Kontakt</a>', '<a class="cta" href="#contact">Контакт</a>'),
    ('<a href="/" hreflang="en" lang="en" aria-current="page">EN</a><a href="/pl/" hreflang="pl" lang="pl">PL</a><a href="/ua/" hreflang="uk" lang="uk">UA</a>',
     '<a href="/" hreflang="en" lang="en">EN</a><a href="/pl/" hreflang="pl" lang="pl" aria-current="page">PL</a><a href="/ua/" hreflang="uk" lang="uk">UA</a>',
     '<a href="/" hreflang="en" lang="en">EN</a><a href="/pl/" hreflang="pl" lang="pl">PL</a><a href="/ua/" hreflang="uk" lang="uk" aria-current="page">UA</a>'),

    # hero
    ('<span class="dot" aria-hidden="true"></span>CTO, Engineering and fractional work</p>',
     '<span class="dot" aria-hidden="true"></span>CTO, Engineering i współpraca fractional</p>',
     '<span class="dot" aria-hidden="true"></span>CTO, Engineering та fractional-співпраця</p>'),
    ('I scrape the web at scale, build software products and <span class="serif">cut cloud bills.</span>',
     'Zbieram dane z internetu na dużą skalę, tworzę produkty i <span class="serif">tnę rachunki za chmurę.</span>',
     'Збираю дані з інтернету у великому масштабі, створюю продукти та <span class="serif">скорочую рахунки за хмару.</span>'),
    ("I'm a lead engineer and former CTO. I've built and run production systems for 10+ years: two startups as <b>founding engineer</b>, an award-winning UK insurer as <b>CTO</b>, and a data platform that reads <b>30,000+ online shops</b>.",
     'Jestem lead engineerem i byłym CTO. Od ponad 10 lat buduję i utrzymuję systemy produkcyjne: dwa startupy jako <b>founding engineer</b>, nagradzany brytyjski ubezpieczyciel jako <b>CTO</b> i platforma danych, która czyta <b>ponad 30 000 sklepów internetowych</b>.',
     'Я lead engineer і колишній CTO. Понад 10 років будую та підтримую продакшн-системи: два стартапи як <b>founding engineer</b>, нагороджений британський страховик як <b>CTO</b> та платформа даних, яка читає <b>понад 30 000 інтернет-магазинів</b>.'),
    ('>Work with me <span class="arr"', '>Pracujmy razem <span class="arr"', '>Працюймо разом <span class="arr"'),
    ('>See what I build <span class="arr"', '>Zobacz, co buduję <span class="arr"', '>Подивіться, що я будую <span class="arr"'),
    ('Łódź, Poland · remote, Central European Time', 'Łódź · zdalnie, czas środkowoeuropejski', 'Лодзь, Польща · віддалено, центральноєвропейський час'),

    # Cartpie demo
    ('<span>Cartpie · my product data API</span>', '<span>Cartpie · moje API produktowe</span>', '<span>Cartpie · моє API товарів</span>'),
    ('<h2 id="demo-h">Any product URL in. Clean JSON out.</h2>', '<h2 id="demo-h">Dowolny URL produktu na wejściu. Czysty JSON na wyjściu.</h2>', '<h2 id="demo-h">Будь-який URL товару на вході. Чистий JSON на виході.</h2>'),
    ('<span>tuned retailers, one schema</span>', '<span>dostrojonych sklepów, jeden schemat</span>', '<span>налаштованих магазинів, одна схема</span>'),
    ('<span>for this product</span>', '<span>dla tego produktu</span>', '<span>для цього товару</span>'),
    ('<b>Free</b><span>failures and cache hits</span>', '<b>Gratis</b><span>nieudane zapytania i cache</span>', '<b>$0</b><span>за невдалі запити й кеш</span>'),
    ('>Try it on cartpie.com ↗</a>', '>Wypróbuj na cartpie.com ↗</a>', '>Спробуйте на cartpie.com ↗</a>'),

    # numbers
    ('The work <span class="serif">in numbers</span>', 'Praca <span class="serif">w liczbach</span>', 'Робота <span class="serif">у цифрах</span>'),
    ('<p>10+ years: two startups from the first commit, an insurer where I ran engineering, and the systems and products I own.</p>',
     '<p>Ponad 10 lat: dwa startupy od pierwszego commita, ubezpieczyciel, w którym kierowałem inżynierią, oraz systemy i produkty, za które odpowiadam.</p>',
     '<p>Понад 10 років: два стартапи з першого коміту, страховик, де я керував інженерією, та системи й продукти, за які я відповідаю.</p>'),
    ('<span>founding engineer: a UK insurer and an IoT hardware company</span>', '<span>founding engineer: brytyjski ubezpieczyciel i firma IoT</span>', '<span>founding engineer: британський страховик та IoT-компанія</span>'),
    ('<span>raised by those two startups on platforms I built</span>', '<span>pozyskały te dwa startupy na platformach, które zbudowałem</span>', '<span>залучили ці два стартапи на платформах, які я побудував</span>'),
    ('<b>Winner</b><span>Home Insurance, National Insurance Awards 2023, while I was CTO</span>', '<b>Zwycięstwo</b><span>Home Insurance, National Insurance Awards 2023, gdy byłem CTO</span>', '<b>Перемога</b><span>Home Insurance, National Insurance Awards 2023, коли я був CTO</span>'),
    ('<span>engineers, data scientists and designers in the team I led</span>', '<span>inżynierów, data scientistów i projektantów w zespole, którym kierowałem</span>', '<span>інженерів, data scientists і дизайнерів у команді, якою я керував</span>'),
    ('<b>30,000+</b><span>online shops read every day by a data platform I owned</span>', '<b>30 000+</b><span>sklepów internetowych codziennie czytanych przez platformę danych, za którą odpowiadałem</span>', '<b>30 000+</b><span>інтернет-магазинів щодня читала платформа даних, за яку я відповідав</span>'),
    ('<span>off cloud and data bills for the companies I work with</span>', '<span>mniej na rachunkach za chmurę i dane w firmach, z którymi pracuję</span>', '<span>менші рахунки за хмару й дані у компаній, з якими я працюю</span>'),

    # products
    ('Things I <span class="serif">build and run</span>', 'Co <span class="serif">buduję i utrzymuję</span>', 'Що я <span class="serif">будую та підтримую</span>'),
    ('<p>My own products, and the companies I build with as a co-founder or fractional CTO.</p>', '<p>Moje własne produkty oraz firmy, które współtworzę jako współzałożyciel lub fractional CTO.</p>', '<p>Мої власні продукти та компанії, які я будую як співзасновник або fractional CTO.</p>'),
    ('alt="Cartpie homepage: any product URL in, clean structured data out"', 'alt="Strona główna Cartpie: dowolny URL produktu na wejściu, czyste dane na wyjściu"', 'alt="Головна сторінка Cartpie: будь-який URL товару на вході, чисті дані на виході"'),
    ('<span class="tag">Founder</span>', '<span class="tag">Założyciel</span>', '<span class="tag">Засновник</span>'),
    ('<p>An API and MCP server for product data. Send any product URL and get the price, availability, variants and GTIN back as JSON. Four extraction methods run in parallel and the most confident result wins.</p>',
     '<p>API i serwer MCP do danych produktowych. Wysyłasz dowolny URL produktu i dostajesz cenę, dostępność, warianty i GTIN w formacie JSON. Cztery metody ekstrakcji działają równolegle, a wygrywa wynik z najwyższą pewnością.</p>',
     '<p>API та MCP-сервер для даних про товари. Надсилаєте будь-який URL товару й отримуєте ціну, наявність, варіанти та GTIN у JSON. Чотири методи екстракції працюють паралельно, а перемагає результат із найвищою впевненістю.</p>'),
    ('alt="Fabla homepage: no more inventing posts from scratch"', 'alt="Strona główna Fabli: koniec z wymyślaniem postów od zera"', 'alt="Головна сторінка Fabla: більше не треба вигадувати пости з нуля"'),
    ('<span class="tag">Co-founder</span>', '<span class="tag">Współzałożyciel</span>', '<span class="tag">Співзасновник</span>'),
    ('<p>AI content planning for small brands, in Polish and English. It learns the business and the audience, writes posts in the brand\'s voice and schedules them. My favourite design call: the anti-AI "humanizer" is a separate rewrite pass over the finished draft, so we can test it and swap its model.</p>',
     '<p>Planowanie treści z AI dla małych marek, po polsku i po angielsku. Poznaje firmę i odbiorców, pisze posty głosem marki i planuje publikacje. Moja ulubiona decyzja projektowa: anty-AI „humanizer” to osobny etap, który przepisuje gotowy szkic, więc możemy go testować i wymieniać jego model.</p>',
     '<p>Планування контенту з AI для малих брендів, польською та англійською. Вивчає бізнес і аудиторію, пише пости голосом бренду та планує публікації. Моє улюблене проєктне рішення: анти-AI «humanizer» працює окремим проходом над готовою чернеткою, тому ми можемо його тестувати й міняти модель.</p>'),
    ('alt="mieszkanko homepage: apartment hunting without chaos"', 'alt="Strona główna mieszkanko: szukanie mieszkania bez chaosu"', 'alt="Головна сторінка mieszkanko: пошук квартири без хаосу"'),
    ('<p>Apartment hunting in Poland without the chaos. Listings from Otodom and Gratka on one board, AI summaries, price tracking and a map of real transaction prices from the official GUGiK registry.</p>',
     '<p>Szukanie mieszkania w Polsce bez chaosu. Ogłoszenia z Otodom i Gratki na jednej tablicy, podsumowania AI, śledzenie cen i mapa rzeczywistych cen transakcyjnych z oficjalnego rejestru GUGiK.</p>',
     '<p>Пошук квартири в Польщі без хаосу. Оголошення з Otodom і Gratka на одній дошці, AI-підсумки, відстеження цін і мапа реальних цін угод з офіційного реєстру GUGiK.</p>'),
    ('alt="reducecost.cloud homepage: cloud cost optimisation, cut 30 to 90 percent"', 'alt="Strona główna reducecost.cloud: optymalizacja kosztów chmury, od 30 do 90 procent mniej"', 'alt="Головна сторінка reducecost.cloud: оптимізація витрат на хмару, на 30–90 відсотків менше"'),
    ('<p>Cloud cost work paid from verified savings. A read-only audit first, then the fixes. Results so far: AWS 78% lower in 4 weeks, BigQuery 72% lower in 3 weeks, Datadog 90% lower in 2 weeks.</p>',
     '<p>Optymalizacja kosztów chmury opłacana ze zweryfikowanych oszczędności. Najpierw audyt tylko do odczytu, potem poprawki. Dotychczasowe wyniki: AWS taniej o 78% w 4 tygodnie, BigQuery o 72% w 3 tygodnie, Datadog o 90% w 2 tygodnie.</p>',
     '<p>Оптимізація витрат на хмару з оплатою з підтверджених заощаджень. Спочатку аудит лише на читання, потім виправлення. Результати: AWS дешевше на 78% за 4 тижні, BigQuery на 72% за 3 тижні, Datadog на 90% за 2 тижні.</p>'),
    ('<span>Scrapers I publish and maintain: SHEIN products, job data from ATS systems, app reviews and Google Trends.</span>',
     '<span>Scrapery, które publikuję i utrzymuję: produkty SHEIN, oferty pracy z systemów ATS, recenzje aplikacji i Google Trends.</span>',
     '<span>Скрейпери, які я публікую та підтримую: товари SHEIN, вакансії з ATS-систем, відгуки про застосунки та Google Trends.</span>'),

    # companies
    ('Companies I <span class="serif">built with</span>', 'Firmy, które <span class="serif">współtworzyłem</span>', 'Компанії, які я <span class="serif">будував</span>'),
    ('<p>Two startups from the first commit, and the data platform of a shopping app. What I did and what changed.</p>',
     '<p>Dwa startupy od pierwszego commita i platforma danych aplikacji zakupowej. Co zrobiłem i co się zmieniło.</p>',
     '<p>Два стартапи з першого коміту та платформа даних застосунку для покупок. Що я зробив і що змінилося.</p>'),
    ('Locket · 2020–2024 · Founding engineer, then CTO', 'Locket · 2020–2024 · Founding engineer, potem CTO', 'Locket · 2020–2024 · Founding engineer, згодом CTO'),
    ('<h3>From the first line of code to CTO of an award-winning insurer</h3>', '<h3>Od pierwszej linijki kodu do CTO nagradzanego ubezpieczyciela</h3>', '<h3>Від першого рядка коду до CTO нагородженого страховика</h3>'),
    ('<p>Locket is a UK home insurer regulated by the FCA. I joined as the first engineer and built the product that customers bought: a policy in about 2 minutes, with a price in 1 to 2 seconds.</p>',
     '<p>Locket to brytyjski ubezpieczyciel domów nadzorowany przez FCA. Dołączyłem jako pierwszy inżynier i zbudowałem produkt, który kupowali klienci: polisa w około 2 minuty, cena w 1–2 sekundy.</p>',
     '<p>Locket є британським страховиком житла під наглядом FCA. Я приєднався першим інженером і побудував продукт, який купували клієнти: поліс приблизно за 2 хвилини, ціна за 1–2 секунди.</p>'),
    ("<p>As CTO I led the move to B2B. We built a multi-tenant platform for other insurers, with APIs and a mobile SDK, that a customer could install into its own cloud account in one step. Large insurers' security teams reviewed it. I led a team of about 15 and presented the technology to investors.</p>",
     '<p>Jako CTO poprowadziłem przejście na B2B. Zbudowaliśmy platformę multi-tenant dla innych ubezpieczycieli, z API i mobilnym SDK, którą klient mógł jednym krokiem zainstalować na własnym koncie w chmurze. Przeszła przeglądy bezpieczeństwa dużych ubezpieczycieli. Kierowałem zespołem około 15 osób i prezentowałem technologię inwestorom.</p>',
     '<p>Як CTO я провів перехід на B2B. Ми побудували multi-tenant платформу для інших страховиків з API та мобільним SDK, яку клієнт міг за один крок встановити у власний хмарний акаунт. Її перевіряли команди безпеки великих страховиків. Я керував командою приблизно з 15 людей і презентував технологію інвесторам.</p>'),
    ('<b>~2 min</b><span>to buy a policy</span>', '<b>~2 min</b><span>na zakup polisy</span>', '<b>~2 хв</b><span>на купівлю поліса</span>'),
    ('<span>raised on Seedrs</span>', '<span>pozyskane na Seedrs</span>', '<span>залучено на Seedrs</span>'),
    ('<span>people in the team</span>', '<span>osób w zespole</span>', '<span>людей у команді</span>'),
    ('<p class="o-k">Time to buy home insurance</p>', '<p class="o-k">Czas zakupu ubezpieczenia domu</p>', '<p class="o-k">Час купівлі страхування житла</p>'),
    ('<span class="fill acc w13"></span></span><b>~2 min</b>', '<span class="fill acc w13"></span></span><b>~2 min</b>', '<span class="fill acc w13"></span></span><b>~2 хв</b>'),
    ('<span class="who-l">Other insurers</span>', '<span class="who-l">Inni ubezpieczyciele</span>', '<span class="who-l">Інші страховики</span>'),
    ('<b>15+ min</b>', '<b>15+ min</b>', '<b>15+ хв</b>'),
    ('<b>Winner, Home Insurance</b>', '<b>Zwycięzca, Home Insurance</b>', '<b>Переможець, Home Insurance</b>'),
    ('Hero Labs (now Watergate) · 2018–2020, 2023–2024 · Founding engineer, later interim CTO', 'Hero Labs (obecnie Watergate) · 2018–2020, 2023–2024 · Founding engineer, później interim CTO', 'Hero Labs (тепер Watergate) · 2018–2020, 2023–2024 · Founding engineer, пізніше interim CTO'),
    ('<h3>The platform behind a smart water valve</h3>', '<h3>Platforma za inteligentnym zaworem wody</h3>', '<h3>Платформа для розумного водяного клапана</h3>'),
    ('<p>Hero Labs makes Sonic, a smart water valve for homes. I designed and built the platform from the start: the device cloud, the backend and the mobile app. The company raised £1 million in 3 months with the first version.</p>',
     '<p>Hero Labs produkuje Sonic, inteligentny zawór wody do domów. Zaprojektowałem i zbudowałem platformę od zera: chmurę urządzeń, backend i aplikację mobilną. Z pierwszą wersją firma pozyskała 1 mln funtów w 3 miesiące.</p>',
     '<p>Hero Labs виробляє Sonic, розумний водяний клапан для дому. Я спроєктував і побудував платформу з нуля: хмару для пристроїв, бекенд і мобільний застосунок. З першою версією компанія залучила 1 млн фунтів за 3 місяці.</p>'),
    ('<p>I also built the data platform that let the data scientists teach a model to recognise appliances and find leaks, with users labelling their own water events in the app. Years later the company asked me back as interim CTO to modernise the platform and prepare it for due diligence.</p>',
     '<p>Zbudowałem też platformę danych, na której data scientists uczyli model rozpoznawać urządzenia i wykrywać wycieki, a użytkownicy oznaczali w aplikacji własne zdarzenia zużycia wody. Po latach firma poprosiła mnie o powrót jako interim CTO, żeby zmodernizować platformę i przygotować ją do due diligence.</p>',
     '<p>Також я побудував платформу даних, на якій data scientists навчали модель розпізнавати прилади й знаходити протікання, а користувачі позначали в застосунку власні події споживання води. Через роки компанія повернула мене як interim CTO, щоб модернізувати платформу й підготувати її до due diligence.</p>'),
    ('<span>raised in 3 months</span>', '<span>pozyskane w 3 miesiące</span>', '<span>залучено за 3 місяці</span>'),
    ('<b>1 s</b><span>telemetry from every device</span>', '<b>1 s</b><span>telemetria z każdego urządzenia</span>', '<b>1 с</b><span>телеметрія з кожного пристрою</span>'),
    ('<p class="o-k">Raised with the first version I built</p>', '<p class="o-k">Pozyskane z pierwszą wersją, którą zbudowałem</p>', '<p class="o-k">Залучено з першою версією, яку я побудував</p>'),
    ('£1m <span>in 3 months</span>', '£1m <span>w 3 miesiące</span>', '£1m <span>за 3 місяці</span>'),
    ('<span class="w-lbl">water flow, pressure and temperature, every second</span>', '<span class="w-lbl">przepływ, ciśnienie i temperatura wody co sekundę</span>', '<span class="w-lbl">потік, тиск і температура води щосекунди</span>'),
    ('Basket (wntd.ai) · 2024–2026 · Lead engineer, technical owner', 'Basket (wntd.ai) · 2024–2026 · Lead engineer, właściciel techniczny', 'Basket (wntd.ai) · 2024–2026 · Lead engineer, технічний власник'),
    ('<h3>A data platform that reads 30,000+ online shops</h3>', '<h3>Platforma danych, która czyta ponad 30 000 sklepów internetowych</h3>', '<h3>Платформа даних, що читає понад 30 000 інтернет-магазинів</h3>'),
    ('<p>Basket is a shopping app: users save products from any online shop and the app tracks the price. I owned the data platform behind it for two years and led a team of five.</p>',
     '<p>Basket to aplikacja zakupowa: użytkownicy zapisują produkty z dowolnego sklepu internetowego, a aplikacja śledzi cenę. Przez dwa lata odpowiadałem za platformę danych i kierowałem pięcioosobowym zespołem.</p>',
     '<p>Basket є застосунком для покупок: користувачі зберігають товари з будь-якого інтернет-магазину, а застосунок стежить за ціною. Два роки я відповідав за платформу даних і керував командою з п’яти людей.</p>'),
    ('<p>Then I designed a new version and moved production to it. AI agents wrote the code to my design and under my review, in about two weeks. Both versions ran side by side on the same work before the switch.</p>',
     '<p>Potem zaprojektowałem nową wersję i przeniosłem na nią produkcję. Agenci AI napisali kod według mojego projektu i pod moim review, w około dwa tygodnie. Przed przełączeniem obie wersje działały równolegle na tych samych danych.</p>',
     '<p>Потім я спроєктував нову версію і переніс на неї продакшн. AI-агенти написали код за моїм дизайном і під моїм рев’ю приблизно за два тижні. Перед перемиканням обидві версії працювали паралельно на тих самих даних.</p>'),
    ('<span>a month cut from cloud and data bills</span>', '<span>miesięcznie mniej na rachunkach za chmurę i dane</span>', '<span>на місяць менше в рахунках за хмару й дані</span>'),
    ('<p class="o-k">Before and after the new version</p>', '<p class="o-k">Przed i po nowej wersji</p>', '<p class="o-k">До і після нової версії</p>'),
    ('<span class="ba-l">Success rate</span>', '<span class="ba-l">Skuteczność</span>', '<span class="ba-l">Успішність</span>'),
    ('<span class="ba-l">Time per page</span><span class="ba-v">25 s → <b>3 s</b></span>', '<span class="ba-l">Czas na stronę</span><span class="ba-v">25 s → <b>3 s</b></span>', '<span class="ba-l">Час на сторінку</span><span class="ba-v">25 с → <b>3 с</b></span>'),
    ('<span class="ba-l">Cost of data collection</span><span class="ba-v"><b>80%+</b> lower</span>', '<span class="ba-l">Koszt zbierania danych</span><span class="ba-v"><b>80%+</b> mniej</span>', '<span class="ba-l">Вартість збору даних</span><span class="ba-v"><b>80%+</b> менше</span>'),
    ('<i class="sw"></i>before <i class="sw acc"></i>after', '<i class="sw"></i>przed <i class="sw acc"></i>po', '<i class="sw"></i>до <i class="sw acc"></i>після'),

    # approach
    ('How I <span class="serif">work</span>', 'Jak <span class="serif">pracuję</span>', 'Як я <span class="serif">працюю</span>'),
    ('<p>Habits from 10+ years of building and running production systems.</p>', '<p>Nawyki z ponad 10 lat budowania i utrzymywania systemów produkcyjnych.</p>', '<p>Звички з понад 10 років побудови та підтримки продакшн-систем.</p>'),
    ('<h3>Measure before you spend.</h3><p>The obvious cause of a problem is often the wrong one. Before I put money or engineering time into a fix, I measure where the failures and the costs really are.</p>',
     '<h3>Najpierw mierz, potem wydawaj.</h3><p>Oczywista przyczyna problemu często okazuje się błędna. Zanim przeznaczę pieniądze lub czas inżynierów na poprawkę, mierzę, gdzie naprawdę są błędy i koszty.</p>',
     '<h3>Спершу вимірюй, потім витрачай.</h3><p>Очевидна причина проблеми часто виявляється хибною. Перш ніж вкладати гроші чи час інженерів у виправлення, я вимірюю, де насправді помилки та витрати.</p>'),
    ('<h3>Success is the result, not the status code.</h3><p>A green dashboard proves little. I define success by the outcome the user needs: the data arrived, the policy was issued, the bill went down.</p>',
     '<h3>Sukces to wynik, a nie kod statusu.</h3><p>Zielony dashboard niewiele dowodzi. Sukces definiuję przez wynik, którego potrzebuje użytkownik: dane dotarły, polisa została wystawiona, rachunek spadł.</p>',
     '<h3>Успіх означає результат, а не статус-код.</h3><p>Зелений дашборд мало що доводить. Я визначаю успіх через результат, потрібний користувачу: дані прийшли, поліс видано, рахунок зменшився.</p>'),
    ('<h3>Cheapest method first.</h3><p>Expensive tools are the last step, not the default. Most work does not need them, and the savings add up every month.</p>',
     '<h3>Najpierw najtańsza metoda.</h3><p>Drogie narzędzia to ostatni krok, a nie domyślny wybór. Większość pracy ich nie potrzebuje, a oszczędności rosną z każdym miesiącem.</p>',
     '<h3>Спершу найдешевший метод.</h3><p>Дорогі інструменти є останнім кроком, а не вибором за замовчуванням. Більшості задач вони не потрібні, а заощадження накопичуються щомісяця.</p>'),
    ('<h3>A backup is done when the restore works.</h3><p>I test restores, write runbooks and run incident drills before anything breaks.</p>',
     '<h3>Backup jest gotowy, gdy działa odtworzenie.</h3><p>Testuję odtwarzanie, piszę runbooki i robię ćwiczenia z incydentów, zanim cokolwiek się zepsuje.</p>',
     '<h3>Бекап готовий, коли працює відновлення.</h3><p>Я тестую відновлення, пишу runbooks і проводжу навчання з інцидентів ще до того, як щось зламається.</p>'),
    ('<h3>Delete before you add.</h3><p>Unused resources and dead code cost money and attention every month. Removing them is often the cheapest improvement there is.</p>',
     '<h3>Usuwaj, zanim dodasz.</h3><p>Nieużywane zasoby i martwy kod co miesiąc kosztują pieniądze i uwagę. Ich usunięcie to często najtańsze możliwe usprawnienie.</p>',
     '<h3>Видаляй, перш ніж додавати.</h3><p>Невикористані ресурси й мертвий код щомісяця коштують грошей та уваги. Їх видалення часто є найдешевшим можливим покращенням.</p>'),
    ('<h3>Agents write the code. I own the design and the review.</h3><p>I set teams up to work agent-first: repository instructions, shared skills and a model for each task. A person still owns every design decision and every review.</p>',
     '<h3>Agenci piszą kod. Ja odpowiadam za projekt i review.</h3><p>Ustawiam zespoły do pracy agent-first: instrukcje w repozytorium, wspólne skille i model dobrany do każdego zadania. Każda decyzja projektowa i każde review nadal należą do człowieka.</p>',
     '<h3>Агенти пишуть код. Я відповідаю за дизайн і рев’ю.</h3><p>Я налаштовую команди на роботу agent-first: інструкції в репозиторії, спільні skills і модель під кожну задачу. Кожне проєктне рішення та кожне рев’ю досі за людиною.</p>'),

    # now + writing
    ('<h3 id="now-h">Now</h3>', '<h3 id="now-h">Teraz</h3>', '<h3 id="now-h">Зараз</h3>'),
    ('<p class="when">Updated October 2026 · Łódź, Poland</p>', '<p class="when">Aktualizacja: październik 2026 · Łódź</p>', '<p class="when">Оновлено: жовтень 2026 · Лодзь</p>'),
    ('<b>Building Cartpie</b>, a product data API and MCP server.', '<b>Buduję Cartpie</b>, API i serwer MCP do danych produktowych.', '<b>Будую Cartpie</b>, API та MCP-сервер для даних про товари.'),
    ('<b>Co-founding Fabla</b>, AI content planning for small brands, in closed beta.', '<b>Współtworzę Fablę</b>, planowanie treści z AI dla małych marek, w zamkniętej becie.', '<b>Співзасновник Fabla</b>, планування контенту з AI для малих брендів, у закритій беті.'),
    ('<b>Fractional CTO</b> for small companies in e-commerce, property and logistics, mieszkanko among them.', '<b>Fractional CTO</b> w małych firmach z e-commerce, nieruchomości i logistyki, m.in. w mieszkanko.', '<b>Fractional CTO</b> для малих компаній в e-commerce, нерухомості та логістиці, серед них mieszkanko.'),
    ('<b>Cutting cloud bills</b> through reducecost.cloud, paid from the savings.', '<b>Tnę rachunki za chmurę</b> w ramach reducecost.cloud, z wynagrodzeniem z oszczędności.', '<b>Скорочую рахунки за хмару</b> через reducecost.cloud з оплатою із заощаджень.'),
    ('<b>Looking for</b> my next full-time leadership role: CTO, Head of Engineering or Principal, remote from Poland.', '<b>Szukam</b> kolejnej roli lidera na pełen etat: CTO, Head of Engineering lub Principal, zdalnie z Polski.', '<b>Шукаю</b> наступну керівну роль на повну зайнятість: CTO, Head of Engineering або Principal, віддалено з Польщі.'),
    ('<h3>Writing</h3>', '<h3>Teksty</h3>', '<h3>Публікації</h3>'),
    ('<p class="when">Short technical posts on LinkedIn</p>', '<p class="when">Krótkie posty techniczne na LinkedIn, po angielsku</p>', '<p class="when">Короткі технічні пости в LinkedIn, англійською</p>'),
    ('<b>One parser per site, or four in parallel</b><span>How I scrape e-commerce without a careful parser for each shop.</span>', '<b>Jeden parser na stronę czy cztery równolegle</b><span>Jak scrapuję e-commerce bez osobnego parsera dla każdego sklepu.</span>', '<b>Один парсер на сайт чи чотири паралельно</b><span>Як я збираю дані з e-commerce без окремого парсера для кожного магазину.</span>'),
    ('<b>Every Google Play review, through batchexecute</b><span>How Google Play gives out an app\'s full review history.</span>', '<b>Każda recenzja z Google Play przez batchexecute</b><span>Jak Google Play udostępnia pełną historię recenzji aplikacji.</span>', '<b>Кожен відгук з Google Play через batchexecute</b><span>Як Google Play віддає повну історію відгуків застосунку.</span>'),
    ('<b>What competitive programming taught me about production code</b><span>On olympiads and production code.</span>', '<b>Czego programowanie sportowe nauczyło mnie o kodzie produkcyjnym</b><span>O olimpiadach i kodzie produkcyjnym.</span>', '<b>Чого спортивне програмування навчило мене про продакшн-код</b><span>Про олімпіади та продакшн-код.</span>'),

    # contact
    ('Two ways to <span class="serif">work with me.</span>', 'Dwa sposoby <span class="serif">współpracy.</span>', 'Два способи <span class="serif">співпраці.</span>'),
    ('<span class="k">Full-time</span><h3>CTO, Head of Engineering, Principal or founding engineer</h3><p>Remote from Łódź, Poland. B2B contract or employment. I lead the team and I still write code.</p>',
     '<span class="k">Pełny etat</span><h3>CTO, Head of Engineering, Principal lub founding engineer</h3><p>Zdalnie z Łodzi. Kontrakt B2B lub umowa o pracę. Prowadzę zespół i nadal piszę kod.</p>',
     '<span class="k">Повна зайнятість</span><h3>CTO, Head of Engineering, Principal або founding engineer</h3><p>Віддалено з Лодзі, Польща. Контракт B2B або трудовий договір. Я веду команду й досі пишу код.</p>'),
    ('<span class="k">Fractional and projects</span><h3>Fractional CTO, platform, scraping or cloud cost work</h3><p>Through my company, rēte consulting. Cost work can be paid from verified savings.</p>',
     '<span class="k">Fractional i projekty</span><h3>Fractional CTO, platforma, scraping lub koszty chmury</h3><p>Przez moją firmę, rēte consulting. Pracę nad kosztami można opłacić ze zweryfikowanych oszczędności.</p>',
     '<span class="k">Fractional і проєкти</span><h3>Fractional CTO, платформа, скрейпінг або витрати на хмару</h3><p>Через мою компанію rēte consulting. Роботу з витратами можна оплатити з підтверджених заощаджень.</p>'),
    ('>Show my email <span class="arr"', '>Pokaż mój e-mail <span class="arr"', '>Показати мій email <span class="arr"'),
    ('<span class="mail-note">Hidden from bots. One click shows it.</span>', '<span class="mail-note">Ukryty przed botami. Pokaże się po kliknięciu.</span>', '<span class="mail-note">Прихований від ботів. З’явиться після кліку.</span>'),
    ("c.textContent = 'Copy email';", "c.textContent = 'Kopiuj e-mail';", "c.textContent = 'Скопіювати email';"),
    ("c.textContent = 'Copied'; setTimeout(function () { c.textContent = 'Copy email'; }, 1600);", "c.textContent = 'Skopiowano'; setTimeout(function () { c.textContent = 'Kopiuj e-mail'; }, 1600);", "c.textContent = 'Скопійовано'; setTimeout(function () { c.textContent = 'Скопіювати email'; }, 1600);"),

    # background
    ('<h2 id="bg-h">Background</h2>', '<h2 id="bg-h">Doświadczenie</h2>', '<h2 id="bg-h">Досвід</h2>'),
    ('<p>The short version. The rest is on LinkedIn.</p>', '<p>Wersja skrócona. Reszta jest na LinkedIn.</p>', '<p>Коротка версія. Решта в LinkedIn.</p>'),
    ('<span class="y">2024–now</span>', '<span class="y">2024–teraz</span>', '<span class="y">2024–зараз</span>'),
    ('<span class="d">My consulting business in Poland, and my own products.</span>', '<span class="d">Moja firma doradcza w Polsce i moje własne produkty.</span>', '<span class="d">Моя консалтингова компанія в Польщі та мої власні продукти.</span>'),
    ('<span class="d">Data platform for 30,000+ shops, and AI features. Team of 5.</span>', '<span class="d">Platforma danych dla ponad 30 000 sklepów i funkcje AI. Zespół 5 osób.</span>', '<span class="d">Платформа даних для понад 30 000 магазинів та AI-функції. Команда з 5 людей.</span>'),
    ('<span class="d">Multi-tenant insurance platform for other insurers. Team of about 15.</span>', '<span class="d">Platforma ubezpieczeniowa multi-tenant dla innych ubezpieczycieli. Zespół około 15 osób.</span>', '<span class="d">Multi-tenant страхова платформа для інших страховиків. Команда приблизно з 15 людей.</span>'),
    ('<span class="d">The B2C insurance product, from the first commit.</span>', '<span class="d">Produkt ubezpieczeniowy B2C od pierwszego commita.</span>', '<span class="d">B2C-страховий продукт з першого коміту.</span>'),
    ('<span class="d">IoT platform, mobile app and data platform.</span>', '<span class="d">Platforma IoT, aplikacja mobilna i platforma danych.</span>', '<span class="d">IoT-платформа, мобільний застосунок і платформа даних.</span>'),
    ('<span class="r">Neos, EngineArch, freelance</span><span class="d">An insurance IoT platform, work for UEFA and PKO BP, websites and online shops.</span>',
     '<span class="r">Neos, EngineArch, freelance</span><span class="d">Ubezpieczeniowa platforma IoT, projekty dla UEFA i PKO BP, strony i sklepy internetowe.</span>',
     '<span class="r">Neos, EngineArch, фриланс</span><span class="d">Страхова IoT-платформа, проєкти для UEFA та PKO BP, вебсайти й інтернет-магазини.</span>'),
    ('<span class="y">From age 12</span><span class="r">Competitive programming</span><span class="d">National and international olympiads in Pascal and C/C++.</span>',
     '<span class="y">Od 12. roku życia</span><span class="r">Programowanie sportowe</span><span class="d">Olimpiady krajowe i międzynarodowe w Pascalu i C/C++.</span>',
     '<span class="y">З 12 років</span><span class="r">Спортивне програмування</span><span class="d">Національні та міжнародні олімпіади з Pascal і C/C++.</span>'),
    ('<span>B.A.Sc. Computer Science, Lodz University of Technology. English and Polish at work, Ukrainian and Russian native.</span>',
     '<span>B.A.Sc. Computer Science, Politechnika Łódzka. Angielski i polski w pracy, ukraiński i rosyjski jako języki ojczyste.</span>',
     '<span>B.A.Sc. Computer Science, Лодзька політехніка. Англійська та польська в роботі, українська та російська рідні.</span>'),
    ('>LinkedIn profile <span class="arr"', '>Profil na LinkedIn <span class="arr"', '>Профіль у LinkedIn <span class="arr"'),

    # footer
    ('<span>Plain HTML and CSS. No trackers, no cookies.</span>', '<span>Czysty HTML i CSS. Bez trackerów i ciasteczek.</span>', '<span>Чистий HTML і CSS. Без трекерів і cookies.</span>'),
    ('<a href="#top">Back to top ↑</a>', '<a href="#top">Do góry ↑</a>', '<a href="#top">Нагору ↑</a>'),
]

LANGS = {"pl": 1, "ua": 2}


def build():
    src = (ROOT / "index.html").read_text()
    missing = [en for en, *_ in PAIRS if en not in src]
    if missing:
        print("English strings not found in site/index.html (update tools/i18n.py):")
        for m in missing:
            print("  -", m[:110])
        sys.exit(1)
    for code, col in LANGS.items():
        out = src
        for row in sorted(PAIRS, key=lambda r: -len(r[0])):
            out = out.replace(row[0], row[col])
        (ROOT / code).mkdir(exist_ok=True)
        (ROOT / code / "index.html").write_text(out)
        leftovers = [w for w in re.findall(r">([^<>{}]*[A-Za-z]{4,}[^<>{}]*)<", out) if w.strip()]
        print(f"{code}: written, {len(out)} bytes; text nodes to eyeball: {len(leftovers)}")


if __name__ == "__main__":
    build()
