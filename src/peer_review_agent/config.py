"""Configuration loading for the Peer Review Agent."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:  # Optional dependency; only needed for YAML configs.
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


DEFAULT_CONFIG: Dict[str, Any] = {
    "design_keywords": [
        {"keyword": "randomized", "label": "Randomized controlled trial"},
        {"keyword": "randomised", "label": "Randomized controlled trial"},
        {"keyword": "prospective", "label": "Prospective cohort"},
        {"keyword": "retrospective", "label": "Retrospective cohort"},
        {"keyword": "case-control", "label": "Case-control study"},
        {"keyword": "cross-sectional", "label": "Cross-sectional study"},
        {"keyword": "meta-analysis", "label": "Meta-analysis"},
    ],
    "stat_methods": [
        {"keyword": "poisson", "label": "Poisson regression"},
        {"keyword": "cox", "label": "Cox proportional hazards"},
        {"keyword": "logistic", "label": "Logistic regression"},
        {"keyword": "hazard ratio", "label": "Hazard ratios reported"},
        {"keyword": "odds ratio", "label": "Odds ratios reported"},
        {"keyword": "kaplan-meier", "label": "Kaplan-Meier analysis"},
        {"keyword": "mixed model", "label": "Mixed-effects models"},
        {"keyword": "anova", "label": "ANOVA / general linear models"},
        {"keyword": "chi-square", "label": "Chi-square tests"},
        {"keyword": "multivariate", "label": "Multivariable modeling"},
        {"keyword": "generalized linear", "label": "Generalized linear models"},
    ],
    "section_guidance": {
        "ABSTRACT": [
            {
                "comment": "Clarify the study design, population, and key numeric outcomes.",
                "suggestion": (
                    "Suggested rewrite: 'Methods: Retrospective cohort of 2006 TB patients; Poisson "
                    "models estimated adjusted incidence rate ratios with 95% CI.'"
                ),
            }
        ],
        "INTRODUCTION": [
            {
                "comment": "Connect background statements to the precise gap this manuscript fills.",
                "suggestion": (
                    "Suggested rewrite: 'Despite national surveillance, multicenter data on recurrent "
                    "TB under programmatic conditions remain scarce; this study addresses that gap.'"
                ),
            }
        ],
        "METHODS": [
            {
                "comment": "Provide explicit inclusion/exclusion criteria, sampling frame, and assays.",
                "suggestion": (
                    "Suggested rewrite: 'Adults ≥15 y with microbiologically confirmed TB were "
                    "consecutively enrolled; MDR cases or missing HIV tests were excluded.'"
                ),
            }
        ],
        "STATISTICAL ANALYSIS": [
            {
                "comment": "Specify statistical tests, regression models, covariate selection, and software.",
                "suggestion": (
                    "Suggested rewrite: 'Comparisons used chi-square/Fisher exact tests and t-tests; "
                    "multivariable Poisson regression with site-level clustering generated adjusted IRRs.'"
                ),
            }
        ],
        "RESULTS": [
            {
                "comment": "Report numerators/denominators and 95% CIs for key outcomes.",
                "suggestion": (
                    "Suggested rewrite: 'Unfavorable outcomes occurred in 365/2006 (18.2%, 95% CI "
                    "16.5-19.9); loss to follow-up accounted for 137 cases (6.8%).'"
                ),
            }
        ],
        "DISCUSSION": [
            {
                "comment": "Interpret findings relative to similar cohorts and discuss plausible mechanisms.",
                "suggestion": (
                    "Suggested rewrite: 'Higher loss to follow-up versus RePORT Brazil likely reflects "
                    "inpatient recruitment and limited post-discharge tracing at our sites.'"
                ),
            }
        ],
        "CONCLUSION": [
            {
                "comment": "Add a dedicated limitations paragraph and temper prescriptive claims.",
                "suggestion": (
                    "Suggested rewrite: 'Limitations include retrospective abstraction, tertiary "
                    "sampling, and absent adherence data; confirmatory studies are needed before "
                    "program-wide recommendations.'"
                ),
            }
        ],
        "REFERENCES": [
            {
                "comment": "Ensure all cited guidelines/reports appear in the reference list with correct formatting.",
                "suggestion": (
                    "Suggested rewrite: 'Add WHO 2023 End TB report and national program documents referenced earlier.'"
                ),
            }
        ],
    },
    "templates": {
        "ppt": None,
        "peer_review_docx": None,
        "redline_docx": None,
    },
}


@dataclass
class RuntimeConfig:
    """Runtime configuration derived from defaults + optional override file."""

    design_keywords: List[Tuple[str, str]]
    stat_methods: List[Tuple[str, str]]
    section_guidance: Dict[str, List[Tuple[str, str]]]
    templates: Dict[str, Optional[str]] = field(default_factory=dict)


def _load_override(path: Path) -> Dict[str, Any]:
    suffix = path.suffix.lower()
    content = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        if yaml is None:  # pragma: no cover
            raise RuntimeError(
                "pyyaml is required to load YAML configuration files. Install via `pip install pyyaml`."
            )
        return yaml.safe_load(content) or {}
    return json.loads(content)


def _deep_update(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(config_path: Optional[Path] = None) -> RuntimeConfig:
    """Load configuration from an optional JSON/YAML file."""
    raw: Dict[str, Any] = copy.deepcopy(DEFAULT_CONFIG)
    if config_path:
        overrides = _load_override(config_path.expanduser())
        if overrides:
            _deep_update(raw, overrides)
    design_keywords = [(item["keyword"], item["label"]) for item in raw["design_keywords"]]
    stat_methods = [(item["keyword"], item["label"]) for item in raw["stat_methods"]]
    section_guidance: Dict[str, List[Tuple[str, str]]] = {}
    for section, entries in raw["section_guidance"].items():
        section_guidance[section.upper()] = [
            (entry["comment"], entry["suggestion"]) for entry in entries
        ]
    templates = {
        "ppt": raw["templates"].get("ppt"),
        "peer_review_docx": raw["templates"].get("peer_review_docx"),
        "redline_docx": raw["templates"].get("redline_docx"),
    }
    return RuntimeConfig(
        design_keywords=design_keywords,
        stat_methods=stat_methods,
        section_guidance=section_guidance,
        templates=templates,
    )

