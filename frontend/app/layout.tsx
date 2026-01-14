// [Task]: T030, T099, T110, T122 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Root layout component for Next.js App Router.
 * Provides HTML structure, Tailwind CSS, font optimization, viewport configuration, dark mode support, and error boundary.
 */
import type { Metadata, Viewport } from 'next'
import { ThemeProvider } from '@/components/providers/theme-provider'
import { ErrorBoundary } from '@/components/error-boundary'
import './globals.css'

export const metadata: Metadata = {
  title: 'Phase 2 Todo App',
  description: 'Full-stack task management application with authentication',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        <ErrorBoundary>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
