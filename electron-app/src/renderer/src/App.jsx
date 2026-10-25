import { useState, useEffect } from 'react'

export default function App() {
  const [visaData, setVisaData] = useState(null)
  const [showLoading, setShowLoading] = useState(true)
  const [clickCount, setClickCount] = useState(0)

  useEffect(() => {
    window.api.onVisaData((data) => {
      console.log("Render received data:", data)
      setVisaData(data)
      setShowLoading(false)
    })
  }, [])


  useEffect(() => {
    const secretCode = [
      'ArrowUp', 'ArrowUp',
      'ArrowDown', 'ArrowDown',
      'ArrowLeft', 'ArrowRight',
      'ArrowLeft', 'ArrowRight',
      'b', 'a'
    ]
    let inputBuffer = []

    const handleKeyDown = (e) => {
      inputBuffer.push(e.key)

      inputBuffer = inputBuffer.slice(-secretCode.length)

      if (JSON.stringify(inputBuffer) === JSON.stringify(secretCode)) {
        alert("習得がとても速いですね。なぜこんなことをしているのですか？")
        inputBuffer = []
      }
    }

    // Fixed: Actually register the event listener and clean it up
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const handleHardClick = () => {
    setClickCount((prev) => {
      const nextCount = prev + 1
      if (nextCount >= 5) {
        window.api.easterEgg()
        return 0
      }
      return nextCount
    })
  }

  return (
    <div className={'main'}>
      {visaData ? (
        <div className="card-container">
          {visaData.image_url && (
            <div className="my-4 card-deal">
              <img
                src={visaData.image_url}
                alt={`${visaData.rank} of ${visaData.suit}`}
                className="w-32 h-auto rounded shadow-lg border border-red-600/50"
                draggable={false}
                onClick={handleHardClick}
              />
            </div>
          )}

          {visaData.status === "PENALTY" && (
            <>
              <h2 id="status-display">{visaData.label}</h2>
              <h2>PENALTY</h2>
              <p id="details-display">Days Valid: {visaData.days_valid}</p>
              <p id="query-display">Wallpaper Query: {visaData.query}</p>
            </>
          )}

          {visaData.status === "NEW_CARD" && (
            <>
              <h2 id="status-display">{visaData.rank} of {visaData.suit}</h2>
              <p id="details-display">Days Valid: {visaData.days_valid}</p>
              <p id="query-display">Wallpaper Query: {visaData.query}</p>
            </>
          )}

          {visaData.status === "ACTIVE" && (
            <div className="flex flex-col items-center gap-2 mt-4">
              <h2 id="status-display" className="text-2xl font-bold tracking-wide text-amber-300 drop-shadow">
                {visaData.rank} of {visaData.suit} <span className="text-sm font-normal text-emerald-300">(Active)</span>
              </h2>
              <div className="bg-black/30 backdrop-blur-sm border border-white/10 rounded-lg px-4 py-2 mt-2 text-sm space-y-1">
                <p id="details-display" className="text-gray-200">
                  <strong className="text-amber-400">Days Remaining:</strong> {visaData.days_remaining}
                </p>
                <p id="query-display" className="text-gray-300 italic">
                  <strong className="text-amber-400 not-italic">Wallpaper:</strong> "{visaData.query}"
                </p>
              </div>
            </div>
          )}
        </div>
      ) : (
        showLoading && (
          <div className="loading-container" style={{ textAlign: 'center', marginTop: '50px' }}>
            <div className="card-loader">
              <div className="card card-1"></div>
              <div className="card card-2"></div>
              <div className="card card-3"></div>
            </div>
            <h2>Dealing your cardz</h2>
            <p>This might take a moment</p>
          </div>
        )
      )}
    </div>
  )
}
