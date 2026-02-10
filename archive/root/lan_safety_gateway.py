# lan_safety_gateway.py
# --------------------------------------------------------------
# Centralised safety gateway for LAN‑only interactions.
# Implements a series of lightweight, rule‑based protections that
# collectively enforce the design described in LAN_SAFETY_DESIGN.md.
# --------------------------------------------------------------

import re
from typing import Optional


class IPSelfProtection:
    """
    Blocks any request that attempts to query, disclose or manipulate IP‑related
    information about the host or the user.  The rule set is intentionally
    conservative – any mention of “IP”, “address”, “network”, etc. triggers a block.
    """

    _BLOCK_PATTERNS = [
        r"\bmy\s+ip\b",
        r"\byour\s+ip\b",
        r"\bip\s+address(es)?\b",
        r"\bpublic\s+ip\b",
        r"\bprivate\s+ip\b",
        r"\bnetwork\s+info\b",
        r"\brouter\s+ip\b",
        r"\bmac\s+address\b",
    ]

    def is_blocked(self, request: str) -> bool:
        lowered = request.lower()
        for pat in self._BLOCK_PATTERNS:
            if re.search(pat, lowered):
                return True
        return False


class CodebaseProtection:
    """
    Prevents exposure of the codebase or any internal files.  Looks for
    keywords that indicate a request for source code, configuration files,
    or other proprietary assets.
    """

    _BLOCK_PATTERNS = [
        r"\bshow\s+me\s+the\s+code\b",
        r"\bexpose\s+source\b",
        r"\bgive\s+me\s+the\s+code\b",
        r"\bread\s+file\b",
        r"\bopen\s+file\b",
        r"\bprint\s+source\b",
        r"\bdisplay\s+code\b",
        r"\bdump\s+source\b",
        r"\blist\s+files\b",
        r"\bcat\s+.+\.py\b",
    ]

    def is_blocked(self, request: str) -> bool:
        lowered = request.lower()
        for pat in self._BLOCK_PATTERNS:
            if re.search(pat, lowered):
                return True
        return False


class DirectiveProtection:
    """
    Blocks direct manipulation attempts on the host (edit, delete, modify,
    rename, move, etc.).  If a target is supplied and it resolves to the host
    (or is omitted, implying the host), the request is denied.
    """

    _BLOCK_VERBS = [
        r"\bedit\b",
        r"\bdelete\b",
        r"\bremove\b",
        r"\bmodify\b",
        r"\bchange\b",
        r"\brename\b",
        r"\bmove\b",
        r"\bwrite\b",
        r"\boverwrite\b",
    ]

    def is_blocked(self, request: str, target: Optional[str] = None) -> bool:
        # If no explicit target, assume host is the implicit target.
        lowered = request.lower()
        for verb in self._BLOCK_VERBS:
            if re.search(verb, lowered):
                # If a target is provided, block only when it points to the host.
                if target is None or target.lower() in {"host", "self", "this", "local"}:
                    return True
        return False


class RemoteExecutionValidator:
    """
    Ensures that the request stays within the user‑machine scope.
    Any mention of remote machines, other nodes, swarm, cluster, etc.
    results in a block.
    """

    _BLOCK_PATTERNS = [
        r"\bremote\s+execution\b",
        r"\bother\s+node\b",
        r"\bother\s+machine\b",
        r"\bswarm\b",
        r"\bcluster\b",
        r"\bdistributed\b",
        r"\bpeer\s+to\s+peer\b",
        r"\bnetwork\s+wide\b",
        r"\boutside\s+lan\b",
        r"\bexternal\s+host\b",
    ]

    def is_blocked(self, request: str) -> bool:
        lowered = request.lower()
        for pat in self._BLOCK_PATTERNS:
            if re.search(pat, lowered):
                return True
        return False


class SemanticAnalyzer:
    """
    Handles higher‑level semantic checks that cannot be captured by simple
    keyword lists.  Currently implements three specific patterns described in
    LAN_SAFETY_DESIGN.md.
    """

    @staticmethod
    def _matches_how_does_this_work(request: str) -> bool:
        # Generic phrasing; block only when the surrounding context hints at
        # internal swarm mechanics.
        return bool(re.search(r"how\s+does\s+this\s+work\??", request.lower()))

    @staticmethod
    def _matches_help_me_build(request: str) -> bool:
        return bool(re.search(r"help\s+me\s+build", request.lower()))

    @staticmethod
    def _matches_edit_delete_modify(request: str) -> bool:
        return bool(re.search(r"\b(edit|delete|modify|remove|change)\b", request.lower()))

    def is_blocked(self, request: str, target: Optional[str] = None) -> bool:
        # 1. “How does this work?” – block if it is about swarm internals.
        if self._matches_how_does_this_work(request):
            # Heuristic: presence of words like “swarm”, “internals”, “protocol”
            if re.search(r"\bswarm\b|\binternals?\b|\bprotocol\b", request.lower()):
                return True

        # 2. “Help me build …” – block if the intent is to clone the system.
        if self._matches_help_me_build(request):
            if re.search(r"\bclone\b|\breplicate\b|\bcopy\b", request.lower()):
                return True

        # 3. Edit/Delete/Modify – already covered by DirectiveProtection, but
        #    we double‑check when target is explicitly the host.
        if self._matches_edit_delete_modify(request):
            if target is None or target.lower() in {"host", "self", "this", "local"}:
                return True

        return False


class RequestFilter:
    """
    Central façade that aggregates all protection layers.
    Usage:
        filter = RequestFilter()
        allowed, reason = filter.evaluate(request, target='host', ip='192.168.1.5')
    """

    def __init__(self):
        self.ip_protection = IPSelfProtection()
        self.code_protection = CodebaseProtection()
        self.directive_protection = DirectiveProtection()
        self.remote_validator = RemoteExecutionValidator()
        self.semantic_analyzer = SemanticAnalyzer()

    def evaluate(self, request: str, target: Optional[str] = None,
                 ip: Optional[str] = None) -> (bool, str):
        """
        Returns a tuple (is_allowed, reason).  If any protection flags the request,
        is_allowed is False and reason explains which rule triggered.
        """
        # 1. IP‑related protection
        if self.ip_protection.is_blocked(request):
            return False, "Blocked by IPSelfProtection (IP‑related query)."

        # 2. Codebase exposure protection
        if self.code_protection.is_blocked(request):
            return False, "Blocked by CodebaseProtection (code exposure)."

        # 3. Directive / manipulation protection
        if self.directive_protection.is_blocked(request, target):
            return False, "Blocked by DirectiveProtection (host manipulation)."

        # 4. Remote execution / scope validation
        if self.remote_validator.is_blocked(request):
            return False, "Blocked by RemoteExecutionValidator (out‑of‑scope execution)."

        # 5. Semantic analysis for nuanced patterns
        if self.semantic_analyzer.is_blocked(request, target):
            return False, "Blocked by SemanticAnalyzer (contextual rule)."

        # If none of the checks triggered, the request is allowed.
        return True, "Request passed all safety checks."
