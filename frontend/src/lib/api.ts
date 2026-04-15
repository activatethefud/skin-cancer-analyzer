export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export interface Prediction {
  class_name: string
  confidence: number
}

export interface AnalysisResult {
  id: number
  filename: string
  top_prediction: string
  confidence: number
  all_predictions: Prediction[]
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface User {
  id: number
  username: string
  email: string
}

export const CLASS_LABELS: Record<string, string> = {
  benign: 'Benign lesion',
  malignant: 'Malignant lesion',
}

export function getClassLabel(className: string): string {
  return CLASS_LABELS[className] || className
}

export function isMalignant(className: string): boolean {
  return className === 'malignant'
}
