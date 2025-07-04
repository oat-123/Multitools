"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Shield, Calendar, Award, FileText, BarChart3, LogOut } from "lucide-react"

interface DashboardProps {
  user: { displayName: string; role: string; group: string } | null
  username: string | null
  onLogout: () => void
}

export function Dashboard({ user, username, onLogout }: DashboardProps) {
  const [currentPage, setCurrentPage] = useState("dashboard")
  const [showProfilePopup, setShowProfilePopup] = useState(false)
  const popupRef = useRef<HTMLDivElement>(null)

  // Close popup when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (popupRef.current && !popupRef.current.contains(event.target as Node)) {
        setShowProfilePopup(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  const navItems = [
    { id: "night_duty", title: "เวรรักษาการณ์", icon: Shield },
    { id: "weekend_duty", title: "เวรเตรียมการ", icon: Calendar },
    { id: "ceremony_duty", title: "จัดยอดพิธี", icon: Award },
    { id: "home", title: "ยอดปล่อย", icon: FileText },
    { id: "count", title: "สถิติโดนยอด", icon: BarChart3 },
  ]

  const ModulePage = ({ title, icon: Icon, description }: { title: string; icon: any; description: string }) => (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Button
          onClick={() => setCurrentPage("dashboard")}
          variant="outline"
          className="mb-8 text-white border-white hover:bg-white hover:text-black"
        >
          ← กลับหน้าหลัก
        </Button>

        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-blue-600 rounded-full mb-6">
            <Icon className="h-12 w-12" />
          </div>
          <h1 className="text-4xl font-bold mb-4">{title}</h1>
          <p className="text-xl text-blue-200 mb-8 max-w-2xl mx-auto">{description}</p>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg">เชื่อมต่อระบบเดิม</Button>
        </div>
      </div>
    </div>
  )

  if (currentPage === "night_duty") {
    return (
      <ModulePage title="เวรรักษาการณ์" icon={Shield} description="จัดการและดูข้อมูลเวรยืนกลางคืน ระบบตรวจสอบตลอด 24 ชั่วโมง" />
    )
  }

  if (currentPage === "weekend_duty") {
    return <ModulePage title="เวรเตรียมการ" icon={Calendar} description="จัดการเวรเสาร์-อาทิตย์และวันหยุดราชการ" />
  }

  if (currentPage === "ceremony_duty") {
    return <ModulePage title="จัดยอดพิธี" icon={Award} description="สุ่มและจัดยอดสำหรับงานพิธีต่างๆ อัตโนมัติ" />
  }

  if (currentPage === "home") {
    return <ModulePage title="ยอดปล่อย" icon={FileText} description="พิมพ์และจัดทำรายงานยอดปล่อยประจำวัน" />
  }

  if (currentPage === "count") {
    return <ModulePage title="สถิติโดนยอด" icon={BarChart3} description="อัพเดตและตรวจสอบสถิติการโดนยอด" />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      {/* Header */}
      <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
              <Shield className="h-6 w-6" />
            </div>
            <h1 className="text-2xl font-bold tracking-wider">J.A.R.V.I.S</h1>
          </div>

          {/* Navigation */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navItems.map((item) => (
              <Button
                key={item.id}
                onClick={() => setCurrentPage(item.id)}
                variant="ghost"
                className="text-white hover:bg-blue-600/20 hover:text-blue-200"
              >
                {item.title}
              </Button>
            ))}
          </nav>

          {/* Profile */}
          <div className="relative">
            <button
              onClick={() => setShowProfilePopup(!showProfilePopup)}
              className="w-11 h-11 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 border-2 border-white/20"
            >
              {username?.[0]?.toUpperCase() || "U"}
            </button>

            {/* Profile Popup */}
            {showProfilePopup && (
              <div
                ref={popupRef}
                className="absolute right-0 top-14 w-80 bg-slate-800 border border-slate-600 rounded-xl shadow-2xl p-6 z-50 animate-in slide-in-from-top-2 duration-200"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {username?.[0]?.toUpperCase() || "U"}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{user?.displayName}</h3>
                    <p className="text-sm text-slate-400">{user?.role}</p>
                  </div>
                </div>

                <div className="space-y-2 mb-4 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-400">ชื่อผู้ใช้:</span>
                    <span className="text-white">{username}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">กลุ่ม:</span>
                    <span className="text-white">{user?.group}</span>
                  </div>
                </div>

                <div className="border-t border-slate-600 pt-4">
                  <Button
                    onClick={onLogout}
                    variant="destructive"
                    className="w-full bg-red-600 hover:bg-red-700 text-white"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    ออกจากระบบ
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-white bg-clip-text text-transparent">
            THE FUTURE OF
          </h1>
          <h2 className="text-4xl font-bold text-blue-400 mb-6">MILITARY ASSISTANCE</h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
            ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1 <br />
            ด้วยลักษณะที่ทันสมัยและใช้งานง่าย
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {[
            { number: "150+", label: "นักเรียนนายร้อย" },
            { number: "24/7", label: "ระบบพร้อมใช้งาน" },
            { number: "5", label: "ฟังก์ชันหลัก" },
            { number: "99%", label: "ความแม่นยำ" },
          ].map((stat, index) => (
            <div
              key={index}
              className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 text-center hover:bg-slate-800/70 transition-all duration-300 hover:scale-105"
            >
              <div className="text-4xl font-bold text-blue-400 mb-2">{stat.number}</div>
              <div className="text-slate-300">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {navItems.map((item) => (
            <div
              key={item.id}
              onClick={() => setCurrentPage(item.id)}
              className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8 cursor-pointer hover:bg-slate-800/70 transition-all duration-300 hover:scale-105 group"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:from-blue-600 group-hover:to-blue-700 transition-all duration-300">
                <item.icon className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-bold mb-3">{item.title}</h3>
              <p className="text-slate-400 group-hover:text-slate-300 transition-colors">คลิกเพื่อเข้าใช้งาน {item.title}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-black border-t border-slate-800 p-8 mt-16">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-slate-400">J.A.R.V.I.S © 2025 | พัฒนาโดย Oat | ระบบผู้ช่วยอัจฉริยะ ฝอ.1</p>
        </div>
      </footer>
    </div>
  )
}
