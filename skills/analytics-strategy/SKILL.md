---
name: analytics-strategy
description: Analytics planning and measurement strategy. Stack selection, event mapping, funnels, feature flags, and A/B testing. Used during design phases before implementation.
---

# Analytics Strategy

> Define WHAT to measure, WHERE to measure, and HOW to measure before implementing.

---

## 🎯 When to Use

| Workflow | Phase | Trigger |
|----------|-------|---------|
| `/new-project` | Phase 2.9 | After PAGE-SPECs approved |
| `/legacy-project` | Analytics audit | After reverse engineering |
| `/new-task` | New feature analytics | When feature needs metrics |

> [!NOTE]
> **Skip if:** Project is an internal POC without metrics needs.
> **Mandatory for:** Any product that needs to measure conversion, engagement, or retention.

**Output:** `## 📊 Analytics` section in each PAGE-SPEC + config in TDD.

---

## 📋 Process (5 Steps)

### Step 1: Define Analytics Stack

| Tool | Purpose | Phase |
|------|---------|-------|
| **PostHog** | Product Analytics, Session Replay, Feature Flags, Funnels | MVP |
| **Google Search Console** | SEO: indexing, keywords, CTR | MVP |
| **UTM Tracking** | Campaign attribution (captured by PostHog) | MVP |
| **Google Tag Manager** | Centralized tag management | Growth |
| **Meta Pixel** | Facebook/Instagram Ads, Remarketing | When advertising |
| **Google Ads Tag** | Google Ads conversions | When advertising |

---

### Step 2: Map Events per Page

For **EACH** PAGE-SPEC, add section:

```markdown
## 📊 Analytics (PostHog)

### Custom Events
| Event | Trigger | Properties |
|-------|---------|------------|
| `page_name_viewed` | Pageview | `referrer`, `utm_*` |
| `cta_clicked` | Click CTA | `cta_type`, `section` |
| ... | ... | ... |

### Funnels to Measure
- Funnel 1: ...
- Funnel 2: ...

### Feature Flags (A/B)
- `flag_name`: Test description
```

---

### Step 3: Ask the User (MANDATORY)

```markdown
## 📊 Analytics Strategy

To define tracking for this project, I need to know:

### 1. Success Metrics
What are the **3 main metrics** you want to track?
- [ ] Visitor → signup conversion
- [ ] Free → paid conversion
- [ ] Engagement (time on platform)
- [ ] Retention (return in 7 days)
- [ ] Feature adoption
- [ ] Other: ___

### 2. Paid Acquisition
Do you plan to run **paid ads** (Meta, Google)?
- [ ] Yes, soon → Configure pixels
- [ ] Not now → Skip pixels
- [ ] Not sure yet → Prepare but don't activate

### 3. A/B Testing
Which elements do you want to test?
- [ ] CTAs (text, color)
- [ ] Pricing page (plan order)
- [ ] Onboarding flow
- [ ] None for now
```

---

### Step 4: Update TDD

Add/update section `## 📈 Analytics & Tracking Strategy` in TDD with:
- Stack tools
- Events per page
- Required environment variables (e.g. `NEXT_PUBLIC_POSTHOG_KEY`)

---

### Step 5: Update PAGE-SPECs

For each prioritized PAGE-SPEC, add `## 📊 Analytics (PostHog)` section with:
- Custom events
- Funnels to measure
- Feature flags for A/B

---

## 🔴 Exit Gate

```markdown
[ ] Analytics stack defined in TDD
[ ] Events mapped for each PAGE-SPEC
[ ] Environment variables listed in TDD
[ ] User confirmed success metrics
[ ] PAGE-SPECs updated with Analytics section
```

> [!CAUTION]
> **BLOCKER:** Do not proceed to Breakdown without Analytics Strategy defined.
