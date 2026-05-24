import React, { useEffect, useRef, useState } from 'react';

const API_BASE = 'https://movie-recommendations-z04q.onrender.com';

export default function App() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const boxRef = useRef(null);

  useEffect(() => {
    const delay = setTimeout(async () => {
      if (!query.trim()) {
        setSuggestions([]);
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}`);
        const data = await res.json();
        setSuggestions(Array.isArray(data) ? data : []);
      } catch {
        setSuggestions([]);
      }
    }, 250);

    return () => clearTimeout(delay);
  }, [query]);

  useEffect(() => {
    function handleOutsideClick(e) {
      if (boxRef.current && !boxRef.current.contains(e.target)) {
        setShowSuggestions(false);
      }
    }

    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  async function handleRecommend(movieName) {
    const finalName = (movieName || selectedMovie || query).trim();

    if (!finalName) {
      setError('Please enter a movie name.');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const res = await fetch(`${API_BASE}/recommend?movie=${encodeURIComponent(finalName)}`);
      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Unable to fetch recommendations.');
      } else {
        setSelectedMovie(finalName);
        setResults(Array.isArray(data) ? data : []);
      }
    } catch {
      setError('Cannot connect to backend. Make sure Flask is running on port 3000.');
    } finally {
      setLoading(false);
      setShowSuggestions(false);
    }
  }

  function selectSuggestion(movie) {
    setQuery(movie);
    setSelectedMovie(movie);
    setShowSuggestions(false);
    handleRecommend(movie);
  }

  return (
    <main className="app">
      <div className="bg-layer" />
      <section className="panel">
        <p className="eyebrow">Cinematic Discovery</p>
        <h1>Movie Recommender</h1>
        <p className="subtext">Pick a movie you love and get your next watchlist instantly.</p>

        <div className="search-wrap" ref={boxRef}>
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setShowSuggestions(true);
            }}
            onFocus={() => setShowSuggestions(true)}
            placeholder="Type a movie name..."
          />
          <button onClick={() => handleRecommend()}>Recommend</button>

          {showSuggestions && suggestions.length > 0 && (
            <ul className="suggestions">
              {suggestions.map((movie) => (
                <li key={movie}>
                  <button onClick={() => selectSuggestion(movie)}>{movie}</button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {loading && <p className="status">Finding great matches...</p>}
        {error && <p className="status error">{error}</p>}

        {results.length > 0 && (
          <div className="results">
            <h2>Because you liked {selectedMovie}</h2>
            <div className="cards">
              {results.map((movie, idx) => (
                <article className="card" key={`${movie.movie_id || movie.title}-${idx}`}>
                  <span>{String(idx + 1).padStart(2, '0')}</span>
                  {movie.poster ? (
                    <img src={movie.poster} alt={movie.title} className="poster" loading="lazy" />
                  ) : null}
                  <div>
                    <p>{movie.title || 'Unknown title'}</p>
                    {movie.rating ? <small>Rating: {movie.rating}/10</small> : null}
                  </div>
                </article>
              ))}
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
