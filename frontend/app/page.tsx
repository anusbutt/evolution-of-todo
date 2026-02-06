// [Task]: T052 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Landing page with gradient background and glass feature cards.
 */
import Link from 'next/link'
import { CheckCircle2, Zap, Sparkles, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  const features = [
    {
      icon: CheckCircle2,
      title: 'Simple & Intuitive',
      description: 'Clean interface that lets you focus on what matters most',
      color: 'text-green-400',
      bgColor: 'bg-green-500/20',
    },
    {
      icon: Zap,
      title: 'Fast & Reliable',
      description: 'Lightning-fast performance with secure authentication',
      color: 'text-amber-400',
      bgColor: 'bg-amber-500/20',
    },
    {
      icon: Sparkles,
      title: 'AI-Powered',
      description: 'Natural language task management with AI assistant',
      color: 'text-indigo-400',
      bgColor: 'bg-indigo-500/20',
    },
  ]

  return (
    <div className="min-h-screen gradient-bg dark:gradient-bg gradient-bg-light flex flex-col">
      {/* Navigation */}
      <nav className="glass-nav dark:glass-nav glass-nav-light sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                <span className="text-white font-bold text-xl">T</span>
              </div>
              <span className="text-xl font-bold gradient-text">Todo App</span>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Log In
                </Button>
              </Link>
              <Link href="/signup">
                <Button variant="primary" size="sm">
                  Sign Up
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-16">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/20 border border-indigo-500/30">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="text-sm text-indigo-300">Now with AI Assistant</span>
          </div>

          {/* Headline */}
          <div className="space-y-4">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white leading-tight">
              Manage tasks with{' '}
              <span className="gradient-text">clarity</span>
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              The simple, powerful way to organize your tasks and boost your productivity.
              Now powered by AI for natural language task management.
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Link href="/signup">
              <Button variant="primary" size="lg" className="min-w-[200px]">
                Get Started Free
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="ghost" size="lg" className="min-w-[200px]">
                I already have an account
              </Button>
            </Link>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="max-w-5xl mx-auto mt-24 grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="glass-card p-6 hover-lift animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s`, animationFillMode: 'backwards' }}
            >
              <div className={`w-12 h-12 rounded-xl ${feature.bgColor} flex items-center justify-center mb-4`}>
                <feature.icon className={`w-6 h-6 ${feature.color}`} />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-400 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-gray-500 text-sm">
        <p>Built with Next.js, FastAPI, and Claude AI</p>
      </footer>
    </div>
  )
}
