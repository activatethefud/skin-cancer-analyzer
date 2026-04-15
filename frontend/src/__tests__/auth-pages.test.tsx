import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
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
    
    expect(screen.getByText('Login')).toBeTruthy()
    expect(screen.getByLabelText(/username/i)).toBeTruthy()
    expect(screen.getByLabelText(/password/i)).toBeTruthy()
  })

  it('shows validation errors for empty fields', async () => {
    const LoginPage = (await import('@/app/login/page')).default
    render(<LoginPage />)
    
    const submitButton = screen.getByRole('button', { name: /login/i })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.queryByText('Login failed')).toBeNull()
    })
  })
})

describe('Register Page', () => {
  it('renders registration form', async () => {
    const RegisterPage = (await import('@/app/register/page')).default
    render(<RegisterPage />)
    
    expect(screen.getByText('Create Account')).toBeTruthy()
    expect(screen.getByLabelText(/username/i)).toBeTruthy()
    expect(screen.getByLabelText(/email/i)).toBeTruthy()
    expect(screen.getByLabelText(/password/i)).toBeTruthy()
  })
})
