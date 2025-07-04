"use client"

import { useState } from "react"
import { LoginPage } from "@/components/login-page"
import { Dashboard } from "@/components/dashboard"

// Mock user data
const users = {
  oat: { password: "crma74", displayName: "ผู้ใช้ OAT", role: "ผู้ดูแลระบบ", group: "ชั้น4_พัน4" },
  time: { password: "crma74", displayName: "ผู้ใช้ TIME", role: "ผู้ใช้งาน", group: "ชั้น4_พัน1" },
  chai: { password: "crma74", displayName: "ผู้ใช้ CHAI", role: "ผู้ใช้งาน", group: "ชั้น4_พัน3" },
}

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState<string | null>(null)

  const handleLogin = (username: string, password: string) => {
    if (users[username as keyof typeof users] && users[username as keyof typeof users].password === password) {
      setIsLoggedIn(true)
      setCurrentUser(username)
      return true
    }
    return false
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setCurrentUser(null)
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <Dashboard
      user={currentUser ? users[currentUser as keyof typeof users] : null}
      username={currentUser}
      onLogout={handleLogout}
    />
  )
}
