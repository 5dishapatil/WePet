# 🐾 WePet MVP

### *Animal Climate Risk Intelligence for Pets, Communities, and NGOs*

WePet MVP is a **Python-only Streamlit web application** that helps users understand **hidden climate risks for animals** using **live weather data**, **breed-specific risk logic**, and **role-based actionable recommendations**.

Unlike generic weather apps, WePet focuses on the fact that:

> **What feels manageable to humans may still be dangerous for animals.**

This MVP demonstrates how weather + species/breed sensitivity + context can be combined to provide **useful, non-obvious animal safety guidance**.

---

# 🌍 Problem Statement

Climate change and rising heat conditions are increasingly affecting:

* **Pets**
* **Stray animals**
* **Birds**
* **Shelter animals**
* **Community-fed animals**

Most people judge heat based on **how humans feel**, but animals respond differently because of:

* coat density
* respiratory differences
* body size
* humidity sensitivity
* breed-specific heat tolerance
* indoor heat trapping
* hot-surface exposure

This creates a major gap:

> There is no simple, user-friendly system that says:
> **“Given this animal type + this breed + this location + today’s weather, how risky is it?”**

WePet addresses this gap by converting live weather into:

* **breed-specific climate risk**
* **hidden risk drivers**
* **safe time windows**
* **maximum outdoor exposure recommendations**
* **community 1-minute action tasks**
* **NGO distress severity triage**

---

# 🎯 MVP Goal

This is a **proof-of-concept MVP**, not the full production startup.

The goal is to prove that WePet can:

* Fetch **live weather dynamically**
* Use **breed-specific climate logic**
* Produce **high-value, non-obvious outputs**
* Support **3 user roles**
* Demonstrate a **real market-worthy product direction**

---

# 👥 Supported User Modes

WePet MVP includes **3 user modes**:

## 1. 🐶 Pet Owner

Allows pet owners to:

* select species (Dog / Cat)
* select breed from supported breeds
* optionally upload a pet image (assistive only)
* enter location
* get live weather-based climate risk analysis

### Pet Owner Outputs

* Weather summary
* Overall risk level
* Heat stress score
* Dehydration risk
* Respiratory load
* Surface / paw burn risk
* Indoor heat trap risk
* Hidden risk drivers
* Best safe window today
* Maximum recommended outdoor exposure
* Breed-specific recommendations
* Emergency signs to watch

---

## 2. 🧍 Community User

Designed for normal users who want to help animals without major effort.

Allows users to:

* enter location
* fetch live weather
* receive a **1-minute daily action task**

### Community Outputs

* Today’s 1-minute task
* Why it matters today
* Best time to do it
* Simple reward points / completion tracking

### Example Tasks

* Place one shaded water bowl
* Refill a bird water tray
* Move a water bowl out of direct sun
* Check for distressed stray animals nearby

---

## 3. 🏥 NGO / Shelter

Allows NGOs or shelters to:

* submit distress reports
* upload images
* mark symptoms
* compute severity automatically
* view a severity-sorted dashboard

### NGO Outputs

* Distress report ID
* Severity score
* Severity label (Low / Moderate / High / Critical)
* Response urgency recommendation
* Dashboard of all reports sorted by severity

---

# 🐕 Supported Breeds (MVP Scope)

This MVP intentionally supports **only 10 curated breeds** to prioritise **quality over quantity**.

## Dogs (Top 5)

* German Shepherd
* Labrador Retriever
* Golden Retriever
* Pug
* Siberian Husky

## Cats (Top 5)

* Persian
* Maine Coon
* Siamese
* British Shorthair
* Sphynx

> ⚠️ **Important:**
> WePet MVP does **not** claim universal breed coverage.
> It supports only the above breeds for this proof-of-concept.

---

# 🧠 Core Product Differentiator

WePet is **not** just a weather app.

It does **not** simply say:

* “It’s hot outside”
* “Avoid going out at noon”

Instead, it identifies:

* **hidden climate risks humans may miss**
* **breed-specific heat vulnerabilities**
* **humidity-driven respiratory strain**
* **coat-related heat retention**
* **indoor heat trapping**
* **hot-surface / pavement danger**
* **non-obvious safe windows for activity**

### Example of WePet Intelligence

A human may think:

> “It’s only 31°C, seems manageable.”

But WePet may detect:

* humidity is very high
* apparent temperature is much higher
* the breed is brachycephalic or double-coated
* outdoor exertion may be risky even if it “feels okay” to the owner

This is the core value proposition.

---

# ⚙️ Tech Stack

WePet MVP is built entirely in **Python**.

## Frontend

* **Streamlit**
  Used to create a beautiful, interactive, localhost-based web UI.

## Backend / Logic

* **Python (modular architecture)**
  Used for:

  * risk calculations
  * recommendation generation
  * task selection
  * severity scoring
  * JSON persistence

## API Integration

* **Open-Meteo API**
  Used for:

  * location geocoding
  * live weather
  * hourly forecast

### Why Open-Meteo?

* Free to use for MVP / prototyping
* No API key required
* Reliable for weather + forecast
* Easy integration with Python `requests`

## Data Storage

* **Local JSON files**

  * distress reports
  * task completions / points
  * optional history
  * breed profile data

## Libraries

* `streamlit`
* `requests`
* `pandas`
* `numpy`
* `pillow`
* `plotly` *(optional visualisation)*
* `opencv-python` *(optional, if image support is extended later)*

---

# 🧱 High-Level Architecture

