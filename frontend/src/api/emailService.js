const API_URL = import.meta.env.VITE_API_URL

export async function fetchEmails() {
  const response = await fetch(`${API_URL}/api/emails`)
  if (!response.ok) {
    throw new Error('Failed to fetch emails')
  }
  return response.json()
}