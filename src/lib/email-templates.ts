// Templates de email com suporte multi-idioma
// As traduções vêm dos arquivos messages/{locale}.json

type EmailTranslations = {
  contactSubject: string
  contactHeader: string
  contactInfo: string
  contactProject: string
  contactMessage: string
  contactFooter: string
  autoReplySubject: string
  autoReplyHeader: string
  autoReplyGreeting: string
  autoReplyThanks: string
  autoReplyReceived: string
  autoReplyWhile: string
  autoReplyVisit: string
  autoReplyServices: string
  autoReplyPortfolio: string
  autoReplySignature: string
  autoReplyTeam: string
  autoReplyFooter: string
  autoReplyAdvantages: string
  autoReplyAdvantage1: string
  autoReplyAdvantage2: string
  autoReplyAdvantage3: string
  autoReplyAdvantage4: string
  autoReplyAdvantage5: string
  autoReplyAdvantage6: string
  autoReplyContactTitle: string
  autoReplyContactEmail: string
  autoReplyContactPhone: string
  autoReplyContactWebsite: string
  labels: {
    name: string
    email: string
    phone: string
    company: string
    type: string
    budget: string
    timeline: string
  }
  notInformed: string
}

// Template de email principal (para você receber) - com logo e design profissional
export function getContactEmailTemplate(
  data: {
    name: string
    email: string
    phone: string
    company: string
    projectType: string
    budget: string
    timeline: string
    message: string
  },
  translations: EmailTranslations
) {
  return {
    subject: translations.contactSubject.replace('{{name}}', data.name),
    html: `
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; 
      line-height: 1.6; 
      color: #1f2937; 
      background-color: #f3f4f6;
    }
    .email-wrapper { 
      max-width: 650px; 
      margin: 0 auto; 
      background-color: #ffffff;
    }
    .header { 
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%); 
      padding: 40px 30px;
      text-align: center;
    }
    .logo { 
      color: #ffffff; 
      font-size: 32px; 
      font-weight: 700; 
      letter-spacing: -0.5px;
      margin-bottom: 10px;
    }
    .header-badge {
      display: inline-block;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
      margin-top: 10px;
    }
    .content { 
      padding: 40px 30px; 
      background: #ffffff;
    }
    .section { 
      margin-bottom: 30px; 
      padding-bottom: 30px;
      border-bottom: 1px solid #e5e7eb;
    }
    .section:last-child {
      border-bottom: none;
    }
    .section-title {
      font-size: 18px;
      font-weight: 700;
      color: #1e40af;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .info-row {
      display: flex;
      padding: 12px 0;
      border-bottom: 1px solid #f3f4f7;
    }
    .info-row:last-child {
      border-bottom: none;
    }
    .info-label { 
      font-weight: 600; 
      color: #4b5563;
      min-width: 120px;
      font-size: 14px;
    }
    .info-value {
      color: #1f2937;
      font-size: 14px;
    }
    .info-value a {
      color: #3b82f6;
      text-decoration: none;
    }
    .info-value a:hover {
      text-decoration: underline;
    }
    .message-box { 
      background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
      padding: 25px; 
      border-left: 4px solid #3b82f6; 
      border-radius: 8px;
      margin-top: 15px;
      font-size: 15px;
      line-height: 1.8;
      color: #1f2937;
    }
    .footer { 
      background: #1f2937; 
      padding: 30px; 
      text-align: center; 
      color: #9ca3af; 
      font-size: 12px;
    }
    .footer-links {
      margin-top: 15px;
    }
    .footer-links a {
      color: #60a5fa;
      text-decoration: none;
      margin: 0 10px;
    }
    .footer-links a:hover {
      text-decoration: underline;
    }
    @media only screen and (max-width: 600px) {
      .content { padding: 30px 20px; }
      .header { padding: 30px 20px; }
      .info-row { flex-direction: column; gap: 5px; }
      .info-label { min-width: auto; }
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="header">
      <div class="logo">INNEXAR</div>
      <div class="header-badge">📧 Novo Contato do Site</div>
    </div>
    <div class="content">
      <div class="section">
        <div class="section-title">👤 ${translations.contactInfo}</div>
        <div class="info-row">
          <div class="info-label">${translations.labels.name}:</div>
          <div class="info-value">${data.name}</div>
        </div>
        <div class="info-row">
          <div class="info-label">${translations.labels.email}:</div>
          <div class="info-value"><a href="mailto:${data.email}">${data.email}</a></div>
        </div>
        <div class="info-row">
          <div class="info-label">${translations.labels.phone}:</div>
          <div class="info-value"><a href="tel:${data.phone}">${data.phone}</a></div>
        </div>
        <div class="info-row">
          <div class="info-label">${translations.labels.company}:</div>
          <div class="info-value">${data.company || translations.notInformed}</div>
        </div>
      </div>
      
      <div class="section">
        <div class="section-title">💼 ${translations.contactProject}</div>
        <div class="info-row">
          <div class="info-label">${translations.labels.type}:</div>
          <div class="info-value">${data.projectType || translations.notInformed}</div>
        </div>
        <div class="info-row">
          <div class="info-label">${translations.labels.budget}:</div>
          <div class="info-value">${data.budget || translations.notInformed}</div>
        </div>
        <div class="info-row">
          <div class="info-label">${translations.labels.timeline}:</div>
          <div class="info-value">${data.timeline || translations.notInformed}</div>
        </div>
      </div>
      
      <div class="section">
        <div class="section-title">💬 ${translations.contactMessage}</div>
        <div class="message-box">
          ${data.message.replace(/\n/g, '<br>')}
        </div>
      </div>
    </div>
    <div class="footer">
      <p>${translations.contactFooter}</p>
      <div class="footer-links">
        <a href="https://innexar.app">Website</a> | 
        <a href="mailto:comercial@innexar.app">Email</a> | 
        <a href="tel:+551151085266">Telefone</a>
      </div>
      <p style="margin-top: 15px; color: #6b7280;">© 2025 Innexar. Todos os direitos reservados.</p>
    </div>
  </div>
</body>
</html>
    `,
    text: `
${translations.contactHeader}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 ${translations.contactInfo}

${translations.labels.name}: ${data.name}
${translations.labels.email}: ${data.email}
${translations.labels.phone}: ${data.phone}
${translations.labels.company}: ${data.company || translations.notInformed}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 ${translations.contactProject}

${translations.labels.type}: ${data.projectType || translations.notInformed}
${translations.labels.budget}: ${data.budget || translations.notInformed}
${translations.labels.timeline}: ${data.timeline || translations.notInformed}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 ${translations.contactMessage}

${data.message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${translations.contactFooter}

Website: https://innexar.app
Email: comercial@innexar.app
Telefone: +55 11 5108-5266
    `,
  }
}

