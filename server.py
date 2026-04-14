#!/usr/bin/env python3
"""
LLM Provider Compliance Comparison MCP Server
===============================================
By MEOK AI Labs | https://meok.ai

Compare major LLM providers (Claude, GPT-4, Gemini, Llama, Mistral) against
governance standards, CSOAI articles, and regulatory frameworks. Recommend
providers for specific use cases and jurisdictions. Generate risk profiles
and compliance matrices.

Reference: Provider safety policies, usage policies, and published governance
           documentation as of early 2026.

Install: pip install mcp
Run:     python server.py
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

# Tier authentication (connects to Stripe subscriptions)
try:
    from auth_middleware import get_tier_from_api_key, Tier, TIER_LIMITS
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False  # Runs without auth in dev mode

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)


def _check_rate_limit(caller: str = "anonymous", tier: str = "free") -> Optional[str]:
    if tier == "pro":
        return None
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    _usage[caller] = [t for t in _usage[caller] if t > cutoff]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return (
            f"Free tier limit reached ({FREE_DAILY_LIMIT}/day). "
            "Upgrade to MEOK AI Labs Pro for unlimited: https://meok.ai/mcp/llm-compliance-comparison/pro"
        )
    _usage[caller].append(now)
    return None


# ---------------------------------------------------------------------------
# FastMCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "llm-compliance-comparison",
    instructions=(
        "LLM Provider Compliance Comparison server. Compare Claude, GPT-4, Gemini, "
        "Llama, and Mistral against governance standards (EU AI Act, NIST AI RMF, "
        "ISO 42001, GDPR, SOC 2). Recommend providers for use cases and jurisdictions. "
        "Generate risk profiles and compliance matrices. Crosswalk provider safety "
        "policies to CSOAI articles. By MEOK AI Labs."
    ),
)

# ---------------------------------------------------------------------------
# LLM Provider Profiles — Real governance data
# ---------------------------------------------------------------------------

LLM_PROVIDERS = {
    "claude": {
        "provider": "Anthropic",
        "model_family": "Claude",
        "current_model": "Claude 4 (Opus/Sonnet/Haiku)",
        "headquarters": "San Francisco, CA, USA",
        "governance_approach": "Constitutional AI — training AI systems using a set of principles (a constitution) to be helpful, harmless, and honest. RLHF + RLAIF.",
        "safety_framework": {
            "name": "Responsible Scaling Policy (RSP)",
            "description": "Commits to not training or deploying models that cross defined capability thresholds (AI Safety Levels) without corresponding safety measures.",
            "ai_safety_levels": "ASL-1 through ASL-4, with escalating safety requirements at each level.",
            "key_features": [
                "Constitutional AI alignment approach",
                "Responsible Scaling Policy with safety levels",
                "Red team testing before deployment",
                "Interpretability research (mechanistic interpretability)",
                "Third-party safety evaluations",
                "Bug bounty program",
                "Frontier model safety commitments",
            ],
        },
        "data_practices": {
            "training_data_transparency": "moderate",
            "data_retention": "Conversations not used for training by default on API. Consumer product has opt-out.",
            "data_processing_locations": "United States, with GCP infrastructure",
            "gdpr_compliance": "Data Processing Addendum available, EU data processing support",
            "soc2": "SOC 2 Type II certified",
        },
        "compliance_certifications": ["SOC 2 Type II"],
        "published_policies": [
            "Acceptable Use Policy",
            "Responsible Scaling Policy",
            "Constitutional AI paper",
            "Model Card for Claude models",
            "Privacy Policy",
        ],
        "eu_ai_act_readiness": "high",
        "transparency_score": 8,
        "safety_score": 9,
        "data_governance_score": 8,
        "accountability_score": 8,
    },
    "gpt4": {
        "provider": "OpenAI",
        "model_family": "GPT",
        "current_model": "GPT-4o / GPT-4 Turbo / o1 / o3",
        "headquarters": "San Francisco, CA, USA",
        "governance_approach": "Preparedness Framework — systematic approach to tracking, evaluating, forecasting, and protecting against catastrophic risks from frontier models.",
        "safety_framework": {
            "name": "Preparedness Framework + Model Spec",
            "description": "OpenAI Model Spec defines default behaviors, safety boundaries, and reasoning about hard cases. Preparedness Framework evaluates catastrophic risk across CBRN, cybersecurity, persuasion, and model autonomy.",
            "risk_categories": "Cybersecurity, CBRN, Persuasion, Model Autonomy — each scored Low/Medium/High/Critical.",
            "key_features": [
                "Preparedness Framework with risk scorecards",
                "Model Spec defining default behaviors",
                "Red team network (external experts)",
                "Safety advisory group",
                "RLHF alignment training",
                "Content moderation systems",
                "GPT Store review process",
                "Bug bounty program",
            ],
        },
        "data_practices": {
            "training_data_transparency": "low",
            "data_retention": "API data not used for training by default. ChatGPT conversations used for training with opt-out.",
            "data_processing_locations": "United States, with Azure infrastructure globally",
            "gdpr_compliance": "Data Processing Agreement available, EU operations via Microsoft Azure",
            "soc2": "SOC 2 Type II certified",
        },
        "compliance_certifications": ["SOC 2 Type II", "CSA STAR"],
        "published_policies": [
            "Usage Policies",
            "Model Spec",
            "Preparedness Framework",
            "System Card for GPT-4",
            "Privacy Policy",
        ],
        "eu_ai_act_readiness": "high",
        "transparency_score": 6,
        "safety_score": 8,
        "data_governance_score": 7,
        "accountability_score": 7,
    },
    "gemini": {
        "provider": "Google DeepMind",
        "model_family": "Gemini",
        "current_model": "Gemini 2.5 Pro / Flash / Ultra",
        "headquarters": "Mountain View, CA, USA / London, UK",
        "governance_approach": "AI Principles — seven principles guiding AI development: be socially beneficial, avoid unfair bias, be built and tested for safety, be accountable to people, incorporate privacy, uphold scientific standards, be available for appropriate uses.",
        "safety_framework": {
            "name": "Google AI Principles + Frontier Safety Framework",
            "description": "Google's AI Principles (2018) provide foundational values. Frontier Safety Framework (2024) addresses advanced AI risks with Critical Capability Levels (CCLs) and corresponding mitigations.",
            "key_features": [
                "Seven AI Principles (2018)",
                "Frontier Safety Framework with CCLs",
                "Responsible AI practices documentation",
                "AI Red Team (internal)",
                "Model safety evaluations",
                "Content safety classifiers",
                "Responsibility governance structure",
                "Third-party assessments",
            ],
        },
        "data_practices": {
            "training_data_transparency": "low",
            "data_retention": "API data not used for training. Gemini app conversations may be used with consent.",
            "data_processing_locations": "Global (Google Cloud infrastructure)",
            "gdpr_compliance": "Comprehensive GDPR compliance through Google Cloud, DPA available",
            "soc2": "SOC 2 Type II (via Google Cloud)",
        },
        "compliance_certifications": ["SOC 2 Type II", "ISO 27001", "ISO 27017", "ISO 27018", "FedRAMP", "CSA STAR"],
        "published_policies": [
            "Google AI Principles",
            "Frontier Safety Framework",
            "Gemini API Terms",
            "Prohibited Use Policy",
            "Privacy Policy",
        ],
        "eu_ai_act_readiness": "high",
        "transparency_score": 6,
        "safety_score": 8,
        "data_governance_score": 9,
        "accountability_score": 7,
    },
    "llama": {
        "provider": "Meta",
        "model_family": "Llama",
        "current_model": "Llama 4 (Scout/Maverick)",
        "headquarters": "Menlo Park, CA, USA",
        "governance_approach": "Open-weight model release with Responsible Use Guide and Acceptable Use Policy. Meta believes open models accelerate safety research.",
        "safety_framework": {
            "name": "Open Model Safety + Responsible Use Guide",
            "description": "Meta provides safety tools alongside open model weights: Llama Guard (safety classifier), Purple Llama (safety evaluation suite), and Responsible Use Guide. Downstream deployers are responsible for safety in deployment.",
            "key_features": [
                "Open-weight model releases",
                "Llama Guard safety classifier",
                "Purple Llama safety evaluation tools",
                "Responsible Use Guide",
                "Acceptable Use Policy (license restriction)",
                "Red teaming prior to release",
                "CyberSecEval for security testing",
                "Community safety resources",
            ],
        },
        "data_practices": {
            "training_data_transparency": "moderate",
            "data_retention": "Open-weight — data stays with deployer. No centralized inference logging.",
            "data_processing_locations": "Deployer-controlled (self-hosted or cloud)",
            "gdpr_compliance": "Deployer responsibility — Meta provides model, not hosting service",
            "soc2": "N/A — open model, not a service",
        },
        "compliance_certifications": [],
        "published_policies": [
            "Llama Acceptable Use Policy",
            "Responsible Use Guide",
            "Model Card",
            "Llama Community License Agreement",
        ],
        "eu_ai_act_readiness": "moderate",
        "transparency_score": 8,
        "safety_score": 6,
        "data_governance_score": 7,
        "accountability_score": 5,
    },
    "mistral": {
        "provider": "Mistral AI",
        "model_family": "Mistral",
        "current_model": "Mistral Large / Medium / Small / Codestral",
        "headquarters": "Paris, France",
        "governance_approach": "European AI company committed to EU AI Act compliance from inception. Balances openness with safety through a tiered model release strategy.",
        "safety_framework": {
            "name": "Mistral Moderation + Usage Policies",
            "description": "Mistral provides moderation API alongside models. Tiered approach: some models open-weight (Mistral 7B), flagship models API-only. EU-headquartered gives natural GDPR alignment.",
            "key_features": [
                "EU-based (natural GDPR/EU AI Act alignment)",
                "Moderation API for content filtering",
                "Tiered model release (open + proprietary)",
                "Usage Policy for API access",
                "Guardrailing capabilities in API",
                "System-level safety controls",
            ],
        },
        "data_practices": {
            "training_data_transparency": "low",
            "data_retention": "API data not used for training by default. EU data hosting available.",
            "data_processing_locations": "Europe (primary), with global availability",
            "gdpr_compliance": "Strong — EU-headquartered, GDPR compliance by design",
            "soc2": "SOC 2 Type II in progress",
        },
        "compliance_certifications": ["HDS (Health Data Hosting — France)"],
        "published_policies": [
            "Usage Policy",
            "Terms of Service",
            "Privacy Policy",
            "Model Cards for released models",
        ],
        "eu_ai_act_readiness": "very_high",
        "transparency_score": 5,
        "safety_score": 7,
        "data_governance_score": 8,
        "accountability_score": 6,
    },
}

# ---------------------------------------------------------------------------
# CSOAI Article Mapping to Provider Policies
# ---------------------------------------------------------------------------

CSOAI_PROVIDER_MAPPING = {
    "Article 1 — The Maternal Covenant (Care-based Safety)": {
        "claude": {"alignment": "strong", "note": "Constitutional AI's HHH principle directly embodies care-based safety. 'Helpful, Harmless, Honest' maps to CSOAI's 'Protection Through Care, Not Command'."},
        "gpt4": {"alignment": "moderate", "note": "Model Spec defines safety behaviors but framing is compliance-oriented rather than care-based. Safety boundaries are well-defined."},
        "gemini": {"alignment": "moderate", "note": "AI Principles include 'be socially beneficial' and 'be accountable to people', aligning with care ethos."},
        "llama": {"alignment": "weak", "note": "Safety delegated to deployers. Responsible Use Guide provides guidance but no enforcement mechanism."},
        "mistral": {"alignment": "moderate", "note": "Growing safety framework, EU values alignment provides ethical foundation."},
    },
    "Article 2 — Provable Safety Requirements": {
        "claude": {"alignment": "strong", "note": "Mechanistic interpretability research aims for provable understanding. RSP requires safety evidence before scaling."},
        "gpt4": {"alignment": "strong", "note": "Preparedness Framework requires formal risk evaluation with scorecards before deployment decisions."},
        "gemini": {"alignment": "moderate", "note": "Frontier Safety Framework with Critical Capability Levels provides structured safety assessment."},
        "llama": {"alignment": "weak", "note": "Safety testing done pre-release but no ongoing provable safety requirements for deployments."},
        "mistral": {"alignment": "moderate", "note": "Moderation API provides measurable safety layer. Less published on formal verification."},
    },
    "Article 5 — Constitutional Principles": {
        "claude": {"alignment": "strong", "note": "Constitutional AI is literally built on this concept — AI trained on written constitutional principles."},
        "gpt4": {"alignment": "strong", "note": "Model Spec serves as de facto constitution defining default behaviors and boundaries."},
        "gemini": {"alignment": "moderate", "note": "Seven AI Principles serve as constitutional foundation but are more general."},
        "llama": {"alignment": "weak", "note": "Acceptable Use Policy provides constraints but no constitutional training methodology."},
        "mistral": {"alignment": "moderate", "note": "Usage Policy provides boundaries. No published constitutional training approach."},
    },
    "Article 10 — Transparency & Explainability": {
        "claude": {"alignment": "strong", "note": "Published model cards, Constitutional AI paper, interpretability research. System prompt visibility."},
        "gpt4": {"alignment": "moderate", "note": "System cards published, but training data and methods less transparent than peers."},
        "gemini": {"alignment": "moderate", "note": "AI Principles documentation, model cards published. Google scale adds complexity to transparency."},
        "llama": {"alignment": "strong", "note": "Open weights provide maximum model transparency. Architecture and training details published."},
        "mistral": {"alignment": "moderate", "note": "Open models provide transparency. Proprietary models less documented."},
    },
    "Article 47 — Environmental Sustainability": {
        "claude": {"alignment": "moderate", "note": "Some environmental disclosures. GCP infrastructure has renewable energy commitments."},
        "gpt4": {"alignment": "moderate", "note": "Microsoft/Azure renewable energy commitments. Limited direct compute carbon disclosure."},
        "gemini": {"alignment": "strong", "note": "Google matches 100% renewable energy. Published carbon footprint of ML workloads."},
        "llama": {"alignment": "moderate", "note": "Meta has renewable energy commitments. Open models allow efficient local deployment."},
        "mistral": {"alignment": "moderate", "note": "Smaller compute footprint. Less published on environmental impact."},
    },
}


# ---------------------------------------------------------------------------
# TOOL 1: Compare Providers
# ---------------------------------------------------------------------------
@mcp.tool()
def compare_providers(
    providers: Optional[list[str]] = None,
    comparison_criteria: Optional[list[str]] = None,
    framework: str = "all",
    caller: str = "anonymous",
    tier: str = "free", api_key: str = "") -> str:
    """Compare LLM providers (Claude, GPT-4, Gemini, Llama, Mistral) against
    governance standards. Score providers on transparency, safety, data governance,
    and accountability.

    Args:
        providers: List of providers to compare (default all 5): ["claude", "gpt4", "gemini", "llama", "mistral"]
        comparison_criteria: Specific criteria: ["transparency", "safety", "data_governance", "accountability", "eu_ai_act"]
        framework: Governance framework focus: "all", "eu_ai_act", "nist", "iso42001", "gdpr", "csoai"
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _check_rate_limit(caller, tier):
        return {"error": err}

    target_providers = providers or list(LLM_PROVIDERS.keys())
    criteria = comparison_criteria or ["transparency", "safety", "data_governance", "accountability"]

    comparisons = []
    for pid in target_providers:
        if pid not in LLM_PROVIDERS:
            continue
        p = LLM_PROVIDERS[pid]

        scores = {}
        if "transparency" in criteria:
            scores["transparency"] = p["transparency_score"]
        if "safety" in criteria:
            scores["safety"] = p["safety_score"]
        if "data_governance" in criteria:
            scores["data_governance"] = p["data_governance_score"]
        if "accountability" in criteria:
            scores["accountability"] = p["accountability_score"]

        total = sum(scores.values())
        max_total = len(scores) * 10

        entry = {
            "provider_id": pid,
            "provider": p["provider"],
            "model_family": p["model_family"],
            "current_model": p["current_model"],
            "headquarters": p["headquarters"],
            "governance_approach": p["governance_approach"],
            "scores": scores,
            "total_score": total,
            "max_possible": max_total,
            "percentage": round(total / max_total * 100, 1) if max_total else 0,
            "certifications": p["compliance_certifications"],
            "eu_ai_act_readiness": p["eu_ai_act_readiness"],
            "safety_framework": p["safety_framework"]["name"],
        }
        comparisons.append(entry)

    comparisons.sort(key=lambda c: c["total_score"], reverse=True)

    result = {
        "comparison_type": "LLM Provider Governance Comparison",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "framework_focus": framework,
        "criteria_evaluated": criteria,
        "rankings": comparisons,
        "top_provider": comparisons[0]["provider_id"] if comparisons else None,
        "analysis": {
            "most_transparent": max(comparisons, key=lambda c: c["scores"].get("transparency", 0))["provider_id"] if comparisons else None,
            "safest": max(comparisons, key=lambda c: c["scores"].get("safety", 0))["provider_id"] if comparisons else None,
            "best_data_governance": max(comparisons, key=lambda c: c["scores"].get("data_governance", 0))["provider_id"] if comparisons else None,
            "most_accountable": max(comparisons, key=lambda c: c["scores"].get("accountability", 0))["provider_id"] if comparisons else None,
        },
    }

    return result


