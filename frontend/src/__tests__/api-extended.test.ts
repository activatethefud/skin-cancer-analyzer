import { describe, it, expect } from 'vitest'
import { getClassLabel, isMalignant, API_URL, CLASS_LABELS } from '@/lib/api'

describe('API constants', () => {
  it('API_URL is defined', () => {
    expect(API_URL).toBeDefined()
    expect(typeof API_URL).toBe('string')
  })

  it('CLASS_LABELS contains all 7 classes', () => {
    expect(Object.keys(CLASS_LABELS)).toHaveLength(7)
    expect(CLASS_LABELS).toHaveProperty('nv')
    expect(CLASS_LABELS).toHaveProperty('mel')
    expect(CLASS_LABELS).toHaveProperty('bkl')
    expect(CLASS_LABELS).toHaveProperty('vasc')
    expect(CLASS_LABELS).toHaveProperty('bcc')
    expect(CLASS_LABELS).toHaveProperty('akiec')
    expect(CLASS_LABELS).toHaveProperty('df')
  })
})

describe('getClassLabel', () => {
  it('returns full label for nv class', () => {
    expect(getClassLabel('nv')).toBe('Melanocytic nevi (benign)')
  })

  it('returns full label for mel class', () => {
    expect(getClassLabel('mel')).toBe('Melanoma (malignant)')
  })

  it('returns full label for bkl class', () => {
    expect(getClassLabel('bkl')).toBe('Benign keratosis')
  })

  it('returns full label for vasc class', () => {
    expect(getClassLabel('vasc')).toBe('Vascular lesions')
  })

  it('returns full label for bcc class', () => {
    expect(getClassLabel('bcc')).toBe('Basal cell carcinoma')
  })

  it('returns full label for akiec class', () => {
    expect(getClassLabel('akiec')).toBe('Actinic keratoses')
  })

  it('returns full label for df class', () => {
    expect(getClassLabel('df')).toBe('Dermatofibroma')
  })

  it('returns class name for unknown class', () => {
    expect(getClassLabel('unknown')).toBe('unknown')
    expect(getClassLabel('xyz')).toBe('xyz')
  })

  it('returns empty string for empty input', () => {
    expect(getClassLabel('')).toBe('')
  })
})

describe('isMalignant', () => {
  it('returns true for melanoma', () => {
    expect(isMalignant('mel')).toBe(true)
  })

  it('returns true for basal cell carcinoma', () => {
    expect(isMalignant('bcc')).toBe(true)
  })

  it('returns true for actinic keratoses', () => {
    expect(isMalignant('akiec')).toBe(true)
  })

  it('returns false for melanocytic nevi', () => {
    expect(isMalignant('nv')).toBe(false)
  })

  it('returns false for benign keratosis', () => {
    expect(isMalignant('bkl')).toBe(false)
  })

  it('returns false for vascular lesions', () => {
    expect(isMalignant('vasc')).toBe(false)
  })

  it('returns false for dermatofibroma', () => {
    expect(isMalignant('df')).toBe(false)
  })

  it('returns false for unknown class', () => {
    expect(isMalignant('unknown')).toBe(false)
  })

  it('returns false for empty string', () => {
    expect(isMalignant('')).toBe(false)
  })
})
