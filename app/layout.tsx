import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Beyond Static Accuracy | Research Portal",
    template: "%s | Beyond Static Accuracy",
  },
  description:
    "Research portal for temporal stability, probability calibration, explanation stability, cost-sensitive decision value, and reproducibility in banking and insurance customer behavior prediction.",
  keywords: [
    "customer behavior prediction",
    "banking machine learning",
    "insurance machine learning",
    "temporal stability",
    "probability calibration",
    "explainable AI",
    "SHAP stability",
    "cost-sensitive learning",
    "trustworthy AI",
  ],
  authors: [{ name: "Arun Kumar Gharami" }],
  creator: "Arun Kumar Gharami",
  openGraph: {
    title: "Beyond Static Accuracy",
    description:
      "A reproducible research system for trustworthy customer behavior prediction under temporal change.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Beyond Static Accuracy",
    description:
      "Temporal stability, calibration, explanation stability, operational value, and complexity in financial prediction.",
  },
};

const nav = [
  ["Research", "#research"],
  ["Benchmarks", "#benchmarks"],
  ["Evaluation", "#evaluation"],
  ["Pipeline", "#pipeline"],
  ["Status", "#status"],
  ["Reproduce", "#reproduce"],
];

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <header className="siteHeader">
          <div className="shell navWrap">
            <Link className="brand" href="/" aria-label="Research portal home">
              <span className="brandMark" aria-hidden="true">BA</span>
              <span>
                <strong>Beyond Static Accuracy</strong>
                <small>Research Portal · Part 2</small>
              </span>
            </Link>
            <nav className="navLinks" aria-label="Primary navigation">
              {nav.map(([label, href]) => (
                <Link key={href} href={href}>{label}</Link>
              ))}
            </nav>
            <a
              className="button buttonSmall buttonGhost"
              href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2"
              target="_blank"
              rel="noreferrer"
            >
              GitHub ↗
            </a>
          </div>
        </header>
        {children}
        <footer className="footer">
          <div className="shell footerGrid">
            <div>
              <div className="footerTitle">Beyond Static Accuracy</div>
              <p>
                An open, reproducible research system for studying whether financial prediction models remain trustworthy when deployment conditions change.
              </p>
            </div>
            <div>
              <div className="footerLabel">Integrity rule</div>
              <p>No fabricated datasets, metrics, figures, citations, or runtime results.</p>
            </div>
            <div>
              <div className="footerLabel">Repository</div>
              <a href="https://github.com/Arungharami/Customer-Behavior-Prediction-in-Banking-and-Insurance-2" target="_blank" rel="noreferrer">
                Source & reproducibility package ↗
              </a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
