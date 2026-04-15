import { describe, it, expect } from 'vitest'
import { getClassLabel, isMalignant, API_URL, CLASS_LABELS } from '@/lib/api'

describe('API constants', () => {
  it('API_URL is defined', () => {
    expect(API_URL).toBeDefined()
    expect(typeof API_URL).toBe('string')
  })

  it('CLASS_LABELS contains 2 binary classes', () => {
    expect(Object.keys(CLASS_LABELS)).toHaveLength(2)
    expect(CLASS_LABELS).toHaveProperty('benign')
    expect(CLASS_LABELS).toHaveProperty('malignant')
  })
})

describe('getClassLabel', () => {
  it('returns full label for benign class', () => {
    expect(getClassLabel('benign')).toBe('Benign lesion')
  })

  it('returns full label for malignant class', () => {
    expect(getClassLabel('malignant')).toBe('Malignant lesion')
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
  it('returns true for malignant', () => {
    expect(isMalignant('malignant')).toBe(true)
  })

  it('returns false for benign', () => {
    expect(isMalignant('benign')).toBe(false)
  })

  it('returns false for unknown class', () => {
    expect(isMalignant('unknown')).toBe(false)
  })

  it('returns false for empty string', () => {
    expect(isMalignant('')).toBe(false)
  })
})
