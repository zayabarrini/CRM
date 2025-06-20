# Scrapy, b4s
Entrada, tempo de processamento, número de resultados, número de resultados com sucesso

# Sources
Cinema, Psychoanalysis, Businesses/Startups, Gaming
Scale: Institutions size: startups, small, medium, big businesses
Locations: Barcelona, Paris, Berlin, Búzios
Los Angeles, Athens, Tel Aviv, Barcelona, Valencia, Lisboa, Cidade do Cabo, Buenos Aires, Auckland, Perth, Sydney, Moskow, Beijim, Paris, Oslo, Berlín, Tokyo, Seoul, London, Roma, Riad, Nova Delhi, Canberra, Estocolmo, Abuja, Bangkok, Helsinki, Ottawa, Santo Domingo, Cidade del Mexico

# Goals
- Cinema $1M
- Homeoffice $
- International Psychoanalysis
- Pay my own bills, debts, travel, come to Brazil

# Home, Lifestyle
Best places to live in Sunny city with beach, 10 minutes walk from beaches, quiet places, nice sunsets
Camping, Beaches, waterfalls, hiking
Place for 3 cats, Spacetime-flow Zaya Barrini
Money to travel, Money to come to Brazil

# Moving out
- Cats Prep
- Contracts: work, home, payments
- House decor, furniture

# File Tree

├── Crawling
│   ├── clean_scrapy.py
│   ├── crawl_beautiful_soup.py
│   ├── crawl_scrapy.py
│   ├── create_multilingual_md_temp.py
│   ├── create_multilingual_temp.py
│   ├── old-scrapy.py
│   ├── save_emails_gsheet.py
│   ├── send_emails.py
│   ├── sendgrid_emails.py
│   ├── styles.css
│   └── translationFunctions.py
├── Documentation
│   ├── Crawling.md
│   ├── Emails
│   │   ├── Barcelona.md
│   │   ├── Business.html
│   │   ├── Cinema.html
│   │   ├── Psychoanalysis.html
│   │   ├── Psychoanalysis.md
│   │   ├── Psychoanalysis-md.yaml
│   │   ├── Psychoanalysis-ml.md
│   │   ├── Psychoanalysis.yaml
│   │   ├── styles.css
│   │   └── test.html
│   ├── Mallorca-Barcelona.md
│   └── Strategy.md
├── lead_automation_pipeline.py
├── leads_hubspot.py
├── leads_zoho.py
├── README.md
└── Socials
    ├── crawl_contacts.py
    ├── crawl_facebook.py
    ├── crawl_instagram.py
    ├── crawl_linkedin.py
    └── crawl_twitter.py


This **CRM Project** is a comprehensive, semi-automated system for building relationships, managing outreach, and growing a business network across **psychoanalysis, cinema, entrepreneurship, and relocation strategy** (e.g., to Barcelona or Mallorca). Here's a breakdown of its structure and how each part contributes to your goal:

---

## 🧠 **Project Summary**

The CRM system is built to:

1. **Crawl websites and social networks** to collect contact information (especially emails),
2. **Generate and manage multilingual emails** tailored to different sectors,
3. **Send emails via SendGrid or custom SMTP logic**,
4. **Save and manage leads in Google Sheets or CRMs like HubSpot and Zoho**,
5. **Document strategies and manage outreach campaigns** for cities, themes (e.g., cinema, psychoanalysis), and targets.

---

## 📂 **Folder-by-Folder Breakdown**

### **`Crawling/` – Data Extraction & Communication**

Automates data gathering (contacts) and multilingual messaging:

| File                                                             | Purpose                                                             |
| ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| `crawl_scrapy.py`                                                | Uses **Scrapy** to crawl websites and extract email/contact data.   |
| `crawl_beautiful_soup.py`                                        | Same as above, but with **BeautifulSoup** for simpler HTML parsing. |
| `clean_scrapy.py`                                                | Cleans and filters emails/contacts scraped via Scrapy.              |
| `save_emails_gsheet.py`                                          | Pushes collected leads into **Google Sheets**.                      |
| `send_emails.py`                                                 | Custom email sender for batch outreach.                             |
| `sendgrid_emails.py`                                             | Uses **SendGrid API** for professional mass email sending.          |
| `create_multilingual_temp.py` / `create_multilingual_md_temp.py` | Creates email templates in multiple languages.                      |
| `translationFunctions.py`                                        | Functions for automated or assisted translation of email templates. |
| `styles.css`                                                     | Styling for HTML email templates.                                   |

