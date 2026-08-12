const datasets = [
  {
    tag: "Primary temporal benchmark",
    name: "Home Credit — Credit Risk Model Stability",
    task: "Credit-default risk under explicit temporal stability evaluation.",
    role: "Anchor benchmark for drift, temporal degradation, calibration, and stability-aware model selection.",
    accent: "01",
  },
  {
    tag: "Banking external validation",
    name: "UCI Bank Marketing",
    task: "Predict term-deposit subscription from pre-contact information.",
    role: "Date-ordered banking benchmark; post-call duration is excluded from realistic deployment claims.",
    accent: "02",
  },
  {
    tag: "Insurance external validation",
    name: "Porto Seguro Safe Driver",
    task: "Predict next-year insurance claim propensity.",
    role: "Cross-domain insurance validation with common metrics plus Gini where useful.",
    accent: "03",
  },
];

const dimensions = [
  ["Discrimination", "ROC-AUC · PR-AUC · F1 · precision · recall"],
  ["Calibration", "Brier · ECE · slope/intercept · reliability"],
  ["Temporal stability", "window metrics · PSI · degradation slope · drift alerts"],
  ["Explanation stability", "SHAP · rank Spearman · top-k Jaccard"],
  ["Operational value", "Recall@Top-k · capacity precision · normalized cost · net benefit"],
  ["Efficiency", "training time · p50/p95 latency · model size · peak RAM"],
];

const models = [
  ["Tier 1", "Logistic Regression", "Interpretable anchor"],
  ["Tier 2", "RF · XGBoost · LightGBM · CatBoost", "Nonlinear baselines"],
  ["Tier 3", "Stability-aware calibrated ensemble", "Proposed deployment model"],
  ["Tier 4", "Modern tabular benchmark", "Exploratory, resource-feasible only"],
];

const pipeline = [
  ["01", "Provenance", "Authorize benchmark data, record source restrictions, freeze manifests."],
  ["02", "Temporal design", "Freeze train, calibration, and final test windows before comparison."],
  ["03", "Leakage-safe processing", "Fit preprocessing on training data only; enforce deployment-time feature availability."],
  ["04", "Model benchmark", "Train interpretable and nonlinear baselines with deterministic seeds."],
  ["05", "Calibration", "Compare raw, sigmoid/Platt, and isotonic probabilities on a separate calibration window."],
  ["06", "Drift & stability", "Measure feature shift, score drift, and performance degradation over time."],
  ["07", "Explanation stability", "Compare frozen-model SHAP rankings across early and late windows."],
  ["08", "Operational analysis", "Evaluate fixed-capacity ranking and a transparent TP/FP/FN sensitivity grid."],
  ["09", "Complexity", "Record training time, inference latency, RAM, and serialized model size."],
  ["10", "Publication gate", "Generate artifacts, verify figure/table registry, and unlock manuscript numbers only after checks pass."],
];

const status = [
  ["Research question & novelty", "ready", "Defined"],
  ["Dataset protocol & provenance plan", "ready", "Defined"],
  ["Evaluation matrix", "ready", "Defined"],
  ["Reproducibility scaffold", "ready", "Implemented"],
  ["Empirical benchmark execution", "pending", "Pending authorized data"],
  ["Verified manuscript results", "locked", "Locked until run passes"],
  ["Compact model release", "locked", "Gated by accepted run"],
];

