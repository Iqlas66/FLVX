import { useState, useEffect } from 'react'

export default function App() {
  const [visaData, setVisaData] = useState(null)
  const [showLoading, setShowLoading] = useState(false)


  useEffect(() => {
    const  timer = setTimeout(() =>{
      setShowLoading(true)
    },5000)
    window.api.onVisaData((data) => {
      console.log("Render received data:", data)
      setVisaData(data)
      clearTimeout(timer)
    })
    return() => clearTimeout(timer)
  }, [])

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
              />
            </div>
          )}

          {visaData.status === "PENALTY" && (
            <>
              <h2 id="status-display">{visaData.label}</h2>
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
            <>
              <h2 id="status-display">{visaData.rank} of {visaData.suit} (Active)</h2>
              <p id="details-display">Days Remaining: {visaData.days_remaining}</p>
              <p id="query-display">Wallpaper Query: {visaData.query}</p>
            </>
          )}
        </div>
      ) : (
        showLoading &&  <p>Waiting for Visa Data from Python...</p>
      )}
    </div>
  )
}
