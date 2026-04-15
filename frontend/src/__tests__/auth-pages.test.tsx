import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { useRouter } from 'next/navigation'

vi.mock('next/navigation', () => ({
  useRouter: vi.fn()
}))

const mockPush = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
  ;(useRouter as any).mockReturnValue({ push: mockPush })
  localStorage.clear()
})

describe('Login Page', () => {
  it('renders login form', async () => {
    const LoginPage = (await import('@/app/login/page')).default
    render(<LoginPage />)
    
    expect(screen.getByRole('heading', { name: 'Login' })).toBeTruthy()
    expect(screen.getByPlaceholderText('Username')).toBeTruthy()
    expect(screen.getByPlaceholderText('Password')).toBeTruthy()
  })
})

describe('Register Page', () => {
  it('renders registration form', async () => {
    const RegisterPage = (await import('@/app/register/page')).default
    render(<RegisterPage />)
    
    expect(screen.getByRole('heading', { name: 'Create Account' })).toBeTruthy()
    expect(screen.getAllByPlaceholderText('Email').length).toBeGreaterThan(0)
  })
})
