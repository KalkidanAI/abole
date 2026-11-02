import type { DiseaseInfo } from '../types';

interface DiseaseInfoCardProps {
  info: DiseaseInfo;
  disclaimer: string;
}

export function DiseaseInfoCard({ info, disclaimer }: DiseaseInfoCardProps) {
  return (
    <div className="disease-info-card">
      <div className="disease-info-header">
        <h3>{info.name}</h3>
        <p className="scientific-name">{info.scientific_name}</p>
      </div>
      <p className="disease-description">{info.description}</p>
      {info.ethiopian_context && (
        <div className="info-section ethiopian-context">
          <h4>Ethiopian Context</h4>
          <p>{info.ethiopian_context}</p>
        </div>
      )}
      <div className="info-section">
        <h4>Symptoms</h4>
        <ul className="info-list">{info.symptoms.map((s, i) => <li key={i}>{s}</li>)}</ul>
      </div>
      <div className="info-section">
        <h4>Management Practices</h4>
        <ul className="info-list">{info.management_practices.map((p, i) => <li key={i}>{p}</li>)}</ul>
      </div>
      <div className="info-section citations">
        <h4>References</h4>
        <ul className="citation-list">{info.citations.map((c, i) => <li key={i}>{c}</li>)}</ul>
      </div>
      <div className="disclaimer-box"><p>{disclaimer}</p></div>
    </div>
  );
}
