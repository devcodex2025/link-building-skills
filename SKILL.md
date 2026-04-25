---
name: link-building
description: Повний цикл лінкбілдингу з автоматичним використанням тимчасової пошти (через temp-mail-automation skill) + обов'язкове JSON-логування результатів. На старті потрібен тільки target_url і ніша.
compatibility: opencode
version: 2.1
---

## Вхідні дані
- target_url: посилання для просування
- niche / topic (дуже бажано)
- max_attempts: кількість спроб (рекомендовано 8–15)
- desired_anchor (опціонально)

## Етап 0 — Підготовка
1. Завантажую skill temp-mail-automation (якщо не завантажений).
2. Перевіряю browser_status.
3. Ініціалізую або завантажую `link_building_results.json` (якщо файлу немає — створюю []).

## Етап 1 — Пошук донорів
Використовую web_search / browse_page для пошуку релевантних форумів, блогів, Q&A тощо.

## Етап 2 — Тимчасова пошта + Реєстрація (для кожного донора)
1. Викликаю `temp-mail-automation` → отримую нову {email, password}.
2. browser_navigate на сторінку реєстрації.
3. Заповнюю форму реєстрації новою тимчасовою email + password + інші поля.
4. Клікаю Register / Sign up.
5. Викликаю `temp_mail_wait_for_otp()` (автоматичний пошук коду).
   - Якщо OTP знайдено автоматично — вводжу його.
   - Якщо не знайдено за 2–3 хвилини — прошу користувача: "Надішли код підтвердження з пошти [temp_email]".
6. Підтверджую email.
7. Логінюся з тією ж тимчасовою поштою + паролем.

## Етап 3 — Розміщення посилання
- Пишу природний коментар/пост (3–8 речень).
- Органічно вставляю target_url з anchor text.
- Публікую.
- Роблю screenshot.

## Етап 4 — Обов’язкове JSON-логування
Після кожної спроби додаю/оновлюю запис у `link_building_results.json`:

```json
[
  {
    "timestamp": "2026-04-25T10:15:30Z",
    "site_url": "https://forum.example.com",
    "temp_email": "x7k9p2@mail.tm",
    "password": "Pass123!Temp",
    "action": "registration_and_post",
    "anchor_text": "найкращі інструменти ШІ",
    "posted_url": "https://forum.example.com/thread/123#comment-789",
    "status": "success",
    "screenshot": "screenshots/20260425_forum_example.png",
    "otp_used": "748291",
    "notes": "Посилання опубліковано, коментар природний"
  }
]