export default function Home() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    headline:
      "Beyond Static Accuracy: Temporal Stability, Probability Calibration, Explanation Stability, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance",
    author: { "@type": "Person", name: "Arun Kumar Gharami" },
    about: [
      "Customer behavior prediction",
      "Trustworthy machine learning",
      "Temporal stability",
      "Probability calibration",
      "Explainable AI",
      "Banking and insurance analytics",
    ],
    isAccessibleForFree: true,
  };

  return (
    <main>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />

      <section className="hero">
        <div className="heroGlow heroGlowOne" />
        <div className="heroGlow heroGlowTwo" />
        <div className="shell heroGrid">
          <div className="heroCopy">
            <div className="eyebrow"><span className="pulse" /> Research system · Part 2 · Pre-results</div>
            <h1>
              Beyond <span>Static Accuracy.</span>
            </h1>
            <p className="heroTitle">
              Temporal Stability, Probability Calibration, Explanation Stability, and Cost-Sensitive Customer Behavior Prediction in Banking and Insurance
            </p>
            <p className="heroLead">
              A deployment-focused research program asking a harder question than “which model has the best AUC?” — which system remains accurate, calibrated, explainable, efficient, and operationally useful as customer populations change over time?
            </p>
            <div className="heroActions">
              <a className="button buttonPrimary" href="#research">Explore the research ↓</a>
              <a
                className="button buttonGhost"
                href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2"
                target="_blank"
                rel="noreferrer"
              >
                Reproducibility package ↗
              </a>
            </div>
            <div className="integrityInline">
              <strong>Research-integrity state:</strong> methodology is public; empirical results remain locked until executable benchmark runs produce verified artifacts.
            </div>
          </div>

          <div className="heroPanel" aria-label="Trustworthy deployment evaluation stack">
            <div className="panelHeader">
              <span>Deployment trust stack</span>
              <span className="liveDot">Protocol active</span>
            </div>
            <div className="radarCore">
              <div className="coreRing ringOne" />
              <div className="coreRing ringTwo" />
              <div className="coreRing ringThree" />
              <div className="coreCenter">
                <small>MODEL</small>
                <strong>TRUST</strong>
                <span>over time</span>
              </div>
              <span className="orbitLabel orbitOne">Calibration</span>
              <span className="orbitLabel orbitTwo">Stability</span>
              <span className="orbitLabel orbitThree">XAI</span>
              <span className="orbitLabel orbitFour">Cost</span>
              <span className="orbitLabel orbitFive">Efficiency</span>
            </div>
            <div className="panelMetrics">
              <div><span>Selection target</span><strong>Multi-objective</strong></div>
              <div><span>Validation</span><strong>Temporal + external</strong></div>
              <div><span>Evidence</span><strong>Artifact-backed</strong></div>
            </div>
          </div>
        </div>
      </section>

      <section className="trustStrip">
        <div className="shell trustGrid">
          <div><span>01</span><strong>Discrimination</strong><small>Can it rank risk?</small></div>
          <div><span>02</span><strong>Calibration</strong><small>Can probabilities be trusted?</small></div>
          <div><span>03</span><strong>Stability</strong><small>Does quality survive time?</small></div>
          <div><span>04</span><strong>Explainability</strong><small>Do explanations remain coherent?</small></div>
          <div><span>05</span><strong>Decision value</strong><small>Does it help under constraints?</small></div>
          <div><span>06</span><strong>Complexity</strong><small>Is the gain worth the cost?</small></div>
        </div>
      </section>

      <section id="research" className="section">
        <div className="shell twoColIntro">
          <div>
            <div className="sectionKicker">Research thesis</div>
            <h2>The best static model may be the wrong deployment model.</h2>
          </div>
          <div className="leadBlock">
            <p>
              Part 1 established an applied prediction pipeline. Part 2 tests whether model quality survives operational change. Instead of optimizing a single held-out score, the study evaluates six interacting deployment properties across banking and insurance benchmarks.
            </p>
            <p>
              The goal is not to manufacture a universal winner. It is to identify when predictive gains remain meaningful after calibration error, temporal degradation, explanation instability, operating constraints, latency, memory, and model size are considered together.
            </p>
          </div>
        </div>

        <div className="shell researchQuestion">
          <div className="questionNumber">RQ</div>
          <div>
            <span>Central research question</span>
            <h3>Which financial prediction system remains trustworthy when customer populations and operating conditions change over time?</h3>
          </div>
        </div>
      </section>

      <section id="benchmarks" className="section sectionAlt">
        <div className="shell">
          <div className="sectionHeader">
            <div>
              <div className="sectionKicker">Benchmark architecture</div>
              <h2>One temporal anchor. Two external domains.</h2>
            </div>
            <p>
              Public datasets are used with transparent provenance. Competition data are never redistributed through the repository.
            </p>
          </div>
          <div className="datasetGrid">
            {datasets.map((dataset) => (
              <article className="datasetCard" key={dataset.name}>
                <div className="datasetTop"><span>{dataset.accent}</span><small>{dataset.tag}</small></div>
                <h3>{dataset.name}</h3>
                <p>{dataset.task}</p>
                <div className="datasetRole"><span>Research role</span>{dataset.role}</div>
              </article>
            ))}
          </div>
          <div className="optionalDataset">
            <span>Optional stress test</span>
            <strong>IEEE-CIS Fraud Detection</strong>
            <p>Included only if compute, manuscript length, and artifact quality remain manageable; it does not dilute the primary study.</p>
          </div>
        </div>
      </section>

      <section id="evaluation" className="section">
        <div className="shell">
          <div className="sectionHeader">
            <div>
              <div className="sectionKicker">Evaluation matrix</div>
              <h2>Model quality is measured as a system, not a leaderboard.</h2>
            </div>
            <p>Every reported value must map to executable code and a machine-readable artifact.</p>
          </div>
          <div className="dimensionGrid">
            {dimensions.map(([title, metrics], index) => (
              <div className="dimensionCard" key={title}>
                <div className="dimensionIndex">0{index + 1}</div>
                <h3>{title}</h3>
                <p>{metrics}</p>
              </div>
            ))}
          </div>

          <div className="modelSection">
            <div className="modelIntro">
              <div className="sectionKicker">Model strategy</div>
              <h3>Complexity must earn its place.</h3>
              <p>
                A complex model is not treated as superior unless its gain survives stability, calibration, latency, memory, and operational-value comparisons.
              </p>
            </div>
            <div className="modelTable">
              {models.map(([tier, model, role]) => (
                <div className="modelRow" key={tier}>
                  <span>{tier}</span><strong>{model}</strong><small>{role}</small>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="pipeline" className="section sectionDark">
        <div className="shell">
          <div className="sectionHeader darkHeader">
            <div>
              <div className="sectionKicker">Execution pipeline</div>
              <h2>From provenance to publication gate.</h2>
            </div>
            <p>The workflow is deliberately fail-closed: missing data or missing artifacts stop the research pipeline instead of triggering substitutions.</p>
          </div>
          <div className="pipeline">
            {pipeline.map(([number, title, text]) => (
              <div className="pipelineStep" key={number}>
                <span>{number}</span>
                <div><h3>{title}</h3><p>{text}</p></div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="status" className="section">
        <div className="shell statusLayout">
          <div className="statusCopy">
            <div className="sectionKicker">Evidence status</div>
            <h2>Pre-results by design.</h2>
            <p>
              A professional research site should make evidence maturity obvious. This portal will never display placeholder performance metrics as findings. Numeric result sections unlock only after the accepted run passes the repository’s research gate.
            </p>
            <div className="statusPrinciple">
              <span>Integrity principle</span>
              <strong>“Not executed” is a valid scientific state. Fabricated certainty is not.</strong>
            </div>
          </div>
          <div className="statusBoard">
            <div className="statusBoardHeader"><span>Research readiness</span><small>live repository state</small></div>
            {status.map(([name, state, label]) => (
              <div className="statusRow" key={name}>
                <span className={`statusIcon ${state}`} aria-hidden="true" />
                <strong>{name}</strong>
                <small>{label}</small>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="reproduce" className="section sectionAlt">
        <div className="shell reproduceGrid">
          <div>
            <div className="sectionKicker">Reproducibility</div>
            <h2>One research repository. One evidence chain.</h2>
            <p className="reproduceLead">
              The website is a presentation layer for the same repository that contains experiment configuration, model code, provenance checks, artifact gates, figure/table registry, manuscript materials, and CI checks.
            </p>
            <div className="folderGrid">
              <div><code>config/</code><span>Experiment definitions</span></div>
              <div><code>src/</code><span>Models, drift, evaluation</span></div>
              <div><code>scripts/</code><span>Downloads & research gates</span></div>
              <div><code>artifacts/</code><span>Generated evidence</span></div>
              <div><code>paper/</code><span>Manuscript materials</span></div>
              <div><code>docs/</code><span>Protocol & publication registry</span></div>
            </div>
          </div>
          <div className="terminal" aria-label="Reproducibility commands">
            <div className="terminalBar"><span /><span /><span /><small>research-shell</small></div>
            <pre><code>{`# Python research environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Authorized benchmark download
python scripts/download_kaggle_data.py --dataset all

# Deterministic research run
python -m src.pipeline --config config/research.yaml

# Evidence / publication gate
python scripts/research_gate.py \\
  --run-dir artifacts/runs/<run_id> \\
  --manuscript-source paper/manuscript.md

# Research portal
npm install
npm run build`}</code></pre>
          </div>
        </div>
      </section>

      <section className="section finalCta">
        <div className="shell ctaCard">
          <div>
            <div className="sectionKicker">Open research</div>
            <h2>Trace the claim. Inspect the code. Reproduce the evidence.</h2>
            <p>
              The public portal is designed to support peer review, research collaboration, and a clean path from manuscript claim to machine-readable result.
            </p>
          </div>
          <div className="ctaActions">
            <a className="button buttonPrimary" href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2" target="_blank" rel="noreferrer">Open GitHub repository ↗</a>
            <a className="button buttonGhost" href="#status">View evidence status ↑</a>
          </div>
        </div>
      </section>
    </main>
  );
}
