import { describe, it, expect } from 'vitest'
import { getClassLabel, isMalignant } from '@/lib/api'

describe('API utilities', () => {
  describe('getClassLabel', () => {
    it('returns label for benign class', () => {
      expect(getClassLabel('benign')).toBe('Benign lesion')
    })

    it('returns label for malignant class', () => {
      expect(getClassLabel('malignant')).toBe('Malignant lesion')
    })

    it('returns class name for unknown class', () => {
      expect(getClassLabel('unknown')).toBe('unknown')
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
  })
})
