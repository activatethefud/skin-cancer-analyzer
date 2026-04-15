'use client'

import { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { API_URL, AnalysisResult, getClassLabel, isMalignant } from '@/lib/api'

export default function DashboardPage() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setResult(null)
      setError('')
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(selectedFile)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      setFile(droppedFile)
      setResult(null)
      setError('')
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(droppedFile)
    }
  }

  const handleAnalyze = async () => {
    if (!file) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      })

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem('token')
          router.push('/login')
          return
        }
        const data = await response.json()
        throw new Error(data.detail || 'Analysis failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/login')
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">Skin Cancer Analyzer</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm bg-gray-200 rounded-lg hover:bg-gray-300"
          >
            Logout
          </button>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-lg font-semibold mb-4">Upload Image</h2>
            <div
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition"
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="hidden"
              />
              {preview ? (
                <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded" />
              ) : (
                <p className="text-gray-500">
                  Drag and drop an image or click to select
                </p>
              )}
            </div>
            {file && (
              <p className="mt-2 text-sm text-gray-600">{file.name}</p>
            )}
            <button
              onClick={handleAnalyze}
              disabled={!file || loading}
              className="mt-4 w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-4">Results</h2>
            {error && (
              <div className="p-4 bg-red-100 text-red-700 rounded-lg">{error}</div>
            )}
            {result && (
              <div className="space-y-4">
                <div
                  className={`p-4 rounded-lg ${
                    isMalignant(result.top_prediction)
                      ? 'bg-red-100 border-2 border-red-500'
                      : 'bg-green-100 border-2 border-green-500'
                  }`}
                >
                  <p className="font-semibold text-lg">
                    {getClassLabel(result.top_prediction)}
                  </p>
                  <p className="text-2xl font-bold mt-2">
                    {(result.confidence * 100).toFixed(1)}% confidence
                  </p>
                  {isMalignant(result.top_prediction) && (
                    <p className="text-red-700 mt-2 text-sm">
                      Please consult a dermatologist for proper diagnosis.
                    </p>
                  )}
                </div>
                <div className="border rounded-lg p-4">
                  <p className="font-medium mb-2">All Predictions:</p>
                  <ul className="space-y-1">
                    {result.all_predictions.map((pred) => (
                      <li key={pred.class_name} className="flex justify-between">
                        <span>{getClassLabel(pred.class_name)}</span>
                        <span className="font-mono">
                          {(pred.confidence * 100).toFixed(1)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