// Template de resposta automática - PROFISSIONAL com logo, vantagens e informações
export function getAutoReplyTemplate(
  data: { name: string; email: string },
  translations: EmailTranslations
) {
  return {
    subject: translations.autoReplySubject,
    html: `
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; 
      line-height: 1.6; 
      color: #1f2937; 
      background-color: #f3f4f6;
    }
    .email-wrapper { 
      max-width: 650px; 
      margin: 0 auto; 
      background-color: #ffffff;
    }
    .header { 
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%); 
      padding: 50px 30px;
      text-align: center;
    }
    .logo { 
      color: #ffffff; 
      font-size: 42px; 
      font-weight: 700; 
      letter-spacing: -1px;
      margin-bottom: 15px;
      text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header-subtitle {
      color: rgba(255, 255, 255, 0.95);
      font-size: 18px;
      font-weight: 500;
      margin-top: 10px;
    }
    .content { 
      padding: 40px 30px; 
      background: #ffffff;
    }
    .greeting {
      font-size: 20px;
      color: #1f2937;
      margin-bottom: 20px;
      font-weight: 600;
    }
    .message {
      font-size: 16px;
      color: #4b5563;
      margin-bottom: 30px;
      line-height: 1.8;
    }
    .advantages-section {
      background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
      padding: 30px;
      border-radius: 12px;
      margin: 30px 0;
    }
    .advantages-title {
      font-size: 20px;
      font-weight: 700;
      color: #1e40af;
      margin-bottom: 20px;
      text-align: center;
    }
    .advantages-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
      margin-top: 20px;
    }
    .advantage-item {
      background: #ffffff;
      padding: 15px;
      border-radius: 8px;
      border-left: 3px solid #3b82f6;
    }
    .advantage-title {
      font-weight: 600;
      color: #1e40af;
      font-size: 14px;
      margin-bottom: 5px;
    }
    .advantage-text {
      font-size: 13px;
      color: #6b7280;
      line-height: 1.5;
    }
    .cta-section {
      text-align: center;
      margin: 40px 0;
      padding: 30px;
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
      border-radius: 12px;
    }
    .cta-button {
      display: inline-block;
      background: #ffffff;
      color: #1e40af;
      padding: 14px 32px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 700;
      font-size: 16px;
      transition: transform 0.2s;
    }
    .cta-button:hover {
      transform: translateY(-2px);
    }
    .contact-section {
      background: #f9fafb;
      padding: 25px;
      border-radius: 12px;
      margin: 30px 0;
    }
    .contact-title {
      font-size: 18px;
      font-weight: 700;
      color: #1e40af;
      margin-bottom: 15px;
    }
    .contact-item {
      display: flex;
      align-items: center;
      padding: 10px 0;
      color: #4b5563;
      font-size: 14px;
    }
    .contact-item a {
      color: #3b82f6;
      text-decoration: none;
      margin-left: 10px;
    }
    .contact-item a:hover {
      text-decoration: underline;
    }
    .signature {
      margin-top: 30px;
      padding-top: 30px;
      border-top: 1px solid #e5e7eb;
    }
    .signature-name {
      font-weight: 700;
      color: #1e40af;
      font-size: 16px;
      margin-bottom: 5px;
    }
    .signature-role {
      color: #6b7280;
      font-size: 14px;
    }
    .footer { 
      background: #1f2937; 
      padding: 30px; 
      text-align: center; 
      color: #9ca3af; 
      font-size: 12px;
    }
    .footer-links {
      margin: 20px 0;
    }
    .footer-links a {
      color: #60a5fa;
      text-decoration: none;
      margin: 0 12px;
      font-size: 13px;
    }
    .footer-links a:hover {
      text-decoration: underline;
    }
    .social-links {
      margin-top: 15px;
    }
    .social-links a {
      display: inline-block;
      margin: 0 8px;
      color: #9ca3af;
      text-decoration: none;
    }
    @media only screen and (max-width: 600px) {
      .content { padding: 30px 20px; }
      .header { padding: 40px 20px; }
      .advantages-grid { grid-template-columns: 1fr; }
      .logo { font-size: 36px; }
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="header">
      <div class="logo">INNEXAR</div>
      <div class="header-subtitle">${translations.autoReplyHeader}</div>
    </div>
    <div class="content">
      <div class="greeting">
        ${translations.autoReplyGreeting} <strong>${data.name}</strong>!
      </div>
      
      <div class="message">
        ${translations.autoReplyThanks} <strong style="color: #1e40af;">Innexar</strong>!
      </div>
      
      <div class="message">
        ${translations.autoReplyReceived}
      </div>

      <div class="advantages-section">
        <div class="advantages-title">${translations.autoReplyAdvantages}</div>
        <div class="advantages-grid">
          <div class="advantage-item">
            <div class="advantage-title">⚡ ${translations.autoReplyAdvantage1}</div>
          </div>
          <div class="advantage-item">
            <div class="advantage-title">🔒 ${translations.autoReplyAdvantage2}</div>
          </div>
          <div class="advantage-item">
            <div class="advantage-title">👥 ${translations.autoReplyAdvantage3}</div>
          </div>
          <div class="advantage-item">
            <div class="advantage-title">💡 ${translations.autoReplyAdvantage4}</div>
          </div>
          <div class="advantage-item">
            <div class="advantage-title">📈 ${translations.autoReplyAdvantage5}</div>
          </div>
          <div class="advantage-item">
            <div class="advantage-title">✅ ${translations.autoReplyAdvantage6}</div>
          </div>
        </div>
      </div>

      <div class="cta-section">
        <a href="https://innexar.app" class="cta-button">${translations.autoReplyVisit}</a>
      </div>

      <div class="contact-section">
        <div class="contact-title">${translations.autoReplyContactTitle}</div>
        <div class="contact-item">
          📧 <a href="mailto:comercial@innexar.app">${translations.autoReplyContactEmail}</a>
        </div>
        <div class="contact-item">
          📞 <a href="tel:+551151085266">${translations.autoReplyContactPhone}</a>
        </div>
        <div class="contact-item">
          🌐 <a href="https://innexar.app">${translations.autoReplyContactWebsite}</a>
        </div>
      </div>

      <div class="signature">
        <div class="signature-name">${translations.autoReplyTeam}</div>
        <div class="signature-role">${translations.autoReplySignature}</div>
      </div>
    </div>
    <div class="footer">
      <p>${translations.autoReplyFooter}</p>
      <div class="footer-links">
        <a href="https://innexar.app">Website</a>
        <a href="mailto:comercial@innexar.app">Email</a>
        <a href="tel:+551151085266">Telefone</a>
      </div>
      <div class="social-links">
        <p style="color: #6b7280; margin-top: 15px;">© 2025 Innexar. Todos os direitos reservados.</p>
      </div>
    </div>
  </div>
</body>
</html>
    `,
    text: `
${translations.autoReplyHeader}

${translations.autoReplyGreeting} ${data.name}!

${translations.autoReplyThanks} Innexar!

${translations.autoReplyReceived}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${translations.autoReplyAdvantages}

⚡ ${translations.autoReplyAdvantage1}
🔒 ${translations.autoReplyAdvantage2}
👥 ${translations.autoReplyAdvantage3}
💡 ${translations.autoReplyAdvantage4}
📈 ${translations.autoReplyAdvantage5}
✅ ${translations.autoReplyAdvantage6}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${translations.autoReplyContactTitle}

📧 ${translations.autoReplyContactEmail}: comercial@innexar.app
📞 ${translations.autoReplyContactPhone}: +55 11 5108-5266
🌐 ${translations.autoReplyContactWebsite}: https://innexar.app

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${translations.autoReplySignature}
${translations.autoReplyTeam}

${translations.autoReplyFooter}
    `,
  }
}