---

### **`Documentation/` – Email Campaigns & Strategy**

Holds campaign-specific content and planning:

| File                        | Purpose                                                                |
| --------------------------- | ---------------------------------------------------------------------- |
| `Strategy.md`               | General CRM + Outreach + Growth strategy.                              |
| `Mallorca-Barcelona.md`     | Strategy focused on relocating to and networking in those regions.     |
| `Emails/` subfolder         | HTML and Markdown email templates for different audiences:             |
| – `Psychoanalysis.html/.md` | For clinics, schools, analysts.                                        |
| – `Cinema.html`             | For studios, producers, festivals.                                     |
| – `Business.html`           | For investors, entrepreneurs, and B2B outreach.                        |
| – `Barcelona.md`            | Personalized content related to your move or connections in Barcelona. |

---

### **`lead_automation_pipeline.py` – Central Pipeline**

Main script that **coordinates lead collection, email sending, and CRM integration**, including:

* Reading leads from crawlers
* Sending via email or integrating with CRMs
* Exporting results to Google Sheets

---

### **`leads_hubspot.py` / `leads_zoho.py`**

Integrations for pushing cleaned and categorized leads into professional CRMs:

* **HubSpot**: For pipeline tracking, contact management, and automation.
* **Zoho CRM**: Alternative CRM platform for lead nurturing.

---

### **`Socials/` – Social Media Crawlers**

Custom scripts for gathering public profile data or contact info from social media platforms:

| File                 | Purpose                                                           |
| -------------------- | ----------------------------------------------------------------- |
| `crawl_linkedin.py`  | Crawls or queries for contacts and company profiles via LinkedIn. |
| `crawl_facebook.py`  | Similar, for Facebook Pages or posts.                             |
| `crawl_twitter.py`   | Looks for handles, bios, and contact links on Twitter (X).        |
| `crawl_instagram.py` | Extracts bios or contact emails from Instagram profiles.          |
| `crawl_contacts.py`  | Possibly a generic entry-point combining the above.               |

---

## 💡 Use Cases & Value

| Goal                                         | Feature Supporting It                       |
| -------------------------------------------- | ------------------------------------------- |
| Relocate to Barcelona with sponsorship       | `Mallorca-Barcelona.md`, targeted campaigns |
| Sell psychoanalytic or cinema products       | `Psychoanalysis.html`, `Cinema.html`        |
| Find business or artistic partners globally  | Crawling tools + multilingual outreach      |
| Grow CRM contacts & automate lead nurturing  | `lead_automation_pipeline.py`, Zoho/HubSpot |
| Centralize & visualize network-building data | Google Sheets + structured documentation    |

---

## 🚀 Next Steps You Could Add

* CRM UI (with filters, segments, tagging)
* Integration with WhatsApp or Telegram for outreach
* Sentiment analysis on email replies
* KPI dashboard to monitor open rate, reply rate, etc.

Semiotics-LGBTQAPI+Women
Semiotics-Linguistics
Semiotics-Topology
Semiotics

Topology-Analytical-Scene
Topology-Animalia
Topology-Animations
Topology-Anthro-Cid-um
Topology-Anthropology
Topology-Audio
Topology-Body
Topology-Discourse-Jouissance-Theory
Topology-Eletronics-Compilers-Languages
Topology-Frustrations

Topology-Game
Topology-Lacanian
Topology-Metaphor
Topology-NdP
Topology-Politics
Topology-Torsion
Topology-Trans-Parenting
Topology-Trans-Psychosis

Posts Suggestion:
Gaming and Digital Art: Topology Game, Animations
Cinema: Favorites-2025: Genre - Subjectivity: Children, Adults, LGBTQAPI+, Tragedy-Structure, Language, Family-Loss-Reconciliation
Psychoanalysis: Topology Game + Dichomansion + Lacanian + Metaphor
Business: Creative Director + SCRUM Master
Mental Health: Metaphor, NdP, Psychosis, Trans-Parenting

# To-do

Send emails to Barcelona in the Markets: Escola de Psicanálise Lacaniana, Gaming Industry, Mental Health Sectors, Business in General

Email.hmtl customization

Send emails, Change email's password

* CRM UI (with filters, segments, tagging)
* Integration with WhatsApp or Telegram for outreach
* Sentiment analysis on email replies
* KPI dashboard to monitor open rate, reply rate, etc.




