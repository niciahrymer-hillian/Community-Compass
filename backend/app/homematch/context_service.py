import re

HOUSING_CONTEXT = {
    "srap": (
        "State Rental Assistance Program (SRAP): administered by the Delaware State Housing Authority (DSHA). "
        "Provides rental assistance to low-income Delaware residents who do not qualify for or are waiting on "
        "a federal Section 8 voucher. Tenants pay a portion of income toward rent; DSHA pays the remainder "
        "directly to landlords. Contact DSHA at destatehousing.com or call 302-739-4263 for eligibility and applications."
    ),
    "section8": (
        "Section 8 / Housing Choice Voucher: tenant pays 30% of adjusted income, "
        "the Public Housing Authority pays the remainder directly to the landlord. "
        "Landlords must meet HUD Housing Quality Standards. Vouchers are portable across cities."
    ),
    "hopa": (
        "Housing for Older Persons Act (55+ communities): 80% of units must be occupied "
        "by at least one person 55 or older. Communities must publish and follow policies "
        "demonstrating intent to be 55+ housing. Exempts from familial status rules."
    ),
    "lihtc": (
        "Low Income Housing Tax Credit (income-restricted): income limits set at 50-60% "
        "of Area Median Income. Rents are capped. Tenants must re-certify income annually. "
        "Units are privately owned but regulated by state housing finance agencies."
    ),
    "fair_housing": (
        "Fair Housing Act: landlords cannot discriminate based on race, color, national origin, "
        "religion, sex, familial status, or disability. Many states add source of income, "
        "sexual orientation, and age as protected classes."
    ),
    "income_verification": (
        "SSI maximum is approximately $943/month (2024). SSDI varies by work history. "
        "Most landlords require income of 2.5-3x monthly rent. Section 8 vouchers count "
        "as income in states with source-of-income protections."
    ),
}


# How HomeMatch works — so the assistant can answer "how do I…" questions end-to-end.
SITE_GUIDE = (
    "HomeMatch features and how to use them:\n"
    "- Profile: set income type, voucher type, and age once; it pre-filters every search and the feed.\n"
    "- Search: filter listings by Section 8, 55+, income-restricted, rent, bedrooms, and amenities "
    "(parking, laundry, pets, wheelchair access, elevator, utilities included).\n"
    "- Map: browse listings on a map and click a pin to preview.\n"
    "- Feed: a live, personalized stream of new matching listings plus housing news for your programs.\n"
    "- Save a listing with the heart button; saved listings live in your profile.\n"
    "- Save a search to re-run the same filters later.\n"
    "- Request a tour from any listing; the landlord is notified and confirms a time with you.\n"
    "- Apply through a guided 4-step flow: profile check, income, identity, then submit.\n"
    "- Messages: private, encrypted messaging between renters and landlords.\n"
    "- Accessibility: dark mode, colorblind modes, and click the assistant's head to hear replies read aloud."
)

# Role-specific framing for how the assistant should help each user type.
ROLE_GUIDANCE = {
    "renter": (
        "You are speaking with a RENTER. Help them understand their eligibility, find matching "
        "listings, navigate applications, and exercise their housing rights. When matching listings "
        "are provided below, recommend the best fits and explain why they qualify."
    ),
    "landlord": (
        "You are speaking with a LANDLORD. Help them create and manage listings, understand program "
        "requirements (Section 8 HQS inspections, source-of-income laws, fair housing obligations), "
        "respond to applicants, and review tour requests. Do NOT share other landlords' private data."
    ),
    "admin": (
        "You are speaking with an ADMIN. They manage templates, application questions, users, and "
        "listings platform-wide. Answer operational questions about managing HomeMatch."
    ),
}


def build_system_prompt(
    user_profile: dict,
    topic_keys: list[str] | None = None,
    role: str | None = None,
    matching_listings: list[dict] | None = None,
) -> str:
    base = (
        "You are the HomeMatch assistant. HomeMatch is a platform that connects underserved "
        "renters — Section 8 voucher holders, SRAP recipients, 55+ communities, and fixed-income "
        "households — with housing matched to their actual eligibility. "
        "You can answer questions about housing programs AND about how to use the HomeMatch website itself. "
        "Answer clearly and practically. "
        "Never give legal advice — refer users to a housing attorney or local legal aid for legal questions. "
        "Keep responses under 150 words. Acknowledge the user's specific situation."
    )

    role = role or user_profile.get("role") or "renter"
    role_section = ROLE_GUIDANCE.get(role, ROLE_GUIDANCE["renter"])

    keys = topic_keys or list(HOUSING_CONTEXT.keys())
    context_sections = [HOUSING_CONTEXT[k] for k in keys if k in HOUSING_CONTEXT]

    parts = [base, role_section, SITE_GUIDE, *context_sections, f"User profile: {user_profile}"]

    if matching_listings:
        listing_lines = "\n".join(
            f"- {l['title']} in {l['city']}, {l['state']} — ${l['rent_amount']}/mo, "
            f"{l.get('bedrooms', '?')}bd"
            + (", Section 8" if l.get("section8_accepted") else "")
            + (", 55+" if l.get("age_55_plus") else "")
            + (", income-restricted" if l.get("income_restricted") else "")
            + f" (listing id: {l['id']})"
            for l in matching_listings
        )
        parts.append(
            "Matching listings currently available for this renter "
            "(only recommend from these — never invent listings):\n" + listing_lines
        )

    return "\n\n".join(parts)


def fill_template(body: str, variables: dict) -> str:
    for key, value in variables.items():
        body = body.replace(f"{{{{{key}}}}}", str(value))
    return body


def get_template_vars(body: str) -> list[str]:
    return list(set(re.findall(r"\{\{(\w+)\}\}", body)))
