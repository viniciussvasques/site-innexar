"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { authService } from "@/services/auth";
import api from "@/lib/api";
import { useLanguageContext } from "@/components/LanguageProvider";
import "../login/login.css";
import "./register.css";

export default function RegisterPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { t } = useLanguageContext();

  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [workspace, setWorkspace] = useState("");
  const [slugStatus, setSlugStatus] = useState<"idle" | "checking" | "available" | "taken">("idle");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password_confirm: "",
    first_name: "",
    last_name: "",
    phone: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const planFromQuery = searchParams.get("plan");
    if (planFromQuery) {
      setSelectedPlan(planFromQuery);
      if (typeof window !== "undefined") {
        localStorage.setItem("structurone_selected_plan", planFromQuery);
      }
    }
  }, [searchParams]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleWorkspaceBlur = async () => {
    if (!workspace) {
      setSlugStatus("idle");
      return;
    }
    setSlugStatus("checking");
    try {
      const response = await api.get("/tenants/check-slug/", {
        params: { slug: workspace },
      });
      if (response.data?.available) {
        setSlugStatus("available");
      } else {
        setSlugStatus("taken");
      }
    } catch (err) {
      console.error("Erro ao verificar slug:", err);
      setSlugStatus("idle");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.password_confirm) {
      setError(t("auth.register.passwordMismatch"));
      return;
    }

    setLoading(true);

    try {
      await authService.register({
        ...formData,
        company_name: workspace || undefined,
        desired_slug: workspace || undefined,
      });
      router.push("/onboarding");
    } catch (err: any) {
      const errorData = err.response?.data;
      if (errorData?.detail) {
        setError(errorData.detail);
      } else if (errorData) {
        const errors = (Object.values(errorData) as any[]).flat().join(", ");
        setError(errors);
      } else {
        setError(t("auth.register.error"));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="login-background">
        <div className="login-gradient"></div>
        <div className="login-pattern"></div>
      </div>

      <div className="auth-card">
        <div className="login-header">
          <div className="login-logo">
            <svg
              width="64"
              height="64"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect
                width="64"
                height="64"
                rx="16"
                fill="url(#logoGradientRegister)"
              />
              <path
                d="M32 16L44 28H38V36H26V28H20L32 16Z"
                fill="white"
              />
              <path
                d="M16 42L28 54H22V50H42V54H36L48 42L32 26L16 42Z"
                fill="white"
                fillOpacity="0.9"
              />
              <defs>
                <linearGradient
                  id="logoGradientRegister"
                  x1="0"
                  y1="0"
                  x2="64"
                  y2="64"
                  gradientUnits="userSpaceOnUse"
                >
                  <stop stopColor="#22c55e" />
                  <stop offset="1" stopColor="#16a34a" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="login-title">StructurOne</h1>
          <p className="login-subtitle">{t("auth.register.title")}</p>
        </div>

        {selectedPlan && (
          <div className="auth-plan-banner">
            {t("auth.register.selectedPlan", { plan: selectedPlan })}
          </div>
        )}
          <p className="form-helper-text">
            {t("auth.register.workspacePreview", {
              url: `${workspace || t("auth.register.workspacePlaceholder").split(" ")[0]}.structurone.com`,
            })}
          </p>

        <div className="form-group">
          <label className="form-label">
            {t("auth.register.workspace")}
          </label>
          <input
            type="text"
            name="workspace"
            value={workspace}
            onChange={(e) => {
              setWorkspace(e.target.value.toLowerCase());
              setSlugStatus("idle");
            }}
            onBlur={handleWorkspaceBlur}
            className="form-input"
            placeholder={t("auth.register.workspacePlaceholder")}
          />
          <p className="form-helper-text">
            {t("auth.register.workspaceHelp")}
          </p>
          {slugStatus === "checking" && (
            <p className="form-helper-text">{t("auth.register.workspaceChecking")}</p>
          )}
          {slugStatus === "available" && (
            <p className="form-helper-text form-helper-success">
              {t("auth.register.workspaceAvailable")}
            </p>
          )}
          {slugStatus === "taken" && (
            <p className="form-helper-text form-helper-error">
              {t("auth.register.workspaceTaken")}
            </p>
          )}
        </div>

        {error && (
          <div className="login-error">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M10 6V10M10 14H10.01"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group form-group-inline-2">
            <div className="form-group">
              <label className="form-label">
                {t("auth.register.firstName")}
              </label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label className="form-label">
                {t("auth.register.lastName")}
              </label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">{t("auth.register.email")}</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t("auth.register.phone")}</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="form-input"
            />
          </div>

          <div className="form-group form-group-inline-2">
            <div className="form-group">
              <label className="form-label">
                {t("auth.register.password")}
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label className="form-label">
                {t("auth.register.passwordConfirm")}
              </label>
              <input
                type="password"
                name="password_confirm"
                value={formData.password_confirm}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? t("auth.register.submitting") : t("auth.register.submit")}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {t("auth.register.hasAccount")}{" "}
            <a href="/login" className="form-link">
              {t("auth.register.login")}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
