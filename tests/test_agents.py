from spm_defense.agents import MonitorAgent
from spm_defense.models import SPMSignal
from spm_defense.tokenization import HyperToken


def test_monitor_agent_initialization():
    agent = MonitorAgent()
    assert agent.concepts == {}
    assert agent.alpha == 1.0
    assert agent.beta == 1.0


def test_monitor_agent_process_observation():
    agent = MonitorAgent()

    # First observation
    signal = agent.process_observation(
        concept="Democracy",
        embedding=[0.0, 0.0],
        logos=1.0, pathos=0.0, ethos_force=0.0,
        source="CNN",
        source_reliability=10.0, source_bias=0.0
    )

    # Verify Signal Structure
    assert isinstance(signal, SPMSignal)
    assert signal.concept == "Democracy"
    assert signal.source == "CNN"

    # Verify State Update
    assert "Democracy" in agent.concepts
    token = agent.concepts["Democracy"]
    # HyperToken logic: update_trajectory adds current embedding if empty, then adds new.
    # So if we init and update immediately, we get 2 points.
    assert len(token.trajectory) == 2
    assert token.trajectory[0] == [0.0, 0.0]


def test_monitor_agent_acceleration_logic():
    agent = MonitorAgent()

    # 1. Establish Mass (First point, stability is high/infinite?)
    # If trajectory has 2 points (duplicate), stability is 1/epsilon (variance 0).
    # Mass = alpha*C + beta*S = 1*1 + 1*(1e6) approx 1e6.
    # Acceleration = (eta * Force) / Mass.
    # Force = 1.0. Eta approx 1.0.
    # Acc = 1 / 1e6 approx 0.

    signal1 = agent.process_observation(
        concept="Test",
        embedding=[0.0, 0.0],
        logos=1.0, pathos=0.0, ethos_force=0.0,
        source="Trusted",
        source_reliability=5.0, source_bias=0.0
    )
    assert signal1.mass > 1000  # High stability for static point
    assert signal1.acceleration < 0.01 # Very low acceleration due to high mass

    # 2. Move the concept (Reduce Stability -> Reduce Mass -> Increase Potential Acceleration)
    # We need to simulate a drift.
    # Update with [1,1]
    signal2 = agent.process_observation(
        concept="Test",
        embedding=[10.0, 0.0], # Big jump
        logos=10.0, pathos=10.0, ethos_force=10.0, # High force
        source="Trusted",
        source_reliability=5.0, source_bias=0.0
    )

    # Now trajectory has [0,0], [0,0], [10,0].
    # Stability drops significantly.
    # Mass drops.
    # Acceleration should be higher relative to force.

    assert signal2.mass < signal1.mass
    # Force magnitude is sqrt(300) ~ 17.
    # Mass is approx 1*1 + 1*Stability.
    # Stability: Var of 0, 0, 10 (mean 3.33). (3.3^2 + 3.3^2 + 6.6^2)/3.
    # Stability is relatively low.
    # Acc should be > 1.0.
    assert signal2.acceleration > 1.0


def test_monitor_agent_alert_system():
    agent = MonitorAgent(acceleration_threshold=5.0)

    # Correctly initialize the concept with a HyperToken
    agent.concepts["Volatile"] = HyperToken(embedding=[0.0, 0.0])

    # Manually hack trajectory to be volatile to ensure low mass?
    # Or just rely on the physics.

    # Let's tank the stability manually to be sure.
    # If stability is low (variance high), Mass is low.
    # If Mass is low (e.g. 2.0), and Force is 17 (from 10,10,10), Acc is 8.5 > 5.0.

    # Pre-load trajectory with variance
    agent.concepts["Volatile"].trajectory = [[0, 0], [10, 10], [-10, -10]]

    signal = agent.process_observation(
        concept="Volatile",
        embedding=[10.0, 0.0],
        logos=10.0, pathos=10.0, ethos_force=10.0,
        source="Trusted",
        source_reliability=5.0, source_bias=0.0,
        centrality=0.0  # Zero centrality to minimize mass
    )

    alert = agent.check_alert(signal)
    assert alert is not None
    assert "High Acceleration" in alert


def test_monitor_agent_ethos_circuit_breaker():
    agent = MonitorAgent(ethos_threshold=0.3)

    # Source with low reliability
    signal = agent.process_observation(
        concept="Attack",
        embedding=[0.0, 0.0],
        logos=10.0, pathos=0.0, ethos_force=0.0,
        source="Bot",
        source_reliability=-5.0, source_bias=0.0
    )

    assert signal.ethos == 0.0
    # Acceleration should be 0 because Ethos is 0
    assert signal.acceleration == 0.0
