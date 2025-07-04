"use client"

import type React from "react"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
  SidebarInset,
} from "@/components/ui/sidebar"
import { Shield, Calendar, Award, FileText, BarChart3, LogOut, Database, ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

const users = {
  oat: { password: "crma74", sheet_name: "ชั้น4_พัน4", displayName: "ผู้ใช้ OAT" },
  time: { password: "crma74", sheet_name: "ชั้น4_พัน1", displayName: "ผู้ใช้ TIME" },
  chai: { password: "crma74", sheet_name: "ชั้น4_พัน3", displayName: "ผู้ใช้ CHAI" },
}

const menuItems = [
  {
    id: "night_duty",
    title: "เวรรักษาการณ์",
    description: "จัดการและดูข้อมูลเวรยืนกลางคืน",
    icon: Shield,
    stats: "24/7",
  },
  {
    id: "weekend_duty",
    title: "เวรเตรียมการ",
    description: "จัดการเวรเสาร์-อาทิตย์และวันหยุด",
    icon: Calendar,
    stats: "สุดสัปดาห์",
  },
  {
    id: "ceremony_duty",
    title: "จัดยอดพิธี",
    description: "สุ่มและจัดยอดสำหรับงานพิธีต่างๆ",
    icon: Award,
    stats: "สุ่มอัตโนมัติ",
  },
  {
    id: "home",
    title: "ยอดปล่อย",
    description: "พิมพ์และจัดทำรายงานยอดปล่อย",
    icon: FileText,
    stats: "รายงาน",
  },
  {
    id: "count",
    title: "สถิติโดนยอด",
    description: "อัพเดตและตรวจสอบสถิติการโดนยอด",
    icon: BarChart3,
    stats: "วิเคราะห์",
  },
]

export default function JarvisSystem() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState<string>("")
  const [activeModule, setActiveModule] = useState<string>("")
  const [loginForm, setLoginForm] = useState({ username: "", password: "" })
  const [loginError, setLoginError] = useState("")

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    const { username, password } = loginForm

    if (username in users && users[username as keyof typeof users].password === password) {
      setIsLoggedIn(true)
      setCurrentUser(username)
      setLoginError("")
      setLoginForm({ username: "", password: "" })
    } else {
      setLoginError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    }
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setCurrentUser("")
    setActiveModule("")
  }

  const currentUserData = currentUser ? users[currentUser as keyof typeof users] : null

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
        {/* Space Background */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-60"
          style={{
            backgroundImage: "url('/space-bg.png')",
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/80" />

        {/* Stars Effect */}
        <div className="absolute inset-0">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full opacity-70 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 2}s`,
              }}
            />
          ))}
        </div>

        <Card className="w-full max-w-md bg-black/80 backdrop-blur-xl border-gray-800 shadow-2xl relative z-10">
          <CardHeader className="text-center space-y-6">
            <div className="mx-auto w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center">
              <Shield className="w-10 h-10 text-white" />
            </div>
            <div>
              <CardTitle className="text-3xl font-bold text-white tracking-wider">J.A.R.V.I.S</CardTitle>
              <CardDescription className="text-gray-300 text-lg mt-2">ระบบผู้ช่วย ฝอ.1</CardDescription>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username" className="text-white text-sm font-medium">
                  ชื่อผู้ใช้
                </Label>
                <Input
                  id="username"
                  type="text"
                  value={loginForm.username}
                  onChange={(e) => setLoginForm((prev) => ({ ...prev, username: e.target.value }))}
                  className="bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500/20"
                  placeholder="กรอกชื่อผู้ใช้"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password" className="text-white text-sm font-medium">
                  รหัสผ่าน
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm((prev) => ({ ...prev, password: e.target.value }))}
                  className="bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500/20"
                  placeholder="กรอกรหัสผ่าน"
                  required
                />
              </div>

              {loginError && (
                <div className="text-red-400 text-sm text-center bg-red-900/20 p-3 rounded border border-red-800">
                  {loginError}
                </div>
              )}

              <Button
                type="submit"
                className="w-full bg-transparent border-2 border-white text-white hover:bg-white hover:text-black transition-all duration-300 font-medium py-3 text-lg tracking-wide"
              >
                เข้าสู่ระบบ
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen bg-black text-white">
        {/* Mobile Sidebar */}
        <Sidebar className="border-r border-gray-800 bg-black/95 backdrop-blur-xl">
          <SidebarHeader className="border-b border-gray-800 p-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-white">J.A.R.V.I.S</h2>
                <p className="text-xs text-gray-400">ระบบผู้ช่วย ฝอ.1</p>
              </div>
            </div>
          </SidebarHeader>

          <SidebarContent className="p-4">
            <SidebarMenu>
              {menuItems.map((item) => {
                const IconComponent = item.icon
                return (
                  <SidebarMenuItem key={item.id}>
                    <SidebarMenuButton
                      onClick={() => setActiveModule(item.id)}
                      className={cn(
                        "w-full justify-start space-x-3 p-3 rounded-lg transition-all duration-200",
                        activeModule === item.id
                          ? "bg-blue-600 text-white"
                          : "text-gray-300 hover:bg-gray-800 hover:text-white",
                      )}
                    >
                      <IconComponent className="w-5 h-5" />
                      <div className="text-left">
                        <div className="font-medium">{item.title}</div>
                        <div className="text-xs opacity-70">{item.stats}</div>
                      </div>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </SidebarContent>
        </Sidebar>

        <SidebarInset>
          {/* Header */}
          <header className="sticky top-0 z-50 border-b border-gray-800 bg-black/80 backdrop-blur-xl">
            <div className="flex h-16 items-center justify-between px-6">
              <div className="flex items-center space-x-4">
                <SidebarTrigger className="md:hidden text-white hover:bg-gray-800" />

                {/* Desktop Navigation */}
                <div className="hidden md:flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-700 rounded-lg flex items-center justify-center">
                    <Shield className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h1 className="text-xl font-bold text-white tracking-wider">J.A.R.V.I.S</h1>
                  </div>
                </div>

                {/* Desktop Menu */}
                <nav className="hidden md:flex items-center space-x-8 ml-12">
                  {menuItems.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => setActiveModule(item.id)}
                      className={cn(
                        "text-sm font-medium tracking-wide transition-colors duration-200 hover:text-blue-400",
                        activeModule === item.id ? "text-blue-400" : "text-gray-300",
                      )}
                    >
                      {item.title}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8 border border-gray-700">
                    <AvatarImage src={`/placeholder.svg?height=32&width=32`} />
                    <AvatarFallback className="bg-gray-800 text-white">
                      {currentUser.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  <div className="hidden sm:block">
                    <p className="text-sm font-medium text-white">{currentUserData?.displayName}</p>
                    <p className="text-xs text-gray-400">{currentUserData?.sheet_name}</p>
                  </div>
                </div>

                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handleLogout}
                  className="text-gray-300 hover:text-white hover:bg-gray-800"
                >
                  <LogOut className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1">
            {!activeModule ? (
              <div className="relative min-h-screen">
                {/* Hero Section */}
                <div
                  className="relative h-screen flex items-center justify-center bg-cover bg-center"
                  style={{
                    backgroundImage: "url('/space-bg.png')",
                  }}
                >
                  <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/80" />

                  {/* Stars Effect */}
                  <div className="absolute inset-0">
                    {[...Array(50)].map((_, i) => (
                      <div
                        key={i}
                        className="absolute w-1 h-1 bg-white rounded-full opacity-60 animate-pulse"
                        style={{
                          left: `${Math.random() * 100}%`,
                          top: `${Math.random() * 100}%`,
                          animationDelay: `${Math.random() * 3}s`,
                          animationDuration: `${2 + Math.random() * 2}s`,
                        }}
                      />
                    ))}
                  </div>

                  <div className="relative z-10 text-center max-w-4xl mx-auto px-6">
                    <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 tracking-wider leading-tight">
                      THE FUTURE OF
                      <br />
                      <span className="text-blue-400">MILITARY ASSISTANCE</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto leading-relaxed">
                      ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1 ด้วยเทคโนโลยีที่ทันสมัยและใช้งานง่าย
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                      <Button
                        onClick={() => setActiveModule("night_duty")}
                        className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-black transition-all duration-300 px-8 py-3 text-lg font-medium tracking-wide"
                      >
                        เริ่มใช้งาน
                      </Button>
                      <Button
                        variant="ghost"
                        className="text-white hover:text-blue-400 transition-colors duration-300 px-8 py-3 text-lg"
                      >
                        เรียนรู้เพิ่มเติม
                        <ChevronDown className="ml-2 h-5 w-5" />
                      </Button>
                    </div>
                  </div>

                  {/* Scroll Indicator */}
                  <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
                    <ChevronDown className="h-8 w-8 text-white opacity-60" />
                  </div>
                </div>

                {/* Stats Section */}
                <div className="bg-black py-20">
                  <div className="max-w-6xl mx-auto px-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                      <div className="text-center">
                        <div className="text-4xl md:text-5xl font-bold text-blue-400 mb-2">150+</div>
                        <div className="text-gray-400 text-sm tracking-wide">นักเรียนนายร้อย</div>
                      </div>
                      <div className="text-center">
                        <div className="text-4xl md:text-5xl font-bold text-blue-400 mb-2">24/7</div>
                        <div className="text-gray-400 text-sm tracking-wide">ระบบพร้อมใช้งาน</div>
                      </div>
                      <div className="text-center">
                        <div className="text-4xl md:text-5xl font-bold text-blue-400 mb-2">5</div>
                        <div className="text-gray-400 text-sm tracking-wide">ฟังก์ชันหลัก</div>
                      </div>
                      <div className="text-center">
                        <div className="text-4xl md:text-5xl font-bold text-blue-400 mb-2">99%</div>
                        <div className="text-gray-400 text-sm tracking-wide">ความแม่นยำ</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-6">
                <div className="max-w-6xl mx-auto">
                  <div className="flex items-center justify-between mb-8">
                    <Button
                      variant="ghost"
                      onClick={() => setActiveModule("")}
                      className="text-gray-300 hover:text-white hover:bg-gray-800"
                    >
                      ← กลับหน้าหลัก
                    </Button>
                    <Badge variant="outline" className="border-blue-500 text-blue-400">
                      {menuItems.find((item) => item.id === activeModule)?.title}
                    </Badge>
                  </div>

                  <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-xl">
                    <CardHeader>
                      <CardTitle className="flex items-center space-x-3 text-white">
                        {(() => {
                          const item = menuItems.find((item) => item.id === activeModule)
                          const IconComponent = item?.icon || Shield
                          return (
                            <>
                              <IconComponent className="w-6 h-6 text-blue-400" />
                              <span>{item?.title}</span>
                            </>
                          )
                        })()}
                      </CardTitle>
                      <CardDescription className="text-gray-400">
                        {menuItems.find((item) => item.id === activeModule)?.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center py-16">
                        <div className="w-20 h-20 mx-auto mb-6 bg-gray-800 rounded-full flex items-center justify-center">
                          <Database className="w-10 h-10 text-gray-400" />
                        </div>
                        <h3 className="text-2xl font-semibold mb-4 text-white">ฟังก์ชันกำลังพัฒนา</h3>
                        <p className="text-gray-400 mb-8 max-w-md mx-auto">
                          ฟังก์ชันนี้จะเชื่อมต่อกับ Google Sheets และระบบฐานข้อมูลเดิม
                        </p>
                        <Button
                          variant="outline"
                          className="border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white bg-transparent"
                        >
                          เชื่อมต่อระบบเดิม
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}
          </main>

          {/* Footer */}
          <footer className="border-t border-gray-800 bg-black">
            <div className="max-w-6xl mx-auto px-6 py-8 text-center">
              <p className="text-gray-400 text-sm tracking-wide">
                J.A.R.V.I.S © 2025 | พัฒนาโดย Oat | ระบบผู้ช่วยอัจฉริยะ ฝอ.1
              </p>
            </div>
          </footer>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}
