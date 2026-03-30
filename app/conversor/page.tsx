import Link from 'next/link';

export default function Page() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 font-sans">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center min-h-screen px-4 text-center bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <h1 className="text-5xl md:text-7xl font-bold mb-4 drop-shadow-lg">
          Conversor XML → Excel
        </h1>
        <p className="text-xl md:text-2xl mb-8 max-w-2xl drop-shadow-md">
          Transforme seus arquivos XML em planilhas Excel de forma rápida, fácil e precisa. Ideal para lojistas e profissionais.
        </p>
        <Link
          href="/conversor"
          className="bg-white text-blue-600 px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transition duration-300 shadow-lg"
        >
          Começar Agora
        </Link>
      </section>

      {/* Como Funciona */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12 text-gray-800">Como Funciona</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <div className="text-6xl mb-4">📤</div>
              <h3 className="text-2xl font-semibold mb-2">1. Faça Upload</h3>
              <p className="text-gray-600">Envie seu arquivo XML de forma segura e rápida.</p>
            </div>

            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <div className="text-6xl mb-4">⚙️</div>
              <h3 className="text-2xl font-semibold mb-2">2. Converta</h3>
              <p className="text-gray-600">
                Nossa ferramenta processa e converte automaticamente para Excel.
              </p>
            </div>

            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <div className="text-6xl mb-4">📊</div>
              <h3 className="text-2xl font-semibold mb-2">3. Baixe</h3>
              <p className="text-gray-600">
                Receba sua planilha Excel pronta para uso.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Vantagens */}
      <section className="py-16 px-4 bg-gray-100">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12 text-gray-800">Vantagens</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">Rápido</h3>
              <p className="text-gray-600">Conversão em segundos.</p>
            </div>

            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold mb-2">Seguro</h3>
              <p className="text-gray-600">Seus dados protegidos.</p>
            </div>

            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Preciso</h3>
              <p className="text-gray-600">Mantém a integridade dos dados.</p>
            </div>

            <div className="p-6 bg-white rounded-lg shadow-md">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-semibold mb-2">Gratuito</h3>
              <p className="text-gray-600">Sem custos ocultos.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Por que lojas precisam disso */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12 text-gray-800">
            Por Que Lojas Como a Sua Precisam Disso?
          </h2>
          <p className="text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
            Gerencie inventários, relatórios fiscais e dados de vendas com facilidade. Converta XMLs de NF-e, produtos e muito mais em Excel para análises rápidas e decisões inteligentes.
          </p>

          <div className="grid md:grid-cols-3 gap-8 text-left">
            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-2">Inventário Eficiente</h3>
              <p className="text-gray-600">Atualize estoques sem complicações.</p>
            </div>

            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-2">Relatórios Fiscais</h3>
              <p className="text-gray-600">Prepare declarações com precisão.</p>
            </div>

            <div className="p-6 bg-gray-50 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-2">Análises de Vendas</h3>
              <p className="text-gray-600">Visualize dados para crescer seu negócio.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Depoimento */}
      <section className="py-16 px-4 bg-gray-100">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-12 text-gray-800">O Que Nossos Usuários Dizem</h2>
          <blockquote className="text-xl italic text-gray-700 mb-4">
            \"Este conversor salvou meu tempo! Consegui processar centenas de XMLs em minutos, facilitando minha gestão de loja. Recomendo a todos os lojistas!\"
          </blockquote>
          <cite className="text-lg font-semibold text-gray-800">
            – Maria Silva, Dona de Loja
          </cite>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-16 px-4 bg-gradient-to-r from-blue-600 to-indigo-700 text-white text-center">
        <h2 className="text-4xl font-bold mb-4">Pronto para Simplificar Sua Gestão?</h2>
        <p className="text-xl mb-8">Comece a converter XML para Excel agora mesmo.</p>

        <Link
          href="/conversor"
          className="bg-white text-blue-600 px-10 py-5 rounded-full font-semibold text-xl hover:bg-gray-100 transition duration-300 shadow-lg"
        >
          Ir ao Conversor
        </Link>
      </section>
    </div>
  );
}