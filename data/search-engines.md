# Search engines and submission endpoints

Coverage: the 12 locales used by the target site: `en`, `uk`, `ru`, `es`, `fr`, `de`, `it`, `pt`, `zh`, `ja`, `pl`, `vi`.

Search engines fall into three groups:

1. **Own index with a submission channel** — the only engines where a manual submission changes anything.
2. **Index resellers** — they use Google or Bing results; submitting separately is pointless.
3. **Crawl-only engines** — no public form; they discover sites through links.

Always submit the sitemap once per engine and request indexing only for pages that matter. Do not resubmit the same URL repeatedly.

## Direct submission endpoints

| Engine | Locales | Index | Submission | Account | CAPTCHA | Notes |
|---|---|---|---|---|---|---|
| Google Search Console | all | own | https://search.google.com/search-console | yes | no | Add a domain property, verify by DNS, submit `sitemap.xml`, use URL Inspection for the 12 locale homepages. |
| Bing Webmaster Tools | all | own | https://www.bing.com/webmasters | yes | no | Import from Google Search Console, submit the sitemap, use URL Submission. |
| IndexNow | all | API | https://www.indexnow.org/documentation | no | no | One POST to `https://api.indexnow.org/indexnow` notifies Bing, Yandex, Seznam, Naver and Yep. Requires a key file in the site root. |
| Yandex Webmaster | ru, uk | own | https://webmaster.yandex.com/ | yes | no | Verify the domain, add the sitemap, use Reindex pages. |
| Baidu Search Resource Platform | zh | own | https://ziyuan.baidu.com/linksubmit/index | yes | no | Site verification required. Mainland-hosted sites usually need an ICP filing. |
| Sogou Webmaster | zh | own | https://zhanzhang.sogou.com/ | yes | no | Chinese-language site verification; supports sitemap and URL push. |
| 360 Webmaster | zh | own | https://zhanzhang.so.com/ | yes | no | Chinese-language site verification; supports sitemap and URL push. |
| Shenma Webmaster | zh | own | https://zhanzhang.sm.cn/ | yes | no | Mobile-first Chinese engine; verification and sitemap submission. |
| Coc Coc | vi | own | https://coccoc.com/search/console/get-your-website-on-coc-coc-search | no | yes | Public URL form with reCAPTCHA. Sitemap form: https://coccoc.com/search/console/submit-sitemap-to-coc-coc-search |
| LetSearch | ru | own | https://letsearch.ru/bots | no | no | Submit by searching for `"domain.tld"` in quotes. Russian-language content only; the site is added to the crawl queue automatically. |
| Marginalia | en | own | https://marginalia-search.com/site/submission | no | no | Search `site:domain.tld` first, then queue the site. Alternative: pull request to the Marginalia submission list on GitHub. |
| Wiby | en | own | https://wiby.me/submit/ | no | yes | Curated index for small, independent sites. Public form with CAPTCHA. |
| Right Dao | en | own | mailto:info@rightdao.com | no | no | No form. Email the URL; the operator adds sites manually. |
| Yep | all | IndexNow | https://www.indexnow.org/documentation | no | no | No public form. Receives IndexNow pushes. |
| Mojeek | all | own | none | no | no | No submission form by design; discovered through genuine links and an HTML sitemap. |
| Brave Search | all | own | none | no | no | No public submission; relies on its own crawler. |

## Index resellers

These engines do not run their own web index. A submission has no separate effect: optimize for Google or Bing and they follow.

| Engine | Locales | Index source |
|---|---|---|
| DuckDuckGo | all | Bing |
| Ecosia | de, all | Bing |
| Qwant | fr, all | Bing |
| Startpage | all | Google |
| Yahoo Search | en | Bing |
| Yahoo Japan | ja | Google |
| MetaGer | de | Metasearch (Bing, Yandex, others) |
| Rambler | ru | Yandex / Google |
| Mail.ru | ru | Yandex / Google |
| Meta.ua | uk | Google |
| Bigmir.net | uk | Google |
| Onet | pl | Google |
| Interia | pl | Google |
| Wirtualna Polska | pl | Google |
| SAPO | pt | Google |
| UOL Busca | pt | Google |
| Terra | es, pt | Google |
| Virgilio | it | Google |
| Libero | it | Google |
| goo | ja | Google |

## Locale coverage matrix

| Locale | Own-index engines with a submission channel | Index resellers |
|---|---|---|
| en | Google, Bing, Marginalia, Wiby, Right Dao, Mojeek (crawl) | DuckDuckGo, Startpage, Yahoo, MetaGer |
| uk | Google, Bing, Yandex | Meta.ua, Bigmir.net |
| ru | Yandex, LetSearch, Google, Bing | Rambler, Mail.ru |
| es | Google, Bing | Terra |
| fr | Google, Bing | Qwant |
| de | Google, Bing, Ecosia (Bing) | MetaGer |
| it | Google, Bing | Virgilio, Libero |
| pt | Google, Bing | SAPO, UOL Busca, Terra |
| zh | Baidu, Sogou, 360, Shenma, Bing | none |
| ja | Google, Bing | Yahoo Japan, goo |
| pl | Google, Bing | Onet, Interia, Wirtualna Polska |
| vi | Google, Bing, Coc Coc | none |

## Submission order

1. Confirm `robots.txt`, `sitemap.xml`, canonical tags, and hreflang for every locale.
2. Deploy the IndexNow key file to the site root and submit all sitemap URLs once.
3. Add the domain to Google Search Console and Bing Webmaster Tools; submit the sitemap.
4. Add the domain to Yandex Webmaster for `ru` and `uk`.
5. Add the domain to Baidu, Sogou, 360, and Shenma for `zh` (verification and, where required, ICP).
6. Submit the URL and sitemap through the Coc Coc forms for `vi`.
7. Submit the domain to LetSearch for `ru` and to Marginalia and Wiby for `en`.
8. Record every submission with its status and review date. Do not repeat submissions that are already pending.

## Rules

- One persistent inbox is used for every registration. See the identity policy in `SKILL.md`.
- CAPTCHA, SMS, and identity verification are operator handoffs; never bypass them.
- Submit each sitemap once per engine unless the sitemap changed materially.
- Do not use mass account creation, automated form farms, or third-party "indexing" services.
- Only pages that are public, indexable, and return `200` should be submitted.

## Platform notes

- Google, Bing, and Yandex require account verification by DNS or an HTML file. The operator must complete this step.
- IndexNow covers Bing, Yandex, Seznam, Naver, and Yep with one request; it does not cover Google or Baidu.
- Coc Coc and Wiby use CAPTCHA, so the operator solves the challenge in the visible browser.
- Baidu, Sogou, 360, and Shenma may require a mainland China entity or ICP filing; without it, indexing can be limited.
- Mojeek has no form. Its documentation recommends genuine links and an HTML sitemap.
