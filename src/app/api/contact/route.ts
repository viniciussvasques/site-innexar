import { NextRequest, NextResponse } from 'next/server'
import { sendEmail, createTransporter } from '@/lib/email'
import { getContactEmailTemplate, getAutoReplyTemplate } from '@/lib/email-templates'
import { getTranslations } from 'next-intl/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validação
    const { name, email, phone, company, projectType, budget, timeline, message, locale = 'pt' } = body
    
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: 'Campos obrigatórios: name, email, message' },
        { status: 400 }
      )
    }

    // Carregar traduções baseado no locale
    const t = await getTranslations({ locale, namespace: 'contact.email' })
    
    const translations = {
      contactSubject: t('contactSubject'),
      contactHeader: t('contactHeader'),
      contactInfo: t('contactInfo'),
      contactProject: t('contactProject'),
      contactMessage: t('contactMessage'),
      contactFooter: t('contactFooter'),
      autoReplySubject: t('autoReplySubject'),
      autoReplyHeader: t('autoReplyHeader'),
      autoReplyGreeting: t('autoReplyGreeting'),
      autoReplyThanks: t('autoReplyThanks'),
      autoReplyReceived: t('autoReplyReceived'),
      autoReplyWhile: t('autoReplyWhile'),
      autoReplyVisit: t('autoReplyVisit'),
      autoReplyServices: t('autoReplyServices'),
      autoReplyPortfolio: t('autoReplyPortfolio'),
      autoReplySignature: t('autoReplySignature'),
      autoReplyTeam: t('autoReplyTeam'),
      autoReplyFooter: t('autoReplyFooter'),
      autoReplyAdvantages: t('autoReplyAdvantages'),
      autoReplyAdvantage1: t('autoReplyAdvantage1'),
      autoReplyAdvantage2: t('autoReplyAdvantage2'),
      autoReplyAdvantage3: t('autoReplyAdvantage3'),
      autoReplyAdvantage4: t('autoReplyAdvantage4'),
      autoReplyAdvantage5: t('autoReplyAdvantage5'),
      autoReplyAdvantage6: t('autoReplyAdvantage6'),
      autoReplyContactTitle: t('autoReplyContactTitle'),
      autoReplyContactEmail: t('autoReplyContactEmail'),
      autoReplyContactPhone: t('autoReplyContactPhone'),
      autoReplyContactWebsite: t('autoReplyContactWebsite'),
      labels: {
        name: t('labels.name'),
        email: t('labels.email'),
        phone: t('labels.phone'),
        company: t('labels.company'),
        type: t('labels.type'),
        budget: t('labels.budget'),
        timeline: t('labels.timeline'),
      },
      notInformed: t('notInformed'),
    }

    // Email de destino (do Google Workspace)
    const recipientEmail = process.env.CONTACT_RECIPIENT_EMAIL || 'comercial@innexar.app'
    const sendAutoReply = process.env.ENABLE_AUTO_REPLY !== 'false' // Default: true

    // Template do email principal (sempre em português para você)
    const contactEmailPt = getContactEmailTemplate({
      name,
      email,
      phone: phone || '',
      company: company || '',
      projectType: projectType || '',
      budget: budget || '',
      timeline: timeline || '',
      message,
    }, await getTranslations({ locale: 'pt', namespace: 'contact.email' }).then(t => ({
      contactSubject: t('contactSubject'),
      contactHeader: t('contactHeader'),
      contactInfo: t('contactInfo'),
      contactProject: t('contactProject'),
      contactMessage: t('contactMessage'),
      contactFooter: t('contactFooter'),
      autoReplySubject: t('autoReplySubject'),
      autoReplyHeader: t('autoReplyHeader'),
      autoReplyGreeting: t('autoReplyGreeting'),
      autoReplyThanks: t('autoReplyThanks'),
      autoReplyReceived: t('autoReplyReceived'),
      autoReplyWhile: t('autoReplyWhile'),
      autoReplyVisit: t('autoReplyVisit'),
      autoReplyServices: t('autoReplyServices'),
      autoReplyPortfolio: t('autoReplyPortfolio'),
      autoReplySignature: t('autoReplySignature'),
      autoReplyTeam: t('autoReplyTeam'),
      autoReplyFooter: t('autoReplyFooter'),
      autoReplyAdvantages: t('autoReplyAdvantages'),
      autoReplyAdvantage1: t('autoReplyAdvantage1'),
      autoReplyAdvantage2: t('autoReplyAdvantage2'),
      autoReplyAdvantage3: t('autoReplyAdvantage3'),
      autoReplyAdvantage4: t('autoReplyAdvantage4'),
      autoReplyAdvantage5: t('autoReplyAdvantage5'),
      autoReplyAdvantage6: t('autoReplyAdvantage6'),
      autoReplyContactTitle: t('autoReplyContactTitle'),
      autoReplyContactEmail: t('autoReplyContactEmail'),
      autoReplyContactPhone: t('autoReplyContactPhone'),
      autoReplyContactWebsite: t('autoReplyContactWebsite'),
      labels: {
        name: t('labels.name'),
        email: t('labels.email'),
        phone: t('labels.phone'),
        company: t('labels.company'),
        type: t('labels.type'),
        budget: t('labels.budget'),
        timeline: t('labels.timeline'),
      },
      notInformed: t('notInformed'),
    })))

    // Enviar email principal para você (sempre em português)
    await sendEmail({
      to: recipientEmail,
      subject: contactEmailPt.subject,
      html: contactEmailPt.html,
      text: contactEmailPt.text,
      replyTo: email, // Permite responder diretamente ao cliente
    })

    // Enviar resposta automática para o cliente (no idioma dele)
    if (sendAutoReply) {
      try {
        const autoReply = getAutoReplyTemplate({ name, email }, translations)
        await sendEmail({
          to: email,
          subject: autoReply.subject,
          html: autoReply.html,
          text: autoReply.text,
        })
      } catch (autoReplyError) {
        // Não falhar se a resposta automática der erro
        console.warn('Erro ao enviar resposta automática:', autoReplyError)
      }
    }

    return NextResponse.json(
      { message: 'Mensagem enviada com sucesso!' },
      { status: 200 }
    )
  } catch (error: any) {
    console.error('Erro ao processar formulário de contato:', error)
    
    // Erro de configuração SMTP
    if (error.code === 'EAUTH' || error.code === 'ECONNECTION') {
      return NextResponse.json(
        { error: 'Erro de configuração de email. Verifique as credenciais SMTP.' },
        { status: 500 }
      )
    }

    return NextResponse.json(
      { error: 'Erro ao processar a mensagem. Tente novamente.' },
      { status: 500 }
    )
  }
}

