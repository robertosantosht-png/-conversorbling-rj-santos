'use client';

import { useState } from 'react';

export default function ConversorPage() {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    xml: null as File | null,
    nome: '',
    email: '',
    markup: '',
    cest: '',
    modo_conversao: 'Simples',
    marca_padrao: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setFormData(prev => ({ ...prev, xml: file }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.xml) {
      alert('Por favor, selecione um arquivo XML.');
      return;
    }
    setLoading(true);

    const data = new FormData();
    data.append('xml', formData.xml);
    data.append('nome', formData.nome);
    data.append('email', formData.email);
    data.append('markup', formData.markup);
    data.append('cest', formData.cest);
    data.append('modo_conversao', formData.modo_conversao);
    data.append('marca_padrao', formData.marca_padrao);

    try {
      const response = await fetch('/api/conversor', {
        method: 'POST',
        body: data,
      });

      if (!response.ok) {
        throw new Error('Erro na conversão');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'planilha_bling.xlsx';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Erro ao processar a conversão: ' + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Conversor de XML para Planilha Bling</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Arquivo XML</label>
            <input
              type="file"
              accept=".xml"
              onChange={handleFileChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Nome</label>
            <input
              type="text"
              name="nome"
              value={formData.nome}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Markup (%)</label>
            <input
              type="number"
              name="markup"
              value={formData.markup}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">CEST</label>
            <input
              type="text"
              name="cest"
              value={formData.cest}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Modo de Conversão</label>
            <select
              name="modo_conversao"
              value={formData.modo_conversao}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
            >
              <option value="Simples">Simples</option>
              <option value="Variação">Variação</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Marca Padrão</label>
            <input
              type="text"
              name="marca_padrao"
              value={formData.marca_padrao}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? 'Convertendo...' : 'Converter'}
          </button>
        </form>
      </div>
    </div>
  );
}