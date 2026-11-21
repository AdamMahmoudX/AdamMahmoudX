mport { useCallback, useEffect, useState } from "react";
import { ActivityOverview } from "@/components/ActivityOverview";
import { AboutMe } from "@/components/AboutMe";
import { Banner } from "@/components/Banner";
import { Contributions } from "@/components/Contributions";
import { EditProfileModal } from "@/components/EditProfileModal";
import { Footer } from "@/components/Footer";
import { PinnedRepos } from "@/components/PinnedRepos";
import { ReadmeKit } from "@/components/ReadmeKit";
import { Sidebar } from "@/components/Sidebar";
import { StatsGrid } from "@/components/StatsGrid";
import { Toast, type ToastMessage } from "@/components/Toast";
import { defaultProfile, type ProfileData } from "@/data/profile";

const STORAGE_KEY = "adam-profile-concept-v1";

function readSavedProfile(): ProfileData {
  if (typeof window === "undefined") return defaultProfile;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultProfile;
    const parsed = JSON.parse(raw) as Partial<ProfileData> | null;
    if (!parsed || typeof parsed !== "object") return defaultProfile;
    return {
      ...defaultProfile,
      ...parsed,
      stats: { ...defaultProfile.stats, ...(parsed.stats ?? {}) },
    };
  } catch {
    return defaultProfile;
  }
}

export default function App() {
  const [profile, setProfile] = useState<ProfileData>(readSavedProfile);
  const [editing, setEditing] = useState(false);
  const [toast, setToast] = useState<ToastMessage | null>(null);

  const notify = useCallback((message: string) => {
    setToast({ id: Date.now(), message });
  }, []);

  const closeEditor = useCallback(() => setEditing(false), []);

  const saveProfile = useCallback(
    (nextProfile: ProfileData) => {
      setProfile(nextProfile);
      notify("Profile details saved in this browser");
    },
    [notify],
  );

  const resetProfile = useCallback(() => {
    setProfile(defaultProfile);
    try {
      window.localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Storage can be unavailable in private browsing; the UI still resets.
    }
    notify("Sample content restored");
  }, [notify]);

  const handleShare = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      notify("Profile link copied to clipboard");
    } catch {
      notify("Copy the profile link from your address bar");
    }
  }, [notify]);

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(profile));
    } catch {
      // No persistence available — the profile remains editable in memory.
    }
  }, [profile]);

  useEffect(() => {
    document.title = `${profile.name} — ${profile.role}`;
  }, [profile.name, profile.role]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(null), 3400);
    return () => window.clearTimeout(timer);
  }, [toast]);

  return (
    <div id="top" className="relative min-h-screen overflow-x-hidden">
      <div aria-hidden="true" className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
        <div className="absolute inset-0 ambient-glow" />
        <div className="absolute inset-0 star-field" />
        <div className="absolute inset-0 bg-grid-faint opacity-[0.22] [mask-image:linear-gradient(to_bottom,black,transparent_52%)]" />
        <div className="animate-drift absolute -top-[26rem] left-[4%] h-[38rem] w-[38rem] rounded-full bg-[#1d4ed8]/[0.09] blur-[150px]" />
        <div className="animate-drift absolute -right-[14rem] top-[22%] h-[32rem] w-[32rem] rounded-full bg-[#0e7490]/[0.07] blur-[140px] [animation-delay:-8s]" />
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-accent-400/25 to-transparent" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_38%,rgba(1,4,10,0.55)_100%)]" />
      </div>

      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[70] focus:rounded-lg focus:border focus:border-accent-400/40 focus:bg-[#071524] focus:px-4 focus:py-2 focus:text-[11px] focus:font-semibold focus:text-ice-100"
      >
        Skip to profile content
      </a>

      <div className="relative z-10 mx-auto w-full max-w-[1420px] px-3.5 pb-5 pt-4 sm:px-6 sm:pb-6 sm:pt-6 lg:px-8 lg:pt-8">
        <div className="grid items-stretch gap-4 sm:gap-5 lg:grid-cols-[minmax(0,322px)_minmax(0,1fr)] xl:grid-cols-[minmax(0,348px)_minmax(0,1fr)]">
          <div className="page-enter min-w-0 lg:h-full">
            <Sidebar profile={profile} onEdit={() => setEditing(true)} onShare={handleShare} />
          </div>

          <main id="main-content" className="flex min-w-0 flex-col gap-4 sm:gap-5">
            <div className="page-enter [animation-delay:60ms]">
              <Banner />
            </div>
            <div className="page-enter [animation-delay:120ms]">
              <StatsGrid profile={profile} />
            </div>
            <div className="page-enter [animation-delay:180ms]">
              <Contributions />
            </div>
            <div className="page-enter [animation-delay:240ms]">
              <PinnedRepos github={profile.github} />
            </div>
            <div className="page-enter [animation-delay:300ms]">
              <ActivityOverview />
            </div>
            <div className="page-enter [animation-delay:360ms]">
              <AboutMe profile={profile} />
            </div>
          </main>
        </div>

        <div className="page-enter [animation-delay:420ms]">
          <ReadmeKit profile={profile} onNotify={notify} />
        </div>

        <div className="page-enter [animation-delay:480ms]">
          <Footer profile={profile} />
        </div>
      </div>

      <EditProfileModal
        open={editing}
        profile={profile}
        onClose={closeEditor}
        onSave={saveProfile}
        onReset={resetProfile}
      />
      <Toast toast={toast} />
    </div>
  );
}
