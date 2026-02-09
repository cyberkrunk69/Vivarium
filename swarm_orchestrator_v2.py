import logging
from safety.wrapper import self_healing_wrapper

# Import node classes – adjust import paths as needed for your project structure
from intent_gatekeeper import IntentGatekeeper
from gut_check import GutCheck
from feature_breakdown import FeatureBreakdown
from feature_planner import FeaturePlanner
from atomizer import Atomizer
from worker_pool import WorkerPool
from critic import Critic
from test_gate import TestGate
from user_proxy import UserProxy


def _safe_execute(node, data):
    """
    Executes a node's `run` method inside the self‑healing wrapper.
    """
    @self_healing_wrapper
    def _inner():
        return node.run(data)

    return _inner()


class SwarmOrchestratorV2:
    """
    Orchestrates the full LLM‑swarm pipeline:
    IntentGatekeeper → GutCheck → FeatureBreakdown → FeaturePlanner(s) →
    Atomizer → WorkerPool → Critic → TestGate(s) → UserProxy
    All steps are protected by `self_healing_wrapper` for resilience.
    """

    def __init__(self, config=None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

        # Instantiate nodes – you can pass configuration dicts if required
        self.intent_gatekeeper = IntentGatekeeper()
        self.gut_check = GutCheck()
        self.feature_breakdown = FeatureBreakdown()
        self.feature_planner = FeaturePlanner()
        self.atomizer = Atomizer()
        self.worker_pool = WorkerPool()
        self.critic = Critic()
        self.test_gate = TestGate()
        self.user_proxy = UserProxy()

    def run(self, user_input):
        """
        Runs the full orchestrated flow on `user_input`.
        Returns the final response produced by the UserProxy node.
        """
        self.logger.info("Starting SwarmOrchestratorV2 pipeline")

        # 1. Intent Gatekeeper
        intent = _safe_execute(self.intent_gatekeeper, user_input)

        # 2. Gut‑Check
        checked_intent = _safe_execute(self.gut_check, intent)

        # 3. Feature Breakdown
        features = _safe_execute(self.feature_breakdown, checked_intent)

        # 4. Feature Planner
        plan = _safe_execute(self.feature_planner, features)

        # 5. Atomizer
        atoms = _safe_execute(self.atomizer, plan)

        # 6. Worker Pool
        work_results = _safe_execute(self.worker_pool, atoms)

        # 7. Critic
        critique = _safe_execute(self.critic, work_results)

        # 8. Test Gate
        test_passed = _safe_execute(self.test_gate, critique)

        # 9. User Proxy (final output)
        final_output = _safe_execute(self.user_proxy, test_passed)

        self.logger.info("SwarmOrchestratorV2 pipeline completed")
        return final_output
from safety_wrapper import self_healing_wrapper

# Import all node classes
from intent_gatekeeper import IntentGatekeeper
from gut_check import GutCheck
from feature_breakdown import FeatureBreakdown
from feature_planners import FeaturePlanners
from atomizer import Atomizer
from worker_pool import WorkerPool
from critic import Critic
from test_gates import TestGates
from user_proxy import UserProxy


class SwarmOrchestratorV2:
    """
    Orchestrates the full swarm workflow:
    IntentGatekeeper → GutCheck → FeatureBreakdown → FeaturePlanners
    → Atomizer → WorkerPool → Critic → TestGates → UserProxy
    Each component is wrapped with `self_healing_wrapper` for safety and
    automatic recovery from failures.
    """

    def __init__(self):
        # Initialise each node, wrapped for self‑healing behaviour
        self.intent_gatekeeper = self_healing_wrapper(IntentGatekeeper())
        self.gut_check = self_healing_wrapper(GutCheck())
        self.feature_breakdown = self_healing_wrapper(FeatureBreakdown())
        self.feature_planners = self_healing_wrapper(FeaturePlanners())
        self.atomizer = self_healing_wrapper(Atomizer())
        self.worker_pool = self_healing_wrapper(WorkerPool())
        self.critic = self_healing_wrapper(Critic())
        self.test_gates = self_healing_wrapper(TestGates())
        self.user_proxy = self_healing_wrapper(UserProxy())

    def run(self, user_input: str):
        """
        Execute the end‑to‑end flow for a given user request.

        Parameters
        ----------
        user_input : str
            Raw input from the user.

        Returns
        -------
        str
            The final response produced by the UserProxy node.
        """

        # 1️⃣ Intent Gatekeeper – decide if we should proceed
        intent = self.intent_gatekeeper.process(user_input)

        # 2️⃣ Gut‑Check – quick validation of the intent
        if not self.gut_check.validate(intent):
            raise ValueError("Gut‑check failed: intent rejected.")

        # 3️⃣ Feature Breakdown – decompose intent into discrete features
        features = self.feature_breakdown.breakdown(intent)

        # 4️⃣ Feature Planners – create execution plans for each feature
        plans = self.feature_planners.plan(features)

        # 5️⃣ Atomizer – split plans into atomic tasks
        atoms = self.atomizer.atomize(plans)

        # 6️⃣ Worker Pool – run atomic tasks in parallel / distributed fashion
        results = self.worker_pool.execute(atoms)

        # 7️⃣ Critic – evaluate results and provide a critique
        critique = self.critic.review(results)

        # 8️⃣ Test Gates – ensure the critique meets quality thresholds
        if not self.test_gates.approve(critique):
            raise ValueError("Test gates rejected the critique.")

        # 9️⃣ User Proxy – format and deliver the final response to the user
        response = self.user_proxy.respond(critique)

        return response