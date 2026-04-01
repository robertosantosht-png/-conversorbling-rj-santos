'use client';

import { useState } from 'react';

export default function ConversorBling() {
  const [file, setFile] = useState<File | null>(null);
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [markup, setMarkup] = useState('');
  const [cest, setCest] = useState('');
  const [modo, setModo] = useState('Simples');
  const [marcaPadrao, setMarcaPadrao] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return alert('Envie o arquivo XML.');

    const formData = new FormData();
    formData.append('xml', file);
    formData.append('nome', nome);
    formData.append('email', email);
    formData.append('markup', markup);
    formData.append('cest', cest);
    formData.append('modo_conversao', modo);
    formData.append('marca_padrao', marcaPadrao);

    setLoading(true);

    try {
      const res = await fetch('/api/conversor', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const err = await res.json();
        alert(`Erro: ${err.error}`);
        return;
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `planilha_bling.xlsx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      alert('Erro ao conectar ao servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 to-blue-200 p-6">
      <div className="bg-white shadow-2xl rounded-3xl p-10 max-w-xl w-full">
        
        <h1 className="text-4xl font-extrabold text-center mb-8 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Conversor XML → Bling
        </h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">

          {/* XML */}
          <div>
            <label className="font-semibold">XML do Produto *</label>
            <input
              type="file"
              accept=".xml"
              required
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
            />
          </div>

          {/* Nome */}
          <div>
            <label className="font-semibold">Nome *</label>
            <input
              type="text"
              required
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
              placeholder="Seu nome"
            />
          </div>

          {/* Email */}
          <div>
            <label className="font-semibold">Email *</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
              placeholder="seu@email.com"
            />
          </div>

          {/* Markup */}
          <div>
            <label className="font-semibold">Markup (ex: 1.3) *</label>
            <input
              type="number"
              step="0.01"
              required
              value={markup}
              onChange={(e) => setMarkup(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
              placeholder="1.3"
            />
          </div>

          {/* CEST */}
          <div>
            <label className="font-semibold">CEST *</label>
            <input
              type="text"
              required
              value={cest}
              onChange={(e) => setCest(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
              placeholder="Digite o CEST"
            />
          </div>

          {/* Modo de conversão */}
          <div>
            <label className="font-semibold">Modo de Conversão *</label>
            <select
              value={modo}
              onChange={(e) => setModo(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
            >
              <option value="Simples">Simples</option>
              <option value="Variação">Variação</option>
            </select>
          </div>

          {/* Marca Padrão */}
          <div>
            <label className="font-semibold">Marca Padrão *</label>
            <input
              type="text"
              required
              value={marcaPadrao}
              onChange={(e) => setMarcaPadrao(e.target.value)}
              className="w-full p-3 border-2 border-gray-300 rounded-lg"
              placeholder="Ex: LANÇA PERFUME"
            />
          </div>

          {/* Botão */}
          <button
            type="submit"
            disabled={loading}
            className={`py-4 text-xl font-bold rounded-xl text-white transition-all
                        ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700 shadow-xl'}`}
          >
            {loading ? 'Processando...' : 'Gerar Planilha XLSX'}
          </button>
        </form>
      </div>
    </main>
  );
}