## Main App Flow

1. User launches `app.py`
2. Chooses a mode:

   * Pet Owner
   * Community User
   * NGO / Shelter
3. App routes to the corresponding page
4. Each page uses shared services

## Core Service Layers

* `weather_service.py` → fetches live weather from Open-Meteo
* `breed_profile_service.py` → loads curated breed profiles
* `risk_engine.py` → computes sub-scores + overall risk
* `recommendation_engine.py` → generates breed-specific recommendations
* `citizen_task_engine.py` → generates 1-minute community tasks
* `severity_engine.py` / `distress_service.py` → computes NGO distress severity
* `storage_service.py` → handles local JSON persistence

---

# 📊 Risk Intelligence Logic (Summary)

The MVP computes multiple sub-scores using:

* temperature
* apparent temperature
* humidity
* UV
* wind
* breed sensitivity
* optional modifiers (senior / overweight / heat-sensitive)

## Core Sub-Scores

* Heat Stress
* Dehydration Risk
* Respiratory Load
* Surface / Paw Burn Risk
* Indoor Heat Trap Risk

These are combined into an **overall risk score (0–100)**.

## Risk Levels

* **Low**
* **Moderate**
* **High**
* **Critical**

---

# 🕒 Key Premium Features

## 1. Best Safe Window Today

Using hourly forecast data, WePet identifies:

* the best 1–2 safer time windows for short activity

## 2. Maximum Outdoor Exposure

Instead of generic advice, WePet estimates:

* “Indoor-only today”
* “Very brief shaded exposure only”
* “Short shaded outing only”
* etc.

## 3. Hidden Risk Drivers

The app explains **why** the risk is elevated, e.g.:

* humidity reduces cooling efficiency
* dense coat retains heat
* brachycephalic respiratory risk
* pavement may be hotter than expected
* indoor window heat trap risk

---

# 📁 Recommended Project Structure

```bash
WePet_mvp/
├── app.py
├── pages/
│   ├── pet_owner.py
│   ├── community.py
│   └── ngo.py
│
├── components/
│   ├── ui.py
│   ├── cards.py
│   └── styles.py
│
├── services/
│   ├── weather_service.py
│   ├── breed_profile_service.py
│   ├── risk_engine.py
│   ├── recommendation_engine.py
│   ├── citizen_task_engine.py
│   ├── distress_service.py
│   ├── severity_engine.py
│   └── storage_service.py
│
├── data/
│   ├── breed_profiles.json
│   ├── citizen_tasks.json
│   └── distress_reports.json
│
├── uploads/
├── assets/
├── requirements.txt
└── README.md
```

---

# 🚀 How to Run the Project

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd WePet_mvp
```

## 2. Create and activate virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the app

```bash
streamlit run app.py
```

---

# 📦 Example `requirements.txt`

```txt
streamlit
requests
pandas
numpy
pillow
plotly
opencv-python
```

> If image features are not used yet, `opencv-python` can be optional.

---

# 🛡️ Safety Notes

WePet MVP is a **decision-support and awareness tool**, not a veterinary diagnosis tool.

## The app does NOT:

* diagnose medical conditions
* confirm heatstroke
* replace veterinary advice
* guarantee safety

## The app SHOULD be interpreted as:

* risk guidance
* preventive insight
* climate-aware animal safety support

If severe symptoms are observed, users should seek **urgent veterinary or rescue assistance** where appropriate.

---

# ⚠️ MVP Limitations

This is a **proof-of-concept** and intentionally simplified.

## Current limitations:

* supports only 10 curated breeds
* image upload is assistive only (not true breed recognition)
* no production authentication yet
* local JSON persistence only
* no real-time map layer yet
* no large-scale report verification system yet
* no model-based species recognition yet

---

# 🔮 Future Scope

Planned future upgrades may include:

* full species expansion beyond dogs/cats
* bird / livestock / stray / wildlife modes
* AI-based image-assisted breed/species recognition
* heatwave alerts + push notifications
* map-based distress clustering
* NGO route optimisation
* volunteer verification
* rewards / gift card redemption
* cloud database
* mobile app version
* multilingual support
* real rescue partner integration

---

# 💼 Real-World Product Vision

WePet has the potential to become a real climate-tech + animal welfare product by serving:

* **Pet Owners** → premium climate safety intelligence
* **Communities** → micro-actions for stray / bird support
* **NGOs / Shelters** → prioritised distress triage

This creates a strong future path for:

* B2C subscriptions
* NGO dashboards
* shelter partnerships
* climate-risk alerts
* welfare impact analytics

---

# 🏆 Why This Project Is Strong

WePet stands out because it combines:

* **social impact**
* **climate relevance**
* **practical utility**
* **clear product-market direction**
* **modular architecture**
* **real API integration**
* **role-based UX**
* **expandability into a startup**

It is not just a college project — it is a **credible product prototype**.

---

# 👩‍💻 Author / Team

**Project Name:** WePet MVP
**Category:** Climate-Tech + Animal Welfare + Intelligent Decision Support
**Built With:** Python + Streamlit + Open-Meteo + Rule-Based Risk Intelligence

---

# 📌 Final Note

WePet MVP is designed to answer one important question:

> **“What if today’s weather is more dangerous for an animal than it appears to a human?”**

This MVP is the first step toward making that invisible risk visible.

---

## 🐾 Built with purpose.

## 🌡️ Designed for climate-aware animal safety.

## ❤️ Created as a meaningful, scalable proof-of-concept.
