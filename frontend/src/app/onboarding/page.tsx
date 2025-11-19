"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { onboardingService } from "@/services/onboarding";
import { authService } from "@/services/auth";
import { useLanguageContext } from "@/components/LanguageProvider";
import {
  getCountryConfig,
  getCountryList,
  type CountryConfig,
} from "@/data/countries";
import api from "@/lib/api";
import "./onboarding.css";

interface AddressData {
  street: string;
  number: string;
  complement?: string;
  neighborhood?: string;
  city: string;
  state: string;
  zipcode: string;
  [key: string]: string | undefined;
}

interface OnboardingData {
  country: string;
  companyType: string;
  companyName: string;
  taxId: string;
  phone: string;
  email: string;
  address: AddressData;
  primaryColor: string;
  language: string;
  currency: string;
  timezone: string;
}

export default function OnboardingPage() {
  const router = useRouter();
  const { t } = useLanguageContext();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [selectedCountry, setSelectedCountry] = useState<string>("");
  const [countryConfig, setCountryConfig] = useState<CountryConfig | null>(
    null
  );
  const [formData, setFormData] = useState<OnboardingData>({
    country: "",
    companyType: "",
    companyName: "",
    taxId: "",
    phone: "",
    email: "",
    address: {
      street: "",
      number: "",
      city: "",
      state: "",
      zipcode: "",
    },
    primaryColor: "#6366f1",
    language: "pt-br",
    currency: "BRL",
    timezone: "America/Sao_Paulo",
  });

  useEffect(() => {
    loadProgress();
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      const config = getCountryConfig(selectedCountry);
      setCountryConfig(config);
      if (config) {
        setFormData((prev) => ({
          ...prev,
          country: selectedCountry,
          language: config.language,
          currency: config.currency,
          timezone: config.timezone,
        }));
      }
    }
  }, [selectedCountry]);

  const loadProgress = async () => {
    try {
      const user = authService.getCurrentUser();
      if (!user) {
        router.push("/login");
        return;
      }

      const progress = await onboardingService.getProgress();
      if (progress.completed) {
        router.push("/dashboard");
        return;
      }

      if (progress.data) {
        const data = progress.data;
        setSelectedCountry(data.country || "");
        setFormData({
          country: data.country || "",
          companyType: data.company_type || "",
          companyName: data.company_name || "",
          taxId: data.tax_id || data.cnpj || "",
          phone: data.phone || "",
          email: data.email || user.email || "",
          address: {
            street: data.address?.street || data.address || "",
            number: data.address?.number || "",
            complement: data.address?.complement || "",
            neighborhood: data.address?.neighborhood || "",
            city: data.address?.city || "",
            state: data.address?.state || "",
            zipcode: data.address?.zipcode || "",
          },
          primaryColor: data.primary_color || "#6366f1",
          language: data.language || "pt-br",
          currency: data.currency || "BRL",
          timezone: data.timezone || "America/Sao_Paulo",
        });
        setCurrentStep(progress.step || 1);
      }
    } catch (err) {
      console.error("Erro ao carregar progresso:", err);
    } finally {
      setLoading(false);
    }
  };

  const applyTaxIdMask = (value: string): string => {
    if (!countryConfig?.taxIdMask) return value;
    return countryConfig.taxIdMask(value);
  };

  const handleTaxIdChange = (value: string) => {
    const masked = applyTaxIdMask(value);
    setFormData((prev) => ({ ...prev, taxId: masked }));
  };

  const validateStep = (step: number): boolean => {
    if (step === 1) {
      if (!formData.country || !formData.companyType || !formData.companyName) {
        setError(t("onboarding.requiredFields"));
        return false;
      }
    }
    if (step === 2) {
      if (!formData.taxId || !formData.email || !formData.phone) {
        setError(t("onboarding.requiredFields"));
        return false;
      }
      if (
        !formData.address.street ||
        !formData.address.number ||
        !formData.address.city ||
        !formData.address.state ||
        !formData.address.zipcode
      ) {
        setError(t("onboarding.requiredAddressFields"));
        return false;
      }
    }
    return true;
  };

  const saveStep = async (step: number) => {
    if (!validateStep(step)) {
      return;
    }

    setSaving(true);
    setError("");

    try {
      const dataToSave: any = {
        country: formData.country,
        company_type: formData.companyType,
        company_name: formData.companyName,
        tax_id: formData.taxId,
        phone: formData.phone,
        email: formData.email,
        address: formData.address,
        primary_color: formData.primaryColor,
        language: formData.language,
        currency: formData.currency,
        timezone: formData.timezone,
      };

      await onboardingService.updateStep(step, dataToSave);

      if (step < 3) {
        setCurrentStep(step + 1);
      } else {
        await handleComplete();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || t("onboarding.error"));
    } finally {
      setSaving(false);
    }
  };

  const handleComplete = async () => {
    setSaving(true);
    setError("");
    try {
      const result = await onboardingService.complete();
      console.log("Onboarding completado:", result);

      // Buscar dados atualizados do usuário do backend
      try {
        const response = await api.get("/auth/me/");
        if (response.data) {
          localStorage.setItem("user", JSON.stringify(response.data));
          console.log("Usuário atualizado:", response.data);
        }
      } catch (fetchErr) {
        console.warn("Erro ao buscar dados atualizados do usuário:", fetchErr);
        // Atualizar localmente mesmo assim
        const user = authService.getCurrentUser();
        if (user) {
          user.onboarding_completed = true;
          localStorage.setItem("user", JSON.stringify(user));
        }
      }

      // Definir próximo destino após onboarding:
      // - Se existe um plano selecionado vindo do site (structurone_selected_plan),
      //   direcionar para o checkout de billing
      // - Caso contrário, ir para o dashboard padrão
      let nextUrl = "/dashboard";
      try {
        if (typeof window !== "undefined") {
          const selectedPlan = localStorage.getItem(
            "structurone_selected_plan"
          );
          if (selectedPlan) {
            nextUrl = "/billing/checkout";
          }
        }
      } catch (e) {
        console.warn("Erro ao ler plano selecionado do localStorage:", e);
      }

      // Redirecionar usando window.location para garantir navegação completa
      setTimeout(() => {
        window.location.href = nextUrl;
      }, 300);
    } catch (err: any) {
      console.error("Erro ao completar onboarding:", err);
      setError(err.response?.data?.detail || t("onboarding.error"));
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="onboarding-loading">
        <div className="onboarding-spinner"></div>
        <p>{t("onboarding.loading")}</p>
      </div>
    );
  }

  const countries = getCountryList();
  const totalSteps = 3;

  return (
    <div className="onboarding-container">
      <div className="onboarding-background">
        <div className="onboarding-gradient"></div>
      </div>

      <div className="onboarding-card">
        <div className="onboarding-header">
          <div className="onboarding-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="12" fill="url(#gradient)" />
              <path d="M24 12L32 20H28V28H20V20H16L24 12Z" fill="white" />
              <path
                d="M12 32L20 40H16V36H32V40H28L36 32L24 20L12 32Z"
                fill="white"
                fillOpacity="0.8"
              />
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="48" y2="48">
                  <stop stopColor="#6366f1" />
                  <stop offset="1" stopColor="#8b5cf6" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="onboarding-title">{t("onboarding.title")}</h1>
          <p className="onboarding-subtitle">
            {t("onboarding.subtitle")}
          </p>
        </div>

        {/* Progress Steps */}
        <div className="onboarding-steps">
          {[1, 2, 3].map((step) => (
            <div
              key={step}
              className={`onboarding-step ${
                currentStep >= step ? "active" : ""
              } ${currentStep === step ? "current" : ""}`}
            >
              <div className="onboarding-step-number">{step}</div>
              <div className="onboarding-step-line"></div>
            </div>
          ))}
        </div>

        {error && (
          <div className="onboarding-error">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                stroke="currentColor"
                strokeWidth="2"
              />
              <path
                d="M10 6V10M10 14H10.01"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Step 1: País e Tipo de Empresa */}
        {currentStep === 1 && (
          <div className="onboarding-step-content">
            <h2 className="onboarding-step-title">{t("onboarding.step1.title")}</h2>
            <p className="onboarding-step-description">
              {t("onboarding.step1.description")}
            </p>

            <div className="onboarding-form-group">
              <label className="onboarding-label">
                {t("onboarding.step1.country")}{" "}
                <span className="required">*</span>
              </label>
              <div className="onboarding-country-grid">
                {countries.map((country) => (
                  <button
                    key={country.code}
                    type="button"
                    className={`onboarding-country-card ${
                      selectedCountry === country.code ? "selected" : ""
                    }`}
                    onClick={() => setSelectedCountry(country.code)}
                  >
                    <div className="onboarding-country-flag">
                      {country.code}
                    </div>
                    <div className="onboarding-country-name">
                      {country.name}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {selectedCountry && countryConfig && (
              <>
                <div className="onboarding-form-group">
                  <label className="onboarding-label">
                    {t("onboarding.step1.companyType")}{" "}
                    <span className="required">*</span>
                  </label>
                  <select
                    className="onboarding-select"
                    value={formData.companyType}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        companyType: e.target.value,
                      }))
                    }
                  >
                    <option value="">
                      {t("onboarding.step1.selectCompanyType")}
                    </option>
                    {countryConfig.companyTypes.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="onboarding-form-group">
                  <label className="onboarding-label">
                    {t("onboarding.step1.companyName")}{" "}
                    <span className="required">*</span>
                  </label>
                  <input
                    type="text"
                    className="onboarding-input"
                    placeholder={t("onboarding.step1.companyName")}
                    value={formData.companyName}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        companyName: e.target.value,
                      }))
                    }
                  />
                </div>
              </>
            )}

            <div className="onboarding-actions">
              <button
                type="button"
                className="onboarding-btn onboarding-btn-primary"
                onClick={() => saveStep(1)}
                disabled={
                  saving ||
                  !selectedCountry ||
                  !formData.companyType ||
                  !formData.companyName
                }
              >
                {saving
                  ? t("onboarding.step1.saving")
                  : t("onboarding.step1.continue")}
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Informações Fiscais e Endereço */}
        {currentStep === 2 && countryConfig && (
          <div className="onboarding-step-content">
            <h2 className="onboarding-step-title">
              {t("onboarding.step2.title")}
            </h2>
            <p className="onboarding-step-description">
              {t("onboarding.step2.description")}
            </p>

            <div className="onboarding-form-group">
              <label className="onboarding-label">
                {t("onboarding.step2.taxId")}{" "}
                <span className="required">*</span>
              </label>
              <input
                type="text"
                className="onboarding-input"
                placeholder={countryConfig.taxIdPlaceholder}
                value={formData.taxId}
                onChange={(e) => handleTaxIdChange(e.target.value)}
                maxLength={
                  countryConfig.code === "BR"
                    ? 18
                    : countryConfig.code === "US"
                    ? 10
                    : 20
                }
              />
            </div>

            <div className="onboarding-form-row">
              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.email")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="email"
                  className="onboarding-input"
                  placeholder="email@company.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, email: e.target.value }))
                  }
                />
              </div>

              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.phone")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="tel"
                  className="onboarding-input"
                  placeholder={countryConfig.phoneFormat || "+00 000 000 0000"}
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, phone: e.target.value }))
                  }
                />
              </div>
            </div>

            <div className="onboarding-section-divider">
              <span>{t("onboarding.step2.address")}</span>
            </div>

            <div className="onboarding-form-group">
              <label className="onboarding-label">
                {countryConfig.addressFormat.fields.includes("street")
                  ? t("onboarding.step2.street")
                  : t("onboarding.step2.address")}{" "}
                <span className="required">*</span>
              </label>
              <input
                type="text"
                className="onboarding-input"
                placeholder={t("onboarding.step2.street")}
                value={formData.address.street}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    address: { ...prev.address, street: e.target.value },
                  }))
                }
              />
            </div>

            <div className="onboarding-form-row">
              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.number")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="text"
                  className="onboarding-input"
                  placeholder="123"
                  value={formData.address.number}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      address: { ...prev.address, number: e.target.value },
                    }))
                  }
                />
              </div>

              {countryConfig.addressFormat.fields.includes("complement") && (
                <div className="onboarding-form-group">
                  <label className="onboarding-label">
                    {t("onboarding.step2.complement")}
                  </label>
                  <input
                    type="text"
                    className="onboarding-input"
                    placeholder={t("onboarding.step2.complement")}
                    value={formData.address.complement || ""}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        address: {
                          ...prev.address,
                          complement: e.target.value,
                        },
                      }))
                    }
                  />
                </div>
              )}
            </div>

            {countryConfig.addressFormat.fields.includes("neighborhood") && (
              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.neighborhood")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="text"
                  className="onboarding-input"
                  placeholder={t("onboarding.step2.neighborhood")}
                  value={formData.address.neighborhood || ""}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      address: {
                        ...prev.address,
                        neighborhood: e.target.value,
                      },
                    }))
                  }
                />
              </div>
            )}

            <div className="onboarding-form-row">
              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.city")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="text"
                  className="onboarding-input"
                  placeholder={t("onboarding.step2.city")}
                  value={formData.address.city}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      address: { ...prev.address, city: e.target.value },
                    }))
                  }
                />
              </div>

              <div className="onboarding-form-group">
                <label className="onboarding-label">
                  {t("onboarding.step2.state")}{" "}
                  <span className="required">*</span>
                </label>
                <input
                  type="text"
                  className="onboarding-input"
                  placeholder={
                    countryConfig.code === "BR" ? "SP" : "CA"
                  }
                  value={formData.address.state}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      address: { ...prev.address, state: e.target.value },
                    }))
                  }
                />
              </div>
            </div>

            <div className="onboarding-form-group">
              <label className="onboarding-label">
                {t("onboarding.step2.zipcode")}{" "}
                <span className="required">*</span>
              </label>
              <input
                type="text"
                className="onboarding-input"
                placeholder={
                  countryConfig.code === "BR" ? "00000-000" : "00000"
                }
                value={formData.address.zipcode}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    address: { ...prev.address, zipcode: e.target.value },
                  }))
                }
              />
            </div>

            <div className="onboarding-actions">
              <button
                type="button"
                className="onboarding-btn onboarding-btn-secondary"
                onClick={() => setCurrentStep(1)}
              >
                {t("onboarding.step2.back")}
              </button>
              <button
                type="button"
                className="onboarding-btn onboarding-btn-primary"
                onClick={() => saveStep(2)}
                disabled={saving}
              >
                {saving
                  ? t("onboarding.step2.saving")
                  : t("onboarding.step2.continue")}
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Personalização */}
        {currentStep === 3 && countryConfig && (
          <div className="onboarding-step-content">
            <h2 className="onboarding-step-title">
              {t("onboarding.step3.title")}
            </h2>
            <p className="onboarding-step-description">
              {t("onboarding.step3.description")}
            </p>

            <div className="onboarding-form-group">
              <label className="onboarding-label">
                {t("onboarding.step3.primaryColor")}
              </label>
              <div className="onboarding-color-picker">
                <input
                  type="color"
                  className="onboarding-color-input"
                  value={formData.primaryColor}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      primaryColor: e.target.value,
                    }))
                  }
                />
                <input
                  type="text"
                  className="onboarding-input"
                  value={formData.primaryColor}
                  onChange={(e) =>
                    setFormData((prev) => ({
                      ...prev,
                      primaryColor: e.target.value,
                    }))
                  }
                  placeholder="#6366f1"
                />
              </div>
            </div>

            <div className="onboarding-info-box">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                  stroke="currentColor"
                  strokeWidth="2"
                />
                <path
                  d="M10 6V10M10 14H10.01"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
              <div>
                <strong>{t("onboarding.step3.autoSettings")}:</strong>
                <ul>
                  <li>
                    {t("onboarding.step3.language")}:{" "}
                    {countryConfig.language === "pt-br"
                      ? "Português (Brasil)"
                      : countryConfig.language === "en-us"
                      ? "English (US)"
                      : "Español"}
                  </li>
                  <li>
                    {t("onboarding.step3.currency")}:{" "}
                    {countryConfig.currency} ({countryConfig.currencySymbol})
                  </li>
                  <li>
                    {t("onboarding.step3.timezone")}: {countryConfig.timezone}
                  </li>
                  <li>
                    {t("onboarding.step3.dateFormat")}:{" "}
                    {countryConfig.dateFormat}
                  </li>
                </ul>
              </div>
            </div>

            <div className="onboarding-actions">
              <button
                type="button"
                className="onboarding-btn onboarding-btn-secondary"
                onClick={() => setCurrentStep(2)}
              >
                {t("onboarding.step3.back")}
              </button>
              <button
                type="button"
                className="onboarding-btn onboarding-btn-primary"
                onClick={() => saveStep(3)}
                disabled={saving}
              >
                {saving
                  ? t("onboarding.step3.finalizing")
                  : t("onboarding.step3.complete")}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
