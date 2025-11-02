'use client'

import { useTranslations } from 'next-intl'
import { motion } from 'framer-motion'
import { 
  CodeBracketIcon, 
  CloudIcon, 
  LightBulbIcon, 
  WrenchScrewdriverIcon 
} from '@heroicons/react/24/outline'

const Services = () => {
  const t = useTranslations('services')

  const services = [
    {
      icon: CodeBracketIcon,
      title: t('development.title'),
      description: t('development.description'),
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: CloudIcon,
      title: t('infrastructure.title'),
      description: t('infrastructure.description'),
      color: 'from-cyan-500 to-cyan-600'
    },
    {
      icon: LightBulbIcon,
      title: t('consulting.title'),
      description: t('consulting.description'),
      color: 'from-indigo-500 to-indigo-600'
    },
    {
      icon: WrenchScrewdriverIcon,
      title: t('support.title'),
      description: t('support.description'),
      color: 'from-purple-500 to-purple-600'
    }
  ]

  return (
    <section id="services" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            {t('title')}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t('subtitle')}
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={service.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 text-center border border-gray-100 hover:border-gray-200 transform hover:-translate-y-2">
                <div className={`w-16 h-16 mx-auto mb-6 rounded-full bg-linear-to-r ${service.color} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                  <service.icon className="h-8 w-8 text-white" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {service.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed">
                  {service.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Services