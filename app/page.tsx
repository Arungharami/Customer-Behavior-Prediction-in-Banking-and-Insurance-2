import status from "../public/research-status.json";

const dimensions = [
  ["Discrimination", "ROC-AUC, PR-AUC, F1, precision, recall"],
  ["Calibration", "Brier, ECE, slope/intercept, reliability"],
  ["Temporal stability", "Window metrics, PSI, drift and degradation slopes"],
  ["Explanation stability", "SHAP rank Spearman and top-k Jaccard"],
  ["Operational utility", "Fixed capacity, normalized cost and net benefit"],
  ["Efficiency", "Training time, p50/p95 latency, RAM and model size"],
];

const datasets = [
  ["Primary temporal benchmark", "Home Credit - Credit Risk Model Stability", "Kaggle competition data; local authorized copy required."],
  ["Banking external validation", "UCI Bank Marketing", "Date-ordered evaluation; post-contact duration excluded."],
  ["Insurance external validation", "Porto Seguro Safe Driver", "Claim-propensity external validation; competition data not redistributed."],
];

const pipeline = [
  "Record provenance and checksums", "Freeze temporal row assignments", "Fit preprocessing on training only",
  "Train LR, RF, XGBoost, LightGBM and CatBoost", "Calibrate on a separate window",
  "Evaluate drift and temporal degradation", "Measure SHAP stability", "Evaluate capacity and cost scenarios",
  "Bootstrap uncertainty and benchmark efficiency", "Verify registry and open publication gate",
];

export default function Home() {
  return <main>
    <section className="hero"><div className="shell heroGrid"><div className="heroCopy">
      <div className="eyebrow"><span className="pulse"/> Evidence-first research system</div>
      <h1>Beyond <span>Static Accuracy.</span></h1>
      <p className="heroTitle">Temporal Stability, Probability Calibration, Explanation Stability, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance</p>
      <p className="heroLead">A publication pipeline for deciding which model remains useful when populations, probabilities, explanations, capacity, and costs change over time.</p>
      <div className="heroActions"><a className="button buttonPrimary" href="#evidence">Inspect evidence state</a><a className="button buttonGhost" href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2">Source repository</a></div>
      <div className="integrityInline"><strong>Current claim boundary:</strong> protocols and software are defined; no empirical performance claim is published because benchmark execution has not occurred.</div>
    </div><aside className="heroPanel evidencePanel"><div className="panelHeader"><span>Publication gate</span><span className="liveDot">Fail closed</span></div>
      <h2>{status.summary.verified} verified result sets</h2><p>Only checksum-backed artifacts may appear as findings.</p>
      <div className="panelMetrics"><div><span>Protocol</span><strong>Defined</strong></div><div><span>Experiments</span><strong>Not executed</strong></div><div><span>Metrics shown</span><strong>None</strong></div></div>
    </aside></div></section>

    <section className="trustStrip"><div className="shell trustGrid">{dimensions.map(([name, metric], i)=><div key={name}><span>0{i+1}</span><strong>{name}</strong><small>{metric}</small></div>)}</div></section>

    <section id="research" className="section"><div className="shell"><div className="sectionHeader"><div><div className="sectionKicker">Research question</div><h2>Which financial prediction system remains trustworthy under temporal change?</h2></div><p>Model selection is multi-objective. Complexity must earn its place after calibration, stability, explanation, utility, and efficiency are considered.</p></div></div></section>

    <section id="benchmarks" className="section sectionAlt"><div className="shell"><div className="sectionHeader"><div><div className="sectionKicker">Dataset provenance</div><h2>One temporal anchor. Two external domains.</h2></div><p>Raw restricted data stay outside GitHub. Every authorized local file is hashed into a run manifest.</p></div><div className="datasetGrid">{datasets.map(([tag,name,role],i)=><article className="datasetCard" key={name}><div className="datasetTop"><span>0{i+1}</span><small>{tag}</small></div><h3>{name}</h3><p>{role}</p><div className="datasetRole"><span>Current state</span>PROTOCOL_DEFINED</div></article>)}</div></div></section>

    <section id="evaluation" className="section"><div className="shell"><div className="sectionHeader"><div><div className="sectionKicker">Frozen evaluation matrix</div><h2>No test-window tuning. No result without lineage.</h2></div><p>Train, calibration, and test assignments are ordered and checksum-frozen. Bootstrap intervals use deterministic seeds.</p></div><div className="dimensionGrid">{dimensions.map(([name,metric],i)=><article className="dimensionCard" key={name}><div className="dimensionIndex">0{i+1}</div><h3>{name}</h3><p>{metric}</p></article>)}</div></div></section>

    <section id="pipeline" className="section sectionDark"><div className="shell"><div className="sectionHeader darkHeader"><div><div className="sectionKicker">Execution pipeline</div><h2>Ten gates from source to manuscript.</h2></div><p>Missing data, failed checks, or incomplete evidence stop publication instead of producing substitutes.</p></div><div className="pipeline">{pipeline.map((text,i)=><div className="pipelineStep" key={text}><span>{String(i+1).padStart(2,"0")}</span><div><h3>{text}</h3><p>{i<3?"Protocol and leakage boundary":"Executed artifacts required before verification"}</p></div></div>)}</div></div></section>

    <section id="evidence" className="section"><div className="shell"><div className="sectionHeader"><div><div className="sectionKicker">Evidence and readiness</div><h2>Scientific state is explicit.</h2></div><p>PROTOCOL_DEFINED is not a result. EXECUTED is not VERIFIED. FAILED and NOT_EXECUTED remain visible.</p></div><div className="statusBoard"><div className="statusBoardHeader"><span>Evidence registry</span><small>schema v{status.schemaVersion}</small></div>{status.items.map(item=><div className="statusRow" key={item.id}><span className={`stateBadge state-${item.state}`}>{item.state}</span><strong>{item.label}</strong><small>{item.note}</small></div>)}</div></div></section>

    <section id="reproduce" className="section sectionAlt"><div className="shell reproduceGrid"><div><div className="sectionKicker">Reproducibility</div><h2>Claim to checksum.</h2><p className="reproduceLead">Each accepted claim must resolve to a run ID, commit, environment snapshot, data manifest, split manifest, config, machine-readable metric, and registered table or figure.</p><div className="folderGrid"><div><code>config/</code><span>Frozen protocol</span></div><div><code>src/</code><span>Execution and metrics</span></div><div><code>artifacts/</code><span>Generated evidence</span></div><div><code>docs/</code><span>Roadmap and manuscript plan</span></div></div></div><div className="terminal"><div className="terminalBar"><span/><span/><span/><small>exact next run</small></div><pre><code>{`python scripts/download_kaggle_data.py --dataset all\npython -m src.pipeline --config config/research.yaml\npython scripts/research_gate.py --run-dir artifacts/runs/<run_id> --manuscript-source paper/manuscript.md\nnpm run build`}</code></pre></div></div></section>

    <section className="section"><div className="shell ctaCard"><div><div className="sectionKicker">Limitations and governance</div><h2>Predictive evidence is not permission to automate harm.</h2><p>Public benchmarks may not represent current populations. Protected-group fairness, lawful basis, adverse-action explanation, human review, monitoring, and institution-specific cost validation remain deployment requirements.</p></div><div className="ctaActions"><a className="button buttonPrimary" href="/RESEARCH_SYSTEM.md">Download research plan</a><a className="button buttonGhost" href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2">Cite and inspect code</a></div></div></section>
  </main>;
}
