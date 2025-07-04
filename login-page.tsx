"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { X } from "lucide-react"

interface LoginPageProps {
  onLogin: (username: string, password: string) => boolean
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")

    // Simulate loading
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const success = onLogin(username, password)
    if (!success) {
      setError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    }
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-iFIHuUwxqPyt6RwgO1oj7Qs4qPm8lV.png')`,
        }}
      />

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black/20" />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between p-6">
        <div className="text-white text-xl font-bold">Logo</div>
        <nav className="hidden md:flex items-center space-x-8">
          <a href="#" className="text-white/80 hover:text-white transition-colors">
            Home
          </a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">
            About
          </a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">
            Services
          </a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">
            Contact
          </a>
          <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black bg-transparent">
            Login
          </Button>
        </nav>
      </header>

      {/* Login Modal */}
      <div className="relative z-20 flex items-center justify-center min-h-[calc(100vh-120px)]">
        <div className="w-full max-w-md mx-4">
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8 relative">
            {/* Close Button */}
            <button className="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
              <X className="h-5 w-5" />
            </button>

            {/* Login Form */}
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Login</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-gray-700 font-medium">
                  Email
                </Label>
                <Input
                  id="email"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="กรอกชื่อผู้ใช้"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-gray-700 font-medium">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="กรอกรหัสผ่าน"
                  required
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="remember"
                    checked={rememberMe}
                    onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                  />
                  <Label htmlFor="remember" className="text-sm text-gray-600">
                    Remember me
                  </Label>
                </div>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-800">
                  Forgot Password?
                </a>
              </div>

              {error && <div className="text-red-600 text-sm text-center bg-red-50 p-3 rounded-lg">{error}</div>}

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gray-800 hover:bg-gray-900 text-white py-3 rounded-lg font-medium transition-colors"
              >
                {isLoading ? "กำลังเข้าสู่ระบบ..." : "Login"}
              </Button>

              <div className="text-center text-sm text-gray-600">
                {"Don't have an account? "}
                <a href="#" className="text-blue-600 hover:text-blue-800 font-medium">
                  Register
                </a>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
