export const metadata = {
  title: "Conversor Bling",
  description: "Ferramenta de conversão XML → Planilha Bling",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}