"""
Clause extraction and analysis module
"""
import logging
import re
from typing import List, Tuple

from src.models.contract_models import Clause, ClauseCategory, RiskLevel
from src.core.risk_assessor import RiskAssessor
from src.core.llm_analysis import analyze_clause as llm_analyze

logger = logging.getLogger(__name__)


class ClauseExtractor:
    """Extract and analyze clauses from contract text"""

    @staticmethod
    def extract_clauses(text: str) -> List[Clause]:
        clauses = []

        clause_texts = ClauseExtractor._split_into_clauses(text)

        for idx, (clause_text, start_pos, end_pos) in enumerate(clause_texts):
            clause_id = f"clause_{idx + 1}"

            # ---------- SAFE DEFAULTS (CRITICAL) ----------
            category = ClauseCategory.OTHER
            risk_level = None
            explanation = None
            alternative = None

            # ---------- LLM ANALYSIS ----------
            try:
                llm_result = llm_analyze(clause_text)

                if isinstance(llm_result, dict):

                    # category
                    t = llm_result.get("type") or llm_result.get("category")
                    if isinstance(t, str):
                        t_norm = t.strip().lower()
                        if t_norm in [c.value for c in ClauseCategory]:
                            category = ClauseCategory(t_norm)

                    # risk
                    r = llm_result.get("risk")
                    if isinstance(r, str):
                        r_norm = r.strip().lower()
                        if r_norm in [x.value for x in RiskLevel]:
                            risk_level = RiskLevel(r_norm)

                    explanation = llm_result.get("explanation")
                    alternative = llm_result.get("suggestion")

            except Exception as e:
                logger.debug("LLM failed for %s: %s", clause_id, e)

            # ---------- HEURISTIC RISK ----------
            assessed_level, risk_score, reason = RiskAssessor.assess_clause_risk(
                clause_text, category
            )

            if risk_level is None:
                risk_level = assessed_level

            # ---------- TITLE ----------
            title = ClauseExtractor._extract_clause_title(clause_text)

            # ---------- EXPLANATION FALLBACK ----------
            if not explanation:
                explanation = ClauseExtractor._generate_explanation(
                    clause_text, category
                )

            # ---------- ALTERNATIVE FALLBACK ----------
            if not alternative:
                alternative = ClauseExtractor._suggest_alternative(
                    clause_text, risk_level
                )

            clause = Clause(
                clause_id=clause_id,
                title=title,
                text=clause_text,
                start_position=start_pos,
                end_position=end_pos,
                category=category,
                risk_level=risk_level,
                risk_score=risk_score,
                reason_for_risk=reason,
                plain_language_explanation=explanation,
                suggested_alternative=alternative,
            )

            clauses.append(clause)

        return clauses

    # =========================================================
    # FIXED CLAUSE SPLIT (major bug fixed here)
    # =========================================================
    @staticmethod
    def _split_into_clauses(text: str) -> List[Tuple[str, int, int]]:
        clauses = []

        clause_pattern = (
            r'(?:^|\n)\s*(?:Article|Section|Clause)?\s*'
            r'(\d+(?:\.\d+)*)\s*[.)]\s*(.+)'
        )

        matches = list(re.finditer(clause_pattern, text, re.MULTILINE))

        if not matches:
            return [(text, 0, len(text))]

        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i < len(matches) - 1 else len(text)

            clause_text = text[start:end].strip()
            if clause_text:
                clauses.append((clause_text, start, end))

        return clauses

    # =========================================================
    @staticmethod
    def _extract_clause_title(clause_text: str) -> str:
        first_line = clause_text.split("\n")[0]

        title = re.sub(r'^\s*\d+(?:\.\d+)*\s*[.)]\s*', '', first_line)
        title = title.strip()
        return title

    # =========================================================
    @staticmethod
    def _generate_explanation(clause_text: str, category: ClauseCategory) -> str:

        explanations = {
            ClauseCategory.OBLIGATION: "This clause describes what you are required to do.",
            ClauseCategory.RIGHT: "This clause describes your rights.",
            ClauseCategory.PROHIBITION: "This clause describes restrictions.",
            ClauseCategory.PENALTY: "This clause explains penalties for breach.",
            ClauseCategory.INDEMNITY: "This clause explains compensation responsibilities.",
            ClauseCategory.TERMINATION: "This clause explains how the contract ends.",
            ClauseCategory.ARBITRATION: "This clause explains dispute resolution.",
            ClauseCategory.CONFIDENTIALITY: "This clause protects confidential information.",
            ClauseCategory.IP_OWNERSHIP: "This clause explains intellectual property ownership.",
            ClauseCategory.OTHER: "This clause contains important legal terms.",
        }

        base = explanations.get(category, explanations[ClauseCategory.OTHER])

        amounts = re.findall(r'(?:₹|Rs\.?|\$)\s*\d+(?:,\d+)*', clause_text)
        if amounts:
            base += f" Monetary amount mentioned: {amounts[0]}."

        return base

    # =========================================================
    @staticmethod
    def _suggest_alternative(clause_text: str, risk_level: RiskLevel):

        if risk_level != RiskLevel.HIGH:
            return None

        text = clause_text.lower()

        if "unlimited liability" in text:
            return "Limit liability to fees paid in last 12 months."

        if "terminate" in text and "without cause" in text:
            return "Add notice period and compensation terms."

        if "non-compete" in text or "non compete" in text:
            return "Reduce scope, geography, and duration."

        return None
