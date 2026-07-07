import React, { useState, useEffect } from 'react';
import { ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine, Scatter, ResponsiveContainer } from 'recharts';

const MacroSimulator = () => {
  // Stati per le variabili esogene (Slider)
  const [G, setG] = useState(30);
  const [T, setT] = useState(30);
  const [M, setM] = useState(350);
  const [A, setA] = useState(1.0);
  
  // Stato per l'Aggiustamento Animato
  const [autoAdjust, setAutoAdjust] = useState(true);
  
  // Stato per i Prezzi (P)
  const [currentP, setCurrentP] = useState(1.0);
  const [animStatus, setAnimStatus] = useState('stable'); // 'stable', 'waiting', 'adjusting'
  const [initialP, setInitialP] = useState(1.0);

  // --- MOTORE MATEMATICO ---
  // Pieno impiego (FE / LRAS)
  const Y_fe = 200 * A;
  
  // Parametri IS
  const A_is = 110 + G - 0.5 * T;
  const m_is = -0.05;
  const q_is = A_is / 10;
  
  // Tasso di interesse di pieno impiego
  const r_fe = q_is + m_is * Y_fe;
  
  // Domanda di moneta e Prezzo Target (Lungo Periodo)
  const L_req = Math.max(0.1, 2 * Y_fe - 20 * r_fe);
  const targetP = M / L_req;

  // Effetto di Animazione per l'aggiustamento dei prezzi
  useEffect(() => {
    if (!autoAdjust) return;
    
    if (Math.abs(currentP - targetP) > 0.01) {
      if (animStatus === 'stable') {
        setAnimStatus('waiting');
        setInitialP(currentP);
      }
      
      const waitTimeout = setTimeout(() => {
        setAnimStatus('adjusting');
        
        const adjustInterval = setInterval(() => {
          setCurrentP(prev => {
            const diff = targetP - prev;
            if (Math.abs(diff) < 0.01) {
              clearInterval(adjustInterval);
              setAnimStatus('stable');
              return targetP;
            }
            return prev + diff * 0.05; // Lerp per un'animazione fluida
          });
        }, 30); // 30ms per circa 30fps
        
        return () => clearInterval(adjustInterval);
      }, 1500); // 1.5 secondi di attesa per mostrare il breve periodo
      
      return () => clearTimeout(waitTimeout);
    } else {
      setAnimStatus('stable');
    }
  }, [G, T, M, A, targetP, autoAdjust, currentP, animStatus]);

  // Generazione dei Dati per i Grafici
  const generateChartData = () => {
    const data = [];
    for (let Y = 10; Y <= 500; Y += 10) {
      // IS
      const r_is = q_is + m_is * Y;
      // LM
      const r_lm = -(M / currentP) / 20 + 0.1 * Y;
      // AD
      const denom_ad = 0.15 * Y - q_is;
      let p_ad = null;
      if (denom_ad > 0.05) { // Evita asintoti ed errori matematici
        p_ad = (M / 20) / denom_ad;
        if (p_ad > 5) p_ad = null; // Taglia i valori estremi per il grafico
      }
      
      data.push({ Y, r_is, r_lm, p_ad });
    }
    return data;
  };

  const chartData = generateChartData();
  
  // Calcolo Equilibrio di Breve Periodo
  const Y_star = (q_is - (-(M / currentP) / 20)) / 0.15;
  const r_star = q_is + m_is * Y_star;

  return (
    <div style={{ display: 'flex', fontFamily: 'sans-serif', height: '100vh' }}>
      
      {/* SIDEBAR - CONTROLLI */}
      <div style={{ width: '25%', padding: '20px', backgroundColor: '#f4f4f4', borderRight: '1px solid #ccc' }}>
        <h3>Pannello di Controllo</h3>
        
        <label style={{ display: 'block', marginBottom: '20px' }}>
          <input 
            type="checkbox" 
            checked={autoAdjust} 
            onChange={(e) => setAutoAdjust(e.target.checked)} 
          />
          <b> Aggiustamento Prezzi (Lungo Periodo)</b>
        </label>

        <div style={{ marginBottom: '15px' }}>
          <label>Spesa Pubblica (G): {G}</label>
          <input type="range" min="0" max="100" value={G} onChange={e => setG(Number(e.target.value))} style={{ width: '100%' }} />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Tasse (T): {T}</label>
          <input type="range" min="0" max="100" value={T} onChange={e => setT(Number(e.target.value))} style={{ width: '100%' }} />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>Offerta di Moneta (M): {M}</label>
          <input type="range" min="100" max="600" step="10" value={M} onChange={e => setM(Number(e.target.value))} style={{ width: '100%' }} />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>Shock Produttività (A): {A.toFixed(1)}</label>
          <input type="range" min="0.5" max="2.0" step="0.1" value={A} onChange={e => setA(Number(e.target.value))} style={{ width: '100%' }} />
        </div>
        
        {!autoAdjust && (
          <div style={{ marginBottom: '15px', color: 'red' }}>
            <label>Livello Prezzi Manuale (P): {currentP.toFixed(2)}</label>
            <input type="range" min="0.5" max="3.0" step="0.05" value={currentP} onChange={e => setCurrentP(Number(e.target.value))} style={{ width: '100%' }} />
          </div>
        )}
      </div>

      {/* MAIN AREA - GRAFICI */}
      <div style={{ width: '75%', padding: '20px', display: 'flex', flexDirection: 'column' }}>
        
        {/* GRAFICO 1: IS-LM-FE */}
        <div style={{ flex: 1, minHeight: '300px' }}>
          <h4 style={{ textAlign: 'center', margin: '5px' }}>Modello IS-LM-FE (Mercato dei Beni e Moneta)</h4>
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Y" type="number" domain={[0, 500]} label={{ value: 'Output (Y)', position: 'insideBottomRight', offset: -5 }} />
              <YAxis domain={[-2, 15]} label={{ value: 'Tasso r', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Line type="monotone" dataKey="r_is" stroke="red" strokeWidth={2} dot={false} isAnimationActive={false} name="IS" />
              <Line type="monotone" dataKey="r_lm" stroke="blue" strokeWidth={2} dot={false} isAnimationActive={false} name="LM" />
              <ReferenceLine x={Y_fe} stroke="green" strokeWidth={2} label="FE" />
              <Scatter data={[{ Y: Y_star, r_is: r_star }]} fill="black" />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* GRAFICO 2: AD-AS */}
        <div style={{ flex: 1, minHeight: '300px' }}>
          <h4 style={{ textAlign: 'center', margin: '5px' }}>Modello AD-AS (Livello dei Prezzi)</h4>
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Y" type="number" domain={[0, 500]} label={{ value: 'Output (Y)', position: 'insideBottomRight', offset: -5 }} />
              <YAxis domain={[0, 4]} label={{ value: 'Prezzi (P)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Line type="monotone" dataKey="p_ad" stroke="purple" strokeWidth={2} dot={false} isAnimationActive={false} name="AD" />
              <ReferenceLine x={Y_fe} stroke="green" strokeWidth={2} label="LRAS" />
              <ReferenceLine y={currentP} stroke="orange" strokeDasharray="5 5" strokeWidth={2} label="SRAS" />
              <Scatter data={[{ Y: Y_star, p_ad: currentP }]} fill="black" />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* PANNELLO TELECRONACA */}
        <div style={{ 
          marginTop: '15px', padding: '15px', borderRadius: '8px',
          backgroundColor: animStatus === 'stable' ? '#d4edda' : animStatus === 'waiting' ? '#fff3cd' : '#d1ecf1',
          color: animStatus === 'stable' ? '#155724' : animStatus === 'waiting' ? '#856404' : '#0c5460'
        }}>
          <b>Dinamica dei Mercati: </b>
          {animStatus === 'waiting' && `⚠️ SHOCK DI BREVE PERIODO! Prezzi vischiosi a P=${currentP.toFixed(2)}. L'economia è fuori dal pieno impiego. L'intersezione AD-SRAS è spostata rispetto alla LRAS.`}
          {animStatus === 'adjusting' && `🔄 AGGIUSTAMENTO... I prezzi stanno reagendo. La retta orizzontale SRAS scorre verso il nuovo equilibrio, contraendo/espandendo (M/P) e trascinando la LM.`}
          {animStatus === 'stable' && (
            <span>
              ✅ STEADY STATE. Prezzi stabilizzati a P={currentP.toFixed(2)}. 
              {targetP > initialP ? " L'eccesso di domanda ha generato INFLAZIONE, spostando la SRAS in alto e la LM in alto per riassorbire lo shock." : 
               targetP < initialP ? " La carenza di domanda ha generato DEFLAZIONE, spostando la SRAS in basso e stimolando l'economia." : 
               " Mercati in perfetto equilibrio al livello naturale."}
            </span>
          )}
        </div>

      </div>
    </div>
  );
};

export default MacroSimulator;