# ---------------------------------------------------------------------------
# TOOL 2: Recommend for Use Case
# ---------------------------------------------------------------------------
@mcp.tool()
def recommend_for_use_case(
    use_case: str,
    jurisdiction: str,
    data_sensitivity: str = "medium",
    self_hosting_required: bool = False,
    budget_constraint: str = "flexible",
    caller: str = "anonymous",
    tier: str = "free", api_key: str = "") -> str:
    """Given a use case and jurisdiction, recommend the most compliant LLM provider.
    Considers regulatory requirements, data residency, safety needs, and
    deployment constraints.

    Args:
        use_case: Description of the intended use case (e.g. "medical triage assistant", "content moderation")
        jurisdiction: Primary jurisdiction: "eu", "us", "canada", "uk", "global", "apac"
        data_sensitivity: Data sensitivity level: "low", "medium", "high", "critical"
        self_hosting_required: Whether the model must be self-hostable (on-premises/private cloud)
        budget_constraint: Budget level: "minimal", "moderate", "flexible", "enterprise"
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _check_rate_limit(caller, tier):
        return {"error": err}

    use_lower = use_case.lower()

    # Determine requirements from use case
    is_high_risk = any(w in use_lower for w in [
        "medical", "health", "clinical", "diagnosis", "legal", "judicial",
        "credit", "lending", "hiring", "employment", "immigration", "criminal",
        "child", "education", "safety", "autonomous", "biometric",
    ])

    requires_strong_safety = any(w in use_lower for w in [
        "customer-facing", "production", "decision-making", "moderation",
        "medical", "legal", "financial", "government",
    ])

    recommendations = []

    for pid, p in LLM_PROVIDERS.items():
        score = 0
        reasons = []
        disqualifiers = []

        # Self-hosting filter
        if self_hosting_required:
            if pid == "llama":
                score += 20
                reasons.append("Open-weight model supports self-hosting")
            elif pid == "mistral":
                score += 10
                reasons.append("Some open-weight models available for self-hosting")
            else:
                disqualifiers.append("API-only provider — does not support self-hosting")

        # Jurisdiction alignment
        if jurisdiction == "eu":
            if pid == "mistral":
                score += 15
                reasons.append("EU-headquartered — native GDPR and EU AI Act alignment")
            elif pid in ("claude", "gpt4", "gemini"):
                score += 8
                reasons.append("GDPR-compliant data processing agreements available")
            if p["eu_ai_act_readiness"] in ("high", "very_high"):
                score += 10
                reasons.append(f"EU AI Act readiness: {p['eu_ai_act_readiness']}")
        elif jurisdiction == "us":
            if p.get("compliance_certifications"):
                score += 10
                reasons.append(f"Certifications: {', '.join(p['compliance_certifications'])}")
        elif jurisdiction == "canada":
            if pid in ("claude", "gpt4"):
                score += 8
                reasons.append("Strong presence in North American market with compliance infrastructure")

        # Safety
        score += p["safety_score"] * 2
        if requires_strong_safety and p["safety_score"] >= 8:
            score += 10
            reasons.append(f"Strong safety framework: {p['safety_framework']['name']}")

        # Data sensitivity
        if data_sensitivity in ("high", "critical"):
            score += p["data_governance_score"] * 2
            if "SOC 2 Type II" in p.get("compliance_certifications", []):
                score += 10
                reasons.append("SOC 2 Type II certified")

        # High-risk use case
        if is_high_risk:
            score += p["accountability_score"] * 2
            score += p["transparency_score"]

        # Budget
        if budget_constraint == "minimal":
            if pid == "llama":
                score += 15
                reasons.append("Open-weight — no per-token costs (compute only)")
            elif pid == "mistral":
                score += 5
                reasons.append("Competitive pricing")

        recommendations.append({
            "provider_id": pid,
            "provider": p["provider"],
            "model": p["current_model"],
            "recommendation_score": score,
            "reasons": reasons,
            "disqualifiers": disqualifiers,
            "suitable": len(disqualifiers) == 0,
        })

    recommendations = [r for r in recommendations if r["suitable"]]
    recommendations.sort(key=lambda r: r["recommendation_score"], reverse=True)

    regulatory_requirements = []
    if jurisdiction == "eu":
        regulatory_requirements = ["EU AI Act compliance", "GDPR compliance", "DPIA required for high-risk"]
    elif jurisdiction == "us":
        regulatory_requirements = ["SOC 2 recommended", "State privacy laws (CCPA/CPRA)", "Sector-specific (HIPAA, GLBA)"]
    elif jurisdiction == "canada":
        regulatory_requirements = ["AIDA compliance (when enacted)", "CPPA compliance", "PIPEDA"]
    elif jurisdiction == "uk":
        regulatory_requirements = ["UK GDPR", "UK AI regulatory framework", "ICO guidance"]

    result = {
        "recommendation_type": "LLM Provider Recommendation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "use_case": use_case,
        "jurisdiction": jurisdiction,
        "constraints": {
            "data_sensitivity": data_sensitivity,
            "self_hosting_required": self_hosting_required,
            "budget": budget_constraint,
            "high_risk_use_case": is_high_risk,
        },
        "regulatory_requirements": regulatory_requirements,
        "recommendations": recommendations,
        "top_recommendation": recommendations[0] if recommendations else None,
    }

    return result


# ---------------------------------------------------------------------------
# TOOL 3: Provider Risk Profile
# ---------------------------------------------------------------------------
@mcp.tool()
def provider_risk_profile(
    provider: str,
    deployment_context: str = "enterprise",
    caller: str = "anonymous",
    tier: str = "free", api_key: str = "") -> str:
    """Generate a detailed risk profile for a specific LLM provider.
    Covers vendor risk, data handling, regulatory compliance, operational
    risks, and AI-specific risks.

    Args:
        provider: Provider ID: "claude", "gpt4", "gemini", "llama", "mistral"
        deployment_context: Context: "enterprise", "startup", "government", "healthcare", "finance"
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _check_rate_limit(caller, tier):
        return {"error": err}

    if provider not in LLM_PROVIDERS:
        return {"error": f"Unknown provider: {provider}. Valid: {list(LLM_PROVIDERS.keys())}"}

    p = LLM_PROVIDERS[provider]

    # Vendor risk assessment
    vendor_risks = []

    # Vendor lock-in risk
    if provider == "llama":
        vendor_risks.append({"risk": "Model update dependency", "level": "low", "note": "Open weights — can fork and self-maintain"})
    elif provider == "mistral":
        vendor_risks.append({"risk": "Vendor lock-in", "level": "medium", "note": "Mix of open and proprietary models. API-dependent for flagship."})
    else:
        vendor_risks.append({"risk": "Vendor lock-in", "level": "high", "note": "API-dependent, proprietary model. Switching costs significant."})

    # Concentration risk
    if provider in ("gpt4", "gemini"):
        vendor_risks.append({"risk": "Concentration risk", "level": "high", "note": f"Large tech company ({p['provider']}) — subject to broad regulatory and antitrust actions"})
    else:
        vendor_risks.append({"risk": "Concentration risk", "level": "medium", "note": "Focused AI company — dependent on continued funding and market position"})

    # Data handling risks
    data_risks = [
        {"risk": "Training data contamination", "level": "medium", "note": "All major providers face challenges with training data provenance and copyright"},
        {"risk": "Inference data privacy", "level": "low" if p["data_practices"]["soc2"] else "medium", "note": p["data_practices"]["data_retention"]},
        {"risk": "Cross-border data transfers", "level": "low" if provider == "mistral" else "medium", "note": p["data_practices"]["data_processing_locations"]},
    ]

    # Regulatory risks
    reg_risks = []
    if p["eu_ai_act_readiness"] in ("very_high", "high"):
        reg_risks.append({"risk": "EU AI Act non-compliance", "level": "low", "note": f"Readiness: {p['eu_ai_act_readiness']}"})
    else:
        reg_risks.append({"risk": "EU AI Act non-compliance", "level": "medium", "note": f"Readiness: {p['eu_ai_act_readiness']} — deployer bears significant compliance burden"})

    if p["compliance_certifications"]:
        reg_risks.append({"risk": "Certification gaps", "level": "low", "note": f"Holds: {', '.join(p['compliance_certifications'])}"})
    else:
        reg_risks.append({"risk": "Certification gaps", "level": "high", "note": "No compliance certifications — deployer must implement own controls"})

    # AI-specific risks
    ai_risks = [
        {"risk": "Model hallucination", "level": "medium", "note": "Inherent to all current LLMs. Mitigation varies by provider."},
        {"risk": "Prompt injection", "level": "medium", "note": "Active area of defense. No provider has fully solved this."},
        {"risk": "Bias in outputs", "level": "medium", "note": "All providers conduct bias testing. Residual bias persists."},
    ]

    if provider == "llama":
        ai_risks.append({"risk": "Fine-tuning misuse", "level": "high", "note": "Open weights can be fine-tuned to remove safety guardrails"})
    else:
        ai_risks.append({"risk": "API abuse", "level": "medium", "note": "Usage policies and monitoring in place but circumvention possible"})

    # Context-specific risks
    context_risks = {
        "government": [{"risk": "FISMA/FedRAMP compliance", "level": "low" if "FedRAMP" in p.get("compliance_certifications", []) else "high", "note": "Government deployment requires elevated compliance"}],
        "healthcare": [{"risk": "HIPAA compliance", "level": "medium", "note": "BAA may be required. Verify with provider."}],
        "finance": [{"risk": "Financial regulation compliance", "level": "medium", "note": "SOC 2, PCI DSS, GLBA implications depending on use."}],
    }

    all_risks = vendor_risks + data_risks + reg_risks + ai_risks + context_risks.get(deployment_context, [])
    risk_counts = defaultdict(int)
    for r in all_risks:
        risk_counts[r["level"]] += 1

    overall = "HIGH" if risk_counts["high"] >= 3 else "MEDIUM" if risk_counts["high"] >= 1 or risk_counts["medium"] >= 4 else "LOW"

    result = {
        "profile_type": "LLM Provider Risk Profile",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": {
            "id": provider,
            "name": p["provider"],
            "model": p["current_model"],
            "headquarters": p["headquarters"],
        },
        "deployment_context": deployment_context,
        "risk_categories": {
            "vendor_risks": vendor_risks,
            "data_handling_risks": data_risks,
            "regulatory_risks": reg_risks,
            "ai_specific_risks": ai_risks,
            "context_specific_risks": context_risks.get(deployment_context, []),
        },
        "risk_summary": {
            "total_risks": len(all_risks),
            "high": risk_counts["high"],
            "medium": risk_counts["medium"],
            "low": risk_counts["low"],
            "overall_risk_level": overall,
        },
        "safety_framework_details": p["safety_framework"],
    }

    return result


