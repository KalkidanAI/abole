export interface ClassProbability {
  class_name: string;
  probability: number;
}

export interface DiseaseInfo {
  name: string;
  scientific_name: string;
  description: string;
  symptoms: string[];
  management_practices: string[];
  ethiopian_context: string | null;
  citations: string[];
}

export interface PredictionResponse {
  predicted_class: string;
  confidence: number;
  all_probabilities: ClassProbability[];
  disease_info: DiseaseInfo;
  warnings: string[];
  disclaimer: string;
  is_demo_prediction: boolean;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  demo_mode: boolean;
  version: string;
}
