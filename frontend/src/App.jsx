import { useState, useEffect } from 'react'
import { CATEGORIES, URGENCY, USER_PROFILE } from './config/categories'
import { fetchEmails } from './api/emailService'

const MOCK_EMAILS = []

function UrgencyBadge({ urgency }) {
  const style = URGENCY[urgency]?.color || 'bg-gray-100 text-gray-600'
  return (
    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${style}`}>
      {urgency}
    </span>
  )
}

function EmailList({ emails, onSelect, selectedId }) {
  return (
    <div className="divide-y divide-gray-100">
      {emails.length === 0 && (
        <p className="text-center text-gray-400 py-12 text-sm">No emails in this category</p>
      )}
      {emails.map(email => (
        <div
          key={email.id}
          onClick={() => onSelect(email)}
          className={`p-4 cursor-pointer transition-colors ${
            selectedId === email.id ? 'bg-blue-50' : 'hover:bg-gray-50'
          } ${!email.read ? 'border-l-4 border-l-blue-500' : ''}`}
        >
          <div className="flex justify-between items-start gap-2">
            <div className="flex-1 min-w-0">
              <p className={`text-sm truncate ${!email.read ? 'font-semibold text-gray-900' : 'text-gray-700'}`}>
                {email.sender}
              </p>
              <p className="text-sm text-gray-600 truncate">{email.subject}</p>
              <p className="text-xs text-gray-400 mt-1 truncate">{email.summary}</p>
            </div>
            <div className="flex flex-col items-end gap-1 shrink-0">
              <UrgencyBadge urgency={email.urgency} />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

function EmailDetail({ email, onBack, isMobile }) {
  const [draft, setDraft] = useState(email.draft_reply || email.draftReply || '')
  const [sent, setSent] = useState(false)

  function handleSend() {
    setSent(true)
    setTimeout(() => setSent(false), 3000)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 p-4 border-b border-gray-100">
        {isMobile && (
          <button onClick={onBack} className="text-blue-500 text-sm font-medium">← Back</button>
        )}
        <UrgencyBadge urgency={email.urgency} />
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <div>
          <h2 className="text-base font-semibold text-gray-900">{email.subject}</h2>
          <p className="text-sm text-gray-500 mt-0.5">{email.sender} · {email.senderEmail}</p>
          <p className="text-xs text-gray-400 mt-0.5">{email.date}</p>
        </div>

        <div className="bg-gray-50 rounded-xl p-4">
          <p className="text-sm text-gray-700 leading-relaxed">{email.body}</p>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">AI Draft Reply</p>
            <span className="text-xs text-blue-400">Editable</span>
          </div>
          <textarea
            value={draft}
            onChange={e => setDraft(e.target.value)}
            rows={6}
            className="w-full text-sm text-gray-700 bg-white border border-gray-200 rounded-xl p-3 leading-relaxed focus:outline-none focus:ring-2 focus:ring-blue-300 resize-none"
          />
        </div>
      </div>

      <div className="p-4 border-t border-gray-100 flex gap-3">
        <button
          onClick={handleSend}
          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white text-sm font-semibold py-3 rounded-xl transition-colors"
        >
          {sent ? '✓ Sent' : 'Send Reply'}
        </button>
        <button
          onClick={isMobile ? onBack : () => {}}
          className="px-4 py-3 text-sm text-gray-500 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors"
        >
          Discard
        </button>
      </div>
    </div>
  )
}

function Sidebar({ activeCategory, setActiveCategory, emails, onSelect, selectedId }) {
  const filtered = activeCategory === 'all'
    ? emails
    : emails.filter(e => e.category === activeCategory)

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 pt-8 pb-3 border-b border-gray-100">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Inbox</h1>
            <p className="text-xs text-gray-400">{USER_PROFILE.name} · {USER_PROFILE.role}</p>
          </div>
          <div className="w-9 h-9 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-semibold">
            {USER_PROFILE.name.charAt(0)}
          </div>
        </div>
        <div className="flex gap-2 overflow-x-auto pb-1">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`shrink-0 text-xs font-medium px-3 py-1.5 rounded-full transition-colors ${
                activeCategory === cat.id
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto">
        <div className="px-4 py-2 border-b border-gray-50">
          <p className="text-xs text-gray-400">{filtered.length} emails</p>
        </div>
        <EmailList emails={filtered} onSelect={onSelect} selectedId={selectedId} />
      </div>
    </div>
  )
}

export default function App() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [selectedEmail, setSelectedEmail] = useState(null)
  const [emails, setEmails] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchEmails()
      .then(data => {
        setEmails(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const filtered = activeCategory === 'all'
    ? emails
    : emails.filter(e => e.category === activeCategory)

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center text-gray-400 text-sm">
      Loading emails...
    </div>
  )

  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-400 text-sm">
      {error}
    </div>
  )

  return (
    <>
      {/* Desktop layout */}
      <div className="hidden md:flex h-screen bg-gray-50">
        <div className="w-80 lg:w-96 bg-white border-r border-gray-100 flex flex-col shrink-0">
          <Sidebar
            activeCategory={activeCategory}
            setActiveCategory={setActiveCategory}
            emails={emails}
            onSelect={setSelectedEmail}
            selectedId={selectedEmail?.id}
          />
        </div>
        <div className="flex-1 bg-white">
          {selectedEmail ? (
            <EmailDetail email={selectedEmail} isMobile={false} />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-300 text-sm">
              Select an email to view
            </div>
          )}
        </div>
      </div>

      {/* Mobile layout */}
      <div className="md:hidden min-h-screen bg-gray-50 flex flex-col max-w-lg mx-auto">
        {!selectedEmail && (
          <>
            <div className="bg-white px-4 pt-10 pb-3 border-b border-gray-100 sticky top-0 z-10">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Inbox</h1>
                  <p className="text-xs text-gray-400">{USER_PROFILE.name} · {USER_PROFILE.role}</p>
                </div>
                <div className="w-9 h-9 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-semibold">
                  {USER_PROFILE.name.charAt(0)}
                </div>
              </div>
              <div className="flex gap-2 overflow-x-auto pb-1">
                {CATEGORIES.map(cat => (
                  <button
                    key={cat.id}
                    onClick={() => setActiveCategory(cat.id)}
                    className={`shrink-0 text-xs font-medium px-3 py-1.5 rounded-full transition-colors ${
                      activeCategory === cat.id
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex-1 bg-white mt-2 rounded-t-2xl overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-50">
                <p className="text-xs text-gray-400">{filtered.length} emails</p>
              </div>
              <EmailList emails={filtered} onSelect={setSelectedEmail} selectedId={selectedEmail?.id} />
            </div>
          </>
        )}
        {selectedEmail && (
          <div className="flex-1 bg-white min-h-screen">
            <EmailDetail email={selectedEmail} onBack={() => setSelectedEmail(null)} isMobile={true} />
          </div>
        )}
      </div>
    </>
  )
}