import axios from 'axios';
import type { PredictionResponse, HealthResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || '/api';
const API_KEY = import.meta.env.VITE_API_KEY || 'abole-demo-key-change-me';

export async function predictImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_URL}/predict`, formData, {
    headers: { 'X-API-Key': API_KEY, 'Content-Type': 'multipart/form-data' },
    timeout: 30000,
  });
  return response.data;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await axios.get(`${API_URL}/health`, { timeout: 5000 });
  return response.data;
}