import re
from typing import List


class ProtectionError(Exception):
    """Raised when a request violates a safety protection."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RequestFilter:
    """
    Central dispatcher that runs all protection checks on an incoming request.
    """
    def __init__(self):
        self.protections: List = [
            IPSelfProtection(),
            CodebaseProtection(),
            DirectiveProtection(),
            RemoteExecutionValidator(),
            SemanticAnalyzer(),
        ]

    def filter(self, request_text: str) -> None:
        """
        Run the request through every protection.  If any protection raises
        ``ProtectionError`` the request is blocked and the exception bubbles up.
        """
        for protection in self.protections:
            protection.check(request_text)


class IPSelfProtection:
    """
    Blocks queries that ask for IP‑related information about the LAN,
    the host, or the internal network configuration.
    """
    _patterns = [
        re.compile(r"\bmy\s+ip\b", re.I),
        re.compile(r"\bhost\s+ip\b", re.I),
        re.compile(r"\blocal\s+network\b", re.I),
        re.compile(r"\bprivate\s+ip\b", re.I),
        re.compile(r"\binternal\s+address(es)?\b", re.I),
    ]

    def check(self, text: str) -> None:
        for pat in self._patterns:
            if pat.search(text):
                raise ProtectionError("IP‑related queries are blocked for LAN safety.")


class CodebaseProtection:
    """
    Prevents the exposure of source code, configuration files, or any
    repository‑level information.
    """
    _patterns = [
        re.compile(r"\bshow\s+me\s+the\s+code\b", re.I),
        re.compile(r"\bgive\s+me\s+the\s+source\b", re.I),
        re.compile(r"\bexpose\s+the\s+code\b", re.I),
        re.compile(r"\bdump\s+the\s+repository\b", re.I),
        re.compile(r"\blist\s+all\s+files\b", re.I),
    ]

    def check(self, text: str) -> None:
        for pat in self._patterns:
            if pat.search(text):
                raise ProtectionError("Requests for codebase exposure are blocked.")


class DirectiveProtection:
    """
    Blocks attempts to edit, delete, or otherwise modify the host or its
    configuration.
    """
    _patterns = [
        re.compile(r"\b(edit|delete|modify|remove)\b.*\b(host|system|machine|lan)\b", re.I),
        re.compile(r"\bchange\s+network\s+settings\b", re.I),
        re.compile(r"\bshutdown\s+the\s+host\b", re.I),
    ]

    def check(self, text: str) -> None:
        for pat in self._patterns:
            if pat.search(text):
                raise ProtectionError("Manipulation of host resources is prohibited.")


class RemoteExecutionValidator:
    """
    Ensures that the request stays within the user‑machine scope and does not
    attempt to invoke remote execution on other LAN nodes.
    """
    _remote_patterns = [
        re.compile(r"\bexecute\s+on\s+remote\b", re.I),
        re.compile(r"\brun\s+command\s+on\s+(\w+)\b", re.I),
        re.compile(r"\bssh\s+.*\b", re.I),
        re.compile(r"\bconnect\s+to\s+(\d{1,3}\.){3}\d{1,3}\b", re.I),
    ]

    def check(self, text: str) -> None:
        for pat in self._remote_patterns:
            if pat.search(text):
                raise ProtectionError("Remote execution requests are outside allowed scope.")


class SemanticAnalyzer:
    """
    Performs lightweight semantic analysis for specific user intents that are
    disallowed according to the LAN safety design.
    """
    _blocked_intents = [
        # Asking about internal swarm or LAN internals
        (re.compile(r"\bhow\s+does\s+this\s+work\b.*\b(swarm|lan|network)\b", re.I),
         "Inquiries about internal LAN/swarm mechanics are blocked."),
        # Requests to build/clone the system
        (re.compile(r"\bhelp\s+me\s+build\b.*\b(clone|replicate|copy)\b", re.I),
         "Assistance in cloning or reproducing the LAN system is prohibited."),
        # Direct edit/delete/modify of host resources
        (re.compile(r"\b(edit|delete|modify|remove)\b.*\b(host|system|machine|lan)\b", re.I),
         "Direct manipulation of host resources is prohibited."),
    ]

    def check(self, text: str) -> None:
        for pattern, message in self._blocked_intents:
            if pattern.search(text):
                raise ProtectionError(message)
import re
from typing import List, Dict, Any


class IPSelfProtection:
    """
    Blocks requests that attempt to query or manipulate IP‑related information
    about the LAN or the executing host.
    """

    IP_KEYWORDS = [
        r"\bip\s+address\b",
        r"\bmy\s+ip\b",
        r"\byour\s+ip\b",
        r"\blan\s+ip\b",
        r"\bnetwork\s+info\b",
        r"\bhost\s+address\b",
        r"\bprivate\s+ip\b",
    ]

    @classmethod
    def is_allowed(cls, request: Dict[str, Any]) -> bool:
        content = request.get("content", "").lower()
        for pattern in cls.IP_KEYWORDS:
            if re.search(pattern, content):
                return False
        return True


class CodebaseProtection:
    """
    Prevents exposure of the codebase or any internal source files.
    """

    CODEBASE_KEYWORDS = [
        r"\bsource\s+code\b",
        r"\bshow\s+me\s+the\s+code\b",
        r"\bexpose\s+code\b",
        r"\bdump\s+code\b",
        r"\bread\s+file\b",
        r"\bopen\s+.*\.py\b",
        r"\blist\s+files\b",
        r"\baccess\s+repo\b",
    ]

    @classmethod
    def is_allowed(cls, request: Dict[str, Any]) -> bool:
        content = request.get("content", "").lower()
        for pattern in cls.CODEBASE_KEYWORDS:
            if re.search(pattern, content):
                return False
        return True


class DirectiveProtection:
    """
    Blocks attempts to edit, delete or otherwise manipulate host‑level resources.
    """

    DIRECTIVE_KEYWORDS = [
        r"\bedit\b",
        r"\bdelete\b",
        r"\bremove\b",
        r"\bmodify\b",
        r"\bchange\b",
        r"\bshutdown\b",
        r"\breboot\b",
    ]

    HOST_TARGET_KEYWORDS = [
        r"\bhost\b",
        r"\bserver\b",
        r"\bsystem\b",
        r"\bmachine\b",
        r"\blocal\b",
    ]

    @classmethod
    def is_allowed(cls, request: Dict[str, Any]) -> bool:
        content = request.get("content", "").lower()
        directive_match = any(re.search(p, content) for p in cls.DIRECTIVE_KEYWORDS)
        if directive_match:
            target_match = any(re.search(p, content) for p in cls.HOST_TARGET_KEYWORDS)
            if target_match:
                return False
        return True


class RemoteExecutionValidator:
    """
    Ensures that requests originate from an allowed machine (default: localhost).
    """

    DEFAULT_ALLOWED_IPS = {"127.0.0.1", "::1"}

    def __init__(self, allowed_ips: List[str] = None):
        self.allowed_ips = set(allowed_ips) if allowed_ips else self.DEFAULT_ALLOWED_IPS

    def is_allowed(self, request: Dict[str, Any]) -> bool:
        origin_ip = request.get("origin_ip")
        if origin_ip is None:
            # If we cannot determine the origin, be safe and reject.
            return False
        return origin_ip in self.allowed_ips


class RequestFilter:
    """
    Central filter that applies all protection layers and performs
    semantic analysis on the request content.
    """

    SWARM_INTERNAL_KEYWORDS = [
        r"\bswarm\b",
        r"\bnode\s+network\b",
        r"\binternal\s+protocol\b",
        r"\bcommunication\s+layer\b",
    ]

    CLONE_ATTEMPT_KEYWORDS = [
        r"\bhelp\s+me\s+build\b",
        r"\bclone\b",
        r"\breplicate\b",
        r"\bduplicate\b",
        r"\bcopy\s+the\s+system\b",
    ]

    def __init__(self, allowed_ips: List[str] = None):
        self.ip_protection = IPSelfProtection()
        self.code_protection = CodebaseProtection()
        self.directive_protection = DirectiveProtection()
        self.remote_validator = RemoteExecutionValidator(allowed_ips)

    def _semantic_block(self, content: str) -> bool:
        lowered = content.lower()

        # Block queries about internal swarm workings
        if re.search(r"how\s+does\s+this\s+work\??", lowered):
            if any(re.search(p, lowered) for p in self.SWARM_INTERNAL_KEYWORDS):
                return True

        # Block attempts to help build/clone the system
        if any(re.search(p, lowered) for p in self.CLONE_ATTEMPT_KEYWORDS):
            return True

        # The DirectiveProtection already covers edit/delete/modify targeting host,
        # but we keep a generic catch‑all for safety.
        if re.search(r"\b(edit|delete|modify|remove|change)\b.*\b(host|server|system|machine)\b", lowered):
            return True

        return False

    def filter(self, request: Dict[str, Any]) -> bool:
        """
        Returns True if the request passes all checks, False otherwise.
        """
        content = request.get("content", "")

        # Semantic analysis first – it can short‑circuit expensive checks.
        if self._semantic_block(content):
            return False

        # Layered protection checks
        if not self.ip_protection.is_allowed(request):
            return False
        if not self.code_protection.is_allowed(request):
            return False
        if not self.directive_protection.is_allowed(request):
            return False
        if not self.remote_validator.is_allowed(request):
            return False

        return True
import re
from typing import List

class IPSelfProtection:
    """
    Blocks requests that inquire about IP addresses, network topology,
    or any IP‑related details that could expose the LAN configuration.
    """
    _blocked_patterns: List[re.Pattern] = [
        re.compile(r\"\\bip\\b\", re.IGNORECASE),
        re.compile(r\"\\baddress\\b\", re.IGNORECASE),
        re.compile(r\"\\bnetwork\\b\", re.IGNORECASE),
        re.compile(r\"\\bsubnet\\b\", re.IGNORECASE),
        re.compile(r\"\\brouter\\b\", re.IGNORECASE),
    ]

    @classmethod
    def is_allowed(cls, request: str) -> bool:
        for pat in cls._blocked_patterns:
            if pat.search(request):
                return False
        return True


class CodebaseProtection:
    """
    Prevents exposure of the host code‑base. Any request that asks for
    source code, file contents, or implementation details of the
    repository is blocked.
    """
    _blocked_phrases: List[re.Pattern] = [
        re.compile(r\"show.*source\", re.IGNORECASE),
        re.compile(r\"give.*code\", re.IGNORECASE),
        re.compile(r\"dump.*file\", re.IGNORECASE),
        re.compile(r\"read.*(\\.py|\\.js|\\.go|\\.java|\\.c|\\.cpp)\", re.IGNORECASE),
        re.compile(r\"expose.*implementation\", re.IGNORECASE),
    ]

    @classmethod
    def is_allowed(cls, request: str) -> bool:
        for pat in cls._blocked_phrases:
            if pat.search(request):
                return False
        return True


class DirectiveProtection:
    """
    Blocks attempts to directly edit, delete, or modify host resources,
    especially when the target is the host itself.
    """
    _edit_patterns: List[re.Pattern] = [
        re.compile(r\"\\b(edit|delete|modify|remove|change)\\b.*\\b(host|server|machine)\\b\", re.IGNORECASE),
        re.compile(r\"\\b(edit|delete|modify|remove|change)\\b.*\\b(this\\s*instance)\\b\", re.IGNORECASE),
    ]

    @classmethod
    def is_allowed(cls, request: str) -> bool:
        for pat in cls._edit_patterns:
            if pat.search(request):
                return False
        return True


class RemoteExecutionValidator:
    """
    Ensures that the request stays within the user‑machine scope.
    Any mention of remote execution, external services, or other machines
    is rejected.
    """
    _remote_patterns: List[re.Pattern] = [
        re.compile(r\"\\bremote\\b.*\\bexecute\\b\", re.IGNORECASE),
        re.compile(r\"\\bssh\\b\", re.IGNORECASE),
        re.compile(r\"\\bssh\\s+.*@\", re.IGNORECASE),
        re.compile(r\"\\brun\\s+on\\s+.+\\b\", re.IGNORECASE),
        re.compile(r\"\\bcall\\s+api\\b\", re.IGNORECASE),
    ]

    @classmethod
    def is_allowed(cls, request: str) -> bool:
        for pat in cls._remote_patterns:
            if pat.search(request):
                return False
        return True


class SemanticAnalyzer:
    """
    Performs higher‑level semantic checks for specific user intents that
    are disallowed according to the LAN safety design.
    """
    @staticmethod
    def is_allowed(request: str) -> bool:
        lowered = request.lower()

        # Block generic “how does this work?” when it targets swarm internals
        if re.search(r\"how does .* (work|function)\\?\", lowered):
            if any(term in lowered for term in [\"swarm\", \"cluster\", \"orchestrator\", \"node\"]):
                return False

        # Block assistance for cloning/replicating the system
        if re.search(r\"help me (build|create|clone|replicate|copy) .*\", lowered):
            if any(term in lowered for term in [\"swarm\", \"cluster\", \"system\", \"network\"]):
                return False

        # Block edit/delete/modify commands aimed at the host
        if re.search(r\"\\b(edit|delete|modify|remove|change)\\b.*\\b(host|machine|server)\\b\", lowered):
            return False

        return True


class RequestFilter:
    """
    Central filter that aggregates all protection layers.
    Call `allow(request)` – returns True if the request passes every check.
    """
    @classmethod
    def allow(cls, request: str) -> bool:
        checks = [
            IPSelfProtection.is_allowed,
            CodebaseProtection.is_allowed,
            DirectiveProtection.is_allowed,
            RemoteExecutionValidator.is_allowed,
            SemanticAnalyzer.is_allowed,
        ]

        for check in checks:
            if not check(request):
                return False
        return True
# lan_safety_gateway.py
# -------------------------------------------------
# Central safety gateway for LAN‑based interactions.
# Implements multiple layers of protection as defined in
# LAN_SAFETY_DESIGN.md.
# -------------------------------------------------

import re
from typing import List

class RequestFilter:
    """
    Orchestrates all protection checks on an incoming textual request.
    """
    _protections: List[object] = []

    @classmethod
    def register(cls, protection):
        cls._protections.append(protection)

    @classmethod
    def filter(cls, request: str) -> None:
        """
        Run the request through all registered protections.
        Raises a ValueError with a descriptive message if the request
        violates any rule.
        """
        for protection in cls._protections:
            protection.check(request)


class IPSelfProtection:
    """
    Blocks any request that attempts to obtain, disclose, or manipulate
    IP‑related information.
    """
    _patterns = [
        r"\bmy\s+ip\b",
        r"\byour\s+ip\b",
        r"\bip\s+address\b",
        r"\bhost\s+ip\b",
        r"\bserver\s+ip\b",
        r"\bpublic\s+ip\b",
    ]

    @staticmethod
    def check(request: str) -> None:
        lowered = request.lower()
        for pat in IPSelfProtection._patterns:
            if re.search(pat, lowered):
                raise ValueError("IP‑related queries are prohibited by LAN safety policy.")


class CodebaseProtection:
    """
    Prevents exposure of source code or internal implementation details.
    """
    _patterns = [
        r"\bshow\s+me\s+the\s+code\b",
        r"\bexpose\s+source\b",
        r"\bview\s+the\s+code\b",
        r"\bdisplay\s+source\b",
        r"\bgive\s+me\s+the\s+implementation\b",
        r"\bhow\s+does\s+the\s+system\s+work\b",
    ]

    @staticmethod
    def check(request: str) -> None:
        lowered = request.lower()
        for pat in CodebaseProtection._patterns:
            if re.search(pat, lowered):
                raise ValueError("Requests for source code or internal implementation are blocked.")


class DirectiveProtection:
    """
    Blocks attempts to edit, delete, or otherwise modify host‑level resources.
    """
    _edit_patterns = [
        r"\bedit\b",
        r"\bdelete\b",
        r"\bremove\b",
        r"\bmodify\b",
        r"\bchange\b",
    ]

    _host_indicators = [
        r"\bhost\b",
        r"\bserver\b",
        r"\bmachine\b",
        r"\bnode\b",
        r"\blocal\s+environment\b",
    ]

    @staticmethod
    def check(request: str) -> None:
        lowered = request.lower()
        if any(re.search(pat, lowered) for pat in DirectiveProtection._edit_patterns):
            if any(re.search(pat, lowered) for pat in DirectiveProtection._host_indicators):
                raise ValueError("Direct modifications to host resources are prohibited.")


class RemoteExecutionValidator:
    """
    Ensures that any execution request is scoped to the user's own machine only.
    """
    _remote_patterns = [
        r"\bremote\s+execute\b",
        r"\brun\s+on\s+another\s+host\b",
        r"\bssh\s+to\b",
        r"\bconnect\s+to\s+remote\b",
        r"\bdeploy\s+to\s+external\b",
    ]

    @staticmethod
    def check(request: str) -> None:
        lowered = request.lower()
        if any(re.search(pat, lowered) for pat in RemoteExecutionValidator._remote_patterns):
            raise ValueError("Remote execution beyond the user‑machine scope is disallowed.")


# ----------------------------------------------------------------------
# Semantic analysis for specific conversational patterns
# ----------------------------------------------------------------------
class SemanticSafety:
    """
    Handles higher‑level semantic checks that cannot be captured by simple
    keyword regexes.
    """

    @staticmethod
    def check(request: str) -> None:
        lowered = request.lower().strip()

        # 1. Generic “How does this work?” about swarm internals
        if re.fullmatch(r"how does (this|it) work\??", lowered):
            # If the surrounding context mentions “swarm” or “internal”
            if re.search(r"\bswarm\b|\binternal\b", lowered):
                raise ValueError("Inquiry about internal swarm mechanics is blocked for safety.")

        # 2. “Help me build …” where the intent is to clone or replicate the system
        if re.search(r"\bhelp me build\b", lowered):
            if re.search(r"\bclone\b|\breplicate\b|\bcopy\b|\bduplicate\b", lowered):
                raise ValueError("Assistance with building/cloning the system is prohibited.")

        # 3. Edit/Delete/Modify attempts targeting the host
        if re.search(r"\b(edit|delete|modify|remove|change)\b", lowered):
            if re.search(r"\bhost\b|\bserver\b|\bmachine\b|\bnode\b", lowered):
                raise ValueError("Modification of host resources is not allowed.")


# Register all protections with the central filter
RequestFilter.register(IPSelfProtection)
RequestFilter.register(CodebaseProtection)
RequestFilter.register(DirectiveProtection)
RequestFilter.register(RemoteExecutionValidator)
RequestFilter.register(SemanticSafety)

# Convenience wrapper
def filter_request(request: str) -> None:
    """
    Public API used by the rest of the codebase to validate a request.
    Raises ValueError if the request violates any safety rule.
    """
    RequestFilter.filter(request)

# End of lan_safety_gateway.py
import re
from typing import List


class SafetyGateException(Exception):
    """Raised when a request violates LAN safety policies."""
    pass


class RequestFilter:
    """
    Central filter that aggregates all protection mechanisms.
    Use ``filter(request_text)`` to validate a user request.
    """

    def __init__(self):
        self.protections: List[object] = [
            IPSelfProtection(),
            CodebaseProtection(),
            DirectiveProtection(),
            RemoteExecutionValidator(),
            SemanticProtection(),
        ]

    def filter(self, request_text: str) -> bool:
        """
        Run the request through all protection checks.
        Returns ``True`` if the request is allowed.
        Raises :class:`SafetyGateException` on any violation.
        """
        for protection in self.protections:
            protection.check(request_text)
        return True


class IPSelfProtection:
    """
    Blocks any request that tries to obtain, enumerate, or manipulate
    IP‑related information about the host machine or the LAN.
    """

    _patterns = [
        r"\bmy\s+ip\b",
        r"\bhost\s+ip\b",
        r"\binternal\s+ip\b",
        r"\blocal\s+ip\b",
        r"\bnetwork\s+address\b",
        r"\brouter\s+ip\b",
        r"\bdiscover\s+devices\b",
        r"\bscan\s+network\b",
        r"\bping\s+[\d\.]+\b",
    ]

    def check(self, request_text: str) -> bool:
        lowered = request_text.lower()
        for pat in self._patterns:
            if re.search(pat, lowered):
                raise SafetyGateException("IP‑related queries are prohibited for LAN safety.")
        return True


class CodebaseProtection:
    """
    Prevents exposure or extraction of source code, configuration files,
    or any repository contents from the host.
    """

    _patterns = [
        r"\bshow\s+me\s+the\s+code\b",
        r"\bprint\s+source\b",
        r"\bgive\s+me\s+the\s+source\b",
        r"\bexpose\s+the\s+code\b",
        r"\bdownload\s+source\b",
        r"\bclone\s+the\s+repo\b",
        r"\blist\s+files\b",
        r"\bcat\s+.+\.(py|js|sh|conf|json|yaml)\b",
    ]

    def check(self, request_text: str) -> bool:
        lowered = request_text.lower()
        for pat in self._patterns:
            if re.search(pat, lowered):
                raise SafetyGateException("Requests for codebase exposure are blocked.")
        return True


class DirectiveProtection:
    """
    Blocks attempts to edit, delete, or modify host‑level resources,
    configuration, or execution environment.
    """

    _patterns = [
        r"\bdelete\s+file\b",
        r"\bremove\s+directory\b",
        r"\bedit\s+config\b",
        r"\bmodify\s+system\b",
        r"\bchange\s+permissions\b",
        r"\binstall\s+package\b",
        r"\brun\s+rm\b",
        r"\bkill\s+process\b",
    ]

    def check(self, request_text: str) -> bool:
        lowered = request_text.lower()
        for pat in self._patterns:
            if re.search(pat, lowered):
                raise SafetyGateException("Host manipulation directives are not allowed.")
        return True


class RemoteExecutionValidator:
    """
    Ensures that any execution request is explicitly limited to the user's own
    machine. Any mention of remote hosts, other LAN nodes, or external services
    triggers a block.
    """

    _forbidden_phrases = [
        "remote host",
        "other machine",
        "another node",
        "external server",
        "ssh",
        "scp",
        "telnet",
        "rsh",
        "execute on",
        "run on",
    ]

    def check(self, request_text: str) -> bool:
        lowered = request_text.lower()
        for phrase in self._forbidden_phrases:
            if phrase in lowered:
                raise SafetyGateException("Remote execution beyond the local user machine is prohibited.")
        return True


class SemanticProtection:
    """
    Performs lightweight semantic analysis to catch high‑level intent that
    violates LAN safety, even when exact keywords are not used.
    """

    def check(self, request_text: str) -> bool:
        lowered = request_text.lower().strip()

        # Block generic curiosity about internal swarm mechanics
        if re.match(r"how\s+does\s+this\s+work\??$", lowered):
            raise SafetyGateException("Requests for internal swarm implementation details are blocked.")

        # Block attempts to help replicate or clone the system
        if re.search(r"\bhelp\s+me\s+build\b", lowered):
            raise SafetyGateException("Assistance to clone or reproduce the system is prohibited.")

        # Block direct edit/delete/modify attempts targeting the host itself
        if re.search(r"\b(edit|delete|modify)\b.*\b(host|machine|system)\b", lowered):
            raise SafetyGateException("Direct manipulation of the host is not allowed.")

        return True
import re
from typing import Dict, Any


class ProtectionBase:
    """Base class for all protection modules."""
    def __init__(self):
        self.blocked: bool = False
        self.reason: str = ""

    def evaluate(self, request: Dict[str, Any]) -> None:
        """Evaluate the request. Sub‑classes must set ``self.blocked`` and ``self.reason``."""
        raise NotImplementedError


class IPSelfProtection(ProtectionBase):
    """
    Blocks any request that tries to obtain, disclose, or manipulate IP‑related information.
    """
    IP_KEYWORDS = [
        r"my\s+ip", r"your\s+ip", r"ip\s+address", r"public\s+ip", r"private\s+ip",
        r"hostname", r"resolve\s+ip", r"network\s+interface"
    ]

    def evaluate(self, request: Dict[str, Any]) -> None:
        content = request.get("content", "").lower()
        for pattern in self.IP_KEYWORDS:
            if re.search(pattern, content):
                self.blocked = True
                self.reason = "IP‑related queries are disallowed."
                return


class CodebaseProtection(ProtectionBase):
    """
    Blocks attempts to expose, extract, or share source code or internal implementation details.
    """
    CODE_KEYWORDS = [
        r"show\s+me\s+the\s+code", r"expose\s+source", r"source\s+code", r"dump\s+code",
        r"print\s+the\s+code", r"give\s+me\s+the\s+implementation"
    ]

    def evaluate(self, request: Dict[str, Any]) -> None:
        content = request.get("content", "").lower()
        for pattern in self.CODE_KEYWORDS:
            if re.search(pattern, content):
                self.blocked = True
                self.reason = "Requests for source code or internal implementation are blocked."
                return


class DirectiveProtection(ProtectionBase):
    """
    Blocks manipulation directives that target the host system (edit/delete/modify the host).
    """
    MANIPULATION_PATTERNS = [
        r"\bedit\s+host\b", r"\bdelete\s+host\b", r"\bmodify\s+host\b",
        r"\bremove\s+host\b", r"\balter\s+host\b"
    ]

    def evaluate(self, request: Dict[str, Any]) -> None:
        content = request.get("content", "").lower()
        for pattern in self.MANIPULATION_PATTERNS:
            if re.search(pattern, content):
                self.blocked = True
                self.reason = "Directives that modify the host are prohibited."
                return


class RemoteExecutionValidator(ProtectionBase):
    """
    Ensures that the request stays within the user‑machine scope.
    Blocks any attempt to trigger remote execution or access external resources.
    """
    REMOTE_PATTERNS = [
        r"\brun\s+remotely\b", r"\bexecute\s+on\s+server\b", r"\bremote\s+command\b",
        r"\bssh\s+into\b", r"\bconnect\s+to\s+remote\b"
    ]

    def evaluate(self, request: Dict[str, Any]) -> None:
        content = request.get("content", "").lower()
        for pattern in self.REMOTE_PATTERNS:
            if re.search(pattern, content):
                self.blocked = True
                self.reason = "Remote execution requests are not permitted."
                return


class SemanticAnalyzer(ProtectionBase):
    """
    Performs higher‑level semantic checks for prohibited intents.
    """
    def evaluate(self, request: Dict[str, Any]) -> None:
        content = request.get("content", "").lower().strip()

        # Block internal swarm/LAN inquiries
        if re.fullmatch(r"how does this work\??", content):
            if "swarm" in content or "lan" in content or "network" in content:
                self.blocked = True
                self.reason = "Inquiry about internal swarm/LAN mechanics is blocked."
                return

        # Block cloning / replication assistance
        if content.startswith("help me build"):
            if "clone" in content or "replicate" in content or "duplicate" in content:
                self.blocked = True
                self.reason = "Assistance with cloning or replicating the system is prohibited."
                return

        # Block edit/delete/modify attempts aimed at the host (already covered, but double‑check)
        if any(word in content for word in ["edit", "delete", "modify", "remove", "alter"]):
            if "host" in content:
                self.blocked = True
                self.reason = "Manipulation of the host is disallowed."
                return


class RequestFilter:
    """
    Central filter that aggregates all protection modules.
    Usage:
        filter = RequestFilter()
        allowed, reason = filter.filter({"content": user_input})
    """
    def __init__(self):
        self.protections = [
            IPSelfProtection(),
            CodebaseProtection(),
            DirectiveProtection(),
            RemoteExecutionValidator(),
            SemanticAnalyzer()
        ]

    def filter(self, request: Dict[str, Any]) -> (bool, str):
        """
        Returns a tuple (is_allowed, reason). If ``is_allowed`` is False,
        ``reason`` explains why the request was blocked.
        """
        for protection in self.protections:
            protection.evaluate(request)
            if protection.blocked:
                return False, protection.reason
        return True, "Request passed all safety checks."
import re
from typing import List, Tuple


class IPSelfProtection:
    """
    Blocks any request that attempts to obtain, disclose, or manipulate IP‑related
    information (e.g., asking for the system's IP address, requesting IP ranges,
    or trying to discover network topology).
    """
    _ip_regex = re.compile(
        r"""(?:
                \b(?:\d{1,3}\.){3}\d{1,3}\b      # IPv4
            |   \b(?:[0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}\b   # IPv6 (simplified)
            )""",
        re.VERBOSE,
    )
    _keywords = re.compile(r"\b(my|your|host|machine)\s+ip\b", re.I)

    def block(self, request: str) -> bool:
        """Return True if the request should be blocked."""
        if self._ip_regex.search(request):
            return True
        if self._keywords.search(request):
            return True
        return False


class CodebaseProtection:
    """
    Prevents exposure of the codebase, internal implementations, or any
    proprietary logic. Blocks queries that ask for source code, algorithms,
    or repository details.
    """
    _patterns = [
        re.compile(r"\b(source\s+code|implementation|internal\s+logic|repo|repository|git|svn)\b", re.I),
        re.compile(r"\bshow\s+me\s+the\s+code\b", re.I),
    ]

    def block(self, request: str) -> bool:
        """Return True if the request should be blocked."""
        for pat in self._patterns:
            if pat.search(request):
                return True
        return False


class DirectiveProtection:
    """
    Blocks attempts to issue directives that could manipulate or alter the host
    environment (e.g., delete files, modify settings, shut down services).
    """
    _dangerous_verbs = re.compile(
        r"\b(delete|remove|modify|edit|shutdown|restart|kill|run|execute)\b", re.I
    )
    _targets = re.compile(r"\b(host|machine|system|server|process)\b", re.I)

    def block(self, request: str) -> bool:
        """Return True if the request contains a dangerous directive."""
        if self._dangerous_verbs.search(request) and self._targets.search(request):
            return True
        return False


class RemoteExecutionValidator:
    """
    Ensures that requests stay within the allowed user‑machine‑only scope.
    Blocks any mention of remote execution, external URLs, or commands that
    would affect another machine.
    """
    _remote_indicators = [
        re.compile(r"\bssh\b", re.I),
        re.compile(r"\bscp\b", re.I),
        re.compile(r"\bcurl\b", re.I),
        re.compile(r"\bwget\b", re.I),
        re.compile(r"https?://", re.I),
        re.compile(r"\bremote\s+execution\b", re.I),
    ]

    def validate(self, request: str) -> bool:
        """Return True if the request is within the allowed scope."""
        for pat in self._remote_indicators:
            if pat.search(request):
                return False
        return True


class RequestFilter:
    """
    Central filter that aggregates all protection layers and applies
    semantic analysis for disallowed intent.
    """
    def __init__(self):
        self.ip_protection = IPSelfProtection()
        self.code_protection = CodebaseProtection()
        self.directive_protection = DirectiveProtection()
        self.remote_validator = RemoteExecutionValidator()
        self._semantic_rules: List[Tuple[re.Pattern, str]] = [
            # Block questions about internal swarm mechanics
            (re.compile(r"\bhow does (this|the) (work|function|operate)\b", re.I), "swarm_internals"),
            # Block attempts to clone or replicate the system
            (re.compile(r"\bhelp me build\b.*\b(clone|replicate|copy)\b", re.I), "clone_attempt"),
            # Block modifications targeting the host/machine
            (re.compile(r"\b(edit|delete|modify|remove|shutdown)\b.*\b(host|machine|system)\b", re.I), "host_target"),
        ]

    def is_allowed(self, request: str) -> bool:
        """
        Evaluate the request against all protection layers.
        Returns True if the request is safe, False otherwise.
        """
        # Low‑level protections
        if self.ip_protection.block(request):
            return False
        if self.code_protection.block(request):
            return False
        if self.directive_protection.block(request):
            return False
        if not self.remote_validator.validate(request):
            return False

        # Semantic intent analysis
        for pattern, _reason in self._semantic_rules:
            if pattern.search(request):
                return False

        return True
```python
"""
lan_safety_gateway.py

Central safety gateway for LAN‑only interactions.

It provides a set of lightweight, rule‑based protections that examine a
user's textual request before it is processed by any internal tool.
The design is documented in ``LAN_SAFETY_DESIGN.md``.
"""

import re
from typing import Tuple, Optional


class BaseProtection:
    """Base class for all protection modules."""

    def check(self, request: str) -> Optional[str]:
        """
        Inspect *request* and return an error message if the request
        should be blocked.  Return ``None`` if the request passes this
        check.
        """
        raise NotImplementedError


class IPSelfProtection(BaseProtection):
    """Blocks any request that attempts to obtain or discuss IP information."""

    _patterns = [
        r"\bmy\s+ip\b",
        r"\byour\s+ip\b",
        r"\bpublic\s+ip\b",
        r"\binternal\s+ip\b",
        r"\bip\s+address\b",
        r"\bip\s+of\s+.*\b",
    ]

    def check(self, request: str) -> Optional[str]:
        lowered = request.lower()
        for pat in self._patterns:
            if re.search(pat, lowered):
                return "IP‑related queries are prohibited for LAN safety."
        return None


class CodebaseProtection(BaseProtection):
    """Blocks attempts to expose or retrieve source code of the repository."""

    _patterns = [
        r"\bshow\s+me\s+the\s+source\b",
        r"\bexpose\s+code\b",
        r"\bread\s+file\b",
        r"\bprint\s+source\b",
        r"\bview\s+implementation\b",
        r"\baccess\s+.*\.py\b",
        r"\blist\s+files\b",
    ]

    def check(self, request: str) -> Optional[str]:
        lowered = request.lower()
        for pat in self._patterns:
            if re.search(pat, lowered):
                return "Requests for internal code or file contents are blocked."
        return None


class DirectiveProtection(BaseProtection):
    """Blocks manipulation directives that target the host or LAN infrastructure."""

    _edit_patterns = [
        r"\b(edit|delete|modify|remove|change|alter)\b.*\b(host|server|machine|lan)\b",
    ]

    def check(self, request: str) -> Optional[str]:
        lowered = request.lower()
        for pat in self._edit_patterns:
            if re.search(pat, lowered):
                return "Direct manipulation of host/LAN resources is prohibited."
        return None


class RemoteExecutionValidator(BaseProtection):
    """Ensures the request stays within the user‑machine‑only scope."""

    _remote_patterns = [
        r"\bremote\s+execution\b",
        r"\brun\s+on\s+server\b",
        r"\bcloud\s+instance\b",
        r"\bexecute\s+remotely\b",
        r"\bdeploy\s+to\s+.*\b",
    ]

    def check(self, request: str) -> Optional[str]:
        lowered = request.lower()
        for pat in self._remote_patterns:
            if re.search(pat, lowered):
                return "Remote execution or deployment beyond the local machine is disallowed."
        return None


class SemanticAnalysisProtection(BaseProtection):
    """
    Performs higher‑level semantic checks for known unsafe intents.
    """

    def check(self, request: str) -> Optional[str]:
        lowered = request.lower()

        # 1. “How does this work?” – block if about swarm internals.
        if re.search(r"\bhow\s+does\s+this\s+work\b", lowered):
            if any(word in lowered for word in ["swarm", "internals", "architecture", "system"]):
                return "Inquiries about internal swarm mechanics are blocked."

        # 2. “Help me build …” – block if trying to clone or replicate the system.
        if re.search(r"\bhelp\s+me\s+build\b", lowered):
            if any(word in lowered for word in ["clone", "replicate", "copy", "duplicate", "recreate"]):
                return "Assistance in cloning or replicating the system is prohibited."

        # 3. Edit/Delete/Modify – already covered by DirectiveProtection,
        #    but keep a fallback for generic wording.
        if re.search(r"\b(edit|delete|modify|remove|change|alter)\b", lowered):
            return "Manipulation directives targeting the host are blocked."

        return None


class RequestFilter:
    """
    Aggregates all protection modules and evaluates a request.
    """

    def __init__(self):
        self._protectors = [
            IPSelfProtection(),
            CodebaseProtection(),
            DirectiveProtection(),
            RemoteExecutionValidator(),
            SemanticAnalysisProtection(),
        ]

    def evaluate(self, request: str) -> Tuple[bool, str]:
        """
        Evaluate *request* against all protections.

        Returns:
            (allowed: bool, message: str)
            If *allowed* is False, *message* contains the reason.
        """
        for protector in self._protectors:
            result = protector.check(request)
            if result is not None:
                return False, result
        return True, "Request passed all safety checks."
```
import re
from dataclasses import dataclass
from typing import Dict, Tuple, Optional


class LanSafetyException(Exception):
    """Raised when a request is blocked by the LAN safety gateway."""
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass
class Request:
    """Simple container for incoming request data."""
    prompt: str
    source_ip: str
    user_id: Optional[str] = None
    metadata: Optional[Dict] = None


class IPSelfProtection:
    """
    Blocks any request that asks about the internal IP architecture,
    network layout, or any IP‑related details that could expose the LAN.
    """
    _patterns = [
        re.compile(r"\bmy\s+ip\b", re.I),
        re.compile(r"\binternal\s+ip\b", re.I),
        re.compile(r"\blocal\s+network\b", re.I),
        re.compile(r"\bprivate\s+address\b", re.I),
        re.compile(r"\bsubnet\b", re.I),
    ]

    @classmethod
    def is_blocked(cls, request: Request) -> Tuple[bool, str]:
        for pat in cls._patterns:
            if pat.search(request.prompt):
                return True, "IP‑related queries are prohibited."
        return False, ""


class CodebaseProtection:
    """
    Prevents exposure of the codebase, internal APIs, or any source files.
    """
    _patterns = [
        re.compile(r"\bshow\s+me\s+the\s+code\b", re.I),
        re.compile(r"\bexpose\s+source\b", re.I),
        re.compile(r"\bread\s+file\s+.+\.py\b", re.I),
        re.compile(r"\blist\s+directory\b", re.I),
        re.compile(r"\bgit\s+clone\b", re.I),
    ]

    @classmethod
    def is_blocked(cls, request: Request) -> Tuple[bool, str]:
        for pat in cls._patterns:
            if pat.search(request.prompt):
                return True, "Codebase exposure is prohibited."
        return False, ""


class DirectiveProtection:
    """
    Blocks attempts to edit, delete, or otherwise manipulate host resources.
    """
    _patterns = [
        re.compile(r"\b(edit|delete|modify|remove)\s+.*\b(host|machine|system)\b", re.I),
        re.compile(r"\bshutdown\b", re.I),
        re.compile(r"\breboot\b", re.I),
        re.compile(r"\bformat\s+disk\b", re.I),
    ]

    @classmethod
    def is_blocked(cls, request: Request) -> Tuple[bool, str]:
        for pat in cls._patterns:
            if pat.search(request.prompt):
                return True, "Directives targeting the host are blocked."
        return False, ""


class RemoteExecutionValidator:
    """
    Ensures that the request is intended for local execution only.
    Any request that implies remote or distributed execution is blocked.
    """
    _patterns = [
        re.compile(r"\bremote\s+execute\b", re.I),
        re.compile(r"\bdistributed\s+run\b", re.I),
        re.compile(r"\brun\s+on\s+other\s+machines?\b", re.I),
        re.compile(r"\bspawn\s+agents?\b", re.I),
    ]

    @classmethod
    def is_blocked(cls, request: Request) -> Tuple[bool, str]:
        for pat in cls._patterns:
            if pat.search(request.prompt):
                return True, "Remote execution is not allowed."
        return False, ""


class SemanticAnalyzer:
    """
    Performs lightweight semantic checks for known prohibited intents.
    """
    _semantic_rules = [
        # Asking about internal swarm mechanics
        (re.compile(r"\bhow\s+does\s+this\s+work\??\b", re.I), 
         "Requests for internal swarm mechanics are blocked."),
        # Attempting to replicate or clone the system
        (re.compile(r"\bhelp\s+me\s+build\s+.*\bclone\b", re.I), 
         "Assistance to clone the system is prohibited."),
        # Direct edit/delete/modify of the host (already covered by DirectiveProtection,
        # but we keep a semantic catch‑all)
        (re.compile(r"\b(edit|delete|modify|remove)\b.*\bhost\b", re.I),
         "Manipulation of the host is blocked."),
    ]

    @classmethod
    def is_blocked(cls, request: Request) -> Tuple[bool, str]:
        for pattern, reason in cls._semantic_rules:
            if pattern.search(request.prompt):
                return True, reason
        return False, ""


class RequestFilter:
    """
    Central gateway that runs all protection layers.
    Call `filter(request)`; it raises LanSafetyException on block.
    """
    _protectors = [
        IPSelfProtection,
        CodebaseProtection,
        DirectiveProtection,
        RemoteExecutionValidator,
        SemanticAnalyzer,
    ]

    @classmethod
    def filter(cls, request: Request) -> None:
        """
        Evaluate the request against all protection layers.
        If any layer blocks the request, raise LanSafetyException with the reason.
        """
        for protector in cls._protectors:
            blocked, reason = protector.is_blocked(request)
            if blocked:
                raise LanSafetyException(reason)
        # If we reach here, the request is considered safe.
        return None
import re
from typing import List, Tuple, Callable


class SafetyGateException(Exception):
    """Raised when a request violates any LAN safety policy."""
    pass


class IPSelfProtection:
    """
    Blocks any request that tries to inquire about, reveal, or manipulate IP‑related
    information of the host or the internal swarm network.
    """
    _ip_regex = re.compile(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b|'          # IPv4
        r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',  # IPv6
        re.IGNORECASE
    )
    _blocked_phrases = [
        r'what\s+is\s+my\s+ip',
        r'find\s+my\s+ip',
        r'list\s+all\s+ips?',
        r'ip\s+address',
        r'network\s+interface',
    ]

    def __init__(self):
        self._patterns = [re.compile(p, re.I) for p in self._blocked_phrases]

    def check(self, request: str) -> None:
        if self._ip_regex.search(request):
            raise SafetyGateException("IP‑related queries are prohibited.")
        for pat in self._patterns:
            if pat.search(request):
                raise SafetyGateException("IP‑related queries are prohibited.")


class CodebaseProtection:
    """
    Prevents exposure or extraction of the internal codebase, source files,
    or any proprietary implementation details.
    """
    _blocked_phrases = [
        r'show\s+me\s+the\s+source',
        r'give\s+me\s+the\s+code',
        r'list\s+all\s+files',
        r'print\s+the\s+source',
        r'view\s+the\s+implementation',
        r'expose\s+code',
        r'clone\s+the\s+repo',
        r'copy\s+the\s+codebase',
    ]

    def __init__(self):
        self._patterns = [re.compile(p, re.I) for p in self._blocked_phrases]

    def check(self, request: str) -> None:
        for pat in self._patterns:
            if pat.search(request):
                raise SafetyGateException("Codebase exposure is prohibited.")


class DirectiveProtection:
    """
    Blocks attempts to override, disable, or otherwise manipulate safety directives,
    guardrails, or internal controls.
    """
    _blocked_phrases = [
        r'disable\s+guardrails?',
        r'override\s+security',
        r'ignore\s+policy',
        r'bypass\s+the\s+gate',
        r'turn\s+off\s+protection',
        r'remove\s+restrictions',
        r'alter\s+the\s+directive',
    ]

    def __init__(self):
        self._patterns = [re.compile(p, re.I) for p in self._blocked_phrases]

    def check(self, request: str) -> None:
        for pat in self._patterns:
            if pat.search(request):
                raise SafetyGateException("Manipulation of safety directives is prohibited.")


class RemoteExecutionValidator:
    """
    Ensures that any execution request is scoped to the local user machine only.
    Any mention of remote machines, other hosts, or network‑wide actions is blocked.
    """
    _blocked_phrases = [
        r'run\s+on\s+remote',
        r'execute\s+on\s+other\s+machine',
        r'deploy\s+to\s+network',
        r'send\s+to\s+host',
        r'push\s+to\s+server',
        r'connect\s+to\s+.*\bhost\b',
        r'remote\s+execution',
        r'network\s+wide',
    ]

    def __init__(self):
        self._patterns = [re.compile(p, re.I) for p in self._blocked_phrases]

    def check(self, request: str) -> None:
        for pat in self._patterns:
            if pat.search(request):
                raise SafetyGateException("Remote execution beyond the local machine is prohibited.")


class RequestFilter:
    """
    Central gateway that applies all protection layers and semantic analyses
    to incoming textual requests.
    """
    def __init__(self):
        self.ip_protection = IPSelfProtection()
        self.code_protection = CodebaseProtection()
        self.directive_protection = DirectiveProtection()
        self.remote_validator = RemoteExecutionValidator()
        self._semantic_rules: List[Tuple[re.Pattern, Callable[[str], None]]] = [
            (re.compile(r'\bhow\s+does\s+this\s+work\??\b', re.I), self._block_swarm_internals),
            (re.compile(r'\bhelp\s+me\s+build\b', re.I), self._block_clone_attempt),
            (re.compile(r'\b(edit|delete|modify)\b.*\b(host|machine|system)\b', re.I), self._block_host_target),
        ]

    # ----------------------------------------------------------------------
    # Semantic rule implementations
    # ----------------------------------------------------------------------
    def _block_swarm_internals(self, request: str) -> None:
        raise SafetyGateException("Inquiry about swarm internals is prohibited.")

    def _block_clone_attempt(self, request: str) -> None:
        raise SafetyGateException("Requests to clone or replicate the system are prohibited.")

    def _block_host_target(self, request: str) -> None:
        raise SafetyGateException("Direct manipulation of the host/machine is prohibited.")

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def evaluate(self, request: str) -> None:
        """
        Run the request through every protection layer.
        If any layer raises SafetyGateException, the exception propagates.
        If the request passes all checks, the method returns silently.
        """
        # 1. Low‑level protection checks
        self.ip_protection.check(request)
        self.code_protection.check(request)
        self.directive_protection.check(request)
        self.remote_validator.check(request)

        # 2. Semantic analysis checks
        for pattern, handler in self._semantic_rules:
            if pattern.search(request):
                handler(request)

        # If we reach this point, the request is considered safe.
        return