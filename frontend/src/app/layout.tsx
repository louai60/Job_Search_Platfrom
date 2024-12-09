import React from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import SideBar from "@/components/shared/SideBar";
import Navbar from "@/components/shared/Navbar";

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <div className="flex h-screen w-full overflow-hidden">
        {/* Sidebar */}
        <div className="w-64 fixed h-full bg-navy-800">
          <SideBar />
        </div>

        {/* Main Content Area */}
        <div className="flex-1 ml-64 flex flex-col w-[calc(100%-16rem)]">
          {/* Navbar positioned at the top */}
          <Navbar 
            onOpenSidenav={() => {}} 
            brandText="Dashboard" 
            avatar="/path/to/avatar.jpg"
          />

          {/* Main content */}
          <div className="flex-1 p-4 overflow-y-auto bg-gray-100">
            {children}
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
}

export default Layout;