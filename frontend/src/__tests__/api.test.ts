import { describe, it, expect } from 'vitest'
import { getClassLabel, isMalignant, AnalysisResult } from '@/lib/api'

describe('API utilities', () => {
  describe('getClassLabel', () => {
    it('returns label for nv class', () => {
      expect(getClassLabel('nv')).toBe('Melanocytic nevi (benign)')
    })

    it('returns label for mel class', () => {
      expect(getClassLabel('mel')).toBe('Melanoma (malignant)')
    })

    it('returns label for bcc class', () => {
      expect(getClassLabel('bcc')).toBe('Basal cell carcinoma')
    })

    it('returns class name for unknown class', () => {
      expect(getClassLabel('unknown')).toBe('unknown')
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
  })
})
