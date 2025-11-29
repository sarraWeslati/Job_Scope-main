import "../styles/globals.css";

export const metadata = {
  title: "JobScope",
  description: "Intelligent Job Market Analytics Dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}