# ---------------------------------------------------------------------------
# TOOL 4: Compliance Matrix
# ---------------------------------------------------------------------------
@mcp.tool()
def compliance_matrix(
    frameworks: Optional[list[str]] = None,
    providers: Optional[list[str]] = None,
    caller: str = "anonymous",
    tier: str = "free", api_key: str = "") -> str:
    """Generate a compliance matrix showing all providers against all frameworks.
    Shows coverage status per provider per framework with rationale.

    Args:
        frameworks: Governance frameworks to assess against: ["eu_ai_act", "gdpr", "nist_rmf", "iso42001", "soc2", "aida"]
        providers: Providers to include (default all 5)
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _check_rate_limit(caller, tier):
        return {"error": err}

    target_frameworks = frameworks or ["eu_ai_act", "gdpr", "nist_rmf", "iso42001", "soc2"]
    target_providers = providers or list(LLM_PROVIDERS.keys())

    framework_info = {
        "eu_ai_act": {"name": "EU AI Act", "type": "Regulation", "jurisdiction": "EU"},
        "gdpr": {"name": "GDPR", "type": "Regulation", "jurisdiction": "EU"},
        "nist_rmf": {"name": "NIST AI RMF", "type": "Framework", "jurisdiction": "US"},
        "iso42001": {"name": "ISO/IEC 42001", "type": "Standard", "jurisdiction": "International"},
        "soc2": {"name": "SOC 2", "type": "Certification", "jurisdiction": "US"},
        "aida": {"name": "Canada AIDA", "type": "Legislation", "jurisdiction": "Canada"},
    }

    def _assess_compliance(pid: str, fw: str) -> dict:
        p = LLM_PROVIDERS[pid]

        assessments = {
            "eu_ai_act": {
                "status": p["eu_ai_act_readiness"],
                "note": f"Provider readiness: {p['eu_ai_act_readiness']}. Deployer retains significant obligations.",
                "deployer_responsibility": "high",
            },
            "gdpr": {
                "status": "compliant" if p["data_practices"]["gdpr_compliance"] else "partial",
                "note": p["data_practices"]["gdpr_compliance"],
                "deployer_responsibility": "high",
            },
            "nist_rmf": {
                "status": "aligned" if p["safety_score"] >= 7 else "partial",
                "note": f"Safety framework ({p['safety_framework']['name']}) provides NIST AI RMF alignment",
                "deployer_responsibility": "medium",
            },
            "iso42001": {
                "status": "partial",
                "note": "No major LLM provider is ISO 42001 certified. Deployers must implement own AIMS.",
                "deployer_responsibility": "high",
            },
            "soc2": {
                "status": "certified" if "SOC 2 Type II" in p.get("compliance_certifications", []) else "not_certified",
                "note": f"Certifications: {', '.join(p['compliance_certifications']) or 'None'}",
                "deployer_responsibility": "medium" if "SOC 2 Type II" in p.get("compliance_certifications", []) else "high",
            },
            "aida": {
                "status": "pending",
                "note": "AIDA not yet enacted. Compliance assessment will depend on final regulation.",
                "deployer_responsibility": "high",
            },
        }

        return assessments.get(fw, {"status": "unknown", "note": "Framework not assessed"})

    matrix = {
        "matrix_type": "LLM Provider Compliance Matrix",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matrix": {},
    }

    for pid in target_providers:
        if pid not in LLM_PROVIDERS:
            continue
        p = LLM_PROVIDERS[pid]
        matrix["matrix"][pid] = {
            "provider": p["provider"],
            "model": p["current_model"],
            "frameworks": {},
        }
        for fw in target_frameworks:
            if fw in framework_info:
                assessment = _assess_compliance(pid, fw)
                matrix["matrix"][pid]["frameworks"][fw] = {
                    "framework": framework_info[fw]["name"],
                    **assessment,
                }

    matrix["key"] = {
        "statuses": {
            "certified": "Holds formal certification/compliance",
            "compliant": "Meets requirements based on published evidence",
            "aligned": "Substantially aligned but no formal certification",
            "high": "High readiness / strong alignment",
            "very_high": "Very high readiness",
            "moderate": "Moderate readiness — some gaps",
            "partial": "Partially meets requirements",
            "not_certified": "Does not hold certification",
            "pending": "Legislation/standard not yet applicable",
        },
        "deployer_responsibility": "Indicates how much compliance burden falls on the deploying organization vs the provider",
    }

    return matrix


# ---------------------------------------------------------------------------
# TOOL 5: Crosswalk Providers to CSOAI Articles
# ---------------------------------------------------------------------------
@mcp.tool()
def crosswalk_providers(
    providers: Optional[list[str]] = None,
    csoai_articles: Optional[list[str]] = None,
    caller: str = "anonymous",
    tier: str = "free", api_key: str = "") -> str:
    """Map LLM provider safety policies to CSOAI Partnership Charter articles.
    Shows how each provider's governance aligns with CSOAI's 52-article framework.

    Args:
        providers: Providers to map (default all 5)
        csoai_articles: Specific CSOAI articles to map (or all mapped articles if omitted)
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _check_rate_limit(caller, tier):
        return {"error": err}

    target_providers = providers or list(LLM_PROVIDERS.keys())
    target_articles = csoai_articles or list(CSOAI_PROVIDER_MAPPING.keys())

    mappings = []
    provider_scores = defaultdict(lambda: {"strong": 0, "moderate": 0, "weak": 0})

    for article in target_articles:
        if article not in CSOAI_PROVIDER_MAPPING:
            continue
        article_mapping = CSOAI_PROVIDER_MAPPING[article]

        provider_alignments = {}
        for pid in target_providers:
            if pid in article_mapping:
                alignment = article_mapping[pid]
                provider_alignments[pid] = alignment
                provider_scores[pid][alignment["alignment"]] += 1

        mappings.append({
            "csoai_article": article,
            "provider_alignments": provider_alignments,
        })

    # Calculate overall alignment per provider
    provider_summaries = {}
    for pid in target_providers:
        scores = provider_scores[pid]
        total = scores["strong"] + scores["moderate"] + scores["weak"]
        if total == 0:
            continue
        alignment_pct = ((scores["strong"] * 100 + scores["moderate"] * 60 + scores["weak"] * 20) / total)
        provider_summaries[pid] = {
            "provider": LLM_PROVIDERS[pid]["provider"] if pid in LLM_PROVIDERS else pid,
            "strong_alignments": scores["strong"],
            "moderate_alignments": scores["moderate"],
            "weak_alignments": scores["weak"],
            "overall_alignment_score": round(alignment_pct, 1),
        }

    # Rank by alignment
    ranked = sorted(provider_summaries.items(), key=lambda x: x[1]["overall_alignment_score"], reverse=True)

    result = {
        "crosswalk_type": "LLM Provider to CSOAI Partnership Charter Crosswalk",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "article_mappings": mappings,
        "provider_summaries": dict(ranked),
        "most_aligned_provider": ranked[0][0] if ranked else None,
        "recommendation": (
            "No single provider fully satisfies all CSOAI articles. "
            "Anthropic/Claude scores highest on care-based safety (Articles 1, 5) and provable safety (Article 2). "
            "Meta/Llama scores highest on transparency (Article 10) through open weights. "
            "Google/Gemini leads on environmental sustainability (Article 47). "
            "Organizations should evaluate against their specific CSOAI priority articles."
        ),
    }

    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()