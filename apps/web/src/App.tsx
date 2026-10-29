import { useEffect, useState } from 'react';
import { getHealth } from './services/api';

type ApiStatus = 'checking' | 'online' | 'offline';

const modules = [
  { index: '01', title: 'Guided capture', details: 'Camera framing, image quality and capture flow', status: 'Planned' },
  { index: '02', title: 'Visual screening', details: 'Assigned six-class dataset and trained classifier', status: 'Dataset pending' },
  { index: '03', title: 'Understanding', details: 'Reviewed information, explanations and agent tools', status: 'Planned' },
  { index: '04', title: 'Costs & clinics', details: 'MOH / CHAS / CPF references and clinic discovery', status: 'Planned' },
];

function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>('checking');
  useEffect(() => {
    const controller = new AbortController();
    getHealth(controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) setApiStatus(result.status === 'ok' ? 'online' : 'offline');
      })
      .catch(() => {
        if (!controller.signal.aborted) setApiStatus('offline');
      });
    return () => controller.abort();
  }, []);

  return (
    <main className="page">
      <header className="topbar">
        <div className="wordmark">IT2226 <span>/</span> GROUP 07</div>
        <div className={`status status--${apiStatus}`}><i aria-hidden="true" /> API {apiStatus}</div>
      </header>
      <section className="hero" aria-labelledby="hero-title">
        <div className="eyebrow">Dental health · Singapore · Prototype scaffold</div>
        <h1 id="hero-title">A clearer view.<br /><em>A better next step.</em></h1>
        <p>Photo guidance, visual screening, understandable information, and a practical way to explore dental care. This repository is ready for your team to start building.</p>
        <div className="hero-meta"><span>4 proposed capabilities</span><span>Colab-first training</span><span>Local development</span></div>
      </section>
      <section className="modules" aria-label="Planned project capabilities">
        <div className="section-heading"><span>PROJECT MODULES</span><span>00 / 04 IMPLEMENTED</span></div>
        {modules.map((module) => (
          <article className="module" key={module.index}>
            <span className="module-number">{module.index}</span>
            <div><h2>{module.title}</h2><p>{module.details}</p></div>
            <span className="module-status">{module.status}</span>
          </article>
        ))}
      </section>
      <footer><span>Initial scaffold · No model connected</span><span>Web → FastAPI → future ML and tools</span></footer>
    </main>
  );
}

export default App;
