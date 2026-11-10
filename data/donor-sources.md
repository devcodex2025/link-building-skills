# Donor sources

Reference material for Stage 1 (discovery) and Stage 2 (vetting). Treat every entry as a lead, not a guarantee: submission rules, prices, and link attributes change often. Re-check before submitting.

## Search query families

Use several families so the shortlist is not dominated by one kind of site.

**Directories and catalogs**

```text
<niche> directory submit tool
"submit your tool" <niche> free
"submit your website" <niche> directory
<niche> tools list "add your tool"
best <niche> tools 2026
```

**Communities and Q&A**

```text
site:reddit.com <niche> "what do you use"
site:news.ycombinator.com <niche> tools
<niche> forum "share your project"
<niche> discord community resources
```

**Comparison and alternative pages**

```text
<competitor> alternatives
<competitor> vs <competitor>
"best free <niche>" review
```

**Resource pages and roundups**

```text
<niche> "resources" "suggest a link"
<niche> link roundup submit
intitle:"useful resources" <niche>
```

## Source categories

| Category | Why it works | Watch out for |
|---|---|---|
| Tool directories | Permanent listings, fast review, relevant audience. | Many are nofollow; some require a backlink badge. |
| Startup directories | Good for new products with no community footprint. | Launch traffic fades quickly; some require paid tiers. |
| Free-software catalogs | Strong for utilities and browser tools. | Review can take weeks; submissions may need a real contact email. |
| Niche forums | Contextual, in-content links; real referral traffic. | Self-promotion rules vary; usually nofollow. |
| Q&A sites | Durable answers that keep sending visitors. | Links must answer the question, not decorate it. |
| Awesome lists (GitHub) | Human-curated, permanent, often dofollow. | Requires a pull request and matching inclusion criteria. |
| Profile and bio pages | Cheap brand entity signals. | Low link value; never the core of a campaign. |

## Worked example: password-security niche

Leads used for the `generatepasswordto.me` pilot. Verify each before use.

| Domain | Type | Account needed | Notes |
|---|---|---|---|
| toolsdirectoryonline.com | Tool directory | No | Free, 24–48h review, URL + description form. |
| thetooldirectory.com | Tool directory | Email contact | Reviewed listings, category "Utilities" fits. |
| freeaidirectories.com | Tool directory | Email contact | Requires logo and screenshot upload. |
| twelve.tools | Startup directory | Yes | Free tier requires a backlink; paid option available. |
| futuretools.io | Tool directory | Email contact | Human review; free lane is competitive. |
| producthunt.com | Launch platform | Yes | Best used for a launch, not a quiet listing. |
| alternativeto.net | Software catalog | Yes | Add as an alternative to a known password manager tool page. |
| saashub.com | Software catalog | Yes | Free listing; paid featured placement optional. |

## Recording results

Add a record to `link_building_results.json` for every lead you investigate, even when the outcome is `skipped`. The reason is the most valuable field for the next campaign.

Minimum fields for a lead: `site_url`, `donor_type`, `relevance_score`, `status`, `notes`.
