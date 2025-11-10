'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { motion } from 'framer-motion'
import { EyeIcon, CodeBracketIcon } from '@heroicons/react/24/outline'

const Portfolio = () => {
  const t = useTranslations('portfolio')
  const [activeFilter, setActiveFilter] = useState('all')

  const projects = [
    {
      id: 1,
      title: 'E-commerce Platform',
      category: 'web',
      image: '/api/placeholder/600/400',
      technologies: ['React', 'Node.js', 'PostgreSQL'],
      description: 'Modern e-commerce platform with advanced analytics'
    },
    {
      id: 2,
      title: 'Mobile Banking App',
      category: 'mobile',
      image: '/api/placeholder/600/400',
      technologies: ['React Native', 'Firebase', 'TypeScript'],
      description: 'Secure mobile banking application'
    },
    {
      id: 3,
      title: 'Cloud Infrastructure',
      category: 'cloud',
      image: '/api/placeholder/600/400',
      technologies: ['AWS', 'Kubernetes', 'Docker'],
      description: 'Scalable cloud infrastructure solution'
    },
    {
      id: 4,
      title: 'Data Analytics Dashboard',
      category: 'data',
      image: '/api/placeholder/600/400',
      technologies: ['Python', 'TensorFlow', 'React'],
      description: 'Real-time data analytics and visualization'
    },
    {
      id: 5,
      title: 'Corporate Website',
      category: 'web',
      image: '/api/placeholder/600/400',
      technologies: ['Next.js', 'Tailwind CSS', 'Vercel'],
      description: 'Professional corporate website with CMS'
    },
    {
      id: 6,
      title: 'IoT Monitoring System',
      category: 'cloud',
      image: '/api/placeholder/600/400',
      technologies: ['IoT Core', 'MongoDB', 'Express'],
      description: 'IoT device monitoring and management system'
    }
  ]

  const filters = [
    { key: 'all', label: t('filterAll') },
    { key: 'web', label: t('filterWeb') },
    { key: 'mobile', label: t('filterMobile') },
    { key: 'cloud', label: t('filterCloud') },
    { key: 'data', label: t('filterData') }
  ]

  const filteredProjects = activeFilter === 'all' 
    ? projects 
    : projects.filter(project => project.category === activeFilter)

  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
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

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16"
        >
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">50+</div>
            <div className="text-gray-600">{t('projectsCount')}</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-cyan-600 mb-2">30+</div>
            <div className="text-gray-600">{t('clientsCount')}</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-indigo-600 mb-2">5+</div>
            <div className="text-gray-600">{t('yearsCount')}</div>
          </div>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
          className="flex flex-wrap justify-center gap-4 mb-12"
        >
          {filters.map((filter) => (
            <button
              key={filter.key}
              onClick={() => setActiveFilter(filter.key)}
              className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                activeFilter === filter.key
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:bg-blue-50 hover:text-blue-600'
              }`}
            >
              {filter.label}
            </button>
          ))}
        </motion.div>

        {/* Projects Grid */}
        <motion.div
          layout
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {filteredProjects.map((project, index) => (
            <motion.div
              key={project.id}
              layout
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 30 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
            >
              <div className="relative overflow-hidden">
                <div className="w-full h-48 bg-linear-to-br from-blue-100 to-cyan-100 flex items-center justify-center">
                  <CodeBracketIcon className="h-16 w-16 text-blue-600" />
                </div>
                <div className="absolute inset-0 bg-blue-600 bg-opacity-0 group-hover:bg-opacity-90 transition-all duration-300 flex items-center justify-center">
                  <button className="bg-white text-blue-600 px-6 py-2 rounded-full font-semibold opacity-0 group-hover:opacity-100 transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 flex items-center">
                    <EyeIcon className="h-4 w-4 mr-2" />
                    {t('viewProject')}
                  </button>
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {project.title}
                </h3>
                <p className="text-gray-600 mb-4">
                  {project.description}
                </p>
                
                <div className="mb-4">
                  <span className="text-sm font-semibold text-gray-700 mb-2 block">
                    {t('technologies')}:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech) => (
                      <span
                        key={tech}
                        className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

export default Portfolio